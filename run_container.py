import argparse
import os

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
        self.parser.add_argument("--files", action="store", \
            dest="files", default="", help="txt file where the ROOT files to use are reported")
        self.parser.add_argument("--labels", action="store", \
            dest="labels", default="", help="labels of the ROOT files")
        self.parser.add_argument("--model", action="store", \
            dest="model", default="", help="Definition of the model")
        self.parser.add_argument("--params", action="store", \
            dest="params", default="", help="json file with relevant parameters")

def main():
    "Main function"
    optmgr = OptionParser()
    opts = optmgr.parser.parse_args()
    name = opts.name
    memory = opts.memory
    cpus = opts.cpus
    files = opts.files
    labels = opts.labels
    model = opts.model
    params = opts.params
    stream = os.popen(f'docker run -v /Users/luca.giommi/Computer_Windows/Universita/Dottorato/TFaaS/MLaaS4HEP_server/folder_test:/workarea/folder_test -it --name={name} --memory={memory} --cpus={cpus} felixfelicislp/mlaas_cloud:ubuntu --files={files} --labels={labels} --model={model} --params={params}')
    return stream.read()

if __name__ == '__main__':
    main()