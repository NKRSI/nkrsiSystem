import io
import json

import base64
import seaborn as sns
import matplotlib.pyplot as plt

import pandas as pd
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from resource_monitoring.tasks import fetch_resources_usage_dataframes, process_ram_data, process_cpu_cores_temperature
from resource_monitoring.models import ResourceUsage

@login_required()
def resources_dashboard(request):
    server_infos = fetch_resources_usage_dataframes()

    server_infos = [
        (
            s['server_name'],
            s['gpu_df'].to_html(),
            s['ram_df'].to_html(),
            s['cpu_df'].to_html()
        )
        for s in server_infos
    ]
    return render(request, 'resource_monitoring/dashboard.html', {'server_infos': server_infos})


@login_required()
def stat_plots(request):
    table_gateway = ResourceUsage
    query_object = table_gateway.objects
    query_object = query_object.all().order_by('server', 'timestamp')
    record_set = query_object.values()

    data = record_set
    for data_entry in data:
        data_entry['gpu_data'] = pd.read_csv(io.StringIO(data_entry['gpu_data']))
        data_entry['ram_data'] = process_ram_data(pd.read_csv(io.StringIO(data_entry['ram_data']), sep='\t'))
        data_entry['cpu_data'] = process_cpu_cores_temperature(json.load(io.StringIO(data_entry['cpu_data'])))
        data_entry['cpu_data'] = data_entry['cpu_data'].transpose().reset_index()

        for k in ['gpu_data', 'ram_data', 'cpu_data']:
            data_entry[k]['server'] = data_entry['server']
            data_entry[k]['timestamp'] = data_entry['timestamp']

    gpu_data = pd.concat([data_entry['gpu_data'] for data_entry in data])
    ram_data = pd.concat([data_entry['ram_data'] for data_entry in data])
    cpu_data = pd.concat([data_entry['cpu_data'] for data_entry in data])

    servers = cpu_data['server'].unique()

    fig, axs = plt.subplots(1, len(servers), figsize=(14, 7))

    for ax, s in zip(axs, servers):
        sns.lineplot(data=cpu_data[cpu_data['server'] == s], x="timestamp", y="input", hue='index', legend='full', ax=ax)
        ax.set_title(s)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    graphic = graphic.decode('utf-8')

    return render(request, 'resource_monitoring/stat_plots.html', {'graphic': graphic})
