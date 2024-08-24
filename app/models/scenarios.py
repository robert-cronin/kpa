# Copyright (c) 2024 Robert Cronin
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from dataclasses import dataclass
from typing import List

@dataclass
class Scenario:
    id: int
    name: str
    description: str
    tasks: List[str]
    validation: str