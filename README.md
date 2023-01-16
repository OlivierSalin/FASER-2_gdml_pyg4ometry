# FASER-2_gdml_pyg4ometry

This repository contains FASER-2 geometries in a gdml format with several different configurations. 
Those geometries are focused on the SciFi trackers layers with a different numbers of layers and material based on Sune Jakobsen estimation.
The gdml filed are created using [pyg4ometry](http://www.pp.rhul.ac.uk/bdsim/pyg4ometry/)

## Install pyg4ometry
Using Docker (Tested on Windows without visualisation)
*Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
*Open a terminal (linux) or cmd (windows)
*Download the [pre-built image from Stewart Boogert](https://hub.docker.com/r/sboogert/pyg4ometry-ubuntu20/tags)
```
$ docker pull sboogert/pyg4ometry-ubuntu20:latest
```
*Start the container
```
$ docker run -ti sboogert/pyg4ometry-ubuntu20:latest
```
*run the python functions in /tmp/pyg4ometry/src

