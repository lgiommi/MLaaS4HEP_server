import argparse
import os, json

class OptionParser(object):
    "Option parser class for reader arguments"
    def __init__(self):
        "User based option parser"
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.parser.add_argument("--name", action="store", \
            dest="name", default="", help="Name of the process")
        self.parser.add_argument("--memory", action="store", \
            dest="memory", default="", help="The maximum amount of memory the container can use")
        self.parser.add_argument("--cpus", action="store", \
            dest="cpus", default="", help="How much of the available CPU resources a container can use")
        self.parser.add_argument("--host_folder", action="store", \
            dest="host_folder", default="", help="Specify the path of the host folder where the local data are located")
        self.parser.add_argument("--cert_folder", action="store", \
            dest="cert_folder", default="", help="Specify the path of the host folder where the certificates are located")
        self.parser.add_argument("--files", action="store", \
            dest="files", default="", help="txt file where the ROOT files to use are reported")
        self.parser.add_argument("--labels", action="store", \
            dest="labels", default="", help="labels of the ROOT files")
        self.parser.add_argument("--model", action="store", \
            dest="model", default="", help="Definition of the model")
        self.parser.add_argument("--params", action="store", \
            dest="params", default="", help="json file with relevant parameters")
        self.parser.add_argument("--fout", action="store", \
            dest="fout", default="", help="location of the output trained ML model")

def main():
    "Main function"
    optmgr = OptionParser()
    opts = optmgr.parser.parse_args()
    name = opts.name
    memory = opts.memory
    cpus = opts.cpus
    host_folder = opts.host_folder
    cert_folder = opts.cert_folder
    files = opts.files
    labels = opts.labels
    model = opts.model
    params = opts.params
    fout = opts.fout
    params_file = {"name": fout, "model": "saved_model.pb"}
    with open(os.path.join(host_folder, fout + "_params.json"), "w") as file:
        json.dump(params_file, file)
    stream = os.popen(f'docker run -v /data/models_repo:/data/models -v /data/compose-xrootd/proxy/x509_proxy:/workarea/folder_test/x509_proxy -v {cert_folder}:/workarea/certificates -v {host_folder}:/workarea/folder_test --name={name} --memory={memory} --cpus={cpus} felixfelicislp/mlaas:xrootd_pip --files={files} --labels={labels} --model={model} --params={params} --fout={fout} && cp {host_folder}/{fout}_params.json {host_folder}/{fout}/params.json && rm -f {host_folder}/{fout}_params.json && cp -rf {host_folder}/{fout} /data/models_repo && tar -czvf {host_folder}/{fout}.tar.gz -C {host_folder}/{fout} . && rm -r -f {host_folder}/{fout}')
    #stream = os.popen(f'docker run -v /data/compose-xrootd/proxy/x509_proxy:/workarea/folder_test/x509_proxy -v {cert_folder}:/workarea/certificates -v {host_folder}:/workarea/folder_test -it --name={name} --memory={memory} --cpus={cpus} felixfelicislp/mlaas:xrootd_pip --files={files} --labels={labels} --model={model} --params={params} --fout={fout} && tar -czvf {host_folder}/{fout}.tar.gz -C {host_folder}/{fout} . && rm -r -f {host_folder}/{fout}')
    #stream = os.popen(f'docker run -v /data/compose-xrootd/proxy/x509_proxy:{host_folder}/x509_proxy -v {cert_folder}:/workarea/certificates -v {host_folder}:/workarea/folder_test --entrypoint /bin/bash -dt felixfelicislp/mlaas:xrootd_pip')
    return stream.read()

if __name__ == '__main__':
    main()
