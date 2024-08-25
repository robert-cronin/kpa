# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pydantic import BaseModel, Field
from typing import List, Optional
from openai import OpenAI
from app.services import db
import json

client = OpenAI()


class Step(BaseModel):
    explanation: str
    output: str


class MathReasoning(BaseModel):
    steps: List[Step]
    final_answer: str


class Participant(BaseModel):
    name: str
    role: str


class KubernetesScenario(BaseModel):
    title: str
    description: str
    setup_commands: List[str]
    tasks: List[str]
    hints: List[str]
    solution: dict = Field(
        ..., description="A dictionary containing 'commands' (list of strings) and 'explanation' (string)")
    verification_commands: List[str]


class ScenarioResponse(BaseModel):
    reflections: dict = Field(
        ..., description="A dictionary containing 'perceived_weaknesses' and 'learning_opportunities' (both lists of strings)")
    scenarios: List[KubernetesScenario]


class ChatHandler:
    def __init__(self, kubectl_executor):
        self.kubectl_executor = kubectl_executor

    def generate_scenarios(self, prompt: str) -> ScenarioResponse:
        notes = db.get_notes()
        # Fetch only the most recent scenarios for context
        previous_scenarios = [db.get_scenario(i) for i in range(
            max(1, db.get_last_scenario_id() - 4), db.get_last_scenario_id() + 1)]

        system_prompt = f"""
        You are a Kubernetes expert creating practice scenarios. Based on the user notes and previous
        scenarios, generate 5 Kubernetes practice scenarios suitable for CKA/CKS exam preparation.
        Focus on addressing perceived weaknesses and providing learning opportunities. Reflect on
        the user's progress and generate scenarios accordingly.
        """
        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Notes: {notes}\nPrevious scenarios: {
                    previous_scenarios}\nGenerate scenarios based on: {prompt}"}
            ],
            response_format={"type": "json_schema",
                             "schema": ScenarioResponse.model_json_schema()}
        )

        response = ScenarioResponse.model_validate_json(
            completion.choices[0].message.content)

        # Store the generated scenarios in the database
        for scenario in response.scenarios:
            db.store_scenario(scenario.dict())

        return response

    def evaluate_progress(self, scenario_id: int, user_commands: List[str]) -> dict:
        scenario = db.get_scenario(scenario_id)
        chat_history = db.get_chat_history(scenario_id)

        prompt = f"""
        Evaluate the progress on the following Kubernetes scenario:

        Scenario: {scenario}

        Chat history: {chat_history}

        User commands: {user_commands}

        Provide feedback and the next hint if needed.
        """

        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                    "content": "You are a Kubernetes expert evaluating progress on a mock scenario."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_schema", "schema": {
                "type": "object",
                "properties": {
                    "progress": {"type": "number"},
                    "feedback": {"type": "string"},
                    "next_hint": {"type": "string"}
                },
                "required": ["progress", "feedback", "next_hint"],
                "additionalProperties": False
            }}
        )

        evaluation = json.loads(completion.choices[0].message.content)

        # Store the evaluation as a chat message
        db.store_chat_message(scenario_id, "assistant", json.dumps(evaluation))

        # Update scenario progress
        current_progress = db.get_scenario_progress(scenario_id)
        if current_progress:
            completed_tasks = current_progress['completed_tasks']
            if evaluation['progress'] > len(completed_tasks) / len(scenario['tasks']):
                completed_tasks.append(scenario['tasks'][len(completed_tasks)])
        else:
            completed_tasks = [scenario['tasks'][0]
                               ] if evaluation['progress'] > 0 else []

        db.update_scenario_progress(
            scenario_id, "in_progress", completed_tasks)

        return evaluation

    def explain_concept(self, concept: str) -> dict:
        prompt = f"Explain the Kubernetes concept '{concept}'."

        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                    "content": "You are a Kubernetes expert explaining concepts."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_schema", "schema": {
                "type": "object",
                "properties": {
                    "explanation": {"type": "string"},
                    "examples": {"type": "array", "items": {"type": "string"}},
                    "related_concepts": {"type": "array", "items": {"type": "string"}}
                },
                "required": ["explanation", "examples", "related_concepts"],
                "additionalProperties": False
            }}
        )

        return json.loads(completion.choices[0].message.content)

    def troubleshoot_issue(self, problem_description: str, user_commands: List[str], system_output: str) -> dict:
        prompt = f"""
        Troubleshoot the following Kubernetes issue:

        Problem: {problem_description}
        User commands: {user_commands}
        System output: {system_output}

        Provide possible causes, suggested actions, and an explanation.
        """

        completion = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system",
                    "content": "You are a Kubernetes expert troubleshooting issues."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_schema", "schema": {
                "type": "object",
                "properties": {
                    "possible_causes": {"type": "array", "items": {"type": "string"}},
                    "suggested_actions": {"type": "array", "items": {"type": "string"}},
                    "explanation": {"type": "string"}
                },
                "required": ["possible_causes", "suggested_actions", "explanation"],
                "additionalProperties": False
            }}
        )

        return json.loads(completion.choices[0].message.content)
