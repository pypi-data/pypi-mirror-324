"""Welcome to the API of the asmu module!

To get started, the specific sub-modules are explained below:

- [asmu.interface][]: This holds the most important class for nearly every setup you will be working with, the `Interface`. Get familiar with its input arguments and how to choose the correct device.
- [asmu.generator][]: In this sub-module you can find all generators, so "audio processors" with one or multiple outputs.
- [asmu.effect][]: In this sub-module you can find all effects, so "audio processors" with one or multiple inputs and outputs.
- [asmu.analyzer][]: In this sub-module you can find all analyzers, so "audio processors" with one or multiple inputs.
- [asmu.io][]: In this sub-module you can find the Input and Output classes used in the "audio processors". You will rarely use them directly, but the special IInput and IOutput classes used by the interface, store a lot of important information you may want to access or modify."""
# enable sounddevice ASIO
import os
os.environ["SD_ENABLE_ASIO"] = "1"

from .afile import AFile
from .asetup import ASetup
from .interface import Interface
from . import io
from . import generator
from . import effect
from . import analyzer

# enable logging
import logging
logging.getLogger("asmu").addHandler(logging.NullHandler())

def query_devices(device = None, kind = None):
    import sounddevice as sd
    return sd.query_devices(device, kind)
