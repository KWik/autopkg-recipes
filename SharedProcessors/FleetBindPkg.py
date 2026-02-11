#!/usr/local/autopkg/python
"""Generates a FleetDM bind pkg using fleetctl"""

from autopkglib import Processor, ProcessorError

import pathlib
import subprocess
import sys

__all__ = ["FleetBindPkg"]

def reverse_domain(url:str) -> str:
    return '.'.join(reversed(url.split('/')[-1].split('.')))
    

class FleetBindPkg(Processor):

    description = __doc__
    input_variables = {
        "fleetctl_path": {
            "required": True,
            "description": "Path to fleetctl binary",
        },
        "FLEET_SERVER_URL": {
            "required": True,
            "description": "URL to FleetDM server",
        },
        "FLEET_SERVER_ENROLL_SECRET": {
            "required": True,
            "description": "Enrollmen secret for FleetDM server",
        },
        "FLEET_BIND_PKG_IDENTIFIER": {
            "required": False,
            "description": "Identifier for output pkg",
        },
        "FLEET_BIND_PKG_NAME": {
            "required": False,
            "description": "Filename for output pkg",
        },
        "version": {
            "required": True,
            "description": "version of fleetctl, but in ill formed format",
        }
    }

    output_variables = {
        "fleetbindpkg": { "description": "Path to fleetdm pkg" },
        "fleetctl_version": { "description": "Version of fleetctl" }
    }

    def main(self):
        try:
            # Anything vital must be within the try
            fleet_url = self.env["FLEET_SERVER_URL"]
            fleet_enroll_secret = self.env["FLEET_SERVER_ENROLL_SECRET"]
            fleet_server_url = self.env["FLEET_SERVER_URL"]
            fleetctl = pathlib.Path(self.env["fleetctl_path"])

            fleet_server_hostname = fleet_server_url.split('.')[0].split('/')[-1]

            outdir = pathlib.Path(self.env["RECIPE_CACHE_DIR"]) / self.env["NAME"]
            outdir.mkdir(parents=True, exist_ok=True)
            
            pkg_name = self.env.get("version") + '-osquery-' + fleet_server_hostname
            if override_pkg_name := self.env.get("FLEET_BIND_PKG_NAME"):
                pkg_name = override_pkg_name
            pkg_path = outdir / f'{pkg_name}.pkg'
                
            run_arguments = [f'package',
                             f'--type=pkg',
                             f'--outfile={pkg_path}',
                             f'--fleet-url={fleet_server_url}',
                             f'--enroll-secret={fleet_enroll_secret}',]

            if pkg_identifier := self.env.get("FLEET_BIND_PKG_IDENTIFIER"):
                run_arguments.append(f'--indentifier={pkg_identifier}')
                # Error: --enroll-secret and --fleet-url must be provided together

            # Debug, not needed due to %version%
            # result = subprocess.run([f'{fleetctl}', '--version'],
            #                         capture_output=True,
            #                         text=True,
            #                         check=True)
            
            # Optional TODO
            #     --arch="aamd64"
            #     --fleet-certificate="{instance}.pem"
            
            subprocess.run([fleetctl] + run_arguments )
        except Exception as err:
            raise ProcessorError(err)
        self.env["fleetbindpkg"] = f'{pkg_path}'
        self.env["fleetctl_version"] = self.env["version"].split('v')[-1]
        
if __name__ == "__main__":
    PROC = FleetBindPkg()
    PROC.execute_shell()

