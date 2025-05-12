Script to make a weighted random selection for the next lab meeting presenter.

How to use:

   1. Update the MC.
   2. Update the list of current members.
   3. Add the most recent presentations to presentation.json (mind the name spelling).
   4. Run ``python whosnext.py``

Dependencies:

   - python >= 3
   - pyfiglet

Either ``pip install pyfiglet`` or ``conda install -c conda-forge pyfiglet``

You may experience issues due to having multiple Python installations on your
machine, in which case troubleshoot with:

Linux/MacOS::

   which python
   python --version
   whereis python
   ls -ls /usr/bin/python*

Windows::

   python --version
   C:\Users\admin>py -0p

and target the specific version when installing pyfiglet ``/usr/bin/python3.9
-m pip install pyfiglet`` (3.9 or your specific version) and running
``whosnext.py`` with ``/usr/bin/python3.9 whosnext.py``.

License: MIT
