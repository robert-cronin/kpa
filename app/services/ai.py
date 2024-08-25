# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pydantic import BaseModel, Field
from typing import List, Optional
from openai import OpenAI
from app.services import db
from app.utils.logger import logger
import json

client = OpenAI()


# A dictionary containing 'commands' (list of strings) and 'explanation' (string)"
class KubernetesScenarioSolution(BaseModel):
    explanation: str
    commands: List[str]


class KubernetesScenario(BaseModel):
    title: str
    description: str
    setup_commands: List[str]
    tasks: List[str]
    hints: List[str]
    solution: KubernetesScenarioSolution
    verification_commands: List[str]


class ScenarioReflection(BaseModel):
    perceived_weaknesses: List[str]
    learning_opportunities: List[str]


class ScenarioResponse(BaseModel):
    scenarios: List[KubernetesScenario]


class ChatHandler:
    def __init__(self, kubectl_executor):
        self.kubectl_executor = kubectl_executor

    def generate_scenarios(self, prompt: str) -> ScenarioResponse:
        logger.info("Generating scenarios")
        notes = db.get_notes()
        last_scenario_id = db.get_last_scenario_id()
        previous_scenarios = [
            db.get_scenario(i) for i in range(max(1, last_scenario_id - 4), last_scenario_id + 1)
            if db.get_scenario(i) is not None
        ]
        
        num_scenarios = 1

        system_prompt = f"""
        You are a Kubernetes expert creating practice scenarios. Based on the user notes and previous
        scenarios, generate {num_scenarios} Kubernetes practice scenarios suitable for CKA/CKS exam preparation.
        Focus on addressing perceived weaknesses and providing learning opportunities.
        """
        try:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Notes: {notes}\nPrevious scenarios: {previous_scenarios}\nGenerate scenarios based on: {prompt}"}
                ],
                response_format=ScenarioResponse
            )
            response = completion.choices[0].message.parsed
            logger.info("Scenarios generated successfully")

            # Store the generated scenarios in the database
            for scenario in response.scenarios:
                db.store_scenario(scenario.model_dump())
                logger.info(f"Scenario stored: {scenario.title}")

            return response
        except Exception as e:
            logger.error(f"Error generating scenarios: {e}")
            raise

    def evaluate_progress(self, scenario_id: int, user_commands: List[str]) -> dict:
        logger.info(f"Evaluating progress for scenario_id: {scenario_id}")
        try:
            scenario = db.get_scenario(scenario_id)
            chat_history = db.get_chat_history(scenario_id)

            prompt = f"""
            Evaluate the progress on the following Kubernetes scenario:

            Scenario: {scenario}

            Chat history: {chat_history}

            User commands: {user_commands}

            Provide feedback and the next hint if needed.
            """

            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {"role": "system", "content": "You are a Kubernetes expert evaluating progress on a mock scenario."},
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
            logger.info(f"Evaluation completed for scenario_id: {scenario_id}")

            # Store the evaluation as a chat message
            db.store_chat_message(scenario_id, "assistant", json.dumps(evaluation))
            logger.info(f"Evaluation stored in chat history for scenario_id: {scenario_id}")

            # Update scenario progress
            current_progress = db.get_scenario_progress(scenario_id)
            if current_progress:
                completed_tasks = current_progress['completed_tasks']
                if evaluation['progress'] > len(completed_tasks) / len(scenario['tasks']):
                    completed_tasks.append(scenario['tasks'][len(completed_tasks)])
            else:
                completed_tasks = [scenario['tasks'][0]] if evaluation['progress'] > 0 else []

            db.update_scenario_progress(scenario_id, "in_progress", completed_tasks)
            logger.info(f"Scenario progress updated for scenario_id: {scenario_id}")

            return evaluation
        except Exception as e:
            logger.error(f"Error evaluating progress for scenario_id {scenario_id}: {e}")
            raise

    def explain_concept(self, concept: str) -> dict:
        logger.info(f"Explaining concept: {concept}")
        prompt = f"Explain the Kubernetes concept '{concept}'."

        try:
            completion = client.beta.chat.completions.parse(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {"role": "system", "content": "You are a Kubernetes expert explaining concepts."},
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

            explanation = json.loads(completion.choices[0].message.content)
            logger.info(f"Concept explained: {concept}")
            return explanation
        except Exception as e:
            logger.error(f"Error explaining concept {concept}: {e}")
            raise

    def troubleshoot_issue(self, problem_description: str, user_commands: List[str], system_output: str) -> dict:
        logger.info(f"Troubleshooting issue: {problem_description}")
        prompt = f"""
        Troubleshoot the following Kubernetes issue:

        Problem: {problem_description}
        User commands: {user_commands}
        System output: {system_output}

        Provide possible causes, suggested actions, and an explanation.
        """

        try:
            completion = client.chat.completions.create(
                model="gpt-4o-mini-2024-07-18",
                messages=[
                    {"role": "system", "content": "You are a Kubernetes expert troubleshooting issues."},
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

            troubleshooting = json.loads(completion.choices[0].message.content)
            logger.info(f"Issue troubleshooted: {problem_description}")
            return troubleshooting
        except Exception as e:
            logger.error(f"Error troubleshooting issue {problem_description}: {e}")
            raise