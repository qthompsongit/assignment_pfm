# pylint: disable=invalid-name
# pylint: disable=R0801
"""
This is a test python file to check the functionality of pre-commit hooks.


"""

import numpy as np
import pandas as pd

TEXT_CHECK = "gffgdsfgdsfgdfsgdsfgsdfgdf\
    sgdsfgfdgsdfgsdfgdfighfdghudfhg\
        uoidsfglhfglsdfgfdjgdsfgsdfg"

TEXT_CHECK = TEXT_CHECK + "asdadasdadasdadadadasdasdadasdadadadasdadad"
mynparray = np.array([TEXT_CHECK])
myseriesget = pd.Series(mynparray)
