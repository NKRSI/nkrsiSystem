import requests
import pandas as pd
import io
import json
from nkrsiSystem.config import GPU_SERVERS
from nkrsiSystem.settings import RESOURCE_MONITORING_PORT
from celery import shared_task
from resource_monitoring.models import ResourceUsage


def process_ram_data(ram_df_raw) -> pd.DataFrame:
    columns = ram_df_raw.columns[0].split()
    index_column = []
    data = []
    for row in ram_df_raw.values:
        row_split = row[0].split()
        index_column.append(row_split[0])
        data.append(row_split[1:])
    return pd.DataFrame(data, columns=columns, index=index_column).fillna('')


def process_cpu_cores_temperature(sensors_data) -> pd.DataFrame:
    sensor_names = list(sensors_data.keys())
    assert len(sensor_names) == 1
    sensor_data = sensors_data[sensor_names[0]]
    sensor_data.pop('Adapter')
    refined_data = {}
    for core_name, core_info in sensor_data.items():
        refined_data[core_name] = {k[6:]: v for k, v in core_info.items()}
        refined_data[core_name].pop('crit_alarm')
        refined_data[core_name].pop('crit')
    return pd.DataFrame.from_dict(refined_data)


def fetch_resources_usage():
    result = []
    for (server_name, server_ip) in GPU_SERVERS:
        r = requests.get('http://' + server_ip + ':' + RESOURCE_MONITORING_PORT + '/resources')
        data = r.json()
        data['server_name'] = server_name
        result.append(data)
    return result


def fetch_resources_usage_dataframes():
    servers_data = fetch_resources_usage()

    result = []
    for server_data in servers_data:
        gpu_df = pd.read_csv(io.StringIO(server_data['gpu_res']))
        ram_df_raw = pd.read_csv(io.StringIO(server_data['ram_res']), sep='\t')
        ram_df = process_ram_data(ram_df_raw)
        sensors_data = json.load(io.StringIO(server_data['cpu_ct_res']))
        cpu_temp_df = process_cpu_cores_temperature(sensors_data)
        result.append({
            'server_name': server_data['server_name'],
            'gpu_df': gpu_df,
            'ram_df': ram_df,
            'cpu_df': cpu_temp_df,
        })
    return result


@shared_task()
def dump_resources_usage():

    resource_usage = fetch_resources_usage()

    for server_data in resource_usage:
        server_name = server_data['server_name']
        ru = ResourceUsage(
            server=server_name,
            cpu_data=server_data['cpu_ct_res'],
            gpu_data=server_data['gpu_res'],
            ram_data=server_data['ram_res'],
        )
        ru.save()
        print(server_name+" data stored")
