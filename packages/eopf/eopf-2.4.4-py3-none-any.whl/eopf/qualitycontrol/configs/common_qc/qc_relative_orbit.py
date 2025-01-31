from typing import Any

from eopf.logging import EOLogging
from eopf.product import EOProduct
from eopf.qualitycontrol.abstract import EOQCUnit

logger = EOLogging().get_logger()


class QC_Relative_orbit(EOQCUnit):
    def run(
        self,
        input: EOProduct,
        **kwargs: Any,
    ) -> EOProduct:
        ret = False

        try:
            if "parameters" in kwargs:
                parameters = kwargs["parameters"]

            val_relative_orbit = int(input.attrs["properties"]["eopf:product"]["relative_orbit_number"])
            val_relative_orbit_min = int(parameters["v_min"])
            val_relative_orbit_max = int(parameters["v_max"])
            if val_relative_orbit > val_relative_orbit_min and val_relative_orbit < val_relative_orbit_max:
                ret = True
        except Exception as e:
            logger.warning(f"An error is occured while trying to check the relative orbit number : {e}")

        output = EOProduct(QC_Relative_orbit.__name__)
        output.attrs[QC_Relative_orbit.__name__] = {"status": ret}

        return output
