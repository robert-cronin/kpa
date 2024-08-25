# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask import Flask, render_template
from app.api.routes import setup_routes
from app.services.db import init_db
from app.services.ai import ChatHandler
from app.services.kubectl import Executor
from app.utils.logger import logger
import os


def create_app():
    curr_dir = os.path.dirname(os.path.realpath(__file__))
    app = Flask(__name__,
                template_folder=os.path.join(curr_dir, 'web/templates'),
                static_folder=os.path.join(curr_dir, 'web/static'))

    # Initialize database
    logger.info("Initializing database")
    init_db('kpa.db')
    logger.info("Database initialized successfully")

    # Initialize services
    logger.info("Initializing services")
    kubectl_executor = Executor()
    ai_chat = ChatHandler(kubectl_executor)
    logger.info("Services initialized successfully")

    # Setup routes
    logger.info("Setting up routes")
    setup_routes(app, kubectl_executor, ai_chat)
    logger.info("Routes set up successfully")

    @app.route('/')
    def scenario_select():
        logger.info("Rendering scenario_select.html")
        return render_template('scenario_select.html')

    @app.route('/scenario/<int:id>')
    def scenario(id):
        logger.info(f"Rendering index.html for scenario id: {id}")
        return render_template('index.html')

    return app


if __name__ == '__main__':
    logger.info("Starting application")
    app = create_app()
    app.run(debug=True, port=8080)
    logger.info("Application started successfully")
