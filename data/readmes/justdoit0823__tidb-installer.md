==============
tidb_installer
==============


.. image:: https://readthedocs.org/projects/tidb-installer/badge/?version=latest
        :target: https://tidb-installer.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Tidb-installer is a simple tool for building a tidb cluster based on Vagrant_.
It wraps the official Tidb-ansible_ repository and supports the command line interface.
And it's easy to start your own tidb cluster automatically.


.. _Vagrant: https://www.vagrantup.com/docs/
.. _Tidb-ansible: https://github.com/pingcap/tidb-ansible


Features
--------

* Deploy tidb cluster based on vagrant


Requirements
-------------

* Python3.5+

* Vagrant


Tutorial
---------

First, you should clone this repository into your machine.

.. code-block:: console

    git clone https://github.com/justdoit0823/tidb-installer

Then, install this tool with ``Python3``,

.. code-block:: console

    cd tidb-installer
    python3 setup.py install

Now, you can use command ``tidb_installer`` which supports ``init`` and ``create`` subcommands.


Get started
------------

* create tidb ansible environment

.. code-block:: console

    tidb_installer init -p /tmp/test-tidb -v 2.0

* create tidb cluster

.. code-block:: console

    tidb_installer create -f /tmp/test-tidb --host-type vagrant -d 10.20.1.100 \
    -d 10.20.1.101 -d 10.20.1.102 -p 10.20.1.100 -p 10.20.1.101 -p 10.20.1.103 \
    -k 10.20.1.104 -k 10.20.1.105 -k 10.20.1.106


Limitations
------------

* Machine node filesystem mount option check

* User-defined user name

* ntp check


License
---------

This tool is distributed under MIT license.


Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
