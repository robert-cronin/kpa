# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import subprocess
from app.utils.logger import logger


class Executor:
    def execute(self, command):
        logger.info(f"Executing command: {command}")
        args = command.split()
        if not args or args[0] != "kubectl":
            logger.error(f"Invalid kubectl command: {command}")
            raise ValueError(f"Invalid kubectl command: {command}")

        try:
            result = subprocess.run(
                args, capture_output=True, text=True, check=True)
            logger.info(f"Command executed successfully: {command}")
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.error(f"Command failed: {command}\nStderr: {e.stderr}")
            raise Exception(f"Command failed: {e}\nStderr: {e.stderr}")
