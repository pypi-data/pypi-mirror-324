from typing import Any, Union

import numpy

from eopf.exceptions import FormattingError

from .abstract import EOAbstractFormatter


class ToStr(EOAbstractFormatter):
    """Formatter for string conversion"""

    # docstr-coverage: inherited
    name = "to_str"

    # docstr-coverage: inherited
    def _format(self, input: Any) -> str:
        """Convert input to string

        Parameters
        ----------
        input: Any

        Returns
        ----------
        str:
            String representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return str(input)
        except Exception as e:
            raise FormattingError(f"{e}")


class ToLowerStr(EOAbstractFormatter):
    """Formatter for string conversion to lowercase"""

    # docstr-coverage: inherited
    name = "to_str_lower"

    # docstr-coverage: inherited
    def _format(self, input: Any) -> str:
        """Convert input to string

        Parameters
        ----------
        input: Any

        Returns
        ----------
        str:
            String representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return str(input).lower()
        except Exception as e:
            raise FormattingError(f"{e}")


class ToFloat(EOAbstractFormatter):
    """Formatter for float conversion"""

    # docstr-coverage: inherited
    name = "to_float"

    def _format(self, input: Any) -> float:
        """Convert input to float

        Parameters
        ----------
        input: Any

        Returns
        ----------
        float:
            Float representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return float(input)
        except Exception as e:
            raise FormattingError(f"{e}")


class ToInt(EOAbstractFormatter):
    """Formatter for int conversion"""

    # docstr-coverage: inherited
    name = "to_int"

    def _format(self, input: Any) -> Union[int, float]:
        """Convert input to int

        Parameters
        ----------
        input: Any

        Returns
        ----------
        int:
            Integer representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            if input == "N/A":
                return numpy.NAN
            return int(input)
        except Exception as e:
            raise FormattingError(f"{e}")


class ToBool(EOAbstractFormatter):
    """Formatter for bool conversion"""

    # docstr-coverage: inherited
    name = "to_bool"

    def _format(self, input: Any) -> bool:
        """Convert input to boolean

        Parameters
        ----------
        input: Any

        Returns
        ----------
        bool:
            Boolean representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return bool(input)
        except Exception as e:
            raise FormattingError(f"{e}")


class IsOptional(EOAbstractFormatter):
    name = "is_optional"

    def _format(self, input: Any) -> Any:
        """Silent formatter, used only for parsing the path
        logic is present in stac_mapper method of XMLManifestAccessor

        Parameters
        ----------
        input: Any
            input

        Returns
        ----------
        Any:
            Returns "Not found"
        """
        if input is None:
            return "null"
        else:
            return input


class ToMicromFromNanom(EOAbstractFormatter):
    """Formatter converting nanometers to micrometers"""

    # docstr-coverage: inherited
    name = "to_microm_from_nanom"

    def _format(self, input: Any) -> float:
        """Convert nanometers to micrometers

        Parameters
        ----------
        input: Any

        Returns
        ----------
        float:
            Float representation of the input

        Raises
        ----------
        FormattingError
            When formatting can not be carried out
        """
        try:
            return float(input) * float(0.001)
        except Exception as e:
            raise FormattingError(f"{e}")
