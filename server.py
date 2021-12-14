from flask import Flask, request
app = Flask(__name__)

import subprocess
import os
import json
gpu_pid = -1

def process(device, memory, cpus, model, nevts):
    "Process request and return PID"
    proc = subprocess.Popen(['python', 'run_container.py', '--device', str(device), \
        '--memory', str(memory), '--cpus', str(cpus), '--model', str(model), '--nevts', str(nevts)])
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
    return json.dumps(feedback)

@app.route('/submit', methods=['POST'])
def submit():
    request_data = request.get_json()
    model = request_data["model"]
    memory = request_data["memory"]
    cpus = request_data["cpus"]
    nevts = request_data["nevts"]
    device = request_data["device"]
    if device == "gpu" and gpu_pid != -1:
        json_file = json.loads(return_status(gpu_pid))
        if json_file["status"] == "Running":
            return "ERROR: GPU already busy by another process, your request cannot be accepted.\nRetry later.\n"
    pid = process(device, memory, cpus, model, nevts)
    data = {"job_id": pid}
    return json.dumps(data, indent=True)

@app.route('/status', methods=['GET'])
def status():
    pid = request.args["pid"]
    return return_status(pid)

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)