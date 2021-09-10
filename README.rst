miutil
======

Medical imaging utilities.

|Version| |Py-Versions| |Conda| |Tests| |Coverage| |DOI| |LICENCE|

Basic functionality needed for `AMYPAD <https://github.com/AMYPAD/AMYPAD>`_
and `NiftyPET <https://github.com/NiftyPET/NiftyPET>`_.


Install
-------

Intended for inclusion in requirements for other packages.
The package name is ``miutil``. Extra install options include:

- cuda

  - provides `miutil.cuinfo <https://github.com/AMYPAD/miutil/blob/master/miutil/cuinfo.py>`_

- mbeautify

  - provides `miutil.mlab.beautify <https://github.com/AMYPAD/miutil/blob/master/miutil/mlab/beautify.py>`_

- nii

  - provides `miutil.imio.nii <https://github.com/AMYPAD/miutil/blob/master/miutil/imio/nii.py>`_

- plot

  - provides `miutil.plot <https://github.com/AMYPAD/miutil/blob/master/miutil/plot.py>`_

    - includes a useful 3D multi-volume ``imscroll`` function which depends only on ``matplotlib``

- web

  - provides `miutil.web <https://github.com/AMYPAD/miutil/blob/master/miutil/web.py>`_


To install extras and their dependencies,
use the package name ``miutil[option1,option2]``.


.. |Tests| image:: https://img.shields.io/github/workflow/status/AMYPAD/miutil/Test?logo=GitHub
   :target: https://github.com/AMYPAD/miutil/actions
.. |Coverage| image:: https://codecov.io/gh/AMYPAD/miutil/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/AMYPAD/miutil
.. |Version| image:: https://img.shields.io/pypi/v/miutil.svg?logo=python&logoColor=white
   :target: https://github.com/AMYPAD/miutil/releases
.. |Py-Versions| image:: https://img.shields.io/pypi/pyversions/miutil.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/miutil
.. |Conda| image:: https://img.shields.io/conda/v/conda-forge/miutil.svg?label=conda&logo=conda-forge
   :target: https://anaconda.org/conda-forge/miutil
.. |DOI| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.4281542.svg
   :target: https://doi.org/10.5281/zenodo.4281542
.. |LICENCE| image:: https://img.shields.io/pypi/l/miutil.svg
   :target: https://raw.githubusercontent.com/AMYPAD/miutil/master/LICENCE.md
