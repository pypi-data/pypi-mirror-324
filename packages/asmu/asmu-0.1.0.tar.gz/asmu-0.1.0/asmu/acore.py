"""acore.py

Keep in mind, that all the acore classes run in a different thread, called by the sounddevice callback function.
Therfore reading or writing to variables, except for initialization, has to be thread safe!!!"""
from typing import TYPE_CHECKING, Optional, Tuple
from abc import ABC, abstractmethod
import numpy as np
import sounddevice as sd

if TYPE_CHECKING:
    from .types import InAs, AData, ABuf

class AGenerator(ABC):
    def __init__(self, out_buffer: bool, blocksize: int, start_frame: int) -> None:
        """This is the base class for audio generators.

        Args:
            out_buffer (bool): Flag that decides if outputs are buffered.
            blocksize (int): Blocksize of the audio arrays.
            start_frame (int): The number of the first frame (to start counting from).
        """
        self._out_buffer = out_buffer
        self._blocksize = blocksize
        self._frame = start_frame

        # set output channels and update _out_buf
        self.out_chs = 1
        self._reload = True

    @property
    def out_chs(self) -> Optional[int]:
        return self._out_chs
    @out_chs.setter
    def out_chs(self, value: Optional[int]) -> None:
        self._out_chs = value
        # update _out_buf size
        if self._out_buffer and value is not None:
            self._out_buf = np.empty((self._blocksize, value), dtype=np.float32)
        else:
            self._out_buf = None

    def upstream(self, outdata: "AData", ch: int, frame: int) -> None:
        """This method is called by other AProcessors, connected to the outputs, to obtain the outputs data of the given channel.
        It is called in the opposite of audio flow and is therefore called upstream.
        The connected (other) AProcessors pass their outdata reference (to write to) and the channel ch they want to obtain the data from.
        Inside upstream, buffering and the appropriate calls for _mod and _inc are handled.

        Args:
            outdata (numpy.ndarray): Reference of the 1D array to write to, with length blocksize.
            ch (int): The channel corresponding to the outdata at hand.
            frame (int): Current frame number to be processed, this always increases by +1 and is incremented by the callback.
        """
        # if the next frame is called, increment and set buffer reload flag
        if frame != self._frame:
            self._frame = frame
            self._inc()
            self._reload = True
        # if out_buffer is enabled and reload flag is set fill _out_buf
        if self._out_buffer and self._reload:
            if self._out_buffer:
                for out_ch in range(self._out_chs):
                    self._mod(self._out_buf[:, out_ch], out_ch)
        self._reload = False

        # if buffer is enabled return buffer
        if self._out_buffer:
            np.copyto(outdata, self._out_buf[:, ch], casting="no")
        # otherwise process given array
        else:
            self._mod(outdata, ch)

    @abstractmethod
    def _mod(self, outdata: "AData", ch: int) -> None:
        """This function is envoked by upstream(). 
        It should write something in outdata for the given output channel ch.
        Make sure to copy your data or write directly into outdata and not just set outdata to a new reference.
        See sounddevice callback manual for more details.

        Args:
            outdata (numpy.ndarray): The 1D array to write to, with length blocksize.
            ch (int): The channel corresponding to the outdata at hand.
        """
    
    @abstractmethod
    def _inc(self) -> None:
        """This function is envoked by upstream(). 
        If the class changes over time, this function can be used to perform these changes.
        It is called exactly once after all channels of the class have been processed.
        """

