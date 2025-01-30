"""Module for concatenating netCDF files."""

import logging
import shutil
from collections.abc import Iterable
from os import PathLike
from pathlib import Path
from typing import Literal

import netCDF4
import numpy as np

from cloudnetpy import utils
from cloudnetpy.exceptions import InconsistentDataError


def truncate_netcdf_file(
    filename: str, output_file: str, n_profiles: int, dim_name: str = "time"
) -> None:
    """Truncates netcdf file in dim_name dimension taking only n_profiles.
    Useful for creating small files for tests.
    """
    with (
        netCDF4.Dataset(filename, "r") as nc,
        netCDF4.Dataset(output_file, "w", format=nc.data_model) as nc_new,
    ):
        for dim in nc.dimensions:
            dim_len = None if dim == dim_name else nc.dimensions[dim].size
            nc_new.createDimension(dim, dim_len)
        for attr in nc.ncattrs():
            value = getattr(nc, attr)
            setattr(nc_new, attr, value)
        for key in nc.variables:
            array = nc.variables[key][:]
            dimensions = nc.variables[key].dimensions
            fill_value = getattr(nc.variables[key], "_FillValue", None)
            var = nc_new.createVariable(
                key,
                array.dtype,
                dimensions,
                zlib=True,
                fill_value=fill_value,
            )
            if dimensions and dim_name in dimensions[0]:
                if array.ndim == 1:
                    var[:] = array[:n_profiles]
                if array.ndim == 2:
                    var[:] = array[:n_profiles, :]
            else:
                var[:] = array
            for attr in nc.variables[key].ncattrs():
                if attr != "_FillValue":
                    value = getattr(nc.variables[key], attr)
                    setattr(var, attr, value)


def update_nc(old_file: str, new_file: str) -> int:
    """Appends data to existing netCDF file.

    Args:
        old_file: Filename of an existing netCDF file.
        new_file: Filename of a new file whose data will be appended to the end.

    Returns:
        1 = success, 0 = failed to add new data.

    Notes:
        Requires 'time' variable with unlimited dimension.

    """
    try:
        with (
            netCDF4.Dataset(old_file, "a") as nc_old,
            netCDF4.Dataset(new_file) as nc_new,
        ):
            valid_ind = _find_valid_time_indices(nc_old, nc_new)
            if len(valid_ind) > 0:
                _update_fields(nc_old, nc_new, valid_ind)
                return 1
            return 0
    except OSError:
        return 0


def concatenate_files(
    filenames: Iterable[PathLike | str],
    output_file: str,
    concat_dimension: str = "time",
    variables: list | None = None,
    new_attributes: dict | None = None,
    ignore: list | None = None,
    allow_difference: list | None = None,
) -> list:
    """Concatenate netCDF files in one dimension.

    Args:
        filenames: List of files to be concatenated.
        output_file: Output file name.
        concat_dimension: Dimension name for concatenation. Default is 'time'.
        variables: List of variables with the 'concat_dimension' to be concatenated.
            Default is None when all variables with 'concat_dimension' will be saved.
        new_attributes: Optional new global attributes as {'attribute_name': value}.
        ignore: List of variables to be ignored.
        allow_difference: Names of scalar variables that can differ from one file to
            another (value from the first file is saved).

    Returns:
        List of filenames that were successfully concatenated.

    Notes:
        Arrays without 'concat_dimension', scalars, and global attributes will be taken
        from the first file. Groups, possibly present in a NETCDF4 formatted file,
        are ignored.

    """
    with _Concat(filenames, output_file, concat_dimension) as concat:
        concat.get_common_variables()
        concat.create_global_attributes(new_attributes)
        return concat.concat_data(variables, ignore, allow_difference)


