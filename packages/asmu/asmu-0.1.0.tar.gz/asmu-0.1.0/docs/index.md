---
hide:
  - toc
---
# Acoustic Signal Measurement Utilities

The **asmu** Python package enables multichannel real-time audio playback, processing and recording. It is implemented in pure Python with a few additional packages:

- [numpy](https://pypi.org/project/numpy/) - Is the fundamental package for scientific computing, array manipulation and signal processing.
- [sounddevice](https://pypi.org/project/sounddevice/) - Is a Python wrapper for the [PortAudio](https://www.portaudio.com/) functions. It is used for the communication with the soundcard or audio interface.
- [soundfile](https://pypi.org/project/soundfile/) - Is an audio library to read and write sound files through [libsndfile](http://www.mega-nerd.com/libsndfile/).

The main focus of **asmu** is modularity and easy expandability. It provides a few base classes, to implement nearly every "audio processor". 

- **Generator**: The base class for audio processors with one or multiple outputs.
- **Effects**: The base class for audio processors with one or multiple inputs and outputs.
- **Analyzer**: The base class for audio processors with one or multiple inputs.
- **Interface**: The base class for the soundcard or audio interface with one or multiple inputs and outputs.

These base classes enable easy connection between each other, allowing efficient buffer transport, and `threading.Event()` or `queueing.Queue()` based communication for information exchange during an active audio stream. Additionally, **asmu** offer some pre implemented audio processors, that can be used right away.

!!! warning
    This software is still under development. This means:

    - No input checking, which can cause exceptions that are complicated to debug
    - The structure of the package can change drastically
    - No entitlement to backwards compatibility
    - The documentation is still in development and not complete
