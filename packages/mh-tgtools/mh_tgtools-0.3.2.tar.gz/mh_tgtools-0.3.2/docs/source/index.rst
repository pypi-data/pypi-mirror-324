.. Siklu by Ceragon TgTools documentation master file, created by
   sphinx-quickstart on Thu Oct 24 10:03:00 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Tools for Siklu by Ceragon TG Radios
=======================================

:Author: Daniel Ephraty
:Source code: https://github.com/DanielEphraty/tgtools
:PyPI project: https://pypi.org/project/mh-tgtools
:Licence: MIT Licence
:Version: |version|

:program:`TgTools` is a collection of tools to help manage large networks with multiple
Siklu by Ceragon MultiHaul TG radios. 

.. note::
   Program still under development and more tools are being actively added.
   
Available Tools:

 * **TgCrawl** crawls the network discovering TG radios, collecting, parsing information, and saving to csv files:
  
   - telemetry
   - events
   - configuration
   
   TgCrawler can run a single time, or repeatedly (polling mode).
   
:program:`TgTools` is currently released as a command-line script / executable.
It is an improved version of `Batchscanner <https://batchscanner.readthedocs.io/en/stable/index.html>`_,
but focuses exclusively on MultiHaul TG radios.

.. note::
   This program is a personal initiative and contribution.
   Although it is designed for interacting with `Siklu by Ceragon <https://www.siklu.com>`_ radios, no use
   has been made of any company resources, nor any intellectual proprietary nor
   confidential information.


.. toctree::
   :maxdepth: 1
   :caption: Installation
   :titlesonly:

   install

   
.. toctree::
   :maxdepth: 1
   :caption: Quick Start
   :titlesonly:
      
   tgcrawl

   
.. toctree::
   :maxdepth: 1
   :caption: Technical Documentation
   :titlesonly:
  
   crawl/index
   utils/utils


.. toctree::
   :maxdepth: 1
   :caption: Misc
   :titlesonly:
  
   constants


.. toctree::
   :caption: Change Log
   :titlesonly:

   changelog

.. Indices and tables
.. ==================

.. * :ref:`genindex`
.. * :ref:`modindex`
.. * :ref:`search`