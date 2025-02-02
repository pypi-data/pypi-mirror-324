import json
import pathlib
import logging
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .interface import Interface

logger = logging.getLogger(__name__)

class ASetup:
    def __init__(self, path: str, ) -> None:
        """The ASetup class handles .asmu JSON files. 
        It is used to load and store Interface general settings 
        and IInput/IOutput configuration and calibration values.

        Args:
            path (str): Path to .asmu file. Defaults to None.
        """
        self.path = pathlib.Path(path)
        self.interface: "Interface" = None
        # add time/date and other info here
        now = datetime.now()
        self.date = now.strftime("%Y-%m-%dT%H:%M:%S%z") # ISO 8601


    def __del__(self):
        if self.interface is not None:
            self.interface.asetup = None

    def load(self):
        if self.interface is None:
            raise ValueError("No associated Interface to load to.")
        with open(self.path, "r", encoding="utf-8") as asetup:
            self.deserialize(json.load(asetup))

    def save(self, path: str = None):
        if self.interface is None:
            raise ValueError("No associated Interface to save from.")

        if path is not None:
            path = pathlib.Path(path)
        else:
            path = self.path

        with open(path, "w", encoding="utf-8") as asetup:
            asetup.write(json.dumps(self.serialize(), sort_keys=True, indent=4, separators=(',', ': ')))

    def serialize(self):
        data = self.interface.serialize()
        data["created"] = self.date
        return data

    def deserialize(self, data: dict):
        self.date = data["created"]
        self.interface.deserialize(data)
