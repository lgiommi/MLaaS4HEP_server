from flask import Flask, request
app = Flask(__name__)

import subprocess
import os
import json

def process(model, nevts):
    "Process request and return PID"
    proc = subprocess.Popen(['python', 'python_script.py', '--model', str(model), '--nevts', str(nevts)])
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
    model=request_data["model"]
    nevts=request_data["nevts"]
    pid = process(model, nevts)
    data = {"job_id": pid}
    return json.dumps(data, indent=True)

@app.route('/status', methods=['GET'])
def status():
    pid = request.args["pid"]
    return return_status(pid)

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)