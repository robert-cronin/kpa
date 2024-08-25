# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
from flask import jsonify, request
from app.services import db, ai


class Handler:
    def __init__(self, kubectl_executor, ai_chat):
        self.kubectl_executor = kubectl_executor
        self.ai_chat = ai_chat

    def handle_generate_scenarios(self):
        data = request.json
        prompt = data.get('prompt', '')

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

        return jsonify(stored_scenarios)

    def handle_get_scenario(self, id):
        scenario = db.get_scenario(id)
        if scenario:
            return jsonify(scenario)
        return jsonify({'error': 'Scenario not found'}), 404

    def handle_validate(self, id):
        # Implementation for validating a scenario
        pass

    def handle_ai_chat(self):
        data = request.json
        message = data.get('message')
        scenario_id = data.get('scenarioId')

        response = self.ai_chat.generate_response(message, scenario_id)
        return jsonify({'response': response})
