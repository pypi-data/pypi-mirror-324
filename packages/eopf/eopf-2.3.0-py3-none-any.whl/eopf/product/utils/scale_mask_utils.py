from typing import Any, Optional

import dask.array as da
import numpy as np
from xarray import DataArray

from eopf.exceptions.errors import MaskingError, ScalingError


def mask_array(
    data: da.Array,
    valid_min: Optional[np.number[Any]],
    valid_max: Optional[np.number[Any]],
    fill_value: Optional[np.number[Any]],
) -> da.Array:
    """
    Mask a dask array

    Parameters
    ----------
    data : da.Array
        dask array to mask
    valid_min : Optional[np.number[Any]]
        valid minimum value
    valid_max : Optional[np.number[Any]]
        valid maximum value
    fill_value : Optional[np.number[Any]]
        fill value

    Returns
    -------
    da.Array
    """

    try:
        # data may be already masked but not marked as masked
        mask = da.logical_or(False, data == fill_value)

        if valid_min is not None:
            mask = da.logical_or(mask, data < valid_min)
        if valid_max is not None:
            mask = da.logical_or(mask, data > valid_max)

        return da.ma.masked_array(data, mask, fill_value=fill_value)
    except Exception as e:
        raise MaskingError(f"{e}")


def scale_dask_array(
    data: da.Array,
    scale_factor: Optional[np.number[Any]],
    add_offset: Optional[np.number[Any]],
    target_dtype: Optional[np.dtype[Any]],
) -> da.Array:
    """
    Scale and/or offset a dask array

    Parameters
    ----------
    data : da.Array
        dask array to mask
    scale_factor : Optional[np.number[Any]]
        valid minimum value
    add_offset : Optional[np.number[Any]]
        valid maximum value
    target_dtype: Optional[np.dtype[Any]]
        force dtype after scaling/offsetting

    Returns
    -------
    da.Array
    """

    try:
        # the data mask is needed to avoid scalling masked data
        if isinstance(data._meta, np.ma.core.MaskedArray):
            data_mask = da.ma.getmaskarray(data)
        else:
            data_mask = False

        # apply scale factor if present
        if scale_factor is not None:  # for these 0 is also ignored
            data = da.multiply(data, scale_factor, where=data_mask == False)  # noqa: E712

        # apply offset if present
        if add_offset is not None:
            data = da.add(data, add_offset, where=data_mask == False)  # noqa: E712

        # make sure the scaled data has the target_dtype if present
        if target_dtype is not None:
            data = data.astype(target_dtype)

        return data
    except Exception as e:
        raise ScalingError(f"{e}")


def scale_numpy_array(
    data: DataArray,
    scale_factor: Optional[np.number[Any]],
    add_offset: Optional[np.number[Any]],
    target_dtype: Optional[np.dtype[Any]],
) -> DataArray:
    """
    Scale and/or offset a numpy array

    Parameters
    ----------
    data : da.Array
        dask array to mask
    scale_factor : Optional[np.number[Any]]
        valid minimum value
    add_offset : Optional[np.number[Any]]
        valid maximum value
    target_dtype: Optional[np.dtype[Any]]
        force dtype after scaling/offsetting

    Returns
    -------
    da.Array
    """

    try:
        # the data mask is needed to avoid scalling masked data
        if isinstance(data, np.ma.core.MaskedArray):
            data_mask = data.mask
        else:
            data_mask = False

        # apply scale factor if present
        if scale_factor is not None:  # for these 0 is also ignored
            data = DataArray(np.multiply(data, scale_factor, where=data_mask == False))  # noqa: E712

        # apply offset if present
        if add_offset is not None:
            data = DataArray(np.add(data, add_offset, where=data_mask == False))  # noqa: E712

        # make sure the scaled data has the target_dtype if present
        if target_dtype is not None:
            data = data.astype(target_dtype)

        return data
    except Exception as e:
        raise ScalingError(f"{e}")


def scale_val(
    val: np.number[Any],
    scale_factor: Optional[np.number[Any]],
    add_offset: Optional[np.number[Any]],
    target_dtype: Optional[np.dtype[Any]],
) -> np.number[Any]:
    """
    Scale and/or offset a numpy number

    Parameters
    ----------
    data : da.Array
        dask array to mask
    scale_factor : Optional[np.number[Any]]
        valid minimum value
    add_offset : Optional[np.number[Any]]
        valid maximum value
    target_dtype: Optional[np.dtype[Any]]
        force dtype after scaling/offsetting

    Returns
    -------
    np.number[Any]
    """

    try:
        # apply scale factor if present
        if scale_factor is not None:  # for these 0 is also ignored
            val = np.multiply(val, scale_factor)

        # apply offset if present
        if add_offset is not None:
            val = np.add(val, add_offset)

        # make sure the scaled val has the target_dtype if present
        if target_dtype is not None:
            val = np.dtype(target_dtype).type(val)

        return val
    except Exception as e:
        raise ScalingError(f"{e}")


def unscale_array(
    data: da.Array,
    scale_factor: Optional[np.number[Any]],
    add_offset: Optional[np.number[Any]],
    target_dtype: Optional[np.dtype[Any]],
) -> da.Array:
    """
    Un-scale and/or un-offset a dask array

    Parameters
    ----------
    data : da.Array
        dask array to mask
    scale_factor : Optional[np.number[Any]]
        valid minimum value
    add_offset : Optional[np.number[Any]]
        valid maximum value
    target_dtype: Optional[np.dnp.dtype[Any]]
        force dtype after un-scaling/un-offsetting

    Returns
    -------
    da.Array
    """

    try:
        # the data mask is needed to avoid unscalling masked data
        if isinstance(data._meta, np.ma.core.MaskedArray):
            data_mask = da.ma.getmaskarray(data)
        else:
            data_mask = False

        # unapply offset if present
        if add_offset is not None:
            data = da.subtract(data, add_offset, where=data_mask == False)  # noqa: E712

        # unapply scale factor if present
        if scale_factor is not None:  # for these 0 is also ignored
            data = da.divide(data, scale_factor, where=data_mask == False)  # noqa: E712

        # make sure the unscaled data has the target_dtype if present
        if target_dtype is not None:
            data = data.astype(target_dtype)

        return data
    except Exception as e:
        raise ScalingError(f"{e}")


def unscale_val(
    val: np.number[Any],
    scale_factor: Optional[np.number[Any]],
    add_offset: Optional[np.number[Any]],
    target_dtype: Optional[np.dtype[Any]],
) -> np.number[Any]:
    """
    Scale and/or offset a numpy number

    Parameters
    ----------
    data : da.Array
        dask array to mask
    scale_factor : Optional[np.number[Any]]
        valid minimum value
    add_offset : Optional[np.number[Any]]
        valid maximum value
    target_dtype: Optional[np.dtype[Any]]
        force dtype after scaling/offsetting

    Returns
    -------
    np.number[Any]
    """

    try:
        # apply offset if present
        if add_offset is not None:
            val = np.subtract(val, add_offset)

        # apply scale factor if present
        if scale_factor is not None:  # for these 0 is also ignored
            val = np.divide(val, scale_factor)

        # make sure the unscaled val has the target_dtype if present
        if target_dtype is not None:
            val = np.dtype(target_dtype).type(val)

        return val
    except Exception as e:
        raise ScalingError(f"{e}")
