#!/usr/local/autopkg/python
"""Hello AutoPkg"""

from autopkglib import Processor, ProcessorError
from subprocess import Popen

import sys

__all__ = ["HelloWorld"]

class HelloWorld(Processor):

    description = __doc__
    input_variables = {
        "hello_name": {
            "required": True,
            "description": "Who do you think you are?",
        }
    }

    output_variables = {
        "pass_it_on": { "description": "What is being said." }
    }

    def main(self):
        try:
            pass_it_on = "Hello %s" % self.env["hello_name"]
            self.output(pass_it_on)
            self.output("This python is '%s'" % sys.version)
        except Exception as err:
            raise ProcessorError(err)
        self.env["pass_it_on"] = pass_it_on
        for e in self.env.keys():
            print(f'Key: {e} : {self.env[e]}')

if __name__ == "__main__":
    PROC = SampleSharedProcessor()
    PROC.execute_shell()

