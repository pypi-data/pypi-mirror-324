from typing import Any

from eopf.logging import EOLogging
from eopf.product import EOProduct
from eopf.qualitycontrol.abstract import EOQCUnit

logger = EOLogging().get_logger()


class QC_Sensing_Time(EOQCUnit):
    def run(
        self,
        input: EOProduct,
        **kwargs: Any,
    ) -> EOProduct:
        ret = False
        try:
            t_start = input.attrs["properties"]["start_datetime"]
            t_stop = input.attrs["properties"]["end_datetime"]

            if t_stop >= t_start:
                ret = True
        except Exception as e:
            logger.warning(f"An error is occured while trying to check the product sensing time : {e}")

        output = EOProduct(QC_Sensing_Time.__name__)
        output.attrs[QC_Sensing_Time.__name__] = {"status": ret}

        return output
