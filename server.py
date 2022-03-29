from flask import Flask, request
app = Flask(__name__)

import subprocess
import os
import json
gpu_pid = -1
users_proc = {}

def process(name, device, memory, cpus, host_folder, files, labels, model, params, fout):
    "Process request and return PID"
    proc = subprocess.Popen(['python', 'run_container.py', '--name', str(name), '--memory', str(memory), '--cpus', str(cpus), \
        '--host_folder', str(host_folder), '--files', str(files), '--labels', str(labels), '--model', str(model), '--params', str(params), \
        '--fout', str(fout)])
    if  device == "gpu":
        global gpu_pid
        gpu_pid = proc.pid
    return proc.pid

def return_status(pid):
    stream = os.popen(f'ps -a {pid}')
    output = stream.read()
    output_string = "Running"
    if output.count('\n') == 1:
        output_string = "Ended"
    feedback = {"job_id": pid, "status": output_string}
    return json.dumps(feedback, indent=True)

def return_status_docker(name):
    stream = os.popen(f'docker ps -a -f "name={name}"')
    output = stream.read()
    feedback = {"process_name": name, "status": output.split("\n")[1].split("   ")[4]}
    return json.dumps(feedback, indent=True)

def return_logs(name, log_file):
    stream = os.popen(f'docker logs {name} &> {log_file}')
    #output = stream.read()
    #feedback = {"process_name": name, "logs": output}
    #return json.dumps(feedback, indent=True)
    return ""

@app.route('/submit', methods=['POST'])
def submit():
    global users_proc
    request_data = request.get_json()
    name = request_data["name"]
    device = request_data["device"]
    memory = request_data["memory"]
    cpus = request_data["cpus"]
    host_folder = request_data["host_folder"]
    files = request_data["files"]
    labels = request_data["labels"]
    model = request_data["model"]
    params = request_data["params"]
    fout = request_data["fout"]

    if name in users_proc:
        count = int(users_proc[name].split("_")[1])
        count+=1
        users_proc[name] = f"{name}_{count}"
    else:
        users_proc[name] = f"{name}_1"

    if device == "gpu" and gpu_pid != -1:
        json_file = json.loads(return_status(gpu_pid))
        if json_file["status"] == "Running":
            return "ERROR: GPU already busy by another process, your request cannot be accepted.\nRetry later.\n"
    pid = process(users_proc[name], device, memory, cpus, host_folder, files, labels, model, params, fout)
    data = {"process_name": users_proc[name], "job_id": pid}
    return json.dumps(data, indent=True)

@app.route('/status_docker', methods=['GET'])
def status_docker():
    process_name = request.args["process_name"]
    return return_status_docker(process_name)

@app.route('/logs', methods=['GET'])
def logs():
    process_name = request.args["process_name"]
    log_file = request.args["log_file"]
    return return_logs(process_name, log_file)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World"


if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)