[![Build Status](https://travis-ci.com/JannisNe/muvi_maker.svg?branch=master)](https://travis-ci.com/JannisNe/muvi_maker)
# MuviMaker
MuviMaker is a package that generates moving images from a sound file.
It uses ```librosa``` to analyses soundfiles, ```gizeh``` to generate vector graphics and 
```moviepy``` to produce movie files

### Structure
The code uses ```tkinter``` to create a GUI. Running ```muvi_maker/main.py``` will start it.

The GUI part of the code can be found in ```muvi_maker/editor/``` while the part that generates pictures, analyses the soundfile, etc is located in ```muvi_maker/core```.



### Installing MuviMaker
Right now there is no easy way of installing MuviMaker. 

Cloning the repository is the easiest way to get the code:

```bash
 git clone git@github.com:JannisNe/muvi_maker
```
