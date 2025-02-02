"""generator.py"""
import queue
import threading
from typing import TYPE_CHECKING
import numpy as np
from .acore import AGenerator
from .processor import Generator
from .io import Output

if TYPE_CHECKING:
    from .afile import AFile
    from .interface import Interface
    from .types import AData


class Player(Generator):
    def __init__(self, interface: "Interface", afile: "AFile", loop: bool = False) -> None:
        """The Player class generator is used to play audio of a given file.
        It is a multi output generator, with the output count extracted from the given AFile.

        Args:
            interface (Interface): Reference to an Interface instance.
            afile (AFile): Reference to an AFile instance.
            loop (bool, optional): Flag to enable looping. Defaults to False.

        Raises:
            ValueError: The given AFile was not opened.
        """
        # check afile is open and reset
        self._afile = afile
        if afile.closed:
            raise ValueError("AFile was not opened - can not be used in Recorder.")
        afile.flush()
        afile.seek(0)

        self._loop = loop

        self._aplayer = self._APlayer(afile, loop, interface.blocksize, interface.start_frame)
        super().__init__(agenerator = self._aplayer,
                         interface = interface,
                         outputs = tuple(Output(self) for i in range(afile.channels)),
                         out_update = False)

    def finished(self, block: bool = True, timeout: float = 1) -> bool:
        """This function can be used to wait for the Player to finish playback.
        
        Args:
            block (bool, optional): Decides if the call of finished() should block. Defaults to True.
            timeout (float, optional): The timeout after which False is returned. Defaults to 1.

        Returns:
            bool: Returns True if the Player finished and False on timeout.
        """
        if block:
            return self._aplayer.finished_event.wait(timeout = timeout)
        else:
            return self._aplayer.finished_event.is_set()

    def restart(self) -> bool:
        """Restart the Player, unset the finished() flag.
        
        Returns:
            bool: Returns True if successful and False if the Player isn't finished yet."""
        if not self.finished(block=False):
            return False
        self._afile.seek(0)
        self._aplayer.finished_event.clear()
        return True

    def looped(self, block: bool = True, timeout: float = 1) -> bool:
        """This function can be used to wait for the Player to loop.
        
        Args:
            block (bool, optional): Decides if the call of looped() should block. Defaults to True.
            timeout (float, optional): The timeout after which False is returned. Defaults to 1.

        Returns:
            bool: Returns True if a loop occured and False on timeout.
        """
        looped = False
        if block:
            looped = self._aplayer.looped_event.wait(timeout = timeout)
        else:
            looped = self._aplayer.looped_event.is_set()
        if looped:
            self._aplayer.looped_event.clear()
        return looped

    def set_seek(self, position: int = 0) -> None:
        """Reset the Player to the given file position.
        This is updated at the next upcoming frame.
        The function call blocks when called faster than the frames.
        
        Args:
            position (int, optional): Position to seek. Defaults to 0."""
        self._aplayer.seek_queue.put(position)

    class _APlayer(AGenerator):
        def __init__(self, afile: "AFile", loop: bool, blocksize: int, start_frame: int) -> None:
            self.finished_event = threading.Event()
            self.looped_event = threading.Event()
            self.seek_queue = queue.Queue()

            self._afile = afile
            self._loop = loop
            self._samples = afile.frames

            self._firstread = False
            super().__init__(out_buffer = True, # The _out_buf is used to write the file into on _inc()
                             blocksize = blocksize,
                             start_frame = start_frame)

        def _mod(self, outdata: "AData", ch: int) -> None:
            if not self._firstread:
                self._inc()
                self._firstread = True

        def _inc(self) -> None:
            if self.finished_event.is_set():
                return
            if not self.seek_queue.empty():
                self._afile.seek(self.seek_queue.get())
            # calculate the rest to play
            rest = self._samples-self._afile.tell()
            if self._loop and rest < self._blocksize:
                # read rest (not full vlock)
                self._afile.read(rest, dtype="float32", always_2d=True, out=self._out_buf[:rest, :])
                self.looped_event.set() 
                self._afile.seek(0)
                self._afile.read(self._blocksize-rest, dtype="float32", always_2d=True, out=self._out_buf[rest:, :])
                return
            # if there are no samples left to play
            if rest == 0:
                self.finished_event.set() 
                return
            # load a block of samples in the buffer
            self._afile.read(self._blocksize, dtype="float32", always_2d=True, fill_value=0, out=self._out_buf)


class Sine(Generator):
    def __init__(self, interface: "Interface", frequency: float, phase: float = 0, out_buffer: bool = False) -> None:
        """The Sine class generator is used to craete a sine wave with given frequency and phase.
        It is a single output generator.

        Args:
            interface (Interface): Reference to an Interface instance.
            frequency (float): Sine frequency in Hertz.
            phase (float, optional): Sine phase in radiant. Defaults to 0.
            out_buffer (bool, optional): Flag that decides if outputs are buffered. Defaults to False.
        """
        self._frequency = frequency

        self._asine =  self._ASine(frequency, phase, interface.samplerate, out_buffer, interface.blocksize, interface.start_frame)
        super().__init__(agenerator = self._asine,
                         interface = interface,
                         outputs = (Output(self), ),
                         out_update = False)

    def set_frequency(self, frequency: float) -> None:
        """Change the frequency to the given value.
        This is updated at the next upcoming frame.
        The function call blocks when called faster than the frames.
        
        Args:
            frequency (float): The new set frequency in Hertz."""
        self._frequency = frequency
        self._asine.frequency_queue.put(frequency)

    class _ASine(AGenerator):
        def __init__(self, frequency, phase, samplerate, out_buffer, blocksize, start_frame) -> None:
            self.frequency_queue = queue.Queue(maxsize=1)

            self._frequency = frequency
            self._samplerate = samplerate
            self._phase = phase
            self._omega_per_block = 2*np.pi*frequency*blocksize/samplerate

            self._omegas = np.linspace(start_frame*self._omega_per_block, (start_frame+1)*self._omega_per_block, blocksize, endpoint=False, dtype=np.float32)
            super().__init__(out_buffer = out_buffer,
                             blocksize = blocksize,
                             start_frame = start_frame)

        def _mod(self, outdata: "AData", ch: int) -> None:
            np.sin(self._omegas+self._phase, out=outdata)

        def _inc(self) -> None:
            self._phase += self._omega_per_block
            self._phase %= 2*np.pi

            if not self.frequency_queue.empty():
                self._frequency = self.frequency_queue.get()
                self._omega_per_block = 2*np.pi*self._frequency*self._blocksize/self._samplerate
                self._omegas = np.linspace(0, self._omega_per_block, self._blocksize, endpoint=False, dtype=np.float32)


class Constant(Generator):
    def __init__(self, interface: "Interface", value: float) -> None:
        """The Constant class generator is used to generate a constant output value, typically used for testing.
        It is a single output generator.

        Args:
            interface (Interface): Reference to an Interface instance.
            value (float): The constant output value
        """
        self._aconstant =  self._AConstant(value, interface.blocksize, interface.start_frame)
        super().__init__(agenerator = self._aconstant,
                         interface = interface,
                         outputs = (Output(self), ),
                         out_update = False)

    class _AConstant(AGenerator):
        def __init__(self, value, blocksize, start_frame) -> None:
            self._value = value
            super().__init__(out_buffer = False,
                             blocksize = blocksize,
                             start_frame = start_frame)

        def _mod(self, outdata: "AData", ch: int) -> None:
            outdata[:] = self._value

        def _inc(self) -> None:
            pass
