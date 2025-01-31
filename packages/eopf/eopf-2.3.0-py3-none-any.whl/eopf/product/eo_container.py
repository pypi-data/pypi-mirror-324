from typing import (
    Any,
    ItemsView,
    Iterable,
    Iterator,
    KeysView,
    Optional,
    Self,
    Union,
    ValuesView,
)

import numpy as np

from eopf.common import date_utils
from eopf.common.constants import EOPF_CPM_PATH
from eopf.common.file_utils import AnyPath
from eopf.exceptions import StoreMissingAttr
from eopf.product.eo_object import EOObject
from eopf.product.eo_product import EOProduct
from eopf.product.rendering import renderer


class EOContainer(EOObject):
    """
    specialized dict to retain products and do additional things such as stac attributes etc

    """

    @staticmethod
    def create_from_products(name: str, products: Iterable["EOProduct" | Self]) -> "EOContainer":
        """

        Parameters
        ----------
        name
        products

        Returns
        -------

        """
        container = EOContainer(name)
        for pr in products:
            if len(pr.name) == 0:
                raise KeyError("Can't have product without proper name in EOContainer")
            container[pr.name] = pr
        return container

    def __init__(
        self,
        name: str,
        attrs: Optional[dict[str, Any]] = None,
        type: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(name, **kwargs)
        self._prod_dict: dict[str, "EOProduct" | Self] = {}
        self._attrs: dict[str, Any] = dict(attrs) if attrs is not None else {}
        self._mission_specific: Optional[str] = None
        if type is not None:
            self._attrs["stac_discovery"]["product:type"] = type
        self._declare_as_container()

    @property
    def attrs(self) -> dict[str, Any]:
        for prod in self.values():
            self._add_product_to_links(prod)
        return self._attrs

    @property
    def mission_specific(self) -> Optional[str]:
        return self._mission_specific

    @mission_specific.setter
    def mission_specific(self, amission_specific: str) -> None:
        self._mission_specific = amission_specific

    def __setitem__(self, key: str, value: "EOProduct" | Self) -> None:
        from eopf.product import EOProduct

        if len(key) == 0:
            raise KeyError("Empty key is not accepted in eocontainer")
        if not isinstance(value, (EOProduct | EOContainer)):
            raise TypeError(f"Only EOProducts/EOContainer accepted in EOContainer not {type(value)}")
        if len(value.name) == 0:
            raise KeyError("Products with empty name are not accepted in eocontainer")

        # Test the incoming product type
        if len(self._prod_dict) != 0:
            try:
                initial_type: str = self._prod_dict[list(self._prod_dict.keys())[0]].attrs["stac_discovery"][
                    "properties"
                ]["product:type"]
                incoming_type: str = value.attrs["stac_discovery"]["properties"]["product:type"]
                if initial_type != incoming_type:
                    raise TypeError(
                        f"Can't have different product types in container, "
                        f"contained {initial_type} while putting {incoming_type}",
                    )
            except KeyError:
                pass

        self._prod_dict[key] = value
        self._add_product_to_links(value)

    def __getitem__(self, item: str) -> "EOProduct" | Self:
        return self._prod_dict[item]

    def __delitem__(self, key: str) -> None:
        self._remove_product_to_links(self._prod_dict[key])
        del self._prod_dict[key]

    def __iter__(self) -> Iterator["str"]:
        yield from iter(self._prod_dict)

    def __len__(self) -> int:
        return len(self._prod_dict)

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return f"[EOContainer]{hex(id(self))}"

    def _repr_html_(self, prettier: bool = True) -> str:
        """Returns the html representation of the current container displaying the tree.

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
        rendered_template = renderer("container.html", container=self, prettier=prettier)
        final_str = css_str + rendered_template

        return final_str

    def _print_tree_structure(self, obj: Union["EOObject", tuple[str, "EOObject"]], level: int, detailed: bool) -> None:
        if isinstance(obj, tuple):
            cont = obj[1]
        else:
            cont = obj
        if not isinstance(cont, EOContainer):
            return
        if level > 0:
            indent = "|" + " " * level
        else:
            indent = ""
        for v in cont.items():
            if isinstance(v[1], EOProduct):
                print(f"{indent}└───Product {v[0]}")
            else:
                print(f"{indent}└───Container {v[0]}")
            v[1]._print_tree_structure(v, level + 1, detailed)

    def items(self) -> ItemsView[str, "EOProduct" | Self]:
        yield from self._prod_dict.items()

    def keys(self) -> KeysView[str]:
        yield from self._prod_dict.keys()

    def values(self) -> ValuesView["EOProduct" | Self]:
        yield from self._prod_dict.values()

    def validate(self) -> None:
        for pro in self._prod_dict.items():
            pro[1].validate()

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
        if "product:type" not in attributes_dict["stac_discovery"]["properties"]:
            raise StoreMissingAttr("Missing product:type attributes")
        product_type: str = attributes_dict["stac_discovery"]["properties"]["product:type"]
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

    def export_dask_graph(self, folder: AnyPath) -> None:
        for v in self:
            self[v].export_dask_graph(folder)

    @property
    def is_root(self) -> "bool":
        """
        Container are considered root
        Returns
        -------

        """
        return True

    def _declare_as_container(self) -> None:
        self._attrs.setdefault("stac_discovery", dict()).setdefault("links", [])
        self._attrs.setdefault("other_metadata", dict()).setdefault("eopf:category", "eocontainer")

    def _add_product_to_links(self, prod: "EOProduct" | Self) -> None:
        link_list = self._attrs.setdefault("stac_discovery", dict()).setdefault("links", [])
        if prod.name not in link_list:
            link_list.append(prod.name)

    def _remove_product_to_links(self, prod: "EOProduct" | Self) -> None:
        self._attrs.setdefault("stac_discovery", dict()).setdefault("links", []).remove(prod.name)

    @staticmethod
    def is_container(objwithattr: Any) -> "bool":
        """
        Test is the object has the elements to be considered a container
        Mostly tests on the STAC attribute links and category in other:metadata

        Parameters
        ----------
        objwithattr: any EO object or other that has attrs access

        Returns
        -------

        """
        if isinstance(objwithattr, EOContainer):
            return True
        try:
            return (
                "links" in objwithattr.attrs["stac_discovery"]
                and isinstance(objwithattr.attrs["stac_discovery"]["links"], list)
                and objwithattr.attrs["other_metadata"]["eopf:category"] == "eocontainer"
            )
        except KeyError:
            return False
