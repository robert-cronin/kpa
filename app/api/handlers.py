# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
from flask import jsonify, request
from app.services import db, ai
from app.utils.logger import logger


class Handler:
    def __init__(self, kubectl_executor, ai_chat):
        self.kubectl_executor = kubectl_executor
        self.ai_chat = ai_chat

    def handle_generate_scenarios(self):
        logger.info("Generating scenarios")
        data = request.json
        prompt = data.get('prompt', '')

        try:
            generated_scenarios = self.ai_chat.generate_scenarios(prompt)
            stored_scenarios = []

            for scenario in generated_scenarios.scenarios:
                scenario_dict = scenario.dict()
                id = db.store_scenario(scenario_dict)
                stored_scenarios.append({
                    'id': id,
                    'title': scenario_dict['title'],
                    'description': scenario_dict['description']
                })

            logger.info("Scenarios generated and stored successfully")
            return jsonify(stored_scenarios)
        except Exception as e:
            logger.error(f"Error generating scenarios: {e}")
            return jsonify({"error": "Failed to generate scenarios"}), 500

    def get_all_scenarios(self):
        logger.info("Fetching all scenarios")
        try:
            scenarios = db.get_all_scenarios()
            logger.info("All scenarios fetched successfully")
            return jsonify(scenarios)
        except Exception as e:
            logger.error(f"Error fetching all scenarios: {e}")
            return jsonify({"error": "Failed to fetch scenarios"}), 500

    def handle_get_scenario(self, id):
        logger.info(f"Fetching scenario with id: {id}")
        try:
            scenario = db.get_scenario(id)
            if scenario:
                logger.info(f"Scenario with id {id} fetched successfully")
                return jsonify(scenario)
            logger.warning(f"Scenario with id {id} not found")
            return jsonify({'error': 'Scenario not found'}), 404
        except Exception as e:
            logger.error(f"Error fetching scenario with id {id}: {e}")
            return jsonify({"error": "Failed to fetch scenario"}), 500

    def handle_validate(self, id):
        logger.info(f"Validating scenario with id: {id}")
        try:
            # Implementation for validating a scenario
            pass
        except Exception as e:
            logger.error(f"Error validating scenario with id {id}: {e}")
            return jsonify({"error": "Failed to validate scenario"}), 500

    def handle_ai_chat(self):
        logger.info("Handling AI chat request")
        data = request.json
        message = data.get('message')
        scenario_id = data.get('scenarioId')

        try:
            response = self.ai_chat.generate_response(message, scenario_id)
            logger.info("AI chat response generated successfully")
            return jsonify({'response': response})
        except Exception as e:
            logger.error(f"Error handling AI chat request: {e}")
            return jsonify({"error": "Failed to handle AI chat request"}), 500
