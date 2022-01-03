import argparse
import time
import json

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

def main():
    "Main function"
    optmgr = OptionParser()
    opts = optmgr.parser.parse_args()
    device = opts.device
    memory = opts.memory
    cpus = opts.cpus
    model = opts.model

    #while True:
    #    x*x
    #x = bytearray(1024*1024*1000)

    data = {"device": device, "memory": memory, "cpus": cpus, "model": model}
    time.sleep(20) # <-- There's no time.wait, but time.sleep.
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=True)

if __name__ == '__main__':
    main()