#!/usr/bin/env python
# coding=utf-8
"""
Author: Liu Kun && 16031215@qq.com
Date: 2024-09-17 14:58:50
LastEditors: Liu Kun && 16031215@qq.com
LastEditTime: 2024-12-06 14:16:56
FilePath: \\Python\\My_Funcs\\OAFuncs\\oafuncs\\oa_nc.py
Description:
EditPlatform: vscode
ComputerInfo: XPS 15 9510
SystemInfo: Windows 11
Python Version: 3.11
"""

import os

import netCDF4 as nc
import numpy as np
import xarray as xr
from rich import print

__all__ = ["get_var", "extract", "save", "merge", "modify", "rename", "check", "convert_longitude", "isel"]


def get_var(file, *vars):
    """
    Description:
        Read variables from nc file
    Parameters:
        file: str, file path
        *vars: str, variable name or variable names; should be in same size
    Example:
        datas = get_var(file_ecm, 'h', 't', 'u', 'v')
    Return:
        datas: list, variable data
    """
    ds = xr.open_dataset(file)
    datas = []
    for var in vars:
        data = ds[var]
        datas.append(data)
    ds.close()
    return datas


def extract(file, varname, only_value=True):
    """
    Description:
        Extract variables from nc file
        Return the variable and coordinate dictionary
    Parameters:
        file: str, file path
        varname: str, variable name
        only_value: bool, whether to keep only the value of the variable and dimension
    Example:
        data, dimdict = extract('test.nc', 'h')
    """
    ds = xr.open_dataset(file)
    vardata = ds[varname]
    ds.close()
    dims = vardata.dims
    dimdict = {}
    for dim in dims:
        if only_value:
            dimdict[dim] = vardata[dim].values
        else:
            dimdict[dim] = ds[dim]
    if only_value:
        vardata = np.array(vardata)
    return vardata, dimdict


def _numpy_to_nc_type(numpy_type):
    """将NumPy数据类型映射到NetCDF数据类型"""
    numpy_to_nc = {
        "float32": "f4",
        "float64": "f8",
        "int8": "i1",
        "int16": "i2",
        "int32": "i4",
        "int64": "i8",
        "uint8": "u1",
        "uint16": "u2",
        "uint32": "u4",
        "uint64": "u8",
    }
    # 确保传入的是字符串类型，如果不是，则转换为字符串
    numpy_type_str = str(numpy_type) if not isinstance(numpy_type, str) else numpy_type
    return numpy_to_nc.get(numpy_type_str, "f4")  # 默认使用 'float32'


def _calculate_scale_and_offset(data, n=16):
    if not isinstance(data, np.ndarray):
        raise ValueError("Input data must be a NumPy array.")

    # 使用 nan_to_num 来避免 NaN 值对 min 和 max 的影响
    data_min = np.nanmin(data)
    data_max = np.nanmax(data)

    if np.isnan(data_min) or np.isnan(data_max):
        raise ValueError("Input data contains NaN values, which are not allowed.")

    scale_factor = (data_max - data_min) / (2**n - 1)
    add_offset = data_min + 2 ** (n - 1) * scale_factor

    return scale_factor, add_offset


