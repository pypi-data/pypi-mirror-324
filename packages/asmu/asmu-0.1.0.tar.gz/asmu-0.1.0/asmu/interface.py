import logging
from typing import TYPE_CHECKING, List, Tuple, Union, Optional, Callable
import numpy as np
import sounddevice as sd

from .acore import AInterface
from .processor import Processor
from .io import IInput, IOutput

if TYPE_CHECKING:
    from .asetup import ASetup
    from .processor import AAnalyzer

logger = logging.getLogger(__name__)

START_FRAME = 0

class Interface(Processor):
    def __init__(self, 
                 asetup: Optional["ASetup"] = None,
                 device: Optional[Union[Tuple[Union[str, int], Union[str, int]], Union[str, int]]] = None,
                 samplerate: Optional[int] = 44100,
                 blocksize: Optional[int] = 1024,
                 analog_input_channels: List[int] = None,
                 analog_output_channels: List[int] = None,
                 no_audio_device: bool = False):
        """The Interface class represents the audio interface or soundcard. 
        It is holding the audio generator and manages settings.
        The settings can either be specified on intialization, by an ASetup class, or used as default.

        Args:
            asetup (ASetup, optional): Reference to an ASetup instance. If set, loads the settings from the given ASetup.
                If you dont want that, specify it after initialization, by setting `Interface.asetup = ASetup`. Defaults to None.
            device (Union[Tuple[Union[str, int], Union[str, int]], Union[str, int]], optional): Device name, or tuple of device names for different input and output device. If None, the default device(s) are used. Defaults to None.
            samplerate (int, optional): The samplerate in samples per second. Defaults to 44100.
            blocksize (int, optional): The blocksize defines the samples per frame. Defaults to 1024.
            analog_input_channels (List[int], optional): List if analog input channels, only works for ASIO, CoreAudio devices, or no_audio_device. Defaults to None.
            analog_output_channels (List[int], optional): List if analog output channels, only works for ASIO, CoreAudio devices, or no_audio_device. Defaults to None.
            no_audio_device (bool, optional): Flag used for testing. Skips audio device and allows the direct use of the callback function. Defaults to False.

        Notes:
            The device name can be optained by running the following code snippet.
            ```python linenums="1" title="List audio devices"
            import asmu
            asmu.query_devices()
            ```
        """
        # this is used for the analyzers to add themselfes later
        self._analyzers: Tuple["AAnalyzer"] = ()

        self.asetup = asetup
        if asetup is not None:
            asetup.load()
        else:
            # init from given values
            self._samplerate = samplerate
            self._blocksize = blocksize
            self.latency = 0
            # init device
            self._device = device
            if device is None:
                # if None use default
                self._device = sd.default.device
            elif not isinstance(self._device, tuple):
                # if single device use for input and output
                self._device = (self._device, self._device)
            self._no_audio_device = no_audio_device
            if not no_audio_device:
                if not self._is_asio() or not self._is_ca():
                    # if not asio or coraaudio overwrite the channel lists
                    logger.warning("No ASIO or CoreAudio device specified, channel numbers are ignored.")
                    analog_input_channels = list(range(sd.query_devices(device=self._device[0], kind="input")["max_input_channels"]))
                    analog_input_channels = [ch+1 for ch in analog_input_channels]
                    analog_output_channels = list(range(sd.query_devices(device=self._device[1], kind="output")["max_output_channels"]))
                    analog_output_channels = [ch+1 for ch in analog_output_channels]
            # set in-/outputs accordingly
            self._iinputs = ()
            if self._device[0] is not None and analog_input_channels is not None:
                self._iinputs = tuple(IInput(self, iin_ch) for iin_ch in analog_input_channels)
            self._ioutputs = ()
            if self._device[1] is not None and analog_output_channels is not None:
                self._ioutputs = tuple(IOutput(self, iout_ch) for iout_ch in analog_output_channels)

            self._ainterface = AInterface(blocksize = self._blocksize,
                                        start_frame = START_FRAME)
        super().__init__(self)

    def __del__(self):
        # deregister from asetup
        if self._asetup is not None:
            self._asetup.interface = None

    @property
    def samplerate(self):
        return self._samplerate

    @property
    def blocksize(self):
        return self._blocksize

    @property
    def device(self):
        return self._device

    @property
    def start_frame(self) -> int:
        return START_FRAME
    
    @property
    def callback(self) -> Callable:
        return self._ainterface.callback
    
    @property
    def asetup(self) -> Optional["ASetup"]:
        return self._asetup
    @asetup.setter
    def asetup(self, value: Optional["ASetup"]):
        self._asetup = value
        # register in asetup
        if value is not None:
            self._asetup.interface = self

    @property
    def analyzers(self):
        return self._analyzers
    @analyzers.setter
    def analyzers(self, value):
        self._analyzers = value
        self.update_acore()

    @property
    def acore(self):
        return self._ainterface

    @property
    def outputs(self) -> Tuple["IInput"]:
        return self._iinputs

    def iinput(self, idx: int=0, ch: int= None, name: str=None) -> "IInput":
        if ch is not None:
            try:
                return next((outpu for outpu in self._iinputs if outpu.channel == ch))
            except StopIteration:
                raise ValueError(f"No IInput on channel {ch} registered.")
        if name is not None:
            try:
                return next((outpu for outpu in self._iinputs if outpu.name == name))
            except StopIteration:
                raise ValueError(f"No IInput with name {name} registered.")
        return self._iinputs[idx]

    def ioutput(self, idx: int=0, ch: int= None, name: str=None) -> "IOutput":
        if ch is not None:
            try:
                return next((inpu for inpu in self._ioutputs if inpu.channel == ch))
            except StopIteration:
                raise ValueError(f"No IOutput on channel {ch} registered.")
        if name is not None:
            try:
                return next((inpu for inpu in self._ioutputs if inpu.name == name))
            except StopIteration:
                raise ValueError(f"No IOutput with name {name} registered.")
        return self._ioutputs[idx]

    def _cal_latency(self, time):
        """Calculate and store loopback latency without physical connection.

        !!! warning
            Dont rely on this method, as it only calculates the ADC/DAC's internal latency. 
            Use [latency_from_rec.py](../examples.md/#latency_from_rec.py) to compare this result with the real loopback calibration.

        Args:
            time (CData): The time object given in the callback function.
        """
        self.latency = round((time.outputBufferDacTime-time.inputBufferAdcTime)*self.samplerate + 1) # the +1 was measured experimentally (could be the cable?)

    def _is_asio(self) -> bool:
        """Determine if ALL of the set io devices are ASIO compatible.

        Returns:
            bool: Returns True, if all given devices are ASIO compatible.
        """
        asio = True
        if self._device[0] is not None:
            asio = ("asio" in str(sd.query_devices(device = self._device[0], kind = "input")["name"]).lower())
        if self._device[1] is not None:
            asio = ("asio" in str(sd.query_devices(device = self._device[1], kind = "output")["name"]).lower())
        return asio
    
    def _is_ca(self) -> bool:
        """Determine if ALL of the set io devices are CoraAudio compatible.

        Returns:
            bool: Returns True, if all given devices are CoraAudio compatible.
        """
        ca = True
        if self._device[0] is not None:
            ca = ("coreaudio" in str(sd.query_devices(device = self._device[0], kind = "input")["name"]).lower())
        if self._device[1] is not None:
            ca = ("coreaudio" in str(sd.query_devices(device = self._device[1], kind = "output")["name"]).lower())
        return ca
    
    def _is_test(self) -> bool:
        """Determine if at least one of the set io devices is set to test.

        Returns:
            bool: Returns True, if at least one given devices is set to test.
        """
        test = False
        if self._device[0] is not None:
            test = ("test" in str(self._device[0]).lower())
        if self._device[1] is not None:
            test = ("test" in str(self._device[1]).lower())
        return test

    # SOUNDDEVICE 
    def _init_sounddevice(self, stream: sd.default) -> None:
        """Initiializes sounddevice with the classes attributes for the given lists of inputs and outputs.
        !!! warning
            This method is currently only implemented for ASIO devices (Windows).
    
        Args:
            io (tuple of lists): Tuple that contains lists of Input and Output objects.
                If one of them is not needed, leave list empty.

        Raises:
            AttributeError: No audio device specified
        """
        stream.dtype = np.float32
        if self.samplerate is not None:
            stream.samplerate = self.samplerate
        if self.blocksize is not None:
            stream.blocksize = self.blocksize
        stream.device = self.device
        if self._is_asio():
            if self._iinputs:
                in_channels = [inpu.channel - 1 for inpu in self._iinputs] # convert to channel names starting with 0
                asio_in = sd.AsioSettings(channel_selectors=in_channels)

                if not self._ioutputs:
                    stream.extra_settings = asio_in
                    stream.channels = len(in_channels)
                    return

            if self._ioutputs:
                out_channels = [output.channel - 1 for output in self._ioutputs]
                asio_out = sd.AsioSettings(channel_selectors=out_channels)

                if not self._iinputs:
                    stream.extra_settings = asio_out
                    stream.channels = len(out_channels)
                    return
            
            if self._iinputs and self._ioutputs:
                stream.extra_settings = (asio_in, asio_out)
                stream.channels = (len(in_channels), len(out_channels))
                return
            
        elif self._is_ca(): 
            raise NotImplementedError("CoreAudio channel selection is not tested!")
            if self._iinputs:
                in_channels = [inpu.channel - 1 for inpu in self._iinputs] # convert to channel names starting with 0
                ca_in = sd.CoreAudioSettings(channel_map=in_channels)

                if not self._ioutputs:
                    stream.extra_settings = ca_in
                    stream.channels = len(in_channels)
                    return
                
            if self._ioutputs:
                out_channels = [-1]*sd.query_devices(device=self.device, kind="output")["max_output_channels"]
                for idx, c in enumerate(self._ioutputs):
                    out_channels[c.channel -1] = idx
                ca_out = sd.CoreAudioSettings(channel_map=out_channels)

                if not self._iinputs:
                    stream.extra_settings = ca_out
                    stream.channels = len(out_channels)
                    return

            if self._iinputs and self._ioutputs:
                stream.extra_settings = (ca_in, ca_out)
                stream.channels = (len(in_channels), len(out_channels))
                return

    def start(self, end_frame: int = None) -> sd.Stream:
        """Start the audio stream.

        Args:
            end_frame (int, optional): If set, the stream is stopped at the given end_frame. Defaults to None.

        Returns:
            sd.Stream: Reference to the started stream.
        """
        if self._no_audio_device:
            raise ValueError("Starting a stream in no_audio_device mode is not possible!")
        self._init_sounddevice(sd.default)
        self._ainterface.end_frame = end_frame
        stream = sd.Stream(callback=self._ainterface.callback)
        stream.start()
        return stream
        
    def update_acore(self):
        """This is use by the Input and Output classes to update the connections of the AInterface."""
        # create in_as tuple
        in_as = ()
        for inp in self._ioutputs:
            # add proper connection constraint
            if inp.output is None:
                in_as += ((None, 0), )
            else:
                # find channel idx it is connected to
                in_as += ((inp.output.acore, inp.output.idx), )
        self._ainterface.in_as = in_as
        # count outputs that have a connection
        self._ainterface.out_chs = len(self._iinputs)
        # update alz
        self._ainterface.alzs = tuple(alz.acore for alz in self.analyzers)

    def serialize(self):
        data = {}
        data["samplerate"] = self._samplerate
        data["blocksize"] = self._blocksize
        data["latency"] = self.latency
        data["no_audio_device"] = self._no_audio_device

        if not self._no_audio_device:
            device = ()
            if self._device[0] is not None:
                device += (sd.query_devices(device = self._device[0], kind = "input"), )
            else:
                device += (None, )
            if self._device[1] is not None:
                device += (sd.query_devices(device = self._device[1], kind = "output"), )
            else:
                device += (None, )
        data["device"] = tuple(self._device)

        iinputs = []
        for iinput in self._iinputs:
            iinputs.append(iinput.serialize())
        data["iinputs"] = iinputs

        ioutputs = []
        for ioutput in self._ioutputs:
            ioutputs.append(ioutput.serialize())
        data["ioutputs"] = ioutputs
        return data

    def deserialize(self, data: dict):
        if data["samplerate"] is None: raise ValueError("samplerate must be specified!")
        self._samplerate = data["samplerate"]
        if data["blocksize"] is None: raise ValueError("blocksize must be specified!")
        self._blocksize = data["blocksize"]
        self.latency = data["latency"]
        self._no_audio_device = data["no_audio_device"]
        if self._no_audio_device:
            self._device = data["device"]
        else:
            self._device = (data["device"][0]["index"], data["device"][1]["index"])

        self._iinputs = ()
        for iinput_data in data["iinputs"]:
            iinput = IInput(self, iinput_data["channel"])
            iinput.deserialize(iinput_data)
            self._iinputs += (iinput, )

        self._ioutputs = ()
        for ioutput_data in data["ioutputs"]:
            ioutput = IOutput(self, ioutput_data["channel"])
            ioutput.deserialize(ioutput_data)
            self._ioutputs += (ioutput, )

        self._ainterface = AInterface(blocksize = self._blocksize,
                                      start_frame = START_FRAME)