class AEffect(ABC):
    def __init__(self, in_buffer: bool, out_buffer: bool, blocksize: int, start_frame: int) -> None:
        """This is the base class for audio effects

        Args:
            in_buffer (bool): Flag that decides if inputs are buffered.
            out_buffer (bool):Flag that decides if outputs are buffered.
            blocksize (int): Blocksize of the audio arrays.
            start_frame (int): The number of the first frame (to start counting from).
        """
        self._in_buffer = in_buffer
        self._out_buffer = out_buffer
        self._blocksize = blocksize
        self._frame = start_frame

        # set in-/output channels and update buffers
        self.in_as = None
        self.out_chs = None
        self._reload = True

    @property
    def in_as(self) -> "InAs":
        """A tupel defining what objects output and channel, the inputchannels are connected to.
        Evaluating in_as[in_ch] for an input channel in_ch of self, yields a tuple of (Connected Object, Connected Channel)."""
        return self._in_as
    @in_as.setter
    def in_as(self, value: "InAs") -> None:
        """Setting in_as automatically updates the buffer size, if in_buffer is enabled."""
        self._in_as = value
        # update _in_buf size
        if self._in_buffer and value is not None:
            self._in_buf = np.empty((self._blocksize, len(value)), dtype=np.float32)
        else:
            self._in_buf = None

    @property
    def out_chs(self) -> Optional[int]:
        return self._out_chs
    @out_chs.setter
    def out_chs(self, value: Optional[int]) -> None:
        self._out_chs = value
        # update _out_buf size
        if self._out_buffer and value is not None:
            self._out_buf = np.empty((self._blocksize, value), dtype=np.float32)
        else:
            self._out_buf = None

    def upstream(self, outdata: "AData", ch: int, frame: int) -> None:
        """This method is called by other AProcessors, connected to the outputs, to obtain the outputs data of the given channel.
        It is called in the opposite of audio flow and is therefore called upstream.
        The connected (other) AProcessors pass their outdata reference (to write to) and the channel ch they want to obtain the data from.
        Inside upstream, buffering and the appropriate calls for _mod and _inc are handled.

        Args:
            outdata (numpy.ndarray): Reference of the 1D array to write to, with length blocksize.
            ch (int): The channel corresponding to the outdata at hand.
            frame (int): Current frame number to be processed, this always increases by +1 and is incremented by the callback.
        """
        # if the next frame is called, increment and set buffer reload flag
        if frame != self._frame:
            self._frame = frame
            self._inc()
            self._reload = True
        # if in_buffer is enabled and reload flag is set fill _in_buf
        if self._in_buffer and self._reload:
            self._in_buf.fill(0)
            for in_ch, in_a in enumerate(self._in_as):
                if in_a[0] is not None:
                    # send _in_buf upstream
                    in_a[0].upstream(self._in_buf[:, in_ch], in_a[1], frame)
        # if out_buffer is enabled and reload flag is set fill _out_buf
        if self._out_buffer and self._reload:
            for out_ch in range(self._out_chs):
                self._mod(self._out_buf[:, out_ch], out_ch)
        self._reload = False

        # if out_buffer is enabled copy _out_buf
        if self._out_buffer:
            np.copyto(outdata, self._out_buf[:, ch], casting="no")
        # otherwise process given array
        else:
            # _mod HAS TO HANDLE INPUT BUFFER + SETTING!!!
            self._mod(outdata, ch)

    @abstractmethod
    def _mod(self, outdata: "AData", ch: int) -> None:
        """This function is envoked by upstream(). 
        It should write something in outdata for the given output channel ch.
        Make sure to copy your data or write directly into outdata and not just set outdata to a new reference.
        See sounddevice callback manual for more details.

        Args:
            outdata (numpy.ndarray): The 1D array to write to, with length blocksize.
            ch (int): The channel corresponding to the outdata at hand.

        Notes:
            The implementation of this function has to handle the `self.in_buffer` setting 
            and either process the input buffer `self.in_buf`, that is periodically filled by `start_upstream()`
            or obtain data from upstream and process it afterwards for each input channel.
            
            Example:
                def _mod(self, outdata, ch):
                    if self.in_buffer:
                        # process the self._in_buf[:, ch]
                        ...
                    else:
                        if self._in_as[ch][0] is not None:
                            # get outdata from upstream
                            self._in_as[ch][0].upstream(outdata, self._in_as[ch][1], frame) 
                            # process outdata here
                            ...
        """
    
    @abstractmethod
    def _inc(self):
        """This function is envoked by upstream(). 
        If the class changes over time, this function can be used to perform these changes.
        It is called exactly once per audio frame, but not for the first one.
        """


