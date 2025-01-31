from abc import ABC, abstractmethod
from typing import Any

from eopf.product import EOProduct


class EOQCUnitBase(ABC):
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


class EOQCUnit(EOQCUnitBase):
    """Abstract base class of quality control processors i.e. processing units
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

    @abstractmethod
    def run(
        self,
        input: EOProduct,
        **kwargs: Any,
    ) -> EOProduct:  # pragma: no cover
        """
        Abstract method to provide an interface for algorithm implementation

        Parameters
        ----------
        input: EOProduct
            product to analyze

        **kwargs: any
            any needed kwargs (e.g. parameters)

        Returns
        -------
        EOProduct
        """
