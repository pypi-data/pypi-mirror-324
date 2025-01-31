from typing import Any

from eopf.logging import EOLogging
from eopf.product import EOProduct
from eopf.qualitycontrol.abstract import EOQCUnit

logger = EOLogging().get_logger()


class QCAbsoluteOrbit(EOQCUnit):
    """
    Validate the absolute orbit value is between mon and max
    """

    def run(
        self,
        input: EOProduct,
        **kwargs: Any,
    ) -> EOProduct:
        ret = False
        try:
            if "parameters" in kwargs:
                parameters = kwargs["parameters"]

            val_absolute_orbit = int(input.attrs["absolute_orbit_number"])
            val_absolute_orbit_min = int(parameters["v_min"])
            val_absolute_orbit_max = int(parameters["v_max"])
            if val_absolute_orbit_min < val_absolute_orbit < val_absolute_orbit_max:
                ret = True
        except KeyError as e:
            logger.warning(f" An error is occured while trying to check the absolut orbit number : {e}")

        output = EOProduct(QCAbsoluteOrbit.__name__)
        output.attrs[QCAbsoluteOrbit.__name__] = {"status": ret}
        return output
