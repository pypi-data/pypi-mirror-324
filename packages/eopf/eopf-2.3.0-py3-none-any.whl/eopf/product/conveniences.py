from typing import Any

from eopf import EOGroup
from eopf.product import EOProduct


def init_product(
    product_name: str,
    **kwargs: Any,
) -> EOProduct:
    """Convenience function to create a valid EOProduct base.

    Parameters
    ----------
    product_name: str
        name of the product to create
    **kwargs: any
        Any valid named arguments for EOProduct

    Returns
    -------
    EOProduct
        newly created product

    See Also
    --------
    eopf.product.EOProduct
    eopf.product.EOProduct.is_valid
    """
    product = EOProduct(product_name, **kwargs)

    # TODO : open the product ?
    for group_name in product.MANDATORY_FIELD:
        product[group_name] = EOGroup(group_name)
    return product


# -----------------------------------------------
