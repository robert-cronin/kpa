# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from app.models.scenarios import Scenario


class ChatHandler:
    def __init__(self, kubectl_executor):
        self.kubectl_executor = kubectl_executor

    def generate_response(self, message, scenario_id):
        # TODO: Implement AI-based response generation
        return "AI response to: " + message

    def generate_scenarios(self, prompt):
        # TODO: Implement AI-based scenario generation
        # For now, return mock scenarios
        return [
            Scenario(
                id=1,
                name="Mock Scenario 1",
                description=f"A scenario based on the prompt: {prompt}",
                tasks=["Task 1", "Task 2", "Task 3"],
                validation="Validation criteria"
            ),
            Scenario(
                id=2,
                name="Mock Scenario 2",
                description=f"Another scenario based on the prompt: {prompt}",
                tasks=["Task 1", "Task 2", "Task 3"],
                validation="Validation criteria"
            ),
            Scenario(
                id=3,
                name="Mock Scenario 3",
                description=f"Yet another scenario based on the prompt: {
                    prompt}",
                tasks=["Task 1", "Task 2", "Task 3"],
                validation="Validation criteria"
            ),
            Scenario(
                id=4,
                name="Mock Scenario 4",
                description=f"One more scenario based on the prompt: {prompt}",
                tasks=["Task 1", "Task 2", "Task 3"],
                validation="Validation criteria"
            )
        ]