def save(file, data, varname=None, coords=None, mode="w", scale_offset_switch=True, compile_switch=True):
    """
    Description:
        Write data to NetCDF file
    Parameters:
        file: str, file path
        data: data
        varname: str, variable name
        coords: dict, coordinates, key is the dimension name, value is the coordinate data
        mode: str, write mode, 'w' for write, 'a' for append
        scale_offset_switch: bool, whether to use scale_factor and add_offset, default is True
        compile_switch: bool, whether to use compression parameters, default is True
    Example:
        save(r'test.nc', data, 'u', {'time': np.linspace(0, 120, 100), 'lev': np.linspace(0, 120, 50)}, 'a')
    """
    # 设置压缩参数
    kwargs = {"zlib": True, "complevel": 4} if compile_switch else {}

    # 检查文件存在性并根据模式决定操作
    if mode == "w" and os.path.exists(file):
        os.remove(file)
    elif mode == "a" and not os.path.exists(file):
        mode = "w"

    # 打开 NetCDF 文件
    with nc.Dataset(file, mode, format="NETCDF4") as ncfile:
        # 如果 data 是 DataArray 并且没有提供 varname 和 coords
        if varname is None and coords is None and isinstance(data, xr.DataArray):
            data.to_netcdf(file, mode=mode)
            return

        # 添加坐标
        for dim, coord_data in coords.items():
            if dim in ncfile.dimensions:
                if len(coord_data) != len(ncfile.dimensions[dim]):
                    raise ValueError(f"Length of coordinate '{dim}' does not match the dimension length.")
                else:
                    ncfile.variables[dim][:] = np.array(coord_data)
            else:
                ncfile.createDimension(dim, len(coord_data))
                var = ncfile.createVariable(dim, _numpy_to_nc_type(coord_data.dtype), (dim,), **kwargs)
                var[:] = np.array(coord_data)

                # 如果坐标数据有属性，则添加到 NetCDF 变量
                if isinstance(coord_data, xr.DataArray) and coord_data.attrs:
                    for attr_name, attr_value in coord_data.attrs.items():
                        var.setncattr(attr_name, attr_value)

        # 添加或更新变量
        if varname in ncfile.variables:
            if data.shape != ncfile.variables[varname].shape:
                raise ValueError(f"Shape of data does not match the variable shape for '{varname}'.")
            ncfile.variables[varname][:] = np.array(data)
        else:
            # 创建变量
            dim_names = tuple(coords.keys())
            if scale_offset_switch:
                scale_factor, add_offset = _calculate_scale_and_offset(np.array(data))
                dtype = "i2"
                var = ncfile.createVariable(varname, dtype, dim_names, fill_value=-32767, **kwargs)
                var.setncattr("scale_factor", scale_factor)
                var.setncattr("add_offset", add_offset)
            else:
                dtype = _numpy_to_nc_type(data.dtype)
                var = ncfile.createVariable(varname, dtype, dim_names, **kwargs)
            var[:] = np.array(data)

        # 添加属性
        if isinstance(data, xr.DataArray) and data.attrs:
            for key, value in data.attrs.items():
                if key not in ["scale_factor", "add_offset", "_FillValue", "missing_value"] or not scale_offset_switch:
                    var.setncattr(key, value)


def merge(file_list, var_name=None, dim_name=None, target_filename=None):
    """
    Description:
        Merge variables from multiple NetCDF files along a specified dimension and write to a new file.
        If var_name is a string, it is considered a single variable; if it is a list and has only one element, it is also a single variable;
        If the list has more than one element, it is a multi-variable; if var_name is None, all variables are merged.
        
    Parameters:
        file_list: List of NetCDF file paths
        var_name: Name of the variable to be extracted or a list of variable names, default is None, which means all variables are extracted
        dim_name: Dimension name used for merging
        target_filename: Target file name after merging
        
    Example:
        merge(file_list, var_name='u', dim_name='time', target_filename='merged.nc')
        merge(file_list, var_name=['u', 'v'], dim_name='time', target_filename='merged.nc')
        merge(file_list, var_name=None, dim_name='time', target_filename='merged.nc')
    """
    # 看看保存文件是单纯文件名还是包含路径的，如果有路径，需要确保路径存在
    if target_filename is None:
        target_filename = "merged.nc"
    if not os.path.exists(os.path.dirname(str(target_filename))):
        os.makedirs(os.path.dirname(str(target_filename)))
    
    if isinstance(file_list, str):
        file_list = [file_list]
    
    # 初始化变量名列表
    var_names = None

    # 判断 var_name 是单变量、多变量还是合并所有变量
    if var_name is None:
        # 获取第一个文件中的所有变量名
        ds = xr.open_dataset(file_list[0])
        var_names = list(ds.variables.keys())
        ds.close()
    elif isinstance(var_name, str):
        var_names = [var_name]
    elif isinstance(var_name, list):
        var_names = var_name
    else:
        raise ValueError("var_name must be a string, a list of strings, or None")

    # 初始化合并数据字典
    merged_data = {}

    # 遍历文件列表
    print('Reading file ...')
    for i, file in enumerate(file_list):
        # 更新track描述进度
        # print(f"\rReading file {i + 1}/{len(file_list)}...", end="")
        ds = xr.open_dataset(file)
        for var_name in var_names:
            var = ds[var_name]
            # 如果变量包含合并维度，则合并它们
            if dim_name in var.dims:
                if var_name not in merged_data:
                    merged_data[var_name] = [var]
                else:
                    merged_data[var_name].append(var)
            # 如果变量不包含合并维度，则仅保留第一个文件中的值
            else:
                if var_name not in merged_data:
                    merged_data[var_name] = var
        ds.close()

    print("\nMerging data ...")
    for var_name in merged_data:
        if isinstance(merged_data[var_name], list):
            merged_data[var_name] = xr.concat(merged_data[var_name], dim=dim_name)

    merged_data = xr.Dataset(merged_data)

    print("Writing data to file ...")
    if os.path.exists(target_filename):
        print("Warning: The target file already exists.")
        print("Removing existing file ...")
        os.remove(target_filename)
    merged_data.to_netcdf(target_filename)
    print(f'File "{target_filename}" has been created.')


