import os
from collections.abc import MutableMapping
from pathlib import Path, PurePosixPath
from typing import Any, Dict, Iterator, Optional

from dask.delayed import Delayed
from numcodecs import Blosc
from numpy import isnan
from xarray import Dataset, open_zarr
from zarr import consolidate_metadata
from zarr._storage.store import Store
from zarr.errors import GroupNotFoundError

from eopf.common.constants import (
    ADD_OFFSET,
    SCALE_FACTOR,
    VALID_MAX,
    VALID_MIN,
    XARRAY_FILL_VALUE,
    OpeningMode,
)
from eopf.common.file_utils import AnyPath
from eopf.config.config import EOConfiguration
from eopf.daskconfig.dask_utils import compute
from eopf.exceptions.errors import (
    EOGroupReadError,
    EOStoreCantLoadContainerError,
    EOStoreInvalidPathError,
    EOStoreProductAlreadyExistsError,
    EOVariableReadError,
    StoreInvalidMode,
    StoreLoadFailure,
)
from eopf.exceptions.warnings import AlreadyClose, EOZarrStoreWarning
from eopf.logging import EOLogging
from eopf.product import EOGroup, EOProduct, EOVariable
from eopf.product.utils.eoobj_utils import NONE_EOObj
from eopf.store.abstract import EOProductStore, StorageStatus
from eopf.store.mapping_manager import EOPFAbstractMappingManager, EOPFMappingManager
from eopf.store.store_factory import EOStoreFactory

from ..common.type_utils import Chunk
from ..product.eo_container import EOContainer
from ..product.eo_object import EOObject

ZARR_PRODUCT_FORMAT = "zarr"
EOV_ATTRS = "eov_attrs"


