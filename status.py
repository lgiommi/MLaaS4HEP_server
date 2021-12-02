import argparse
import json

class OptionParser(object):
    "Option parser class for reader arguments"
    def __init__(self):
        "User based option parser"
        self.parser = argparse.ArgumentParser(prog='PROG')
        self.parser.add_argument("--pid", action="store", \
            dest="pid", default="", help="Definition of the model")

def main():
    "Main function"
    optmgr = OptionParser()
    opts = optmgr.parser.parse_args()
    pid = opts.pid
    feedback = {"job_id": pid, "status": "ongoing"}
    print(json.dumps(feedback))

if __name__ == '__main__':
    main()