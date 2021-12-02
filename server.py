from flask import Flask, request
app = Flask(__name__)

import subprocess
import time
import json

def process(model, nevts):
    "Process request and return PID"
    proc = subprocess.Popen(['python', 'python_script.py', '--model', str(model), '--nevts', str(nevts)])
    time.sleep(3) # <-- There's no time.wait, but time.sleep.
    return proc.pid

@app.route('/submit', methods=['POST'])
def submit():
    request_data = request.get_json()
    model=request_data["model"]
    nevts=request_data["nevts"]
    pid = process(model, nevts)
    data = {"job_id": pid}
    return json.dumps(data)
    
    
    str(pid)+"\n"

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)