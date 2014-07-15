__author__ = 'rizki'

import sys
if sys.version_info[0] == 2:
    from backend.v1.tasks import *
else:
    from .backend.v1.tasks import *

