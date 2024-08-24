# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import subprocess


class Executor:
    def execute(self, command):
        args = command.split()
        if not args or args[0] != "kubectl":
            raise ValueError(f"Invalid kubectl command: {command}")

        try:
            result = subprocess.run(
                args, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise Exception(f"Command failed: {e}\nStderr: {e.stderr}")
