from flask import Flask, request, send_file
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/luca.giommi/Downloads/prova'
CERT_FOLDER = '/Users/luca.giommi/.grid-security/grid-security/certificates'
ALLOWED_EXTENSIONS = {'gz', 'txt', 'pdf'}

app = Flask(__name__)
app.secret_key = "mlaas4HEP_secret"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import subprocess
import os, tarfile, shutil
import json
gpu_pid = -1
users_proc = {}

def process(name, device, memory, cpus, files, labels, model, params):
    "Process request and return PID"
    proc = subprocess.Popen(['python3', 'run_container.py', '--name', str(name), '--memory', str(memory), '--cpus', str(cpus), \
        '--host_folder', str(os.path.join(UPLOAD_FOLDER,name.rsplit('_', 1)[0])), '--cert_folder', str(CERT_FOLDER), \
        '--files', str(files), '--labels', str(labels), '--model', str(model), '--params', str(params), '--fout', str(name)])
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

def return_logs(name):
    log_path = os.path.join(UPLOAD_FOLDER, name.rsplit('_', 1)[0], name + ".txt")
    os.popen(f'docker logs {name} &> {log_path}').read()
    return send_file(log_path, as_attachment=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/submit', methods=['POST'])
def submit():
    global users_proc
    request_data = request.get_json()
    name = request_data["name"]
    device = request_data["device"]
    memory = request_data["memory"]
    cpus = request_data["cpus"]
    files = request_data["files"]
    labels = request_data["labels"]
    model = request_data["model"]
    params = request_data["params"]

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
    pid = process(users_proc[name], device, memory, cpus, files, labels, model, params)
    data = {"process_name": users_proc[name], "job_id": pid}
    return json.dumps(data, indent=True)

@app.route('/status_docker', methods=['GET'])
def status_docker():
    process_name = request.args["process_name"]
    return return_status_docker(process_name)

@app.route('/logs', methods=['GET'])
def logs():
    process_name = request.args["process_name"]
    return return_logs(process_name)

@app.route('/hello', methods=['GET'])
def hello():
    return "Hello World\n"

@app.route('/upload', methods=['POST'])
def upload():
    # check if the post request has the file part
    if 'file' not in request.files:
        return "No file was provided \n"
    file = request.files['file']
    if 'name' not in request.args:
        return "No name was provided \n"
    name = request.args["name"]
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        tar = tarfile.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        tar.extractall(path=app.config['UPLOAD_FOLDER'])
        tar.close()
        shutil.move(os.path.join(app.config['UPLOAD_FOLDER'], filename.rsplit('.', 2)[0].lower()), os.path.join(app.config['UPLOAD_FOLDER'],name))
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return "Successfully uploaded!\n"

@app.route('/delete_specs', methods=['GET'])
def delete_specs():
    name = request.args["name"]
    specs_path = os.path.join(UPLOAD_FOLDER,name)
    os.popen(f'rm {specs_path}/*specs*').read()
    return "Specs deletion completed!\n"

@app.route('/model', methods=['GET'])
def model():
    process_name = request.args["process_name"]
    model_path = os.path.join(UPLOAD_FOLDER, process_name.rsplit('_', 1)[0], process_name + ".tar.gz")
    return send_file(model_path, as_attachment=True)

@app.route('/delete_folder', methods=['GET'])
def delete_folder():
    name = request.args["name"]
    folder_path = os.path.join(UPLOAD_FOLDER, name)
    os.popen(f'rm -r -f {folder_path}').read()
    return "Folder deletion completed!\n"

if __name__ == '__main__':
    # run app in debug mode on port 5000
    app.run(debug=True, port=5000)