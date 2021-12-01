from flask import Flask, request
app = Flask(__name__)

import subprocess
import time

@app.route('/submit', methods=['POST'])
def json():
    request_data = request.get_json()
    model=request_data["model"]
    nevts=request_data["nevts"]
    proc = subprocess.Popen(['python', 'python_script.py', '--model', str(model), '--nevts', str(nevts)])
    time.sleep(3) # <-- There's no time.wait, but time.sleep.
    pid = proc.pid
    job_ID=f"{{\n\"job_ID\": {pid}\n}}\n"
    return job_ID
    
    
    str(pid)+"\n"

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)