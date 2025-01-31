from enum import Enum

from xarray.backends import zarr

import eopf


class OpeningInfo:
    def __init__(self, str_mode: str):
        self.file_opening_mode: str = str_mode


class OpeningMode(Enum):
    CREATE: OpeningInfo = OpeningInfo("w")
    CREATE_OVERWRITE: OpeningInfo = OpeningInfo("w")
    OPEN: OpeningInfo = OpeningInfo("r")
    UPDATE: OpeningInfo = OpeningInfo("r+")
    APPEND: OpeningInfo = OpeningInfo("a")


class ProductType(Enum):
    S01SEWGRH = "S01SEWGRH"
    S01SEWRAW = "S01SEWRAW"
    S01SEWSLC = "S01SEWSLC"
    S01SIWGRH = "S01SIWGRH"
    S01SIWOCN = "S01SIWOCN"
    S01SIWRAW = "S01SIWRAW"
    S01SIWSLC = "S01SIWSLC"
    S01SSMGRH = "S01SSMGRH"
    S01SSMOCN = "S01SSMOCN"
    S01SSMRAW = "S01SSMRAW"
    S01SSMSLC = "S01SSMSLC"
    S01SWVGRH = "S01SWVGRH"
    S01SWVRAW = "S01SWVRAW"
    S01SWVSLC = "S01SWVSLC"
    S02MSIL0_ = "S02MSIL0_"
    S02MSIL1C = "S02MSIL1C"
    S02MSIL2A = "S02MSIL2A"
    S03AHRL1B = "S03AHRL1B"
    S03AHRL2H = "S03AHRL2H"
    S03ALTL0_ = "S03ALTL0_"
    S03MWRL0_ = "S03MWRL0_"
    S03OLCEFR = "S03OLCEFR"
    S03OLCERR = "S03OLCERR"
    S03OLCL0_ = "S03OLCL0_"
    S03OLCLFR = "S03OLCLFR"
    S03SLSFRP = "S03SLSFRP"
    S03SLSL0_ = "S03SLSL0_"
    S03SLSLST = "S03SLSLST"
    S03SLSRBT = "S03SLSRBT"
    S03SYNSDR = "S03SYNSDR"


VALID_MIN = "valid_min"
VALID_MAX = "valid_max"
FILL_VALUE = "fill_value"
ADD_OFFSET = "add_offset"
SCALE_FACTOR = "scale_factor"
DTYPE = "dtype"
LONG_NAME = "long_name"
STANDARD_NAME = "standard_name"
SHORT_NAME = "short_name"
COORDINATES = "coordinates"
UNITS = "units"
FLAG_VALUES = "flag_values"
FLAG_MASKS = "flag_masks"
FLAG_MEANINGS = "flag_meanings"
DIMENSIONS = "dimensions"
# xarray and zarr dimensions must be identical for compatibility.
DIMENSIONS_NAME = zarr.DIMENSION_KEY
# xarray uses _FillValue for fill_value
XARRAY_FILL_VALUE = "_FillValue"


# overall CDM valid attributes for EOVariables,
# coming either from the xarray of the eovar, should not be define both in xarray and eovar
EOVAR_CDM_VALID_ATTRS = [
    VALID_MIN,
    VALID_MAX,
    FILL_VALUE,
    ADD_OFFSET,
    SCALE_FACTOR,
    DTYPE,
    LONG_NAME,
    STANDARD_NAME,
    COORDINATES,
    UNITS,
    FLAG_VALUES,
    FLAG_MASKS,
    FLAG_MEANINGS,
    DIMENSIONS,
]
EOPF_CPM_PATH = eopf.__path__[0]

ROOT_PATH_DATATREE = "/"
