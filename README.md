# Intro

Basically a space invaders clone to learn work with Python and Basic of GameDev


## Game

* Kill Stuff
* ???
* Profit
## Controls
```
LEFT = a
RIGHT = d

FIRE = space

MUTE/UNMUTE = m
```

## What to build next?
The list is [here](TODO.md)

## Dependencies
todo: Figure out how to include dependencies in the project

### Pygame
Takes care of:
* user inputs (keyboard, kill)
* rendering UI
* managing Clock
* determining Collisions
* sounds

#### Install
`pip install -U pygame --user`

### Pyyaml
Takes care of configuration
#### Install
`pip install PyYAML`


### Pyinstall
Takes care of builds

#### Install
`pip install -U pyinstaller`


## Build

`pyinstaller turbovaders.spec`