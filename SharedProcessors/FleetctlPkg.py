#!/usr/local/autopkg/python
"""Fleetctl runner"""

from autopkglib import Processor, ProcessorError

import pathlib
import subprocess
import sys

__all__ = ["FleetctlPkg"]

def reverse_domain(url:str) -> str:
    return '.'.join(reversed(url.split('/')[-1].split('.')))
    

class FleetctlPkg(Processor):

    description = __doc__
    input_variables = {
        "fleetctl_path": {
            "required": True,
            "description": "Path to fleetctl binary",
        },
        "FLEET_SERVER_URL": {
            "required": True,
            "description": "Path to fleetctl binary",
        },
        "FLEET_SERVER_ENROLL_SECRET": {
            "required": True,
            "description": "Enrollmen secret for FleetDM server",
        },
    }

    output_variables = {
        "fleetpkg": { "description": "Path to fleetdm pkg" },
        "fleetctl_version": { "description": "Version of fleetctl" }
    }

    def main(self):
        fleet_url = self.env["FLEET_SERVER_URL"]
        fleet_enroll_secret = self.env["FLEET_SERVER_ENROLL_SECRET"]
        fleet_server_url = self.env["FLEET_SERVER_URL"]
        
        if "PKG_NAME" in self.env:
            pkg_name = self.env["PKG_NAME"]
        else:
            pkg_name = self.env["NAME"]
            
        if "PKG_IDENTIFIER" in self.env:
            pkg_identifier = self.env["PKG_IDENTIFIER"]
        else:
            pkg_identifier = reverse_domain(fleet_url) + f'.{pkg_name}'
            
        try:
            # test the fleetctl file first
            fleetctl = pathlib.Path(self.env["fleetctl_path"]) # Downloaded binary
            outdir = pathlib.Path(self.env["RECIPE_CACHE_DIR"]) / self.env["NAME"]
            outdir.mkdir(parents=True, exist_ok=True)
            pkg_path = outdir / f'{pkg_name}.pkg'

            run_arguments = [f'package',
                             f'--type=pkg',
                             f'--fleet-url={fleet_server_url}',
                             f'--enroll-secret={fleet_enroll_secret}',
                             f'--indentifier={pkg_identifier}',
                             f'--outfile={pkg_path}']
            #     --fleet-certificate="${instance}.pem"
            
            subprocess.run(['/tmp/dumpargs.py'] + run_arguments )
            result = subprocess.run([f'{fleetctl}', '--version'],
                           capture_output=True,
                           text=True,
                           check=True)
            # self.output(result.stdout)
        except Exception as err:
            raise ProcessorError(err)
        self.env["fleetpkg"] = f'{pkg_path}'
        self.env["fleetctl_version"] = self.env["version"].split('v')[-1]
        
if __name__ == "__main__":
    PROC = FleetctlPkg()
    PROC.execute_shell()