def _modify_var(nc_file_path, variable_name, new_value):
    """    
    Description:
        Modify the value of a variable in a NetCDF file using the netCDF4 library.
        
    Parameters:
        nc_file_path (str): The path to the NetCDF file.
        variable_name (str): The name of the variable to be modified.
        new_value (numpy.ndarray): The new value of the variable.
        
    Example:
        modify_var('test.nc', 'u', np.random.rand(100, 50))
    """
    try:
        # Open the NetCDF file
        dataset = nc.Dataset(nc_file_path, "r+")
        # Get the variable to be modified
        variable = dataset.variables[variable_name]
        # Modify the value of the variable
        variable[:] = new_value
        dataset.close()
        print(f"Successfully modified variable {variable_name} in {nc_file_path}.")
    except Exception as e:
        print(f"An error occurred while modifying variable {variable_name} in {nc_file_path}: {e}")


def _modify_attr(nc_file_path, variable_name, attribute_name, attribute_value):
    """   
    Description:
        Add or modify an attribute of a variable in a NetCDF file using the netCDF4 library.
        
    Parameters:
        nc_file_path (str): The path to the NetCDF file.
        variable_name (str): The name of the variable to be modified.
        attribute_name (str): The name of the attribute to be added or modified.
        attribute_value (any): The value of the attribute.
        
    Example:
        modify_attr('test.nc', 'temperature', 'long_name', 'Temperature in Celsius')
    """
    try:
        ds = nc.Dataset(nc_file_path, "r+")
        if variable_name not in ds.variables:
            raise ValueError(f"Variable '{variable_name}' not found in the NetCDF file.")

        variable = ds.variables[variable_name]
        if attribute_name in variable.ncattrs():
            print(f"Warning: Attribute '{attribute_name}' already exists. Replacing it.")
            variable.setncattr(attribute_name, attribute_value)
        else:
            print(f"Adding attribute '{attribute_name}'...")
            variable.setncattr(attribute_name, attribute_value)

        ds.close()
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")


def modify(nc_file,var_name,attr_name=None,new_value=None):
    """
    Description:
        Modify the value of a variable or the value of an attribute in a NetCDF file.
        
    Parameters:
        nc_file (str): The path to the NetCDF file.
        var_name (str): The name of the variable to be modified.
        attr_name (str): The name of the attribute to be modified. If None, the variable value will be modified.
        new_value (any): The new value of the variable or attribute.
        
    Example:
        modify('test.nc', 'temperature', 'long_name', 'Temperature in Celsius')
        modify('test.nc', 'temperature', None, np.random.rand(100, 50))
    """
    if attr_name is None:
        _modify_var(nc_file, var_name, new_value)
    else:
        _modify_attr(nc_file, var_name, attr_name, new_value)


