from flask import Flask
import subprocess
import json

app = Flask(__name__)

NVIDIASMI_CMD = 'nvidia-smi --query-gpu=gpu_name,index,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.used --format=csv'
RAM_CMD = 'free -t -m'
CPU_CORES_TEMPERATURE_CMD = 'sensors -j'


@app.route("/resources")
def hello():
    gpu_res = subprocess.check_output(NVIDIASMI_CMD, shell=True)
    ram_res = subprocess.check_output(RAM_CMD, shell=True)
    cpu_ct_res = subprocess.check_output(CPU_CORES_TEMPERATURE_CMD, shell=True)

    return json.dumps({
        'gpu_res': gpu_res.decode('utf-8'),
        'ram_res': ram_res.decode('utf-8'),
        'cpu_ct_res': cpu_ct_res.decode('utf-8'),
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=11223)