# Warning : do not remove this is the factory registry mecanism
@EOStoreFactory.register_store(ZARR_PRODUCT_FORMAT)
class EOZarrStore(EOProductStore):

    DEFAULT_COMPRESSION_ALGORITHM = "zstd"
    DEFAULT_COMPRESSION_LEVEL = 3
    DEFAULT_SHUFFLE = Blosc.BITSHUFFLE
    DEFAULT_COMPRESSOR = Blosc(
        cname=DEFAULT_COMPRESSION_ALGORITHM,
        clevel=DEFAULT_COMPRESSION_LEVEL,
        shuffle=DEFAULT_SHUFFLE,
    )
    EXTENSION = ".zarr"

    def __init__(
        self,
        url: str | AnyPath,
        mapping_manager: Optional[EOPFAbstractMappingManager] = None,
        mask_and_scale: Optional[bool] = None,
        *args: Any,
        **kwargs: dict[str, Any],
    ) -> None:
        """
        Initializes the XarrayStore

        Parameters
        ----------
        url: str|AnyPath
            file system path to a product
        mapping_manager: EOPFAbstractMappingManager
           mapping manager used to retrieve short names
        mask_and_scale: Optional[bool] = None
            apply or not masking and scalling by overiding EOConfiguration
        args:
            None
        kwargs:
            storage_options: dict[Any, Any] parameters for AnyPath

        Raises
        -------

        Returns
        -------
        """
        if not EOProductStore.is_valid_url(url):
            raise EOStoreInvalidPathError(f"The url: {url} does not exist.")

        super().__init__(url, *args, **kwargs)
        self._chunking: Optional[Chunk] = None
        self._delayed_list: list[Delayed] = list()
        self._loaded_eops: dict[str, EOProduct] = dict()
        self._loaded_eopc: dict[str, EOContainer] = dict()
        self._mapping: Dict[str, Any] = {}
        self._delayed_writing: bool = True
        self._compressor: Any = None
        self._read_zarr_kwargs: dict[str, Any] = dict()
        self._write_zarr_kwargs: dict[str, Any] = dict()
        self._eov_kwargs: dict[str, Any] = dict()
        self._short_names_map: dict[str, str] = dict()
        self._mapping_manager: EOPFAbstractMappingManager = (
            mapping_manager if mapping_manager is not None else EOPFMappingManager()
        )
        self.LOGGER = EOLogging().get_logger("eopf.store.zarr")
        if mask_and_scale is None:
            eopf_config = EOConfiguration()
            self._mask_and_scale = eopf_config.get("product__mask_and_scale")
        else:
            self._mask_and_scale = mask_and_scale

    def __getitem__(self, key: str) -> "EOObject":
        """
        Retrieves an EOVariable

        Parameters
        ----------
        key: str
            a EOProduct path as str

        Raises
        -------
        StoreNotOpenError
        EOGroupReadError
        EOVariableReadError

        Returns
        -------
        EOObject
        """
        self.check_is_opened()

        if self._mode != OpeningMode.OPEN:
            self.LOGGER.warning(
                f"Functionality available only in mode: {OpeningMode.OPEN} not it current mode: {self._mode}",
                EOZarrStoreWarning,
            )
            return NONE_EOObj

        # Accessed key is a product name url / key.zarr exists
        if self.is_product(key):
            return self.load(key)

        """"
         Backward compatiblity with 2.0.0 behaviour even if only eoproducts should be retrieved on stores
        """

        # use short names
        if key in self._short_names_map:
            key = self._short_names_map[key]

        var_zarray_fspath = self.url / key / ".zarray"
        var_eopath = PurePosixPath(key)
        var_name = var_eopath.name
        group_eopath = var_eopath.parent
        group_fspath: AnyPath = self.url / str(group_eopath)

        if not group_fspath.exists():
            raise EOGroupReadError(f"EOGroup {group_fspath.path} does not exist")

        if not var_zarray_fspath.exists():
            self.LOGGER.warning(
                "Only EOVariables or Products can be retrieved",
                EOZarrStoreWarning,
            )
            return NONE_EOObj

        try:
            ds = open_zarr(group_fspath.to_zarr_store(), consolidated=False, decode_cf=False, **self._read_zarr_kwargs)

            # deserialise eov from xarray.dataarray
            eov_attrs = ds[var_name].attrs.pop(EOV_ATTRS, {})

            # eov data should already have coords attached there is no need to keep coordinates attr
            # this is also done to keep eov representation harmonised over different data types
            if "coordinates" in ds[var_name].attrs:
                # retrieve secondary coords and assign them to the data
                coords_list = ds[var_name].attrs.pop("coordinates", "").split(" ")
                coords_dict = dict()
                for coord_name in coords_list:
                    coords_dict[coord_name] = ds[coord_name]
                data = ds[var_name].assign_coords(coords_dict)
            else:
                data = ds[var_name]

            # the cpm does not allow nan in fill_value, hence only xarray can add it
            # when mask_and_scale paramter of open_zarr is set to false
            # this will break the logic of is_masked, hence we need to pop it
            if XARRAY_FILL_VALUE in data.attrs and isnan(data.attrs[XARRAY_FILL_VALUE]):
                data.attrs.pop(XARRAY_FILL_VALUE)

            eo_obj: EOObject = EOVariable(
                name=var_name,
                data=data,
                attrs=eov_attrs,
                **self._eov_kwargs,
            )

            if isinstance(eo_obj, EOVariable):
                # in oder to retrieve all attrs from zarr with xarray we need to used decode_cf=False
                # however, using this flag will instruct xarray not to perform mask_and_scale within xarray
                # thus, we need to do the masking on the zarr store
                if VALID_MIN in eov_attrs or VALID_MAX in eov_attrs or XARRAY_FILL_VALUE in data.attrs:
                    eo_obj.mask(mask_apply=self._mask_and_scale)
                if SCALE_FACTOR in data.attrs or ADD_OFFSET in data.attrs:
                    eo_obj.scale(scale_apply=self._mask_and_scale)

            ds.close()
        except Exception as err:
            raise EOVariableReadError(f"{var_name} retrieve error: {err}")

        return eo_obj

    def open(
        self,
        mode: OpeningMode = OpeningMode.OPEN,
        delayed_writing: bool = True,
        chunking: Optional[Chunk] = None,
        compressor: Any = DEFAULT_COMPRESSOR,
        **kwargs: Any,
    ) -> "EOProductStore":
        """
        Opens the store

        Parameters
        ----------
        mode: OpeningMode
            default OPEN

        delayed_writing: bool
            default True
        chunking: Optional[dict]
            chunking to be used upon reading
        compressor: ANY
            default DEFAULT_COMPRESSOR
        kwargs:
            read_zarr_kwargs: Xarray open_zarr kwargs
            write_zarr_kwargs: Xarray Dataset to_zarr kwargs
            eov_kwargs: EOVariable init kwargs

        Raises
        -------
        StoreInvalidMode

        Returns
        -------
        EOProductStore
        """
        # Already open
        if self.is_open():
            return self

        super().open(mode=mode, **kwargs)
        if mode == OpeningMode.OPEN:

            # The given url is already a .zarr
            if self.guess_can_read(self.url):
                # in order to use the short names we have to retrieve the mapping
                _, short_names_map = self._mapping_manager.parse_mapping(self.url)
                self._short_names_map = short_names_map if short_names_map is not None else dict()
            # The given url is the root dir of zarrs, compatible with the setitem API
            elif not self.url.exists():
                raise FileNotFoundError(f"{self.url} doesn't exists")

            self._chunking = chunking

            # get xarray open_zarr kwargs
            if "read_zarr_kwargs" in kwargs:
                self._read_zarr_kwargs = kwargs.pop("read_zarr_kwargs")

            # get EOVariable kwargs
            if "eov_kwargs" in kwargs:
                self._eov_kwargs = kwargs.pop("eov_kwargs")

        elif mode in [OpeningMode.CREATE, OpeningMode.CREATE_OVERWRITE]:

            self._delayed_writing = delayed_writing
            self._compressor = compressor

            # get xarray to_zarr kwargs
            if "to_zarr_kwargs" in kwargs:
                self._write_zarr_kwargs = kwargs.pop("to_zarr_kwargs")

        else:
            raise StoreInvalidMode(f"EOZarrStore does not support mode: {mode}")

        return self

    def close(self) -> None:
        """
        Closes the store
        """
        if self._status == StorageStatus.CLOSE:
            self.LOGGER.warning("Store already closed", AlreadyClose)

        self._compressor = None
        self._delayed_writing = True
        self._loaded_eops = {}
        self._delayed_list = []
        self._mapping = {}
        self._chunking = None
        self._read_zarr_kwargs = {}
        self._write_zarr_kwargs = {}
        self._eov_kwargs = {}

        self._status = StorageStatus.CLOSE

    def load_container(self, name: Optional[str] = None, **kwargs: Any) -> EOContainer:
        """
        Creates and returns an EOContainer

        Parameters
        ----------
        name: str
            Name of the EOContainer
        kwargs:
            eop_kwargs: EOProduct init kwargs
            open_kwargs: kwargs for the open function, if open is not called previously
            nested: bool to inform that it is a nested container load

        Raises
        -------
        StoreLoadFailure

        Returns
        -------
        EOContainer
        """
        if not self.is_open():
            open_kwargs = kwargs.get("open_kwargs", {})
            self.open(mode=OpeningMode.OPEN, **open_kwargs)

        if self._mode != OpeningMode.OPEN:
            raise NotImplementedError(
                f"Functionality available only in mode: {OpeningMode.OPEN} not it current mode: {self._mode}",
            )
        # if name not provided take the basename without extension as product name
        final_name = os.path.splitext(self.url.basename)[0] if name is None else name
        # nested container loading, we don't have the extension
        if kwargs.get("nested", False) and name is not None:
            product_url: AnyPath = self.url / name
            container_subfolder: str = name
        # A subproduct with the final_name.zarr is detected
        elif self.is_product(final_name):
            product_url = self.url / (final_name + self.EXTENSION)
            container_subfolder = final_name + self.EXTENSION
        else:
            # For backward compatibility with 2.0.0 when the url is the .zarr folder itself
            product_url = self.url
            container_subfolder = ""
        # read EOProduct attrs
        try:
            ds = open_zarr(product_url.to_zarr_store(), consolidated=False, **self._read_zarr_kwargs)
        except GroupNotFoundError as err:
            raise StoreLoadFailure(
                f"{product_url}/{name + self.EXTENSION if name is not None else ''}"
                f" doesn't seems to contains valid zarr file",
            ) from err
        category: str = "eocontainer" if EOContainer.is_container(ds) else "eoproduct"
        eop_attrs = ds.attrs
        ds.close()
        if category == "eocontainer":
            tmp_cont: EOContainer = EOContainer(name=final_name, attrs=eop_attrs)
            for sub_prod in product_url.ls():
                sub_prod_relpath = sub_prod.relpath(self.url)
                if sub_prod.isdir():
                    if self.is_container(sub_prod_relpath, has_extension=False):
                        loaded_cont = self.load_container(
                            os.path.join(container_subfolder, sub_prod.basename),
                            nested=True,
                            **kwargs,
                        )
                        tmp_cont[loaded_cont.name] = loaded_cont
                    elif self.is_product(sub_prod_relpath, has_extension=False):
                        loaded_prod = self.load(
                            sub_prod.basename,
                            container_loading=True,
                            container_subfolder=container_subfolder,
                            **kwargs,
                        )
                        tmp_cont[loaded_prod.name] = loaded_prod
                    else:
                        self.LOGGER.warning(f"Don't know what to do with folder : {sub_prod}")

            return tmp_cont
        raise EOStoreCantLoadContainerError("Only EOContainer can be retrieved using load_container")

    def load(self, name: Optional[str] = None, **kwargs: Any) -> EOProduct:
        """
        Creates and returns an EOProduct

        Parameters
        ----------
        name: str
            Name of the EOProduct
        kwargs:
            eop_kwargs: EOProduct init kwargs
            open_kwargs: kwargs for the open function, if open is not called previously

        Raises
        -------
        StoreLoadFailure

        Returns
        -------
        EOProduct
        """
        open_kwargs = kwargs.get("open_kwargs", {})
        self.open(mode=OpeningMode.OPEN, **open_kwargs)

        if self._mode != OpeningMode.OPEN:
            raise NotImplementedError(
                f"Functionality available only in mode: {OpeningMode.OPEN} not it current mode: {self._mode}",
            )

        if name is not None and name in self._loaded_eops and self._loaded_eops[name] is not None:
            return self._loaded_eops[name]

        # get EOProduct kwargs and mapping manager
        eop_kwargs = kwargs.pop("eop_kwargs", {})
        eop_mapping_manager = eop_kwargs.get("mapping_factory", self._mapping_manager)

        # A subproduct zarr with the name is detected
        if name is not None and self.is_product(name):
            product_url: AnyPath = self.url / (name + self.EXTENSION)
        elif "container_loading" in kwargs:
            sub_folder = kwargs.get("container_subfolder", "")
            if name is None:
                raise EOStoreCantLoadContainerError("Can't load product from container without a name")
            # Container sub product don't have the .zarr extension
            product_url = self.url / sub_folder / name
            if not self.is_product(product_url.relpath(self.url), has_extension=False):
                raise StoreLoadFailure(f"Can't find a sub product for container in {product_url}")
        else:
            # For backward compatibility with 2.0.0 when the url is the .zarr folder itself
            product_url = self.url
            # name will be the stem filename for zarrs if you don't specify the name
            name = os.path.splitext(self.url.basename)[0] if name is None else name
        try:
            # read EOProduct attrs
            try:
                ds = open_zarr(
                    product_url.to_zarr_store(),
                    consolidated=False,
                    decode_cf=False,
                    **self._read_zarr_kwargs,
                )
            except GroupNotFoundError as err:
                raise StoreLoadFailure(f"{product_url} doesn't seems to contains valid zarr") from err
            category: str = "eocontainer" if EOContainer.is_container(ds) else "eoproduct"
            eop_attrs = ds.attrs
            ds.close()
            if category == "eocontainer":
                self.LOGGER.warning(
                    "Only EOProducts can be retrieved using load, "
                    "container opened as EOProduct, use load_container instead",
                )

            # Find Type
            eo_type = self._mapping["recognition"]["product_type"] if len(self._mapping) > 0 else ""

            # create EOProduct
            tmp_prod = EOProduct(
                name=name,
                attrs=eop_attrs,
                product_type=eo_type,
                mapping_manager=eop_mapping_manager,
                **eop_kwargs,
            )
            # iterate over each group and add eogroup/eovariable
            for group_fspath in self._iter_subgroups(product_url):
                # decode_cf will drop eopf attrs if set to True
                ds = open_zarr(
                    group_fspath.to_zarr_store(),
                    consolidated=False,
                    decode_cf=False,
                    **self._read_zarr_kwargs,
                )
                group_eopath = Path(group_fspath.relpath(self.url)).as_posix()
                tmp_prod[str(group_eopath)] = EOGroup(attrs=ds.attrs)
                # secondary coords are those coords composed of primary coords
                # for example a coord which is actually composed of two primary coords
                # is defined as a secondary coord
                secondary_coords: list[str] = self.__extract_secondary_coords(ds)

                # iterate over all variables in dataset, including the coordinates
                for var_name in ds:
                    # do not consider secondary coords as EOVariable since they are attachd to a data var
                    if var_name in secondary_coords:
                        continue

                    var_eopath = PurePosixPath(group_eopath) / var_name
                    eov_attrs = ds[var_name].attrs.pop(EOV_ATTRS, {})
                    # eov data should already have coords attached, there is no need to keep coordinates attr
                    # this is also done to keep eov representation harmonised over different data types
                    if "coordinates" in ds[var_name].attrs:
                        # retrieve secondary coords and assign them to the data
                        # secondary coords are those coords composed of primary coords
                        # for example a coord which is actually composed of two primary coords
                        # is defined as a secondary coord
                        coords_list = ds[var_name].attrs.pop("coordinates", "").split(" ")
                        coords_dict = dict()
                        for coord_name in coords_list:
                            coords_dict[coord_name] = ds[coord_name]
                        data = ds[var_name].assign_coords(coords_dict)
                    else:
                        data = ds[var_name]

                    # the cpm does not allow nan in fill_value, hence if present it is due to xarray
                    # when mask_and_scale paramter of open_zarr is set to false
                    # this will break the logic of is_masked, hence we need to pop it
                    if XARRAY_FILL_VALUE in data.attrs:
                        try:
                            if isnan(data.attrs[XARRAY_FILL_VALUE]):
                                data.attrs.pop(XARRAY_FILL_VALUE)
                        except Exception as e:
                            # isnan might fail on some data types, e.g., b"-"
                            self.LOGGER.warning(f"isnan failed on var: {var_name} due to: {e}")

                    # in oder to retrieve all attrs from zarr with xarray we need to used decode_cf=False
                    # however, using this flag will instruct xarray not to perform mask_and_scale within xarray
                    # thus, we need to do the masking on the zarr store
                    eov = EOVariable(name=var_name, data=data, attrs=eov_attrs, **self._eov_kwargs)
                    if VALID_MIN in eov_attrs or VALID_MAX in eov_attrs or XARRAY_FILL_VALUE in data.attrs:
                        eov.mask(mask_apply=self._mask_and_scale)
                    if SCALE_FACTOR in data.attrs or ADD_OFFSET in data.attrs:
                        eov.scale(scale_apply=self._mask_and_scale)

                    tmp_prod[var_eopath] = eov

                ds.close()
            self._loaded_eops[name] = tmp_prod

        except Exception as err:
            raise StoreLoadFailure(f"{err}") from err

        return self._loaded_eops[name]

    @staticmethod
    def __extract_secondary_coords(ds: Dataset) -> list[str]:
        secondary_coords: list[str] = []
        for var_name in ds:
            if "coordinates" in ds[var_name].attrs:
                var_secondary_coords = ds[var_name].attrs["coordinates"].split(" ")
                for secondary_coord in var_secondary_coords:
                    if secondary_coord not in secondary_coords:
                        secondary_coords.append(secondary_coord)
        return secondary_coords

    def _iter_subgroups(self, url: AnyPath) -> list[AnyPath]:
        """
        Returns paths to all subgroups in a zarr

        Returns
        -------
        list[str]
        """
        self.check_is_opened()
        zgroups_fspath: list[AnyPath] = url.find(".*zgroup")
        groups_fspath: list[AnyPath] = []
        for zg in zgroups_fspath:
            groups_fspath.append(zg.dirname())

        # the first path is the path of the product
        return groups_fspath[1:]

    def _write_eog(
        self,
        group_anypath: AnyPath,
        group_fsstore: Store,
        eo_obj: EOGroup | EOProduct,
        sub_group_prefix: Optional[str] = None,
    ) -> None:
        """
        Creates and returns an EOProduct

        Parameters
        ----------
        group_fspath: Path
            group path inside the product
        eo_obj: EOObject
            EOObject to be written

        Raises
        -------
        StoreWriteFailure
        """

        self.LOGGER.info(f"Writing {group_anypath}/{sub_group_prefix} and zarr kwargs {self._write_zarr_kwargs}")
        data_vars: dict[str, Any] = dict()
        coords_vars: dict[str, Any] = dict()

        # building data and coordinates dict
        for var_name, var in eo_obj.variables:
            # serialise eov as xarray.dataarray
            var._data.attrs[EOV_ATTRS] = var.attrs
            data_vars[var_name] = var._data
            # retrieve the coordinates
            for coord_name in var._data.coords:
                if coord_name not in coords_vars:
                    coords_vars[str(coord_name)] = var.data.coords[str(coord_name)]

        # create xarray dataset with data and coords
        ds = Dataset(data_vars=data_vars, coords=coords_vars, attrs=eo_obj.attrs)

        # create writing or delayed objects
        encoding = {var_name: {"compressor": self._compressor} for var_name in ds.variables}
        if self._delayed_writing:
            delayed_zarr = ds.to_zarr(
                store=group_fsstore,
                group=sub_group_prefix,
                encoding=encoding,
                consolidated=False,
                compute=False,
                **self._write_zarr_kwargs,
            )
            self._delayed_list.append(delayed_zarr)
        else:
            ds.to_zarr(
                store=group_fsstore,
                group=sub_group_prefix,
                encoding=encoding,
                consolidated=False,
                compute=True,
                **self._write_zarr_kwargs,
            )
        ds.close()

        # recursiverly write sub_groups
        sub_group_prefix_str = sub_group_prefix + "/" if sub_group_prefix is not None else ""
        for sub_group_name, sub_group in eo_obj.groups:
            self._write_eog(group_anypath, group_fsstore, sub_group, sub_group_prefix_str + sub_group_name)
        # If no sub group then we are top level group and we can consolidate after writing all sub group/vars
        if sub_group_prefix is None:
            if self._delayed_writing:
                compute(self._delayed_list)
                self._delayed_list = []
            consolidate_metadata(group_fsstore)

    def _write_eoc(self, container_fspath: AnyPath, container: EOContainer) -> None:
        """

        Parameters
        ----------
        container_fspath : Anypath , the path to write the container to
        container : container to write

        Returns
        -------

        """
        self.LOGGER.info(f"Writing container {container_fspath} and zarr kwargs {self._write_zarr_kwargs}")

        main_dataset = Dataset(attrs=container.attrs)
        main_dataset.to_zarr(
            store=container_fspath.to_zarr_store(),
            **self._write_zarr_kwargs,
            compute=True,
        )
        for name, prod in container.items():
            product_name = prod.name
            product_name_with_extension = product_name
            group_fspath: AnyPath = container_fspath / product_name_with_extension
            if isinstance(prod, EOProduct):
                # EOProduct
                self._write_eog(group_fspath, group_fspath.to_zarr_store(), prod)
            else:
                # Nested container
                self._write_eoc(group_fspath, prod)

        consolidate_metadata(container_fspath.to_zarr_store())

    def __setitem__(self, __key: str, __value: EOObject) -> None:
        """
        Writes and EOProduct/EOGroup to disk

        Parameters
        ----------
        __key: str
            group path inside the product
        __value: EOObject
            EOObject to be written

        Raises
        -------
        StoreWriteFailure
        """
        self.check_is_opened()

        if self._mode not in [OpeningMode.CREATE, OpeningMode.CREATE_OVERWRITE]:
            self.LOGGER.warning(
                f"Functionality available only in mode: {OpeningMode.CREATE} not it current mode: {self._mode}",
                EOZarrStoreWarning,
            )
            return

        self._delayed_list = []
        if isinstance(__value, (EOProduct, EOContainer)):
            if __key == "":
                product_name = __value.get_default_file_name_no_extension()
                product_name_with_extension = product_name + self.EXTENSION
                group_fspath: AnyPath = self.url / product_name_with_extension
            else:
                if not __key.endswith(self.EXTENSION):
                    product_name_with_extension = __key + self.EXTENSION
                else:
                    product_name_with_extension = __key
                group_fspath = self.url / product_name_with_extension
            if self._mode == OpeningMode.CREATE:
                if group_fspath.exists():
                    raise EOStoreProductAlreadyExistsError(
                        f"Product {group_fspath} already exists and {self._mode} mode doesn't allow overwriting",
                    )
            if group_fspath.exists():
                group_fspath.rm(recursive=True)
            group_fspath.mkdir()
            if isinstance(__value, EOProduct):
                self._write_eog(group_fspath, group_fspath.to_zarr_store(), __value)
            else:
                self._write_eoc(group_fspath, __value)
        elif isinstance(__value, EOGroup):
            if __key != "":
                group_fspath = self.url / __key
            else:
                group_fspath = self.url
            self._write_eog(group_fspath, group_fspath.to_zarr_store(), __value)
        else:
            self.LOGGER.warning("Only EOProducts, EOContainer and EOGroup can be written")

    def _zgroup_exists(self, path: str) -> bool:
        """
        Check if the path has a file .zgroup under url/path/

        Parameters
        ----------
        path: Path
            path inside the product url

        Returns
        -------
        bool
        """
        zgroup_fspath: AnyPath = self.url / path / ".zgroup"
        return zgroup_fspath.exists()

    def _zarray_exists(self, path: str) -> bool:
        """
        Check if the path has a file .zarray file under url/path/

        Parameters
        ----------
        path: Path
            path inside the product

        Returns
        -------
        bool
        """
        zarray_fspath: AnyPath = self.url / path / ".zarray"
        return zarray_fspath.exists()

    def _is_valid_zarr(self, path: str, has_extension: bool = True) -> bool:
        """
        Test if the subpath of self.url is a valid url
        Parameters
        ----------
        path
        has_extension

        Returns
        -------

        """
        zarr_path = (
            (self.url / path)
            if not has_extension or path.endswith(self.EXTENSION)
            else (self.url / path + self.EXTENSION)
        )
        if not zarr_path.exists():
            return False
        try:
            ds = open_zarr(zarr_path.to_zarr_store(), consolidated=True, **self._read_zarr_kwargs)
            ds.close()
        except GroupNotFoundError:
            return False
        return True

    def is_group(self, path: str) -> bool:
        """
        Check if it is an EOGroup path

        Parameters
        ----------
        path: Path
            path inside the product

        Returns
        -------
        bool
        """
        self.check_is_opened()

        if self._mode != OpeningMode.OPEN:
            self.LOGGER.warning(
                f"Functionality available only in mode: {OpeningMode.OPEN} not it current mode: {self._mode}",
                EOZarrStoreWarning,
            )
            return False

        return self._zgroup_exists(path)

    def is_variable(self, path: str) -> bool:
        """
        Check if is an EOVariable path

        Parameters
        ----------
        path: Path
            path inside the product

        Returns
        -------
        bool
        """
        self.check_is_opened()

        if self._mode != OpeningMode.OPEN:
            self.LOGGER.warning(
                f"Functionality available only in mode: {OpeningMode.OPEN} not it current mode: {self._mode}",
                EOZarrStoreWarning,
            )
            return False

        return not self._zgroup_exists(path) and self._zarray_exists(path)

    def is_product(self, path: str, has_extension: bool = True) -> bool:
        """Check if the given path under root corresponding to a product representation

        Parameters
        ----------
        path: str
            path to check, either with the extension or not

        Returns
        -------
        bool
            it is a product representation or not

        Raises
        ------
        StoreNotOpenError
            If the store is closed
        """
        # For now we only check that it is a valid zarr
        return self._is_valid_zarr(path, has_extension)

    def is_container(self, path: str, has_extension: bool = True) -> bool:
        zarr_path = (
            (self.url / path)
            if not has_extension or path.endswith(self.EXTENSION)
            else (self.url / path + self.EXTENSION)
        )
        try:
            ds = open_zarr(zarr_path.to_zarr_store(), consolidated=True, **self._read_zarr_kwargs)
        except GroupNotFoundError:
            return False
        is_container = EOContainer.is_container(ds)
        ds.close()
        return is_container

    # docstr-coverage: inherited
    def iter(self, path: str = "") -> Iterator[str]:
        self.check_is_opened()
        for d in self.url.glob("*" + self.EXTENSION):
            yield os.path.splitext(d.basename)[0]

    # docstr-coverage: inherited
    def write_attrs(self, group_path: str, attrs: MutableMapping[str, Any]) -> None:
        """No functionality"""
        return super().write_attrs(group_path, attrs)

    # docstr-coverage: inherited
    def __len__(self) -> int:
        self.check_is_opened()
        """No functionality"""
        return super().__len__()

    @staticmethod
    def guess_can_read(file_path: str | AnyPath, **kwargs: Any) -> bool:
        """The given file path is readable or not by this store

        Parameters
        ----------
        file_path: str
            File path to check
        kwargs:
            storage_options: dict arguments for AnyPath

        Returns
        -------
        bool
        """
        url: AnyPath = AnyPath.cast(file_path, **kwargs.get("storage_options", {}))
        return url.path.endswith((EOZarrStore.EXTENSION, EOZarrStore.EXTENSION + ".zip"))

    @staticmethod
    def is_valid_url(file_path: str | AnyPath, **kwargs: Any) -> bool:
        """
        Test if the file_path exists

        Parameters
        ----------
        file_path : path to test

        Returns
        -------
        yes or not the path is a valid filename. Default all invalid

        """
        path_obj: AnyPath = AnyPath.cast(file_path, **kwargs.get("storage_options", {}))
        # Special case when directly providing a ZarrStore
        if path_obj.basename == "zarr.storage.Store":
            return True
        # special case when reading with kerchunk ( netcdfAccessor )
        if path_obj.protocol == "reference":
            return True

        return path_obj.exists()
