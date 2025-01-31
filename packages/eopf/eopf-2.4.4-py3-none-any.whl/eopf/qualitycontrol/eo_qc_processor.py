import json
import logging
import os
from datetime import datetime
from typing import Any, Optional

from eopf import EOGroup
from eopf.exceptions import InvalidProductError
from eopf.product.eo_product import EOProduct
from eopf.qualitycontrol.eo_qc_config import EOPQCConfigFactory, EOQCConfig


class EOQCProcessor:
    """Class to implement custom checks on products

    Parameters
    ----------
    identifier: int
        The identifier.
    config_path: str
        The quality control configuration to run. By default it's None.

    Attributes
    ----------
    qc_config: EOQCConfig
        The quality control configuration who will be executed.
    """

    def __init__(self, identifier: Optional[int] = None, config_path: Optional[str] = None) -> None:
        self._identifier = identifier or str(id(self))
        self._logger = logging.getLogger("eopf.quality_control")
        self.qc_config: Optional[EOQCConfig] = None
        if config_path is not None:
            self.set_config(config_path=config_path)

    @property
    def identifier(self) -> Any:
        """Identifier of the processing step"""
        return self._identifier

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<{self.identifier}>"

    def __repr__(self) -> str:
        return f"[{id(self)}]{str(self)}"

    def set_config(self, config_path: str) -> None:
        """A qc_config setter.

        Parameters
        ----------
        config_path: str
            The path to the configuration.
        """
        self.qc_config = EOQCConfig(config_path=config_path)

    def run(
        self,
        inputs: dict[str, EOProduct],
        update_attrs: bool = True,
        write_report: bool = False,
        report_path: Optional[str] = None,
        config_path: Optional[str] = None,
        **kwargs: Any,
    ) -> dict[str, EOProduct]:
        """Execute all checks of the default configuration for a EOProduct.

        Parameters
        ----------
        inputs: dict[str, EOProduct]
            EOProducts to check
        update_attrs: bool = True
            To write the result of the checks in quality attribute group of the EOProduct. By default it's True.
        write_report: bool = False
            To write the report of the quality control processor. By default it's False.
        report_path: str = None
            The path where to write the quality control report. By default it's None.
        config_path: Optional[str] = None
            The quality control configuration to run. By default it's None and it load_file the default configuration.
        **kwargs: any
            any needed kwargs

        Returns
        -------
        dict[str, EOProduct]
            The controlled products.
        """
        for name, eoproduct in inputs.items():
            # If no given configuration in Processor, it get the default one.
            if not eoproduct.product_type:
                raise InvalidProductError(f"Missing product type for {eoproduct.name} in {name}")
            qc_config = EOQCConfig(config_path) if config_path else self.qc_config
            if qc_config is None:
                qc_config = EOPQCConfigFactory().get_default(eoproduct.product_type)
            # Run check(s) of the configuration
            for qc in qc_config.qclist.values():
                try:
                    qc.check(eoproduct)
                except Exception as e:
                    self._logger.exception(f"An erreur ocurred in : {qc.id}", e)
                    raise e
            # If true it update the quality attribute of the product.
            if update_attrs:
                self.update_attributs(eoproduct, qc_config)
            # If the it write the quality control report in a .json file.
            if write_report:
                if report_path is not None:
                    self.write_report(eoproduct, report_path, qc_config)
                else:
                    raise ValueError("Can't write report no path given")
        return inputs

    def update_attributs(self, eoproduct: EOProduct, qc_config: EOQCConfig) -> None:
        """This method update the EOProduct quality group attributes with the result of quality control.
        Parameters
        ----------
        eoproduct: EOProduct
            EOProduct to check
        config_path: EOQCConfig
            The quality control configuration which was used.
        """
        if "quality" not in eoproduct:
            eoproduct["quality"] = EOGroup("quality")
        if "qc" not in eoproduct.quality.attrs:
            eoproduct.quality.attrs["qc"] = {}
        for qc in qc_config.qclist.values():
            if qc.status:
                eoproduct.quality.attrs["qc"][qc.id] = {
                    "version": qc.version,
                    "status": qc.status,
                    "message": qc.message_if_passed,
                }
            else:
                eoproduct.quality.attrs["qc"][qc.id] = {
                    "version": qc.version,
                    "status": qc.status,
                    "message": qc.message_if_failed,
                }

    def write_report(self, eoproduct: EOProduct, report_path: str, qc_config: EOQCConfig) -> bool:
        """This method write the quality control report in json in given location.

        Parameters
        ----------
        eoproduct: EOProduct
            EOProduct to check
        report_path: str = None
            The path where to write the qc report.
        config_path: EOQCConfig
            The quality control configuration which was used.

        Returns
        -------
        bool
            Has the quality control report been successfully written, true is ok, false if not.
        """
        report_path = os.path.join(report_path, f"QC_report_{eoproduct.name}.json")
        report: dict[str, Any] = {}
        report["Product_name"] = eoproduct.name
        report["Product_type"] = eoproduct.product_type
        report["QC_config_version"] = qc_config.version
        try:
            report["Start_sensing_time"] = eoproduct.attrs["properties"]["start_datetime"]
            report["Stop_sensing_time"] = eoproduct.attrs["properties"]["end_datetime"]
        except KeyError as e:
            report["Start_sensing_time"] = ""
            report["Stop_sensing_time"] = ""
            self._logger.warning(
                f"start_datetime or end_datetime is missing in the global attributes of {eoproduct.name} due to: {e}",
            )

        try:
            report["Relative_orbit_number"] = eoproduct.attrs["properties"]["eopf:product"]["relative_orbit_number"]
        except KeyError as e:
            report["Relative_orbit_number"] = ""
            self._logger.warning(
                f"relative_orbit_number is missing in the global attributes of {eoproduct.name} due to {e}",
            )

        try:
            report["Absolute_orbit_number"] = eoproduct.attrs["absolute_orbit_number"]
        except KeyError as e:
            report["Absolute_orbit_number"] = ""
            self._logger.warning(
                f"absolute_orbit_number is missing in the global attributes of {eoproduct.name} due to: {e}",
            )

        report["Inspection_date"] = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        for qc in qc_config.qclist.values():
            report[qc.id] = {
                "version": qc.version,
                "status": qc.status,
                "message": qc.message_if_passed if qc.status else qc.message_if_failed,
            }

        try:
            with open(report_path, "w") as outfile:
                json.dump(report, outfile, indent=4)
                return True
        except IOError as e:
            self._logger.warning(f"An error is occured while trying to write the QC Report : {e}")
            raise e
