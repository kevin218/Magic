.. Magic documentation main file, created by Kevin Stevenson.

Documentation for Magic
=======================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

``Magic`` is a general-purpose tool that subtracts the sky background from dithered MIRI images that contain only point sources.
This tool should be run on ``jwst`` Stage 2 data products, followed by the provided wrapper for ``jwst`` Stage 3.
The only file that needs to be modified and then executed is ``make_magic.py``.


Indices and Searching
=====================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Installation
============


It is **strongly** recommended that you install ``Magic`` in a new ``conda`` environment as other packages you've previously
installed could have conflicting requirements with ``Magic``. You can install a lightweight version of conda at
`this link <https://docs.conda.io/en/latest/miniconda.html>`_. Once conda is installed, you can create a
new environment by doing:

.. code-block:: bash

    conda create -n magic python==3.11
    conda activate magic

Once in your new conda environment, you can install ``Magic`` directly from source on
`GitHub <http://github.com/kevin218/Magic>`_ using ``git`` and ``pip`` by running:

.. code-block:: bash

	git clone https://github.com/kevin218/Magic.git
	cd Magic
	pip install -e '.[jwst]'

To update your ``Magic`` installation to the most recent version, you can do the following within that Eureka folder:

.. code-block:: bash

	git pull
	pip install --upgrade -e '.[jwst]'

The ``-e`` flag makes the install editable, which means that you do not have to install the package again and again after each change.  Changes to your files inside the project folder will automatically reflect in changes on your installed package.  However, if you are working in an interactive environment (e.g., ipython, Jupyter) you will need to re-import any modules that have changed.


CRDS Environment Variables
--------------------------

``Magic`` installs the JWST Calibration Pipeline as part of its requirements, and this also requires users to set the proper environment variables so that it can download the proper reference files needed to run the pipeline. For users not on the internal STScI network, two environment variables need to be set to enable this functionality. In your ``~/.zshrc`` (for zsh users) or ``~/.bashrc`` or ``~/.bash_profile`` file (for bash users), or other shell initialization file, add these two lines (specifying your desired location to cache the CRDS files, e.g. ``/Users/your_name/crds_cache`` for Mac users or ``/home/your_name/crds_cache`` for Linux users):

	.. code-block:: bash

		export CRDS_PATH=/PATH/TO/FOLDER/crds_cache

		export CRDS_SERVER_URL=https://jwst-crds.stsci.edu

If these environment variables are not set, Stages 1-3 of the pipeline will fail.


Example Usage
=============

See ``make_magic.py``.

Code
====