class AAnalyzer(ABC):
    def __init__(self, in_buffer: bool, blocksize: int, start_frame: int) -> None:
        """This is the base class for audio analyzers.

        Args:
            in_buffer (bool): Flag that decides if inputs are buffered.
            blocksize (int): Blocksize of the audio arrays.
            start_frame (int): The number of the first frame (to start counting from).
        """
        self._in_buffer = in_buffer
        self._blocksize = blocksize
        self._frame = start_frame

        # set input channels and update _in_buf
        self.in_as = None

    @property
    def in_as(self) -> "InAs":
        """A tupel defining what objects output and channel, the inputchannels are connected to.
        Evaluating in_as[in_ch] for an input channel in_ch of self, yields a tuple of (Connected Object, Connected Channel)."""
        return self._in_as
    @in_as.setter
    def in_as(self, value: "InAs"):
        """Setting in_as automatically updates the buffer size, if in_buffer is enabled."""
        self._in_as = value
        # update _in_buf size
        if self._in_buffer and value is not None:
            self._in_buf = np.empty((self._blocksize, len(value)), dtype=np.float32)
        else:
            self._in_buf = None

    def start_upstream(self, frame: int) -> None:
        # if in_buffer is enabled fill _in_buf
        if self._in_buffer:
            self._in_buf.fill(0)
            for in_ch, in_a in enumerate(self._in_as):
                if in_a[0] is not None:
                    # send _in_buf upstream
                    in_a[0].upstream(self._in_buf[:, in_ch], in_a[1], frame)

        # _process HAS TO HANDLE INPUT BUFFER + SETTING!!!
        self._process()

    @abstractmethod
    def _process(self) -> None:
        """This method is called once per audio frame to start the upstream chain.
        It either processes the obtained input buffer `self._in_buf`or sends data upstream.

        Notes:
            The implementation of this function has to handle the `self._in_buffer` setting 
            and either process the input buffer `self._in_buf`, that is periodically filled by `start_upstream()`
            or send data upstream to process for each input channel.

            Example:
                if self._in_buffer:
                    # process the self._in_buf
                else:
                    for in_ch, in_a in enumerate(self._in_as):
                        if in_a[0] is not None:
                            in_a[0].upstream(NUMPY_ARRAY_TO_WRITE_TO[:, in_ch], in_a[1], frame)
                        else:
                            NUMPY_ARRAY_TO_WRITE_TO[:, in_ch].fill(0)
        """

class AInterface:
    def __init__(self, blocksize: int, start_frame: int):
        """This is the base class of the audio interface.
        It is used to assemble the callback function.

        Args:
            blocksize (int): Blocksize of the audio arrays.
            start_frame (int): The number of the first frame (to start counting from).
        """
        self.in_as = None
        self.alzs = None
        self.out_chs = None

        self._blocksize = blocksize
        self._frame = start_frame

        self.end_frame = None

    @property
    def in_as(self) -> "InAs":
        """A tupel defining what objects output and channel, the inputchannels are connected to.
        Evaluating in_as[in_ch] for an input channel in_ch of self, yields a tuple of (Connected Object, Connected Channel)."""
        return self._in_as
    @in_as.setter
    def in_as(self, value: "InAs"):
        self._in_as = value

    @property
    def out_chs(self) -> Optional[int]:
        return self._out_chs
    @out_chs.setter
    def out_chs(self, value: Optional[int]) -> None:
        self._out_chs = value
        if value is not None and value > 0:
            # update _out_buf size
            self._out_buf = np.empty((self._blocksize, value), dtype=np.float32)
        else:
            self._out_buf = None

    @property
    def alzs(self) -> Tuple["AAnalyzer"]:
        return self._alzs
    @alzs.setter
    def alzs(self, value: Tuple["AAnalyzer"]):
        self._alzs = value

    def callback(self, indata: np.ndarray, outdata: np.ndarray, frames: int, ctime, status):
        outdata.fill(0)
        # copy indata so it can be processed by upstream()
        if self._out_buf is not None:
            np.copyto(self._out_buf, indata)
        # call upstream method of the outputs connected to the inputs
        if self.in_as is not None:
            for in_ch, in_a in enumerate(self._in_as):
                if in_a[0] is not None:
                    in_a[0].upstream(outdata[:, in_ch], in_a[1], self._frame)
        # call AAnalyzers start_upstream method (because they wont get called otherwise)
        for alz in self._alzs:
            alz.start_upstream(self._frame)
        self._frame += 1 # Overflow?
        if self.end_frame is not None and self.end_frame <= self._frame:
            raise sd.CallbackStop

    def upstream(self, outdata: "AData", ch: int, frame: int):
        """This method is called by other AProcessors, connected to the outputs, to obtain the outputs data of the given channel.
        It just copies the bufferd indata of the respected channel to the given outdata reference

        Args:
            outdata (numpy.ndarray): Reference of the 1D array to write to, with length blocksize.
            ch (int): The channel corresponding to the outdata at hand.
            frame (int): Current frame number to be processed, this always increases by +1 and is incremented by the callback.
        """
        np.copyto(outdata, self._out_buf[:, ch])
