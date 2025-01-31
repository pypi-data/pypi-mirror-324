import contextlib
from typing import TYPE_CHECKING, Any, Optional, Union

from distributed import get_client

from eopf.common.constants import OpeningMode
from eopf.common.file_utils import AnyPath
from eopf.config import EOConfiguration
from eopf.daskconfig import init_from_eo_configuration
from eopf.exceptions.errors import EOStoreFactoryNoRegisteredStoreError
from eopf.logging import EOLogging
from eopf.product import EOProduct
from eopf.store import EOProductStore
from eopf.store.store_factory import EOStoreFactory
from eopf.store.zarr import ZARR_PRODUCT_FORMAT

EOConfiguration().register_requested_parameter("store__convert__use_multithreading", True, True)

if TYPE_CHECKING:  # pragma: no cover
    from eopf.daskconfig.dask_context_manager import DaskContext


def convert(
    source_path: AnyPath | str,
    target_path: AnyPath | str,
    target_format: str = ZARR_PRODUCT_FORMAT,
    mask_and_scale: Optional[bool] = None,
    source_store_kwargs: dict[str, Any] = {},
    target_store_kwargs: dict[str, Any] = {},
) -> None:
    """
    Converts a product from one format to another

    Parameters
    ----------
    source_path: AnyPath|str
        file system path to an existing product
    source_path: AnyPath|str
        file system path to where we want the converted to be written
    target_format: EOProductFormat
        format in which the source product will be converted
    mask_and_scale: Optional[bool] = None
        apply or not masking and scaling by overridding EOConfiguration
    source_store_kwargs: dict[str, Any] = {}
        kwargs of the source store
    target_store_kwargs: dict[str, Any] = {}
        kwargs of the source store

    Raises
    -------
    EOStoreFactoryNoRegisteredStoreError

    Returns
    -------
    None
    """
    LOGGER = EOLogging().get_logger("eopf.store.convert")
    source_store_class: Optional[type[EOProductStore]] = None
    target_store_class: Optional[type[EOProductStore]] = None
    source_store: Optional[EOProductStore] = None
    target_store: Optional[EOProductStore] = None
    output_dir: AnyPath
    product_name: str

    eopf_config = EOConfiguration()

    if mask_and_scale is None:
        mask_and_scale = eopf_config.get("product__mask_and_scale")

    source_fspath: AnyPath = AnyPath.cast(url=source_path, kwargs=source_store_kwargs)
    target_fspath: AnyPath = AnyPath.cast(url=target_path, kwargs=target_store_kwargs)

    # determine the source store
    source_store_class = EOStoreFactory.get_product_store_by_file(source_fspath)

    # determine the target store
    try:
        # when the user specifies the name of the product
        target_store_class = EOStoreFactory.get_product_store_by_file(target_fspath)
        output_dir = target_fspath.dirname()
        product_name = target_fspath.basename

    except EOStoreFactoryNoRegisteredStoreError as err:
        # when the user gives the directory where the product should be written
        # and the name is automatically computed as per EOProduct rules
        output_dir = target_fspath
        product_name = ""
        if output_dir.isdir():
            for format, store_class in EOStoreFactory.product_formats.items():
                # iterate over each registed store and check if the target_format matches
                if target_format == format:
                    target_store_class = store_class

        # raise EOStoreFactoryNoRegisteredStoreError when no store could be retrieved
        if target_store_class is None:
            raise err

    # Check if a dask client is already available, if not instanciate default
    dask_context_manager: Union[Any, DaskContext] = contextlib.nullcontext()
    if eopf_config.store__convert__use_multithreading:
        LOGGER.info("MultiThread Convert enabled")
        try:
            client = get_client()
            if client is None:
                # default to multithread local cluster
                dask_context_manager = init_from_eo_configuration()
        except Exception:
            # no client ? # default to EOConfigured one
            dask_context_manager = init_from_eo_configuration()

    with dask_context_manager:
        LOGGER.debug(f"Converting {source_fspath.path} to {target_fspath.path}")
        LOGGER.debug(f"Using dask context {dask_context_manager}")

        # when creating the eop the data should be kept as on disk
        if "eov_kwargs" not in source_store_kwargs:
            source_store_kwargs["source_store_kwargs"] = {"mask_and_scale": False}

        # load the EOProduct from source_path
        source_store = source_store_class(source_fspath, mask_and_scale=mask_and_scale, **source_store_kwargs)
        source_store.open()
        eop: EOProduct = source_store.load()
        source_store.close()

        LOGGER.info(f"EOproduct {eop} succesfully loaded, starting to write")

        # when writing the eop the data should be kept as on disk
        if "eov_kwargs" not in target_store_kwargs:
            source_store_kwargs["source_store_kwargs"] = {"mask_and_scale": False}

        # write the EOProduct with the target_store at the target_path
        target_store = target_store_class(output_dir, mask_and_scale=mask_and_scale, **target_store_kwargs)
        target_store.open(mode=OpeningMode.CREATE_OVERWRITE)
        target_store[product_name] = eop
        target_store.close()

        LOGGER.info("Conversion finished")
