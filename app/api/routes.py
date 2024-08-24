# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from app.api.handlers import Handler


def setup_routes(app, kubectl_executor, ai_chat):
    handler = Handler(kubectl_executor, ai_chat)

    @app.route('/api/scenarios/<int:id>', methods=['GET'])
    def get_scenario(id):
        return handler.handle_get_scenario(id)

    @app.route('/api/scenarios/<int:id>/validate', methods=['POST'])
    def validate_scenario(id):
        return handler.handle_validate(id)

    @app.route('/api/ai-chat', methods=['POST'])
    def ai_chat():
        return handler.handle_ai_chat()

    @app.route('/api/generate-scenarios', methods=['POST'])
    def generate_scenarios():
        return handler.handle_generate_scenarios()
