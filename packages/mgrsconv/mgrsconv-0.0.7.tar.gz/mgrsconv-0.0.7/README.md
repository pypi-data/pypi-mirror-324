Python code for converting between decimal degrees and MGRS. 

Functions:

    dd2mgrs: Decimal Degrees to MGRS

    mgrs2dd: MGRS to Decimal Degrees

To install:

    pip install mgrsconv

Sample usage:

    from mgrsconv import *

    mgrs2dd("31N AA 66021 00000")

Sample output:

    (True, 0.0, -3.976393174348989e-06)

    "True" in this case means the conversion was successful, the coordinates functionally represent 0 degrees latitude and 0 degrees longitude in decimal.

Package available here: https://pypi.org/project/mgrsconv/

GitHub: https://github.com/nousernamesavailabel/MGRSConv

Planning for next version to include DMS coordinates. 
