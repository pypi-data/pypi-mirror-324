============
Installation
============

Gabbia is distributed as single file module. Therefore, it may be
sufficient to download the file or copy the file to another project.

However, it is recommended to install via pip:

.. code-block:: sh

    pip install gabbia


To avoid problems with incompatible libs in the ``pywayland`` and
``pywlroots`` packages (see `pywayland and pywlroots`_ below), it's recommended
to avoid binary wheels at all:

.. code-block:: sh

    pip install --no-binary :all: gabbia


Please note that the dependencies require the following libs:

* libwlroots-dev 0.17.x
* libxkbcommon-dev


Pre-requirements
========================


Debian Linux
^^^^^^^^^^^^

Unfortunately, Gabbia currently doesn't work on Debian 12 (bookworm) as it
only provides wlroots 0.15 (acc. to January 2025).

Debian 13 (trixie):

.. code-block:: sh

    sudo apt install python3 python3-venv
    sudo apt install python3-dev libxkbcommon-dev libwlroots-dev



Void Linux
^^^^^^^^^^

.. code-block:: sh

    sudo xbps-install python3 python3-venv
    sudo xbps-install python3-devel libxkbcommon-devel wlroots0.17-devel



Ubuntu
^^^^^^

.. code-block:: sh

    sudo apt install python3 python3-venv
    sudo apt install python3-dev libxkbcommon-dev libwlroots-dev



Raspberry Pi OS
^^^^^^^^^^^^^^^

.. code-block:: sh

    sudo apt install python3 python3-venv
    sudo apt install python3-dev libxkbcommon-dev libwlroots-dev_0.17.1



pywayland and pywlroots
=======================

After you've installed the pre-requirements, create a virtual environment.

.. code-block:: sh

    mkdir gabbia
    cd gabbia
    python -m venv .venv
    source ./.venv/bin/activate


.. note::

   To avoid problems with incompatible libs shipped with pywayland and
   pywlroots, it's recommended to use the source packages.


After creation of the virtual environment install all requirements and Gabbia:

.. code-block:: sh

    pip install --no-cache-dir --no-binary pywayland
    pip install --no-cache-dir --no-binary pywlroots
    pip install gabbia

