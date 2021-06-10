[![CI](https://github.com/JannisNe/muvi_maker/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/JannisNe/muvi_maker/actions/workflows/continuous_integration.yml)
[![Coverage Status](https://coveralls.io/repos/github/JannisNe/muvi_maker/badge.svg?branch=master)](https://coveralls.io/github/JannisNe/muvi_maker?branch=master)
[![PyPI version](https://badge.fury.io/py/muvimaker.svg)](https://badge.fury.io/py/muvimaker)

# `MuviMaker`
MuviMaker is a package that generates moving images from a sound file.
It uses 
* ```librosa``` to analyses soundfiles, 
* ```gizeh``` to generate vector graphics  
* ```moviepy``` to produce movie files

### Structure
The code uses ```tkinter``` to create a GUI. Running ```muvi_maker/main.py``` will start it.

The GUI part of the code can be found in ```muvi_maker/editor``` 
while the core functionality is located in ```muvi_maker/core```.

##### Central objects
* ````ProjectHandler```` : The central object handling the book keeping, making sure all parts play together well
in terms of framerate etc, see ``muvi_maker/core/project.py``.
* ````Sound````: An object that analyses a sound file, providing 
e.g. its volume, chroma, spectrogram etc, see ````muvi_maker/core/sound.py````
* ````Picture````: An object that produces the frames. 
Various attributes can be triggered by ``Sound``s, see ```muvi_maker/core/pictures/```
* ```Video```: The object combining various ``Sound``s to make the final video file, see ``muvi_maker/core/video.py``


### Installing `MuviMaker`

To be able to use ```moviepy``` the library ```ffmpeg``` has to be installed on your system.
If it is not you can simply execute:
```
sudo apt-get update
sudo apt-get install ffmpeg
sudo apt-get install frei0r-plugins
```

* ##### Only using `MuviMaker`:

You can install `MuviMaker` via pip
```
pip install muvimaker
```

* ##### Working with the source code:

If you want to get the source code and work with it, you can clone the repository:

```bash
 git clone git@github.com:JannisNe/muvi_maker
```

You will have to add the installation directory to the `PYTHONPATH` to be able tu use the code:
```
export PYTHONPATH=/path/to/moviemaker
```

All requirements can be install via pip:
```
pip install -r ./requirements.txt
```
