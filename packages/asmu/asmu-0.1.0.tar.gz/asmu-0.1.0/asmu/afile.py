"""afile.py"""
import tempfile
import pathlib
import logging
import json
from typing import TYPE_CHECKING, Literal
from datetime import datetime
import soundfile
import numpy as np

if TYPE_CHECKING:
    from .interface import Interface
    from .types import ABuf

logger = logging.getLogger(__name__)

class AFile(soundfile.SoundFile):
    def __init__(self, interface: "Interface", mode: Literal["r", "w", "w+"]="r", path:str=None, channels:int=None, temp:bool=False) -> None:
        """The AFile class handles sound files. Metadata is used to store and load additional settings.
        It is recommended to open AFile's in a `with` context manager. 
        At the moment only .wav files with 24-bit encoding are supported.

        Args:
            interface (AInterface): _description_
            mode (Literal["r", "w", "w+", optional): _description_. Defaults to "r".
            path (str, optional): _description_. Defaults to None.
            channels (int, optional): _description_. Defaults to None.
            temp (bool, optional): _description_. Defaults to False.

        Raises:
            ValueError: _description_
            FileNotFoundError: _description_

        Example:
            ```python linenums="1" title="Find shape of audio file"
            import asmu
            with asmu.AFile(interface, mode = "r", path="myfile.wav") as afile:
                print(afile.data.shape)
            ```
        """
        # Check input
        if not mode in ["r", "w", "w+"]: raise ValueError("Specify a valid mode of [\"r\", \"w\", \"w+\"].")
        if path is None and temp is False: raise ValueError("For non-temporary files, a path has to be specified")
        if mode != "r" and channels is None: raise ValueError("Either read (mode = \"r\") a file or specify channels.")

        self._interface = interface
        self._mode = mode
        self.path = path
        if path is not None: 
            self.path = pathlib.Path(path)
            if not self.path.exists() and mode == "r": raise FileNotFoundError(f"File {path} does not exist.")
            if self.path.exists(): logger.debug(f"File {path} exists.")
        self._channels = channels
        self.temp = temp
        self._settings = {}
    
    # store settings as json string in metadata "comment"
    @property
    def settings(self) -> dict:
        """Additional JSON settings in the metadata's comment field."""
        return self._settings
    @settings.setter
    def settings(self, value: dict) -> None:
        self._settings = value
        self.comment = json.dumps(self.settings)

    @property
    def data(self) -> "ABuf":
        """This property can be used to access the data of the AFile.
        Dont use it during an active audio stream, as it resets the file pointer to the
        start of the file.

        Returns:
            ABuf: Data of AFile as numpy array of shape ("samples" x "channels").
        """
        self.flush()
        self.seek(0)
        return self.read(dtype="float32", always_2d=True)
    
    def __enter__(self):
        return self.open()
    
    def __exit__(self, *args):
        self.close()
        return False

    def open(self) -> "AFile":
        """Open a file, with respect to the settings specified at initialization.

        Returns:
            AFile: An instance of th opened AFile.
        """
        if self._mode == "r":
            super().__init__(self.path, mode=self._mode)
            # load settings
            if self.comment:
                self.settings = json.loads(self.comment)
        else:
            if self.temp:
                if self.path is None:
                    self._tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=True)
                else:
                    self._tmp = tempfile.NamedTemporaryFile(prefix=self.path.stem, suffix='.wav', dir=self.path.parent, delete=True)
                super().__init__(self._tmp, mode=self._mode, samplerate=self._interface.samplerate, channels=self._channels, subtype="PCM_24", format="WAV")
            else:
                super().__init__(self.path, mode=self._mode, samplerate=self._interface.samplerate, channels=self._channels, subtype="PCM_24", format="WAV")
            now = datetime.now()
            # set wav metadata
            self.title = self.path.stem
            self.date = now.strftime("%Y-%m-%dT%H:%M:%S%z") # ISO 8601
        return self