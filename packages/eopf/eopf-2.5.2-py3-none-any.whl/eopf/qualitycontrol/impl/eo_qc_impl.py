import importlib
from dataclasses import dataclass
from typing import Any

from eopf.product import EOProduct
from eopf.qualitycontrol.eo_qc import EOQC, EOQCPartialCheckResult
from eopf.qualitycontrol.eo_qc_factory import EOQCFactory
from eopf.qualitycontrol.eo_qc_utils import EOQCFormulaEvaluator


@dataclass
@EOQCFactory.register_eoqc("formulas")
class EOQCFormula(EOQC):
    """Quality formula check class.

    Parameters
    ----------
    id: str
        The identifier of the quality check.
    version: str
        The version of the quality check in formt XX.YY.ZZ .
    thematic: str
        Thematic of the check RADIOMETRIC_QUALITY/GEOMETRIC_QUALITY/GENERAL_QUALITY...
    description: str
        Simple description of the check (less than 100 chars)
    precondition: EOQCFormulaEvaluator
        Precondition evaluator
    evaluator: EOQCFormulaEvaluator
        Expression evaluator
    """

    evaluator: EOQCFormulaEvaluator

    # docstr-coverage: inherited
    def _check(self, eoproduct: EOProduct) -> EOQCPartialCheckResult:

        # Applying the formula
        result = bool(self.evaluator.evaluate(eoproduct))
        if result:
            message = f"PASSED: Formula {self.evaluator.formula} evaluate True on the product {eoproduct.name}"
        else:
            message = f"FAILED: Formula {self.evaluator.formula} evaluate False on the product {eoproduct.name}"
        return EOQCPartialCheckResult(status=result, message=message)


@dataclass
@EOQCFactory.register_eoqc("validate")
class EOQCValid(EOQC):
    """
    Validate a product

    Parameters
    ----------
    id: str
        The identifier of the quality check.
    version: str
        The version of the quality check in formt XX.YY.ZZ .
    thematic: str
        Thematic of the check RADIOMETRIC_QUALITY/GEOMETRIC_QUALITY/GENERAL_QUALITY...
    description: str
        Simple description of the check (less than 100 chars)
    precondition: EOQCFormulaEvaluator
        Precondition evaluator

    """

    def _check(self, eoproduct: EOProduct) -> EOQCPartialCheckResult:
        result = eoproduct.is_valid()
        if result:
            message = f"PASSED: The product {eoproduct.name} is valid"
        else:
            message = f"FAILED: The product {eoproduct.name} is not valid"
        return EOQCPartialCheckResult(status=result, message=message)


@dataclass
@EOQCFactory.register_eoqc("eoqc_runner")
class EOQCRunner(EOQC):
    """
    This EOQC allows to dynamiccaly load an  EOQC and run it.

    Parameters
    ----------
    id: str
        The identifier of the quality check.
    version: str
        The version of the quality check in formt XX.YY.ZZ .
    thematic: str
        Thematic of the check RADIOMETRIC_QUALITY/GEOMETRIC_QUALITY/GENERAL_QUALITY...
    description: str
        Simple description of the check (less than 100 chars)
    precondition: EOQCFormulaEvaluator
        Precondition evaluator
    module: str
        Name to the module to import.
    eoqc_class: str
        eoqc class to be executed in the module.
    parameters: dict[str, Any]
        Parameters to instanciate the eoqc_class.


    """

    module: str
    eoqc_class: str
    parameters: dict[str, Any]

    # docstr-coverage: inherited
    def _check(self, eoproduct: EOProduct) -> EOQCPartialCheckResult:
        module = importlib.import_module(self.module)
        eoqc_class = getattr(module, self.eoqc_class)

        if not issubclass(eoqc_class, EOQC):
            raise TypeError(f"{self.module}/{self.eoqc_class} is not a valid EOQC")
        params = {
            "id": self.id,
            "version": self.version,
            "thematic": self.thematic,
            "description": self.description,
            "precondition": self.precondition,
        }
        params.update(self.parameters)

        eoqc = eoqc_class(**params)

        return eoqc._check(eoproduct)
