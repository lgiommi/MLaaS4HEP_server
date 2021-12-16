import argparse
import os

class OptionParser(object):
    "Option parser class for reader arguments"
    def __init__(self):
        "User based option parser"
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.parser.add_argument("--device", action="store", \
            dest="device", default="", help="CPU or GPU")
        self.parser.add_argument("--memory", action="store", \
            dest="memory", default="", help="The maximum amount of memory the container can use")
        self.parser.add_argument("--cpus", action="store", \
            dest="cpus", default="", help="How much of the available CPU resources a container can use")
        self.parser.add_argument("--model", action="store", \
            dest="model", default="", help="Definition of the model")
        self.parser.add_argument("--nevts", action="store", \
            dest="nevts", default="", help="Number of events to read")

def main():
    "Main function"
    optmgr = OptionParser()
    opts = optmgr.parser.parse_args()
    device = opts.device
    memory = opts.memory
    cpus = opts.cpus
    model = opts.model
    nevts = opts.nevts
    stream = os.popen(f'docker run -v /Users/luca.giommi/Computer_Windows/Universita/Dottorato/TFaaS/MLaaS4HEP_server:/data/ -i -t --memory={memory} --cpus={cpus} mlaas_server --device={device} --memory={memory} --cpus={cpus} --model={model} --nevts={nevts}')
    return stream.read()

if __name__ == '__main__':
    main()