from typing import Any

from eopf.product import EOProduct
from eopf.qualitycontrol.abstract import EOQCUnit


class QC_Product_Valid(EOQCUnit):
    def run(
        self,
        input: EOProduct,
        **kwargs: Any,
    ) -> EOProduct:
        ret = False

        if input.is_valid():
            ret = True

        output = EOProduct(QC_Product_Valid.__name__)
        output.attrs[QC_Product_Valid.__name__] = {"status": ret}

        return output
