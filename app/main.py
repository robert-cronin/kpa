# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import Flask, render_template
from app.api.routes import setup_routes
from app.services.db import init_db
from app.services.ai import ChatHandler
from app.services.kubectl import Executor
import os


def create_app():
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    app = Flask(__name__,
                template_folder=os.path.join(curr_dir, 'web/templates'),
                static_folder=os.path.join(curr_dir, 'web/static'))

    # Initialize database
    init_db('kpa.db')

    # Initialize services
    kubectl_executor = Executor()
    ai_chat = ChatHandler(kubectl_executor)

    # Setup routes
    setup_routes(app, kubectl_executor, ai_chat)

    @app.route('/')
    def scenario_select():
        return render_template('scenario_select.html')

    @app.route('/scenario/<int:id>')
    def scenario(id):
        return render_template('index.html')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)
