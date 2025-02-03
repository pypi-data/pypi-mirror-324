=====
Usage
=====

Gabbia is not intended to run alone without an application, it will always
require an application to be launched together with Gabbia.

When the application exits, Gabbia also quits.


Command line
============

To start Gabbia with an application, use

.. code-block:: sh

    gabbia <APPLICATION>


For example, to launch `Supertuxkart <https://supertuxkart.net/>`_, use

.. code-block:: sh

    gabbia supertuxkart


If you want to provide additional parameters, use ``--``

.. code-block:: sh

    gabbia -- firefox https://gabbia.org/


See :doc:`man page <man/gabbia>` and :class:`gabbia.Config` for a list of options.


Python lib
==========

In order to be able to use Gabbia in other projects, it offers the
:func:`gabbia.run` function, which expects an optional configuration in
addition to the application to be started.

.. note::

   Please note that the code is blocking. It is the caller's responsibility
   to use :py:mod:`multiprocessing` or other technologies.


.. code-block:: python

   import gabbia

   gabbia.run('alacritty')


See :class:`gabbia.Config` for details

.. code-block:: python

   import gabbia
   from gabbia import Config

   gabbia.run('alacritty', config=Config(keyboard_layout='de'))

