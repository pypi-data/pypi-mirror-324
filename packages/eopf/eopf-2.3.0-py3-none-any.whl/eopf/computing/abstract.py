from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Union

from datatree import DataTree

from eopf import EOContainer
from eopf.common.file_utils import AnyPath
from eopf.exceptions.errors import MissingArgumentError
from eopf.product import EOProduct

DataType = Union[EOProduct, EOContainer, DataTree[Any]]


@dataclass
class ADF:
    name: str
    path: AnyPath
    store_params: Optional[dict[str, Any]] = None
    # Data pointer to store opened data or whatever you wants
    data_ptr: Any = None

    def __repr__(self) -> str:
        return f"ADF {self.name} : {self.path} : {self.data_ptr}"


class EOProcessingBase(ABC):
    """
    Define base functionalities for all processing elements such as identifier and representation
    """

    @property
    def identifier(self) -> Any:
        """Identifier of the processing step"""
        return self._identifier

    def __init__(self, identifier: Any = ""):
        self._identifier = identifier or str(id(self))

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<{self.identifier}>"

    def __repr__(self) -> str:
        return f"[{id(self)}]{str(self)}"


class EOProcessingStep(EOProcessingBase):
    """Converts one or several input arrays (of one or several variables)
    into one array (of one intermediate or output variable).

    These algorithms should be usable outside a Dask context to allow re-use in other
    software or integration of existing algorithms.


    Parameters
    ----------
    identifier: str, optional
        a string to identify this processing step (useful for logging)

    See Also
    --------
    dask.array.Array
    """

    def __init__(self, identifier: Any = ""):
        super().__init__(identifier)

    @abstractmethod
    def apply(self, *inputs: Any, **kwargs: Any) -> Any:  # pragma: no cover
        """Abstract method that is applied for one block of the inputs.

        It creates a new array from arrays, can be any accepted type by map_block function from Dask.

        Parameters
        ----------
        *inputs: any
            input arrays (numpy, xarray) with same number of chunks each compatible with map_block functions
        **kwargs: any
            any needed kwargs

        Returns
        -------
        Any : same kind as the input type ( numpy array or xarray DataArray)
        """


class EOProcessingUnit(EOProcessingBase):
    """Abstract base class of processors i.e. processing units
    that provide valid EOProducts with coordinates etc.

    Parameters
    ----------
    identifier: str, optional
        a string to identify this processing unit (useful for logging and tracing)

    See Also
    --------
    eopf.product.EOProduct
    """

    def __init__(self, identifier: Any = "") -> None:
        super().__init__(identifier)

    def get_mandatory_input_list(self, **kwargs: Any) -> list[str]:
        """
        Get the list of mandatory inputs names to be provided for the run method.
        In some cases, this list might depend on parameters and ADFs.
        If parameters are not provided, default behaviour is to provide the minimal list.
        Note: This method does not verify the content of the products, it only provides the list.

        Parameters
        ----------
        kwargs : same parameters as for the run method if available

        Returns
        -------
        the list of mandatory products to be provided
        """
        return []

    def get_mandatory_adf_list(self, **kwargs: Any) -> list[str]:
        """
        Get the list of mandatory ADF input names to be provided for the run method.
        In some cases, this list might depend on parameters.
        If parameters are not provided, default behaviour is to provide the minimal list.
        Note: This method does not verify the content of the ADF, it only provides the list.
        So no check on input ADF can be performed here.

        Parameters
        ----------
        kwargs : same parameters as for the run method if available

        Returns
        -------
        the list of mandatory ADFs to be provided
        """
        return []

    @abstractmethod
    def run(
        self,
        inputs: dict[str, DataType],
        adfs: Optional[dict[str, ADF]] = None,
        **kwargs: Any,
    ) -> dict[str, DataType]:  # pragma: no cover
        """
        Abstract method to provide an interface for algorithm implementation

        Parameters
        ----------
        inputs: dict[str,EOProduct | EOContainer | DataTree]
            all the products to process in this processing unit
        adfs: Optional[dict[str,ADF]]
            all the ADFs needed to process

        **kwargs: any
            any needed kwargs (e.g. parameters)

        Returns
        -------
        dict[str, EOProduct | EOContainer | DataTree ]
        """

    def run_validating(
        self,
        inputs: dict[str, DataType],
        adfs: Optional[dict[str, ADF]] = None,
        **kwargs: Any,
    ) -> dict[str, DataType]:
        """Transforms input products into a new valid EOProduct/EOContainer/DataTree with new variables.

        Parameters
        ----------
        inputs: dict[str,EOProduct | EOContainer | DataTree]
            all the products to process in this processing unit
        adfs: Optional[dict[str,ADF]]
            all the ADFs needed to process

        **kwargs: any
            any needed kwargs

        Returns
        -------
        dict[str, EOProduct | EOContainer | DataTree]
        """
        # verify that the input list is complete
        if not all(i in inputs.keys() for i in self.get_mandatory_input_list(**kwargs)):
            raise MissingArgumentError(
                f"Missing input, provided {inputs.keys()} while requested {self.get_mandatory_input_list(**kwargs)}",
            )
        # verify that the input list is complete
        if adfs is not None and not all(i in adfs.keys() for i in self.get_mandatory_adf_list(**kwargs)):
            raise MissingArgumentError(
                f"Missing input, provided {inputs.keys()} while requested {self.get_mandatory_input_list(**kwargs)}",
            )
        if adfs is not None:
            result_product = self.run(inputs, adfs, **kwargs)
        else:
            result_product = self.run(inputs, **kwargs)
        self.validate_output_products(result_product)
        return result_product

    def validate_output_products(self, products: dict[str, DataType]) -> None:
        """Verify that the given product is valid.

        If the product is invalid, raise an exception.

        See Also
        --------
        eopf.product.EOProduct.validate
        """
        for p in products.items():
            p[1].validate()
