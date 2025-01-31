import importlib
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

from eopf.common import file_utils
from eopf.config.config import EOConfiguration
from eopf.exceptions import (
    EOQCConfigFactoryNoDefaultConfiguration,
    MissingConfigurationParameterError,
)
from eopf.exceptions.errors import MappingMissingError, MissingArgumentError
from eopf.logging import EOLogging

EOConfiguration().register_requested_parameter("mapping_folder", param_is_optional=True)


class EOPFAbstractMappingFactory(ABC):

    @abstractmethod
    def get_mapping(self, *args: Any, **kwargs: Any) -> Any:
        pass

    @abstractmethod
    def register_mapping(self, *args: Any, **kwargs: Any) -> Any:
        pass


class EOPFMappingFactory(EOPFAbstractMappingFactory):
    FILENAME_RECO = "filename_pattern"
    TYPE_RECO = "product_type"
    RECO = "recognition"

    def __init__(self, default_mappings: bool = True) -> None:
        self.LOGGER = EOLogging().get_logger("eopf.mapping_factory")
        self.mapping_set: set[str] = set()
        if default_mappings:
            self._load_default_mapping()

    def _load_default_mapping(self) -> None:
        """

        :return:
        """
        try:
            path_directory = Path(EOConfiguration().mapping_folder)
            for mapping_path in path_directory.glob("*.json"):
                self._register_mapping_internal(str(mapping_path))
        except (MissingConfigurationParameterError, EOQCConfigFactoryNoDefaultConfiguration):
            # mapping has not been provided in configuration
            pass
        for resource in importlib.metadata.entry_points(group="eopf.store.mapping_folder"):
            resources_path_dir = importlib.resources.files(resource.value)
            for mapping_file in resources_path_dir.iterdir():
                if mapping_file.is_file():
                    with importlib.resources.as_file(mapping_file) as file:
                        if file.suffix == ".json":
                            self._register_mapping_internal(str(file))
        self._verify_mappings()

    def get_mapping(
        self,
        file_path: Optional[str] = None,
        product_type: Optional[str] = None,
    ) -> Optional[dict[str, Any]]:
        """
        :param file_path: file path if provided uses regex pattern matching to get the mapping
        :param product_type: if no path provided will try with the product type
        :return:
        the mapping

        :exception:
        MissingArgumentError if no file_name or product type provided
        MappingMissingError if not mapping is found
        """
        if product_type:
            recognised = product_type
            reco = self.TYPE_RECO
        elif file_path:
            recognised = file_path
            reco = self.FILENAME_RECO
        else:
            raise MissingArgumentError("Must provide either file_path or product_type.")

        for json_mapping_path in self.mapping_set:
            json_mapping_data = file_utils.load_json_file(json_mapping_path)
            if self.guess_can_read(json_mapping_data, recognised, reco):
                self.LOGGER.debug(f"Found {json_mapping_path} for file {file_path} and product type {product_type}")
                return json_mapping_data

        raise MappingMissingError(f"No mapping was found for product: {file_path} and product_type {product_type}")

    @staticmethod
    def guess_can_read(json_mapping_data: dict[str, Any], recognised: str, recogniton_key: str) -> bool:
        pattern = json_mapping_data.get("recognition", {}).get(recogniton_key)
        if pattern:
            return re.match(pattern, recognised) is not None
        return False

    def _register_mapping_internal(self, store_class: str) -> None:
        """
        Internal placeholder
        :param store_class:
        :return:
        """
        self.mapping_set.add(store_class)

    def register_mapping(self, store_class: str) -> None:
        """
        Can be call by user to add custom mappings other then the defaults
        :param store_class: A path to a json file
        :return:
        """
        self._register_mapping_internal(store_class)
        # In case someone register from outside
        self._verify_mappings()

    def _verify_mappings(self) -> None:
        """
        Verify the integrity of loaded mappings
        :return:
        """
        # Verify that we don't have two time the same product type
        product_types_availables = []
        for json_mapping_path in self.mapping_set:
            json_mapping_data = file_utils.load_json_file(json_mapping_path)
            product_type = json_mapping_data.get("recognition", {}).get(self.TYPE_RECO)
            if product_type in product_types_availables:
                self.LOGGER.warning(
                    f"Found multiple mappings for product type {product_type} for example in {json_mapping_path}",
                )
            else:
                product_types_availables.append(product_type)
