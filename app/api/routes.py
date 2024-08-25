# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import jsonify, request
from app.services import db
from app.api.handlers import Handler
from app.utils.logger import logger


def setup_routes(app, kubectl_executor, ai_chat):
    handler = Handler(kubectl_executor, ai_chat)

    @app.route('/api/scenarios/<int:id>', methods=['GET'])
    def get_scenario(id):
        logger.info(f"Fetching scenario with id: {id}")
        try:
            response = handler.handle_get_scenario(id)
            logger.info(f"Scenario with id {id} fetched successfully")
            return response
        except Exception as e:
            logger.error(f"Error fetching scenario with id {id}: {e}")
            return jsonify({"error": "Failed to fetch scenario"}), 500

    @app.route('/api/scenarios/<int:id>/validate', methods=['POST'])
    def validate_scenario(id):
        logger.info(f"Validating scenario with id: {id}")
        try:
            response = handler.handle_validate(id)
            logger.info(f"Scenario with id {id} validated successfully")
            return response
        except Exception as e:
            logger.error(f"Error validating scenario with id {id}: {e}")
            return jsonify({"error": "Failed to validate scenario"}), 500

    @app.route('/api/ai-chat', methods=['POST'])
    def ai_chat():
        logger.info("Received AI chat request")
        try:
            response = handler.handle_ai_chat()
            logger.info("AI chat request handled successfully")
            return response
        except Exception as e:
            logger.error(f"Error handling AI chat request: {e}")
            return jsonify({"error": "Failed to handle AI chat request"}), 500

    @app.route('/api/generate-scenarios', methods=['POST'])
    def generate_scenarios():
        logger.info("Generating scenarios")
        try:
            response = handler.handle_generate_scenarios()
            logger.info("Scenarios generated successfully")
            return response
        except Exception as e:
            logger.error(f"Error generating scenarios: {e}")
            return jsonify({"error": "Failed to generate scenarios"}), 500

    @app.route('/api/scenarios', methods=['GET'])
    def get_scenarios():
        logger.info("Fetching all scenarios")
        try:
            scenarios = db.get_all_scenarios()
            logger.info("All scenarios fetched successfully")
            return jsonify(scenarios)
        except Exception as e:
            logger.error(f"Error fetching all scenarios: {e}")
            return jsonify({"error": "Failed to fetch scenarios"}), 500

    @app.route('/api/scenarios/<int:id>', methods=['DELETE'])
    def delete_scenario(id):
        logger.info(f"Deleting scenario with id: {id}")
        try:
            success = db.delete_scenario(id)
            if success:
                logger.info(f"Scenario with id {id} deleted successfully")
                return jsonify({"message": "Scenario deleted successfully"}), 200
            else:
                logger.error(f"Failed to delete scenario with id: {id}")
                return jsonify({"error": "Failed to delete scenario"}), 500
        except Exception as e:
            logger.error(f"Error deleting scenario with id {id}: {e}")
            return jsonify({"error": "Failed to delete scenario"}), 500
