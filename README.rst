miutil
======

Medical imaging utilities.

|Versions| |Py-Versions| |Tests| |Coverage| |LICENCE|

Basic functionality needed for `AMYPAD <https://github.com/AMYPAD/AMYPAD>`_
and `NiftyPET <https://github.com/NiftyPET/NiftyPET>`_.


Install
-------

Intended for inclusion in requirements for other packages.
The package name is ``miutil``. Extra install options include:

- nii

  - provides `miutil.imio.nii <https://github.com/AMYPAD/miutil/blob/master/miutil/imio/nii.py>`_

- plot

  - provides `miutil.plot <https://github.com/AMYPAD/miutil/blob/master/miutil/plot.py>`_

    - includes a useful 3D multi-volume ``imscroll`` function which depends only on ``matplotlib``

- cuda

  - provides `miutil.cuinfo <https://github.com/AMYPAD/miutil/blob/master/miutil/cuinfo.py>`_


To install extras and their dependencies,
use the package name ``miutil[option1,option2]``.


.. |Tests| image:: https://img.shields.io/github/workflow/status/AMYPAD/miutil/Test
   :target: https://github.com/AMYPAD/miutil/actions
.. |Coverage| image:: https://codecov.io/gh/AMYPAD/miutil/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/AMYPAD/miutil
.. |Versions| image:: https://img.shields.io/pypi/v/miutil.svg
   :target: https://github.com/AMYPAD/miutil/releases
.. |Py-Versions| image:: https://img.shields.io/pypi/pyversions/miutil.svg?logo=python&logoColor=white
   :target: https://pypi.org/project/miutil
.. |LICENCE| image:: https://img.shields.io/pypi/l/miutil.svg
   :target: https://raw.githubusercontent.com/AMYPAD/miutil/master/LICENCE.md
