# CNOT CIRCUIT SYNTHESIS

This project was created as part of my bachelorthesis **Improving a Synthesis Algorithm for a Class of Quantum
Circuits**.

The core of the project is formed by the synthesis algorithm, together with some utility functions to make it easier to
run the algorithm repeatedly. This small function library can be found in the ```src ``` folder.
The functions are imported into _IPython_ notebooks, where they are used to execute and evaluate the algorithm. The
notebooks can be found in the ```notebooks``` folder. Any resulting files are saved in the ```resources``` folder.

## Requirements

The whole project was created and used within the _PyCharm_ development environment on a Windows machine. Some parts of
it where executed on a _CUDA_ capable graphics card. It was NOT tested with a different setup.

### Core Functionality

The project was run within an _anaconda3_ environment. In order to run the core functionality of it, make sure you have
installed the following modules:

- os
- psutil
- random
- numpy
- re
- ast
- (pytorch)

The project also includes a _pytorch_ implementation of the algorithm. If you do not want to use this implementation,
feel free to delete ```src/algorithm/torch``` and make sure to remove the _torch_ code from
```src/input/read_files.py```. The latter contains some utilities to load the input from a file directly into a tensor.

### PyTorch and CUDA

If you decide to install _pytorch_ you can omit the _torchvision_ and _torchaudio_ modules. If your machine supports
_CUDA_, you should make sure to install the necessary toolkit for it. The following link should provide you with the
proper installation command for your machine:

<https://pytorch.org/get-started/locally/>

I used:

```shell script
conda install pytorch cudatoolkit=10.2 -c pytorch
```

### IPython Notebooks

The function library consists of standard ```.py``` files. I imported and used them in ```.ipynb``` notebooks. If you
want to work with them, make sure you have installed the following modules:

- jupyter
- datetime
- csv
- pandas
- plotly
- multiprocessing

### Displaying TikZ within Notebooks

The library supports the generation of ```.tikz``` files from given circuits. The content of the generated ```.tikz```
file can be easily embedded in any ```.tex``` file.

Displaying the contents of a ```.tikz``` file within an _IPython_ Notebook, however, requires some additional effort.
Depending on your setup, it may be difficult to get this feature to work. It is only used twice, namely in the
notebooks ```notebooks/circuit_diagrams.ipynb``` and ```notebooks/final_pres_demo.ipynb```.

#### Tools for a UNIX Environment

If the Jupyter Kernel runs in a UNIX like environment, there are some useful tools to display TikZ code. Namely,
_tikzmagic_ (https://github.com/mkrphys/ipython-tikzmagic) or _itikz_
(https://nbviewer.jupyter.org/github/jbn/itikz/blob/master/Quickstart.ipynb).

Make sure, to install the required prerequisites. The prerequisites are available on both the _apt_ and _homebrew_
package manager. The tools themselves should be installed within the environment either using the _pip_ or the
_anaconda_ installer. The tool _tikzmagic_ needs to be installed directly from _github_ or _conda-forge_
(https://anaconda.org/conda-forge/tikzmagic).

#### Displaying TikZ on Windows

The tools previously mentioned combine the conversion and the displaying in one tool. On Windows we are limited to
displaying the generated _.svg_ graphics using ```IPython.display```. However, the conversion can still be archived by
using the Linux Subsystem for Windows _WSL_. The conversion can be performed directly on a _.tikz_ file in the Windows
file System which is mounted within _WSL_.

The conversion itself consists of multiple steps, and can be achieved by calling all the necessary Linux commands
directly from Python
(https://cm-gitlab.stanford.edu/tsob/musicNet/blob/36967c71a16a8d034eb5acaab1327cebfd425d7c/theanets-cwRNN/docs/_bin/tikz2svg).

The other approach is to define a shell script within _WSL_ and execute it as a Linux command. I relied on the
_tikztosvg_ command (https://gitlab.com/pablo-escobar/tikztosvg/-/blob/master). Sadly, the installation of this command
did not work for me, so I decided to create the necessary files manually in the right locations.

##### Step-by-Step Description

The example worked for me on Ubuntu 20.04 LTS. Make sure to install the prerequisites:

```shell script
apt-get install pdf2svg
apt-get install -y texlive-xetex
```

Create the command directly in the binaries:

```shell script
cd ~/../../usr/local/bin
sudo nano
```

Copy the contents of copy the contents of https://gitlab.com/pablo-escobar/tikztosvg/-/blob/master/tikztosvg, write them
out (^O) as _tikztosvg_ and leave nano (^X).

Make the shell script executable:

```shell script
sudo chmod +x tikztosvg
```

Save the man page to the right location:

```shell script
cd /usr/local/share/man
sudo mkdir man1
cd man1
sudo nano
```

Copy the contents of https://gitlab.com/pablo-escobar/tikztosvg/-/blob/master/man/tikztosvg.1 and write them out as
_tikztosvg.1_.

The command _tikztosvg_ should now be available.

I converted a file in the windows file system by calling the following command from within _WSL_:

```shell script
tikztosvg -p tikz-cd -p xfrac /mnt/c/Users/simon/Desktop/tikz_test/example.tikz
```

Linux commands can also be executed from within the Windows Command Prompt, by prefixing them with _wsl_, in this case
the command prompt was opened directly within the directory of interest:

```shell script
wsl tikztosvg -p tikz-cd -p xfrac example.tikz
```

In order to execute a shell command from within a Jupyter, it has to be prefixed with _!_:

```shell script
!wsl tikztosvg -p tikz-cd -p xfrac /mnt/c/Users/simon/Desktop/tikz_test/example2.tikz
```
 
In order to suppress the output of the command ```stdout``` and ```stderr``` are redirected to ```/dev/null.```

```shell script
!wsl tikztosvg -p tikz-cd -p xfrac /mnt/c/Users/simon/Desktop/tikz_test/example2.tikz > /dev/null 2>&1
```

## Contributors

- Simon Tonner [simon.tonner@student.uibk.ac.at](simon.tonner@student.uibk.ac.at)

## Licence & Copyright

© Simon Tonner, Universität Innsbruck

This work is licensed under CC BY-NC 4.0

To view a copy of this license, visit <http://creativecommons.org/licenses/by-nc/4.0/>