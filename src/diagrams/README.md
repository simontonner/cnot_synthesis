# DISPLAYING TIKZ WITHIN JUPYTER

The content of the generated _.tikz_ file can easily be embedded in any _.tex_ file. Displaying the contents of a
_.tikz_ file within a Jupyter Notebook, however, requires some additional effort.

### TOOLS FOR A UNIX ENVIRONMENT

If the Jupyter Kernel runs in a UNIX like environment, there are some useful tools to display TikZ code. Namely,
_tikzmagic_ (https://github.com/mkrphys/ipython-tikzmagic) or _itikz_
(https://nbviewer.jupyter.org/github/jbn/itikz/blob/master/Quickstart.ipynb).

Make sure, to install the required prerequisites. The required prerequisites are available on both the _apt_ and
_homebrew_ package manager. The tools themselves should be installed within the environment either using the _pip_ or
the _anaconda_ installer. The tool _tikzmagic_ needs to be installed directly from _github_ or _conda-forge_
(https://anaconda.org/conda-forge/tikzmagic).

### DISPLAYING TIKZ ON WINDOWS

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

#### STEP BY STEP DESCRIPTION

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