class _Concat:
    common_variables: set[str]

    def __init__(
        self,
        filenames: Iterable[PathLike | str],
        output_file: str,
        concat_dimension: str = "time",
    ):
        self.filenames = sorted(map(Path, filenames), key=lambda f: f.name)
        self.concat_dimension = concat_dimension
        self.first_filename = self.filenames[0]
        self.first_file = netCDF4.Dataset(self.first_filename)
        self.concatenated_file = self._init_output_file(output_file)
        self.common_variables = set()

    def get_common_variables(self) -> None:
        """Finds variables which should have the same values in all files."""
        for key, value in self.first_file.variables.items():
            if self.concat_dimension not in value.dimensions:
                self.common_variables.add(key)

    def create_global_attributes(self, new_attributes: dict | None) -> None:
        """Copies global attributes from one of the source files."""
        _copy_attributes(self.first_file, self.concatenated_file)
        if new_attributes is not None:
            for key, value in new_attributes.items():
                setattr(self.concatenated_file, key, value)

    def concat_data(
        self,
        variables: list | None,
        ignore: list | None,
        allow_vary: list | None,
    ) -> list:
        """Concatenates data arrays."""
        self._write_initial_data(variables, ignore)
        output = [self.first_filename]
        if len(self.filenames) > 1:
            for filename in self.filenames[1:]:
                try:
                    self._append_data(filename, allow_vary)
                except RuntimeError as e:
                    if "NetCDF: HDF error" in str(e):
                        msg = f"Caught a NetCDF HDF error. Skipping file '{filename}'."
                        logging.exception(msg)
                        continue
                    raise
                output.append(filename)
        return output

    def _write_initial_data(self, variables: list | None, ignore: list | None) -> None:
        for key in self.first_file.variables:
            if (
                variables is not None
                and key not in variables
                and key not in self.common_variables
                and key != self.concat_dimension
            ):
                continue
            if ignore and key in ignore:
                continue

            auto_scale = False
            self.first_file[key].set_auto_scale(auto_scale)
            array = self.first_file[key][:]
            dimensions = self.first_file[key].dimensions
            fill_value = getattr(self.first_file[key], "_FillValue", None)
            var = self.concatenated_file.createVariable(
                key,
                array.dtype,
                dimensions,
                zlib=True,
                complevel=3,
                shuffle=False,
                fill_value=fill_value,
            )
            auto_scale = False
            var.set_auto_scale(auto_scale)
            var[:] = array
            _copy_attributes(self.first_file[key], var)

    def _append_data(self, filename: str | PathLike, allow_vary: list | None) -> None:
        with netCDF4.Dataset(filename) as file:
            auto_scale = False
            file.set_auto_scale(auto_scale)
            ind0 = len(self.concatenated_file.variables[self.concat_dimension])
            ind1 = ind0 + len(file.variables[self.concat_dimension])
            for key in self.concatenated_file.variables:
                if key not in file.variables:
                    continue
                array = file[key][:]
                if key in self.common_variables:
                    if allow_vary is not None and key in allow_vary:
                        continue
                    if not np.array_equal(self.first_file[key][:], array):
                        msg = (
                            f"Inconsistent values in variable '{key}' between "
                            f"files '{self.first_filename}' and '{filename}'"
                        )
                        raise InconsistentDataError(msg)
                    continue
                if array.ndim == 0:
                    continue
                if array.ndim == 1:
                    self.concatenated_file.variables[key][ind0:ind1] = array
                else:
                    self.concatenated_file.variables[key][ind0:ind1, :] = array

    def _init_output_file(self, output_file: str) -> netCDF4.Dataset:
        data_model: Literal["NETCDF4", "NETCDF4_CLASSIC"] = (
            "NETCDF4" if self.first_file.data_model == "NETCDF4" else "NETCDF4_CLASSIC"
        )
        nc = netCDF4.Dataset(output_file, "w", format=data_model)
        for dim in self.first_file.dimensions:
            dim_len = (
                None
                if dim == self.concat_dimension
                else self.first_file.dimensions[dim].size
            )
            nc.createDimension(dim, dim_len)
        return nc

    def _close(self) -> None:
        self.first_file.close()
        self.concatenated_file.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()


def _copy_attributes(
    source: netCDF4.Dataset | netCDF4.Variable,
    target: netCDF4.Dataset | netCDF4.Variable,
) -> None:
    for attr in source.ncattrs():
        if attr != "_FillValue":
            value = getattr(source, attr)
            setattr(target, attr, value)


def _find_valid_time_indices(
    nc_old: netCDF4.Dataset,
    nc_new: netCDF4.Dataset,
) -> np.ndarray:
    return np.where(nc_new.variables["time"][:] > nc_old.variables["time"][-1])[0]


def _update_fields(
    nc_old: netCDF4.Dataset,
    nc_new: netCDF4.Dataset,
    valid_ind: np.ndarray,
) -> None:
    ind0 = len(nc_old.variables["time"])
    idx = [ind0 + x for x in valid_ind]
    concat_dimension = nc_old.variables["time"].dimensions[0]
    for field in nc_new.variables:
        if field not in nc_old.variables:
            continue
        dimensions = nc_new.variables[field].dimensions
        if concat_dimension in dimensions:
            concat_ind = dimensions.index(concat_dimension)
            if len(dimensions) == 1:
                nc_old.variables[field][idx] = nc_new.variables[field][valid_ind]
            elif len(dimensions) == 2 and concat_ind == 0:
                nc_old.variables[field][idx, :] = nc_new.variables[field][valid_ind, :]
            elif len(dimensions) == 2 and concat_ind == 1:
                nc_old.variables[field][:, idx] = nc_new.variables[field][:, valid_ind]


def concatenate_text_files(filenames: list, output_filename: str | PathLike) -> None:
    """Concatenates text files."""
    with open(output_filename, "wb") as target:
        for filename in filenames:
            with open(filename, "rb") as source:
                shutil.copyfileobj(source, target)


def bundle_netcdf_files(
    files: list,
    date: str,
    output_file: str,
    concat_dimensions: tuple[str, ...] = ("time", "profile"),
    variables: list | None = None,
) -> list:
    """Concatenates several netcdf files into daily file with
    some extra data manipulation.
    """
    with netCDF4.Dataset(files[0]) as nc:
        concat_dimension = None
        for key in concat_dimensions:
            if key in nc.dimensions:
                concat_dimension = key
                break
        if concat_dimension is None:
            msg = f"Dimension '{concat_dimensions}' not found in the files."
            raise KeyError(msg)
    if len(files) == 1:
        shutil.copy(files[0], output_file)
        return files
    valid_files = []
    for file in files:
        try:
            with netCDF4.Dataset(file) as nc:
                time = nc.variables["time"]
                time_array = time[:]
                time_units = time.units
        except OSError:
            continue
        epoch = utils.get_epoch(time_units)
        for timestamp in time_array:
            if utils.seconds2date(timestamp, epoch)[:3] == date.split("-"):
                valid_files.append(file)
                break
    concatenate_files(
        valid_files,
        output_file,
        concat_dimension=concat_dimension,
        variables=variables,
        ignore=[
            "minimum",
            "maximum",
            "number_integrated_samples",
            "Min_LWP",
            "Max_LWP",
        ],
    )
    return valid_files
