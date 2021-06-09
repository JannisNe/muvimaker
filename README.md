[![CI](https://github.com/JannisNe/muvi_maker/actions/workflows/continuous_integration.yml/badge.svg)](https://github.com/JannisNe/muvi_maker/actions/workflows/continuous_integration.yml)
[![Coverage Status](https://coveralls.io/repos/github/JannisNe/muvi_maker/badge.svg?branch=master)](https://coveralls.io/github/JannisNe/muvi_maker?branch=master)
# MuviMaker
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


### Installing MuviMaker
Right now there is no easy way of installing MuviMaker. 

Cloning the repository is the easiest way to get the code:

```bash
 git clone git@github.com:JannisNe/muvi_maker
```

All requirements can be install via pip:
```
pip install -r ./requirements.txt
```