"""io.py"""
import contextlib
import logging
from typing import TYPE_CHECKING, Tuple, Optional, Union
import numpy as np

if TYPE_CHECKING:
    from .interface import Interface
    from .processor import Analyzer, Effect, Generator

logger = logging.getLogger(__name__)

class Input:
    def __init__(self, processor: Union["Effect", "Interface", "Analyzer"]):
        """Input base class.

        Args:
            processor (Union[Effect, Interface, Analyzer]): Reference to the corresponding Processor object.
        """
        self._processor = processor
        self._output: Optional["Output"] = None

    def __del__(self):
        if self._output is not None:
            self._output.disconnect(self)
        else:
            logger.info("No output to disconnect.")

    @property
    def output(self) -> Optional["Output"]:
        return self._output
    @output.setter
    def output(self, value: Optional["Output"]):
        self._output = value
        # if an output was set or unset, update acore module of processor
        self._processor.update_acore()

class Output:
    def __init__(self, processor: Union["Generator", "Effect", "Interface"]):
        """Output base class.

        Args:
            processor (Union[Generator, Effect, Interface]): Reference to the corresponding Processor object.
        """
        self._processor = processor
        self._inputs: Tuple[Input] = ()

    def __del__(self):
        for inpu in self.inputs:
            self.disconnect(inpu)

    @property
    def inputs(self):
        return self._inputs
    
    @property
    def idx(self) -> int:
        return self._processor.outputs.index(self)
    
    @property
    def acore(self):
        return self._processor.acore
    
    def connect(self, input: "Input"):
        if input not in self._inputs:
            self._inputs += (input, )
            input.output = self
            self._processor.update_acore()
        else:
            logger.info("Input is already connected to output.")

    def disconnect(self, input: "Input"):
        if input.output is self and input in self._inputs:
            self._inputs = tuple(inp for inp in self._inputs if inp != self)
            input.output = None
            self._processor.update_acore()
        else:
            logger.info("Trying to disconnect an input that is not connected to this output")

class IInput(Output):
    def __init__(self,
                 interface: "Interface",
                 channel: int, 
                 reference: Optional[bool] = None,
                 name: Optional[str] = None,
                 gain: Optional[float] = None,
                 latency: Optional[int] = 0,
                 color: Optional[str] = None,
                 cPa: Optional[float] = 1,
                 fPa: Optional[float] = None,
                 cV: Optional[float] = 1,
                 fV: Optional[float] = None,
                 cFR: Optional[np.ndarray] = None,
                 fFR: Optional[np.ndarray] = None):
        """A special type of Output class used for the analog interface inputs.
        It stores various settings and options.

        Args:
            interface (Interface): Reference to an Interface instance.
            channel (int): Channel number on the interface.
            reference (Optional[bool], optional): Flag if the channel is used as reference for computation/calibration. Defaults to None.
            name (Optional[str], optional): Trivial name. Defaults to None.
            gain (Optional[float], optional): The gain setting of the input. Defaults to None.
            latency (Optional[int], optional): Individual IO latency (relative to Interface's system latency). Defaults to 0.
            color (Optional[str], optional): A color used for plotting. Defaults to None.
            cPa (Optional[float], optional): Pressure calibration factor in Pascal. Defaults to 1.
            fPa (Optional[float], optional): Frequency used for pressure calibration. Defaults to None.
            cV (Optional[float], optional): Voltage calibration factor in Volts. Defaults to 1.
            fV (Optional[float], optional): Frequency used for voltage calibration. Defaults to None.
            cFR (Optional[np.ndarray], optional): Frequency response calibration vector. Defaults to None.
            fFR (Optional[np.ndarray], optional): Corresponding frequency vector. Defaults to None.
        """
        self._interface = interface
        self.channel = channel
        self.reference = reference
        self.name = name
        self.gain = gain
        self.latency = latency
        self.color = color
        self.cPa = cPa
        self.fPa = fPa
        self.cV = cV
        self.fV = fV
        self.cFR = cFR
        self.fFR = fFR
        super().__init__(interface)

    def serialize(self) -> dict:
        data = {}
        data["channel"] = self.channel
        if self.reference is not None: data["reference"] = self.reference
        if self.name is not None: data["name"] = self.name
        if self.gain is not None: data["gain"] = self.gain
        if self.latency is not None: data["latency"] = self.latency
        if self.color is not None: data["color"] = self.color
        if self.cPa is not None: data["cPa"] = self.cPa
        if self.fPa is not None: data["fPa"] = self.fPa
        if self.cV is not None: data["cV"] = self.cV
        if self.fV is not None: data["fV"] = self.fV
        if self.cFR is not None:
            path = self._interface.path.with_suffix(f"/in_ch{self.channel:3.0f}_cFR.npy")
            np.save(path, self.cFR)
            data["cFR"] = path
        if self.fFR is not None:
            path = self._interface.path.with_suffix(f"/in_ch{self.channel:3.0f}_fFR.npy")
            np.save(path, self.fFR)
            data["fFR"] = path
        return data
    
    def deserialize(self, data: dict) -> None:
        self.channel = data["channel"]
        with contextlib.suppress(KeyError): self.reference = data["reference"]
        with contextlib.suppress(KeyError): self.name = data["name"]
        with contextlib.suppress(KeyError): self.gain = data["gain"]
        with contextlib.suppress(KeyError): self.latency = data["latency"]
        with contextlib.suppress(KeyError): self.color = data["color"]
        with contextlib.suppress(KeyError): self.cPa = data["cPa"]
        with contextlib.suppress(KeyError): self.fPa = data["fPa"]
        with contextlib.suppress(KeyError): self.cV = data["cV"]
        with contextlib.suppress(KeyError): self.fV = data["fV"]
        with contextlib.suppress(KeyError): self.cFR = np.load(data["cFR"])
        with contextlib.suppress(KeyError): self.fFR = np.load(data["fFR"])


