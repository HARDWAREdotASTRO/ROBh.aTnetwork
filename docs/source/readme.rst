======
Readme
======

Motor Dome Controller for Winona State University
-------------------------------------------------

Nick Meyer and Carl Ferkinhoff (2017)

| The **R**\ obotic **Ob**\ servatory by **h**\ ardware\ **.a**\ stronomy and **T**\ elescope **Network**
| **an open hardware project for robotizing small observatories.**
| MIT Licensed!

To install this package: 

.. code-block:: bash
	
	cd ~
	git clone https://github.com/HARDWAREdotASTRO/ROBh.aTnetwork.git Robhat
	cd Robhat/Robhat
	python setup.py develop

Example use case is given in ``ExampleUseCases/run.py``

To build docs:

.. code-block:: bash
	
	cd ~/Robhat/docs
	make html
