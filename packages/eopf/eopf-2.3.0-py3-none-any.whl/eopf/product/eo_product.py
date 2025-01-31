import copy
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, MutableMapping, Optional, cast
from warnings import warn

# TODO replace by something in compute or common utils
import numpy as np
from datatree import DataTree

from eopf.common import date_utils
from eopf.common.constants import EOPF_CPM_PATH, ROOT_PATH_DATATREE
from eopf.common.file_utils import AnyPath
from eopf.exceptions import InvalidProductError, StoreMissingAttr
from eopf.exceptions.errors import EOPathError, MappingMissingError
from eopf.exceptions.warnings import EOPFDeprecated, NoMappingFile
from eopf.logging import EOLogging
from eopf.product.eo_group import EOGroup
from eopf.product.eo_variable import EOVariable
from eopf.product.rendering import renderer
from eopf.product.utils.eopath_utils import is_absolute_eo_path, product_relative_path
from eopf.store.mapping_manager import EOPFAbstractMappingManager, EOPFMappingManager

if TYPE_CHECKING:  # pragma: no cover
    from eopf.product.eo_object import EOObject


class EOProduct(EOGroup):
    """A EOProduct contains EOGroups (and through them, their EOVariables),
    linked to its EOProductStore (if existing).

    Read and write both dynamically or on demand to the EOProductStore.
    It can be used in a dictionary like manner with relative and absolute paths.
    It has personal attributes and both personal and inherited coordinates.

    Parameters
    ----------
    name: str
        name of this product
    storage_driver: Union[str, EOProductStore], optional
        a EOProductStore or a string to create to a EOZarrStore
    attrs: dict[str, Any], optional
        global attributes of this product

    See Also
    --------
    """

    MANDATORY_FIELD = ("measurements",)
    _TYPE_ATTR_STR = "product_type"

    def __init__(
        self,
        name: str,
        attrs: Optional[MutableMapping[str, Any]] = None,
        product_type: Optional[str] = None,
        strict: bool = False,
        mapping_manager: Optional[EOPFAbstractMappingManager] = None,
        **kwargs: Any,
    ) -> None:
        """

        Parameters
        ----------
        name
        storage_driver
        url
        attrs
        product_type
        strict
        mapping_factory
        kwargs
        """
        self._logger = EOLogging().get_logger("eopf.product.eo_product")
        self._mapping_manager = mapping_manager if mapping_manager is not None else EOPFMappingManager()
        EOGroup.__init__(self, attrs=attrs)
        # incoming attrs doesn't have the product:type tag
        if self.product_type is None and product_type is not None:
            self.product_type = product_type
        self._name: str = name
        self._strict = strict
        self.__short_names: dict[str, str] = {}
        self.__short_names_origin_type: Optional[str] = None
        self._mission_specific: Optional[str] = None
        if "storage" in kwargs or "storage_driver" in kwargs:
            self._logger.warning(
                "The EOProduct has no store attached since version 2.0.0",
                EOPFDeprecated,
            )
            warn(
                "The EOProduct has no store attached since version 2.0.0",
                EOPFDeprecated,
            )

    def __deepcopy__(self, memo: dict[int, Any]) -> "EOProduct":
        new_instance: EOProduct = EOProduct(
            self.name,
            copy.deepcopy(self.attrs),
            self.product_type if self.product_type is not None else "",
            self._strict,
            self._mapping_manager,
        )
        self.copy_tree(new_instance)
        memo[id(self)] = new_instance
        return new_instance

    def __contains__(self, key: Any) -> bool:
        key = self.short_names.get(key, key)
        if is_absolute_eo_path(key):
            key = product_relative_path(self.path, key)
        return super().__contains__(key)

    def __delitem__(self, key: str) -> None:
        # Support short name to path conversion
        key = self.short_names.get(key, key)
        if key[0] == "/":
            self.__delitem__(key[1:])
        else:
            super().__delitem__(key)

    def __getitem__(self, key: str) -> "EOObject":
        # Support short name to path conversion
        key = self.short_names.get(key, key)
        return super().__getitem__(key)

    def __repr__(self) -> str:
        return f"[EOProduct]{hex(id(self))}"

    def __setitem__(self, key: str, value: "EOObject") -> None:
        # Support short name to path conversion
        key = self.short_names.get(key, key)
        super().__setitem__(key, value)

    def __str__(self) -> str:
        return self.__repr__()

    def add_group(self, name: str, attrs: dict[str, Any] = {}, dims: tuple[str, ...] = tuple()) -> "EOGroup":
        warn(
            "eoproduct.add_group(name, ...) is deprecated. Use eoproduct[name] = EOGroup(...) instead",
            DeprecationWarning,
        )

        key = self.short_names.get(name, name)
        return super().add_group(key, attrs, dims)

    def add_variable(self, name: str, data: Optional[Any] = None, **kwargs: Any) -> "EOVariable":
        warn(
            "eoproduct.add_variable(name, ...) is deprecated. Use eoproduct[name] = EOVariable(...) instead",
            DeprecationWarning,
        )

        key = self.short_names.get(name, name)
        return super().add_variable(key, data, **kwargs)

    def get_default_file_name_no_extension(self, mission_specific: Optional[str] = None) -> str:
        """
        get the default filename using the convention :
            - Take product:type or internal product_type (8 characters, see #97)
            - Add "_"
            - Take start_datetime as YYYYMMDDTHHMMSS
            - Add "_"
            - Take end_datetime and start_datetime and calculate the difference in seconds (between 0000 to 9999)
            - Add "_"
            - Take the last character of "platform"  (A or B)
            - Take sat:relative_orbit (between 000 and 999)
            - Add "_"
            - Take product:timeline: if it is NRT or 24H or STC, add "T";  if it is NTC, add "S"
            - Generate CRC on 3 characters
            if mission specific provided :
            - Add "_"
            - Add <mission_specific>
        """
        _req_attr_in_properties = [
            "start_datetime",
            "end_datetime",
            "platform",
            "sat:relative_orbit",
            "product:timeline",
        ]
        filename = ""
        # get the properties attribute dict
        attributes_dict: dict[str, Any] = self.attrs
        if "stac_discovery" not in attributes_dict:
            raise StoreMissingAttr("Missing [stac_discovery] in attributes")
        if "properties" not in attributes_dict["stac_discovery"]:
            raise StoreMissingAttr("Missing [properties] in attributes[stac_discovery]")
        attributes_dict_properties = attributes_dict["stac_discovery"]["properties"]
        for attrib in _req_attr_in_properties:
            if attrib not in attributes_dict_properties:
                raise StoreMissingAttr(
                    f"Missing one required property in product to generate default filename : {attrib}",
                )
        # get the product type
        if self.product_type is None or self.product_type == "":
            if "product:type" not in attributes_dict["stac_discovery"]:
                raise StoreMissingAttr("Missing product type and product:type attributes")
            product_type: str = attributes_dict["stac_discovery"]["product:type"]
        else:
            product_type = self.product_type
        start_datetime = attributes_dict_properties["start_datetime"]
        start_datetime_str = date_utils.get_date_yyyymmddthhmmss_from_tm(
            date_utils.get_datetime_from_utc(start_datetime),
        )
        end_datetime = attributes_dict_properties["end_datetime"]
        duration_in_second = int(
            (
                date_utils.get_datetime_from_utc(end_datetime) - date_utils.get_datetime_from_utc(start_datetime)
            ).total_seconds(),
        )
        platform_unit = attributes_dict_properties["platform"][-1]
        relative_orbit = attributes_dict_properties["sat:relative_orbit"]
        timeline_tag = "X"
        if attributes_dict_properties["product:timeline"] in ["NR", "NRT", "NRT-3h"]:
            timeline_tag = "T"
        elif attributes_dict_properties["product:timeline"] in ["ST", "24H", "STC", "Fast-24h", "AL"]:
            timeline_tag = "_"
        elif attributes_dict_properties["product:timeline"] in ["NTC", "NT"]:
            timeline_tag = "S"
        else:
            raise StoreMissingAttr("Unrecognized product:timeline attribute, should be NRT/24H/STC/NTC")
        crc = np.random.randint(100, 999, 1)[0]
        if mission_specific is not None:
            mission_specific = f"_{mission_specific}"
        elif self.mission_specific is not None:
            mission_specific = f"_{self.mission_specific}"
        else:
            mission_specific = ""
        filename = (
            f"{product_type}_{start_datetime_str}_{duration_in_second:04d}_{platform_unit}{relative_orbit:03d}_"
            f"{timeline_tag}{crc}{mission_specific}"
        )
        return filename

    def is_valid(self) -> bool:
        """Check if the product is a valid eopf product

        Returns
        -------
        bool

        See Also
        --------
        EOProduct.validate"""
        return all(key in self for key in self.MANDATORY_FIELD)

    # docstr-coverage: inherited
    @property
    def path(self) -> str:
        return "/"

    # docstr-coverage: inherited
    @property
    def product(self) -> "EOProduct":
        return self

    # docstr-coverage: inherited
    @property
    def relative_path(self) -> Iterable[str]:
        return []

    def _get_short_names(self, product_type: str) -> dict[str, str]:
        if product_type not in ["", " ", "\x00"]:
            try:
                short_names = self._mapping_manager.parse_shortnames(product_type=product_type)
                if short_names is None:
                    raise KeyError(f"No shortnames found for type {product_type}")
                return short_names
            except (KeyError, MappingMissingError):
                self._logger.warning(NoMappingFile(f"No mapping for {product_type}"))
                warn(NoMappingFile(f"No mapping for {product_type}"))
        return {}

    @property
    def product_type(self) -> Optional[str]:
        """

        Returns
        -------
        product type coming from attribute ["stac_discovery"]["properties"]["product:type"]
        """
        try:
            return self.attrs["stac_discovery"]["properties"]["product:type"]
        except KeyError:
            return None

    @product_type.setter
    def product_type(self, intype: str) -> None:
        self.attrs.setdefault("stac_discovery", {}).setdefault("properties", {})["product:type"] = intype

    def set_type(
        self,
        intype: str,
        url: Optional[AnyPath] = None,
        short_names: Optional[dict[str, str]] = None,
    ) -> None:
        self._logger.warning(
            "eoproduct.set_type(intype, ...) is deprecated. Use eoproduct.product_type = type instead",
            DeprecationWarning,
        )
        warn(
            "eoproduct.set_type(intype, ...) is deprecated. Use eoproduct.product_type = type instead",
            DeprecationWarning,
        )
        self.product_type = intype
        if short_names is not None:
            self.__short_names = short_names
            self.__short_names_origin_type = intype

    @property
    def mission_specific(self) -> Optional[str]:
        return self._mission_specific

    @mission_specific.setter
    def mission_specific(self, amission_specific: str) -> None:
        self._mission_specific = amission_specific

    @property
    def short_names(self) -> dict[str, str]:
        """
        Get the shortnames if available for the product type else empty dict
        Returns
        -------

        """
        if self.product_type is not None and self.__short_names_origin_type != self.product_type:
            # Product type have been changed or was shortnames where never set -> generate the shortnames
            self.__short_names = self._get_short_names(self.product_type)
            self.__short_names_origin_type = self.product_type

        return self.__short_names

    def validate(self) -> None:
        """check if the product is a valid eopf product, raise an error if is not a valid one

        Raises
        ------
        InvalidProductError
            If the product not follow the harmonized common data model

        See Also
        --------
        EOProduct.is_valid
        """
        if not self.is_valid():
            groups = [gr for gr in self.groups]
            raise InvalidProductError(
                f"Invalid product {self}, missing mandatory groups. "
                f"Available {groups} while mandatory : {self.MANDATORY_FIELD}",
            )

    # docstr-coverage: inherited

    def _add_local_variable(self, name: str = "", data: Any = None, new_eo: bool = True, **kwargs: Any) -> "EOVariable":
        if self._strict:
            raise InvalidProductError("Products can't directly store variables.")
        else:
            return super()._add_local_variable(name, data, **kwargs)

    def _init_similar(self) -> "EOProduct":
        attrs = {k: v for (k, v) in self.attrs.items() if k != "_ARRAY_DIMENSIONS"}
        return EOProduct(self.name, attrs=attrs)

    @property
    def is_root(self) -> "bool":
        """
        Is this object a root of the data tree ?
        """
        return True

    def _repr_html_(self, prettier: bool = True) -> str:
        """Returns the html representation of the current product displaying the tree.

        Parameters
        ----------
        prettier: str
            Flag for using SVG as label for each Product, Group, Variable, Attribute.
        """

        eopf_cpm_path = AnyPath(EOPF_CPM_PATH)
        css_file = eopf_cpm_path / "product/templates/static/css/style.css"

        with css_file.open(mode="r") as css:
            css_content = css.read()

        css_str = f"<style>{css_content}</style>\n"
        rendered_template = renderer("product.html", product=self, prettier=prettier)
        final_str = css_str + rendered_template

        return final_str

    def subset(
        self,
        region: tuple[int, int, int, int],
        reference: Optional[str] = "",
    ) -> "EOProduct":
        return cast(EOProduct, super().subset(region, reference))

    def to_datatree(self) -> DataTree[Any]:
        """
        Converts the current object into a DataTree.

        Returns
        -------
        DataTree
            The constructed DataTree object representing the current object.
        """
        dt: DataTree[Any] = DataTree(name=self.name)

        # Ensuring self.attrs is of type Dict[Hashable, Any]
        if not isinstance(self.attrs, dict):
            raise TypeError("self.attrs must be a dictionary")
        dt.attrs = {k: v for k, v in self.attrs.items()}  # Creating a new dictionary of type Dict[Hashable, Any]

        for obj in self.walk():
            if isinstance(obj, EOVariable) and obj.data is not None:
                dt[str(obj.path)] = obj.data
            else:
                dt[str(obj.path)] = DataTree(name=obj.name)

            if not isinstance(obj.attrs, dict):
                raise TypeError("obj.attrs must be a dictionary")
            dt[str(obj.path)].attrs.update(
                {k: v for k, v in obj.attrs.items()},
            )  # Ensuring obj.attrs is of type Dict[Hashable, Any]

        return dt

    @classmethod
    def from_datatree(cls, datatree: DataTree[Any]) -> "EOProduct":
        """
        Creates an instance of the class from a given DataTree.

        Parameters
        ----------
        datatree : DataTree
            The DataTree object from which to create the class instance.

        Returns
        -------
        cls
            An instance of the class representing the given DataTree.
        """
        attrs_with_str_keys: Dict[str, Any] = {
            str(k): v for k, v in datatree.attrs.items()
        }  # Convert the dictionary to have only string keys
        mutable_attrs: MutableMapping[str, Any] = attrs_with_str_keys  # Now cast it to MutableMapping[str, Any]

        eoproduct = cls(name=str(datatree.name), attrs=mutable_attrs)
        for obj in datatree.subtree:
            if obj.path == ROOT_PATH_DATATREE:
                continue
            try:
                eoproduct[obj.path]
            except (EOPathError, KeyError):
                eoproduct[obj.path] = EOGroup(Path(obj.path).name, attrs=obj.attrs)
            else:
                eoproduct[obj.path].attrs.update(obj.attrs)
            for var_name in obj.variables:
                if var_name not in obj.coords:
                    variable = obj[var_name]
                    eoproduct[obj.path][var_name] = EOVariable(name=var_name, data=variable)  # type: ignore
        return eoproduct
