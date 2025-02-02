"""analyzer.py"""
import threading
from typing import TYPE_CHECKING, Literal
import numpy as np
from .acore import AAnalyzer
from .processor import Analyzer
from .io import Input

if TYPE_CHECKING:
    from .io import IInput
    from .afile import AFile
    from .interface import Interface
    from .types import AData, FFTData


class Recorder(Analyzer):
    def __init__(self, interface: "Interface", afile: "AFile") -> None:
        """The Recorder class analyzer is used to record audio to a given file.
        It is a multi input analyzer, with the input count extracted from the given AFile.

        Args:
            interface (Interface): Reference to an Interface instance.
            afile (AFile): Reference to an AFile instance.

        Raises:
            ValueError: The given AFile was not opened.
        """
        # check afile is open and reset
        self._afile = afile
        if afile.closed:
            raise ValueError("The given AFile was not opened.")
        afile.flush()
        afile.seek(0)

        arecorder = self._ARecorder(afile, interface.blocksize, interface.start_frame)
        super().__init__(aanalyzer = arecorder,
                         interface = interface,
                         inputs = tuple(Input(self) for i in range(afile.channels)),
                         in_update = False)

    class _ARecorder(AAnalyzer):
        def __init__(self, afile: "AFile", blocksize, start_frame) -> None:
            self._afile = afile
            super().__init__(in_buffer = True,
                             blocksize = blocksize,
                             start_frame = start_frame)

        def _process(self) -> None:
            self._afile.write(self._in_buf)


class CalIInput(Analyzer):
    def __init__(self, interface: "Interface", value: float, unit: str = Literal["V", "Pa", "SPL"], gain: float = 0, averages: int = 100) -> None:
        """The CalcIInput class analyzer is used to calibrate the connected interface IInput.
        It is a single input analyzer.

        Args:
            interface (Interface): Reference to an Interface instance.
            value (float): The value of the signal used for calibration.
            unit (Literal["V", "Pa", "SPL"]): The unit of the value given
                - "V"   : Peak amplitude of the sinusoidal signal in Volt.
                - "Pa"  : Peak amplitude of the sinusoidal signal in Pascal.
                - "SPL" : Sound Pressure Level (RMS pressure in Dezibel).
            gain (float, optional): Gain setting of the interface. This is not used for the calculation, but stored in the IInput. Defaults to 0.
            averages (int, optional): How many averages should be calcualted. Defaults to 100.
        """
        self._value = value
        self._unit = unit
        self._gain = gain

        self._calciinput = self._CalIInput(averages, interface.blocksize, interface.start_frame)
        super().__init__(aanalyzer = self._calciinput,
                         interface = interface,
                         inputs = (Input(self), ),
                         in_update = False)

    def evaluate(self, save: bool = True, iinput: "IInput" = None) -> None:
        """If the measurement is finished, this evaluates the result and returns True.
        If the measurement is still running, False is returned.

        Args:
            save (bool, optional): Decides if the results should be daved to the connected or given IInput. Defaults to True.
            iinput (IInput, optional): The IInput to save the calibration to. Defaults to None.

        Returns:
            tuple(float, float) | False: Returns (frequency, calibration_factor) if everything was successful or False if the measurement is not done yet.

        Raises:
            ValueError: Given Unit is unknown.
        """
        if not self.finished(block = False):
            return False
        # calculate peak amplitude
        if self._unit == "V" or self._unit == "Pa":
            peak = self._value
        elif self._unit == "SPL":
            peak = 2e-5 * 10 ** (self._value / 20) * np.sqrt(2)
        else:
            raise ValueError("Given Unit is unknown.")
        # calculate calibration factor and frquency
        print(np.mean(self._calciinput.us[2:]))
        c = peak/np.mean(self._calciinput.us[2:])
        fs = np.fft.rfftfreq(self._interface.blocksize, 1/self._interface.samplerate)
        f = np.interp(np.mean(self._calciinput.ks[2:]), np.arange(fs.size), fs)
        # get iinput if given
        if iinput is None:
            iinput = self._inputs[0].output
        # write to IInput
        if save:
            iinput.gain = self._gain
            if self._unit == "V":
                iinput.cV = c
                iinput.fV = f
            elif self._unit == "SPL" or self._unit == "Pa":
                iinput.cPa = c
                iinput.fPa = f
        return (f, c)
        
    def finished(self, block: bool = True, timeout: float = 1) -> bool:
        """This function can be used to wait for the calibration to be done.
        
        Args:
            block (bool, optional): Decides if the call of finished() should block. Defaults to True.
            timeout (float, optional): The timeout after which False is returned. Defaults to 1.

        Returns:
            bool: Returns True if the calibration finished and False on timeout.
        """
        if block:
            return self._calciinput.finished_event.wait(timeout = timeout)
        else:
            return self._calciinput.finished_event.is_set()

    def restart(self) -> bool:
        """Restart the calibration, unset the finished() flag.
        If the audio stream is still running, it starts with the next measurement series right away.
        
        Returns:
            bool: Returns True if successful and False if the calibration isn't finished yet."""
        if not self.finished(block=False):
            return False
        self._calciinput.counter = 0
        self._calciinput.finished_event.clear()
        return True

    class _CalIInput(AAnalyzer):
        def __init__(self, averages: int, blocksize: int, start_frame: int) -> None:
            self.finished_event = threading.Event()

            # result averaging
            self._avgs = averages + 3 # we dont consider the first three measurements
            self.counter = 0
            self.us = np.zeros(self._avgs, dtype=np.float32)
            self.ks = np.zeros(self._avgs, dtype=np.float32)

            # arrays needed for the array processing
            self._fft = np.empty(int(blocksize/2+1), dtype=np.complex128)
            self._spectrum = np.empty(int(blocksize/2+1), dtype=np.float32)
            self._window = np.hanning(blocksize)
            super().__init__(in_buffer = True,
                             blocksize = blocksize,
                             start_frame = start_frame)

        def _process(self) -> None:
            if self.finished_event.is_set():
                return
            if self.counter < self._avgs:
                self.physical_fft(self._in_buf[:, 0], self._fft, window = self._window)
                np.abs(self._fft, out = self._spectrum)

                kmax = np.argmax(self._spectrum)
                self.ks[self.counter] = kmax
                self.us[self.counter] = self._spectrum[kmax]
                self.counter += 1
            elif not self.finished_event.is_set():
                self.finished_event.set()

        def physical_fft(self, indata: "AData", outdata: "FFTData", window: "AData" = 1) -> None:
            np.fft.rfft(indata*window, norm = "forward", out = outdata)
            outdata[:] *= 2/np.mean(window)