def rename(ncfile_path, old_name, new_name):
    """
    Description:
        Rename a variable and/or dimension in a NetCDF file.

    Parameters:
        ncfile_path (str): The path to the NetCDF file.
        old_name (str): The current name of the variable or dimension.
        new_name (str): The new name to assign to the variable or dimension.

    example:
        rename('test.nc', 'temperature', 'temp')
    """
    try:
        with nc.Dataset(ncfile_path, "r+") as dataset:
            # If the old name is not found as a variable or dimension, print a message
            if old_name not in dataset.variables and old_name not in dataset.dimensions:
                print(f"Variable or dimension {old_name} not found in the file.")

            # Attempt to rename the variable
            if old_name in dataset.variables:
                dataset.renameVariable(old_name, new_name)
                print(f"Successfully renamed variable {old_name} to {new_name}.")

            # Attempt to rename the dimension
            if old_name in dataset.dimensions:
                # Check if the new dimension name already exists
                if new_name in dataset.dimensions:
                    raise ValueError(f"Dimension name {new_name} already exists in the file.")
                dataset.renameDimension(old_name, new_name)
                print(f"Successfully renamed dimension {old_name} to {new_name}.")

    except Exception as e:
        print(f"An error occurred: {e}")


def check(ncfile: str, delete_switch: bool = False) -> bool:
    """
    Check if a NetCDF file is corrupted with enhanced error handling.

    Handles HDF5 library errors gracefully without terminating program.
    """
    is_valid = False

    if not os.path.exists(ncfile):
        print(f"File missing: {ncfile}")
        return False

    try:
        # # 深度验证文件结构
        # with nc.Dataset(ncfile, "r") as ds:
        #     # 显式检查文件结构完整性
        #     ds.sync()  # 强制刷新缓冲区
        #     ds.close()  # 显式关闭后重新打开验证

        # 二次验证确保变量可访问
        with nc.Dataset(ncfile, "r") as ds_verify:
            if not ds_verify.variables:
                print(f"Empty variables: {ncfile}")
            else:
                # 尝试访问元数据
                _ = ds_verify.__dict__
                # 抽样检查第一个变量
                for var in ds_verify.variables.values():
                    _ = var.shape  # 触发实际数据访问
                    break
                is_valid = True

    except Exception as e:  # 捕获所有异常类型
        print(f"HDF5 validation failed for {ncfile}: {str(e)}")
        error_type = type(e).__name__
        if "HDF5" in error_type or "h5" in error_type.lower():
            print(f"Critical HDF5 structure error detected in {ncfile}")

    # 安全删除流程
    if not is_valid:
        if delete_switch:
            try:
                os.remove(ncfile)
                print(f"Removed corrupted: {ncfile}")
            except Exception as del_error:
                print(f"Delete failed: {ncfile} - {str(del_error)}")
        return False

    return True


def convert_longitude(ds, lon_name="longitude", convert=180):
    """
    Description:
        Convert the longitude array to a specified range.
        
    Parameters:
        ds (xarray.Dataset): The xarray dataset containing the longitude data.
        lon_name (str): The name of the longitude variable, default is "longitude".
        convert (int): The target range to convert to, can be 180 or 360, default is 180.
        
    Returns:
        xarray.Dataset: The xarray dataset with the converted longitude.
    """
    to_which = int(convert)
    if to_which not in [180, 360]:
        raise ValueError("convert value must be '180' or '360'")

    if to_which == 180:
        ds = ds.assign_coords({lon_name: (ds[lon_name] + 180) % 360 - 180})
    elif to_which == 360:
        ds = ds.assign_coords({lon_name: (ds[lon_name] + 360) % 360})

    return ds.sortby(lon_name)


def isel(ncfile, dim_name, slice_list):
    """
    Description:
        Choose the data by the index of the dimension

    Parameters:
        ncfile: str, the path of the netCDF file
        dim_name: str, the name of the dimension
        slice_list: list, the index of the dimension

    Example:
        slice_list = [[y*12+m for m in range(11,14)] for y in range(84)]
        slice_list = [y * 12 + m for y in range(84) for m in range(11, 14)]
        isel(ncfile, 'time', slice_list)
    """
    ds = xr.open_dataset(ncfile)
    slice_list = np.array(slice_list).flatten()
    slice_list = [int(i) for i in slice_list]
    ds_new = ds.isel(**{dim_name: slice_list})
    ds.close()
    return ds_new


if __name__ == "__main__":
    data = np.random.rand(100, 50)
    save(r"test.nc", data, "data", {"time": np.linspace(0, 120, 100), "lev": np.linspace(0, 120, 50)}, "a")
