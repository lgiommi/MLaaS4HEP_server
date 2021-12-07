import argparse
import os

class OptionParser(object):
    "Option parser class for reader arguments"
    def __init__(self):
        "User based option parser"
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.parser.add_argument("--model", action="store", \
            dest="model", default="", help="Definition of the model")
        self.parser.add_argument("--nevts", action="store", \
            dest="nevts", default="", help="Number of events to read")

def main():
    "Main function"
    optmgr = OptionParser()
    opts = optmgr.parser.parse_args()
    model = opts.model
    nevts = opts.nevts
    os.popen(f'docker run -v /Users/luca.giommi/Computer_Windows/Universita/Dottorato/TFaaS/MLaaS4HEP_server:/data/ -i -t mlaas_server --model={model} --nevts={nevts}')
    output = stream.read()
    return output

if __name__ == '__main__':
    main()