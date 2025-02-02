"""types.py"""
import numpy as np
import numpy.typing as npt
from typing import Optional, Tuple, Union, Annotated
from .acore import AGenerator, AEffect, AAnalyzer, AInterface

# used for the in_as variable of the acore elements AEffect, AAnalyzer, AInerface
InAs = Optional[Tuple[Tuple[Optional[Union[AGenerator, AEffect, AInterface]], int], ...]]

# Used for the single channel data chunks transferred by all audio blocks
AData = Annotated[npt.NDArray[np.float32], "blocksize"]

# Used for FFt data chunks obtained by transforming a single channel data chunk
FFTData = Annotated[npt.NDArray[np.complex128], "int(blocksize/2+1)"]

# Used for the internal acore buffers
ABuf = Annotated[npt.NDArray[np.float32], "blocksize x channels"]

# all four acore elements
ACore = Union[AGenerator, AAnalyzer, AEffect, AInterface]