class IOutput(Input):
    def __init__(self,
                 interface: "Interface",
                 channel: int, 
                 reference: Optional[bool] = None,
                 name: Optional[str] = None,
                 gain: Optional[float] = None,
                 latency: Optional[int] = 0,
                 color: Optional[str] = None,
                 cPa: Optional[float] = 1,
                 fPa: Optional[float] = None,
                 cV: Optional[float] = 1,
                 fV: Optional[float] = None,
                 cFR: Optional[np.ndarray] = None,
                 fFR: Optional[np.ndarray] = None):
        """A special type of Input class used for the analog interface outputs.
        It stores various settings and options.

        Args:
            interface (Interface): Reference to an Interface instance.
            channel (int): Channel number on the interface.
            reference (Optional[bool], optional): Flag if the channel is used as reference for computation/calibration. Defaults to None.
            name (Optional[str], optional): Trivial name. Defaults to None.
            gain (Optional[float], optional): The gain setting of the output. Defaults to None.
            latency (Optional[int], optional): Individual IO latency (relative to Interface's system latency). Defaults to 0.
            color (Optional[str], optional): A color used for plotting. Defaults to None.
            cPa (Optional[float], optional): Pressure calibration factor in Pascal. Defaults to 1.
            fPa (Optional[float], optional): Frequency used for pressure calibration. Defaults to None.
            cV (Optional[float], optional): Voltage calibration factor in Volts. Defaults to 1.
            fV (Optional[float], optional): Frequency used for voltage calibration. Defaults to None.
            cFR (Optional[np.ndarray], optional): Frequency response calibration vector. Defaults to None.
            fFR (Optional[np.ndarray], optional): Corresponding frequency vector. Defaults to None.
        """
        self._interface = interface
        self.channel = channel
        self.reference = reference
        self.name = name
        self.gain = gain
        self.latency = latency
        self.color = color
        self.cPa = cPa
        self.fPa = fPa
        self.cV = cV
        self.fV = fV
        self.cFR = cFR
        self.fFR = fFR
        super().__init__(interface)

    def serialize(self) -> dict:
        data = {}
        data["channel"] = self.channel
        if self.reference is not None: data["reference"] = self.reference
        if self.name is not None: data["name"] = self.name
        if self.gain is not None: data["gain"] = self.gain
        if self.latency is not None: data["latency"] = self.latency
        if self.color is not None: data["color"] = self.color
        if self.cPa is not None: data["cPa"] = self.cPa
        if self.fPa is not None: data["fPa"] = self.fPa
        if self.cV is not None: data["cV"] = self.cV
        if self.fV is not None: data["fV"] = self.fV
        if self.cFR is not None:
            path = self._interface.path.with_suffix(f"/out_ch{self.channel:3.0f}_cFR.npy")
            np.save(path, self.cFR)
            data["cFR"] = path
        if self.fFR is not None:
            path = self._interface.path.with_suffix(f"/out_ch{self.channel:3.0f}_fFR.npy")
            np.save(path, self.fFR)
            data["fFR"] = path
        return data
    
    def deserialize(self, data: dict, hashmap: dict = {}) -> None:
        self.channel = data["channel"]
        with contextlib.suppress(KeyError): self.reference = data["reference"]
        with contextlib.suppress(KeyError): self.name = data["name"]
        with contextlib.suppress(KeyError): self.gain = data["gain"]
        with contextlib.suppress(KeyError): self.latency = data["latency"]
        with contextlib.suppress(KeyError): self.color = data["color"]
        with contextlib.suppress(KeyError): self.cPa = data["cPa"]
        with contextlib.suppress(KeyError): self.fPa = data["fPa"]
        with contextlib.suppress(KeyError): self.cV = data["cV"]
        with contextlib.suppress(KeyError): self.fV = data["fV"]
        with contextlib.suppress(KeyError): self.cFR = np.load(data["cFR"])
        with contextlib.suppress(KeyError): self.fFR = np.load(data["fFR"])