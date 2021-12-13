import argparse
import time
import json

class OptionParser(object):
    "Option parser class for reader arguments"
    def __init__(self):
        "User based option parser"
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.parser.add_argument("--device", action="store", \
            dest="device", default="", help="Definition of the model")
        self.parser.add_argument("--model", action="store", \
            dest="model", default="", help="Definition of the model")
        self.parser.add_argument("--nevts", action="store", \
            dest="nevts", default="", help="Number of events to read")

def main():
    "Main function"
    optmgr = OptionParser()
    opts = optmgr.parser.parse_args()
    device = opts.device
    model = opts.model
    nevts = opts.nevts
    data = {"device": device, "model": model, "nevts": nevts}
    time.sleep(30) # <-- There's no time.wait, but time.sleep.
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile, indent=True)

if __name__ == '__main__':
    main()