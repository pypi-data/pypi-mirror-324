"""processor.py"""
import logging
from typing import TYPE_CHECKING, Tuple
from abc import ABC, abstractmethod

from .io import Input, Output

if TYPE_CHECKING:
    from .acore import AGenerator, AEffect, AAnalyzer
    from .interface import Interface
    from .types import ACore

logger = logging.getLogger(__name__)

class Processor(ABC):
    def __init__(self, interface: "Interface") -> None:
        self._interface = interface

    @property
    @abstractmethod
    def acore(self) -> "ACore":
        """Returns the ACore element of the processor."""

    @abstractmethod
    def update_acore(self) -> None:
        """Set in_as and out_chs of acore. This is called by the inputs/outputs."""

class Generator(Processor):
    def __init__(self, agenerator: "AGenerator", interface: "Interface", outputs: Tuple["Output"], out_update: bool) -> None:
        """This is the base class for generators, holding the audio generator.

        Args:
            agenerator (AGenerator): Reference to the corresponding ACore object.
            interface (Interface): Reference to an Interface instance.
            outputs (Tuple[Output]): A tuple of Output instances.
            out_update (bool): Flag that decides if dynamic output updates are enabled.
        """
        self._agenerator = agenerator
        self._outputs = outputs
        self._out_update = out_update
        # update_acore() is not called here, because it is called on the first connection anyways!
        super().__init__(interface)

    @property
    def acore(self) -> "AGenerator":
        return self._agenerator

    @property
    def outputs(self) -> Tuple["Output"]:
        return self._outputs

    def output(self, idx: int = 0) -> "Output":
        while idx > len(self._outputs) -1 and self._out_update:
            self._outputs += (Output(self), )
        return self._outputs[idx]

    def update_acore(self) -> None:
        """This is use by the Input and Output classes to update the connections of the AGenerator."""
        self._agenerator.out_chs = len(self._outputs)

class Effect(Processor):
    def __init__(self, aeffect: "AEffect", interface: "Interface", inputs: Tuple["Input"], outputs: Tuple["Output"], in_update: bool, out_update: bool) -> None:
        """This is the base class for effects, holding the audio effect.

        Args:
            aeffect (AEffect): Reference to the corresponding ACore object.
            interface (Interface): Reference to an Interface instance.
            inputs (Tuple[Input]): A tuple of Input instances.
            outputs (Tuple[Output]): A tuple of Output instances.
            in_update (bool): Flag that decides if dynamic input updates are enabled.
            out_update (bool): Flag that decides if dynamic output updates are enabled.

        Notes:
            If both update flags are enabled, input and output counts are syncronized.
        """
        self._aeffect = aeffect
        self._inputs = inputs
        self._outputs = outputs
        self._in_update = in_update
        self._out_update = out_update
        # update_acore() is not called here, because it is called on the first connection anyways!
        super().__init__(interface)

    @property
    def acore(self) -> "AEffect":
        return self._aeffect

    @property
    def outputs(self) -> Tuple["Output"]:
        return self._outputs

    def input(self, idx: int = 0) -> "Input":
        while idx > len(self._inputs) -1 and self._in_update:
            self._inputs += (Input(self), )
            # if update flags are true, keep channel count equal
            if self._out_update: self._outputs += (Output(self), )
        return self._inputs[idx]

    def output(self, idx: int = 0) -> "Output":
        while idx > len(self._outputs) -1 and self._out_update:
            self._outputs += (Output(self), )
            # if update flags are true, keep channel count equal
            if self._in_update: self._inputs += (Input(self), )
        return self._outputs[idx]

    def update_acore(self) -> None:
        """This is use by the Input and Output classes to update the connections of the AEffect."""
        # create in_as tuple
        in_as = ()
        for inp in self._inputs:
            # add proper connection constraint
            if inp.output is None:
                in_as += ((None, 0), )
                logger.info(f"Input {inp} is not yet connected to any outputs.")
            else:
                # find channel idx it is connected to
                in_as += ((inp.output.acore, inp.output.idx), )
        self._aeffect.in_as = in_as
        # count outputs that have a connection
        self._aeffect.out_chs = len(self._outputs)

class Analyzer(Processor):
    def __init__(self, aanalyzer: "AAnalyzer", interface: "Interface", inputs: Tuple["Input"], in_update: bool) -> None:
        """This is the base class for analyzers, holding the audio analyzer.

        Args:
            aanalyzer (AAnalyzer): Reference to the corresponding ACore object.
            interface (Interface): Reference to an Interface instance.
            inputs (Tuple[Input]): A tuple of Input instances.
            in_update (bool): Flag that decides if dynamic input updates are enabled.
        """
        self._aanalyzer = aanalyzer
        self._inputs = inputs
        self._in_update = in_update
        # add to analyzer list in interface
        interface.analyzers += (self, )
        # update_acore() is not called here, because it is called on the first connection anyways!
        super().__init__(interface)

    def __del__(self):
        # remove from analyzer list in interface
        self._interface.analyzers = tuple(alz for alz in self._interface.analyzers if alz != self)

    @property
    def acore(self) -> "AAnalyzer":
        return self._aanalyzer

    def input(self, idx: int=0) -> "Input":
        while idx > len(self._inputs) -1 and self._in_update:
            self._inputs += (Input(self), )
        return self._inputs[idx]

    def update_acore(self) -> None:
        """This is use by the Input and Output classes to update the connections of the AAnalyzer."""
        # create in_as tuple
        in_as = ()
        for inp in self._inputs:
            # add proper connection constraint
            if inp.output is None:
                in_as += ((None, 0), )
                logger.info(f"Input {inp} is not yet connected to any outputs.")
            else:
                # find channel idx it is connected to
                in_as += ((inp.output.acore, inp.output.idx), )
        self._aanalyzer.in_as = in_as
