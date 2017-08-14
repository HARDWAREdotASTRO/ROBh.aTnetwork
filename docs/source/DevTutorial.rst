.. highlight:: shell-session

####################
Development Tutorial
####################

Required Tools
==============

* `Git <https://git-scm.com/downloads>`_
* `Anaconda Python 3.6+ <https://www.continuum.io/downloads>`_
* Text Editor or IDE

  * `Atom <https://atom.io>`_ or `PyCharm <https://www.jetbrains.com/pycharm/>`_ are recommended
  * However, VSCode, SublimeText3, Vim, Micro, Emacs, and Geany are all good options as well.

* A working C/C++ Compiler (MinGW recommended)
* `CircuitMaker <https://circuitmaker.com>`_
* `Arduino IDE <https://www.arduino.cc/en/Main/Software>`_

Setup Process
=============

1. Install your C/C++ Compiler, making sure that its tools end up in your path.
2. Install CircuitMaker and Arduino using their default settings
3. Install Git using its default settings.
4. Install Anaconda using its default options.
5. Restart Computer at this point.
6. Open up the Git-Bash command prompt and run the following commands::

    conda update --all
    cd ~
    git clone https://github.com/HARDWAREdotASTRO/ROBh.aTnetwork Robhat
    cd Robhat
    pip install -U -e Robhat/
    conda update --all

7. For a runtime example, open :code:`ExampleUseCases/run.py` using :code:`python`

To Make Documentation
=====================

1. Run the following commands::

    cd ~/Robhat/docs
    pip install -U sphinx recommonmark sphinx-bootstrap-theme sphinx-autobuild
    make html && make latexpdf
    cd build/
    explorer .

2. Then, in the explorer window that just opened, navigate to `html/index.html` and open it.
3. Alternatively, you can go to `latex/RObhaTDomeController.pdf` and open that instead.