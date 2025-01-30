# -*- coding: utf-8 -*-
import datetime

import numpy as np
import pandas as pd
import tomli
from metget.metget_build import MetGetBuildRest
from pyproj import CRS

from cht_meteo import gfs_forecast_0p25
from cht_meteo.cht.meteo.coamps_utils import (
    check_coamps,
    get_da_from_url,
    tc_vitals_storm,
)


class Dataset:
    def __init__(self):
        self.quantity = None
        self.unit = None
        self.time = []
        self.x = None
        self.y = None
        self.crs = None
        self.val = None
        self.source = []
        self.metget = None


def download(
    param_list,
    lon_range,
    lat_range,
    time_range,
    cycle_time,
    resolution=0.25,
    config_path=None,
):
    """Function to download coamps-tc forecasts using the metget tool api
    Right now resolution is hardcoded to 0.25 degrees but this can change"""

    fill_values = dict(
        wind=0.0, precipitation=0.0, barometric_pressure=102000.0
    )  # fill values to use in case of nan
    units = dict(
        wind="m/s", precipitation="kg.m-2.hour-1", barometric_pressure="Pa"
    )  # units

    if not config_path:
        raise ValueError(
            "The path to a configuration file needs to be provided with the argument 'config_path'"
        )
    else:
        with open(config_path, mode="rb") as fp:
            config = tomli.load(fp)

    # Read data from the config file
    apikey = config["apikey"]
    endpoint = config["endpoint"]
    api_version = config["api_version"]
    if "tau" in config:
        tau = config["tau"]
    else:
        tau = 0
    if "override" in config:
        override = True
    else:
        override = False  # noqa: F841

    # Connect parameters names with coamps-tc names
    param_names = {
        "wind": "wind_pressure",
        "barometric_pressure": "wind_pressure",
        "precipitation": "rain",
    }
    variables = list(
        np.unique([param_names[name] for name in param_list])
    )  # ['wind_pressure', 'rain']

    # Get individual times requested
    # TODO how is time-step handled in cosmos?
    requested_times = (
        pd.date_range(start=time_range[0], end=time_range[1], freq="3H")
        .to_pydatetime()
        .tolist()
    )
    requested_times = [
        ti.replace(tzinfo=datetime.timezone.utc) for ti in requested_times
    ]

    timestep = int(
        (requested_times[1] - requested_times[0]).total_seconds()
    )  # get time-step of requested time assuming that the time-step stays the same
    ntime = len(requested_times)

    # Get the available storms in the Coamps-TC forecast
    try:
        coamps_storms = check_coamps(apikey, endpoint, time_range[0], time_range[1])
    except Exception:
        coamps_storms = {}

    # Get the storm names that have a forecast available for the requested cycle
    storms = [
        name
        for name in coamps_storms.keys()
        if cycle_time.strftime("%Y-%m-%d %H:%M:%S")
        in coamps_storms[name]["cycles_complete"]
    ]

    # If there are no storms available raise Error
    if len(storms) == 0:
        raise ValueError(
            f"There are no COAMPS-TC forecasts available for cycle: {cycle_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    # Check if there is a priority storm given
    if "priority_storm" in config:
        if config["priority_storm"] == "tc_vitals":
            # Get storm priority from noaa
            priority_storm = tc_vitals_storm()
            if not priority_storm:
                print(
                    "Priority storm could not be loaded from https://ftp.nhc.noaa.gov/atcf/com/tcvitals"
                )
            else:
                print(
                    f"Priority storm {priority_storm} found from https://ftp.nhc.noaa.gov/atcf/com/tcvitals"
                )
        else:
            priority_storm = config["priority_storm"]
            print(f"Priority storm {priority_storm} provided in config file.")
    else:
        priority_storm = None

    if priority_storm is not None and priority_storm not in storms:
        priority_storm = None
        print(
            f"Priority storm {priority_storm} not found in available COAMPS-TC forecasted storms {storms}."
        )
        datasets = gfs_forecast_0p25.download(
            param_list, lon_range, lat_range, time_range, cycle_time
        )
        print(
            "Could not find any coamps-tc data in requested time range! Using gfs instead"
        )
        return datasets

    # Choose storm according to input
    if not priority_storm and len(storms) == 1:  # if only a single storm is available
        storm = storms[0]
    elif (
        not priority_storm and len(storms) > 1
    ):  # if multiple storms are available use latest
        ids = [int(i.split("L")[0]) for i in storms]
        ind = np.argmax(ids)
        storm = storms[ind]
    else:
        storm = priority_storm

    print(f"Forecast will be downloaded for storm {storm}")

    # Prepare metget domain
    domain = (
        [f"coamps-{storm}"]
        + [resolution]
        + [lon_range[0], lat_range[0], lon_range[1], lat_range[1]]
    )
    t1 = requested_times[0]
    t2 = requested_times[-1]

    dss, metadata = {}, {}

    for ii, var in enumerate(variables):
        # ...Building the request
        request_data = MetGetBuildRest.generate_request_json(
            start_date=t1.strftime("%Y%m%d %H%M%S"),
            end_date=t2.strftime("%Y%m%d %H%M%S"),
            format="hec-netcdf",
            data_type=var,
            time_step=timestep,
            domains=MetGetBuildRest.parse_command_line_domains([domain], tau),
            epsg=4326,
            filename=f"{storm}_{var}",
            backfill=True,
            # nowcast=False,
            multiple_forecasts=True,  # This makes sure that we use multiple forecasts
            # compression=True,
            save_json_request=False,
            # dry_run=True,
            strict=True,
        )
        client = MetGetBuildRest(endpoint, apikey, api_version)
        data_id, status_code = client.make_metget_request(request_data)
        urls, meta = client.download_metget_data(
            data_id,
            30,  # sleep_time in seconds
            3,  # max_wait in hours
            output_directory=None,
            return_only_url=True,
        )
        # TODO Check why this should be a list?
        ds_list = []
        for url in urls:
            ds = get_da_from_url(url)
            ds_list.append(ds)
        if ds_list is not None:
            dss[var] = ds_list[0]
            metadata[var] = meta
        else:
            dss[var] = None

    # if no data could be downloaded (CHECK AGAIN WHAT SHOULD HAPPEN IN THIS CASE)
    if all([dss[k] is None for k in list(dss.keys())]):
        datasets = gfs_forecast_0p25.download(
            param_list, lon_range, lat_range, time_range, cycle_time
        )
        print(
            "Could not find any coamps-tc data in requested time range! Using gfs instead"
        )
        return datasets
    else:  # Else if there are available data get lon lat info
        for key in dss.keys():
            if dss[key] is not None:
                data0 = dss[key]
                lon = np.array(data0["lon"])
                lat = np.array(data0["lat"])
                if lat[1] - lat[0] > 0:  # lat should be in descending order
                    lat = lat[::-1]
                    reverse = True
                else:
                    reverse = False
                lon = (lon + 360) % 360  # added this to be consistent with gfs
                nrows = len(lat)
                ncols = len(lon)

    # Prepare datasets
    datasets = []
    for param in param_list:
        dataset = Dataset()
        dataset.crs = CRS.from_epsg(4326)
        dataset.quantity = param
        dataset.x = lon
        dataset.y = lat
        dataset.time = pd.to_datetime(
            [tt.replace(tzinfo=None) for tt in requested_times]
        ).to_pydatetime()
        if dataset.quantity == "wind":
            dataset.u = np.empty((ntime, nrows, ncols))
            dataset.u[:] = np.nan
            dataset.v = np.empty((ntime, nrows, ncols))
            dataset.v[:] = np.nan
        else:
            dataset.val = np.empty((ntime, nrows, ncols))
            dataset.val[:] = np.nan
        datasets.append(dataset)

    for it, time_i in enumerate(requested_times):
        # Loop through requested parameters
        for ind, param in enumerate(param_list):
            dataset = datasets[ind]
            okay = False
            makezeros = False
            #  First check if there are coamps-tc data available for this parameter
            if dss[param_names[param]] is not None:
                okay = True
                model_t = pd.to_datetime(
                    dss[param_names[param]].time.to_numpy()
                ).to_pydatetime()
                model_t_ind = np.where(model_t == time_i.replace(tzinfo=None))[0][0]
            else:
                makezeros = True

            if okay:
                # Get metadata of input used
                dataset.coampsflag = True
                dataset.metget = metadata[param_names[param]]["input"]
                inputs = [
                    name
                    for name in metadata[param_names[param]]["input_files"][
                        f"coamps-tc-{storm}"
                    ]
                    if time_i.strftime("%Y%m%d%H%M") in name
                ]
                input_name = inputs[0].split(".")[2]
                cycle_used = input_name.split("_")[2]
                cycle_hour = input_name.split("_")[3]
                dataset.source.append(f"coamps_{storm}_{cycle_used}z_{cycle_hour}")

                if param == "wind":
                    data = dss[param_names[param]]
                    u = data["wind_u"]
                    v = data["wind_v"]
                    dataset.unit = u.units

                    if np.any(np.isnan(u)) or np.any(
                        np.isnan(v)
                    ):  # check if there are nans and fill them up
                        u = u.fillna(fill_values[param])
                        v = v.fillna(fill_values[param])

                    u = u.metpy.unit_array.squeeze()
                    v = v.metpy.unit_array.squeeze()

                    if reverse:
                        dataset.u[it, :, :] = np.array(u[model_t_ind, ::-1, :])
                        dataset.v[it, :, :] = np.array(v[model_t_ind, ::-1, :])
                    else:
                        dataset.u[it, :, :] = np.array(u[model_t_ind, :, :])
                        dataset.v[it, :, :] = np.array(v[model_t_ind, :, :])
                else:
                    if param == "barometric_pressure":
                        var_name = "mslp"
                    elif param == "precipitation":
                        var_name = "rain"  # Check when available in scrubber tool!
                    data = dss[param_names[param]]
                    val = data[var_name]

                    # Added this check to ensure that pressure is in Pa
                    if param == "barometric_pressure":
                        if val.units == "mb":
                            val = val * 100
                            val.attrs["units"] = "Pa"
                    dataset.unit = val.units

                    if (
                        param == "precipitation"
                    ):  # Added this check to ensure that nan in precipitation are correctly interpreted
                        val = val.where(val >= 0, np.nan)

                    if np.any(
                        np.isnan(val)
                    ):  # check if there are nans and fill them up
                        val = val.fillna(fill_values[param])

                    val = np.array(val.metpy.unit_array.squeeze())

                    if reverse:
                        dataset.val[it, :, :] = np.array(val[model_t_ind, ::-1, :])
                    else:
                        dataset.val[it, :, :] = np.array(val[model_t_ind, :, :])

            elif makezeros:  # add zeros
                try:
                    #  Currently data are used directly from gfs since grid is the same, but  resampling should be done in a new version
                    datasets_gfs = gfs_forecast_0p25.download(
                        param_list, lon_range, lat_range, [time_i, time_i], cycle_time
                    )
                    if param == "wind":
                        dataset.u[it, :, :] = datasets_gfs[ind].u
                        dataset.v[it, :, :] = datasets_gfs[ind].v
                    else:
                        dataset.val[it, :, :] = datasets_gfs[ind].val
                    dataset.unit = datasets_gfs[ind].unit
                    dataset.src.append("gfs")
                    print(
                        param
                        + " was not found on server for {} --> using gfs forecast data instead".format(
                            time_i
                        )
                    )
                except Exception:
                    if param == "wind":
                        dataset.u[:] = fill_values[param]
                        dataset.v[:] = fill_values[param]
                        dataset.unit = units[param]
                        dataset.src.append("default_value")
                        print(
                            param
                            + " was not found on server for {} --> using {} {} instead !!!".format(
                                time_i, fill_values[param], units[param]
                            )
                        )

                    else:
                        dataset.val[:] = fill_values[param]
                        dataset.unit = units[param]
                        dataset.src.append("default_value")
                        print(
                            param
                            + " was not found on server ... --> using {} {} instead !!!".format(
                                fill_values[param], units[param]
                            )
                        )

    return datasets
