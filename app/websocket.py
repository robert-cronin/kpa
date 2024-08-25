# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from flask_socketio import SocketIO, emit
from app.services.kubectl import Executor
from app.utils.logger import logger

socketio = SocketIO()
kubectl_executor = Executor()


@socketio.on('connect')
def handle_connect():
    logger.info('Client connected')


@socketio.on('disconnect')
def handle_disconnect():
    logger.info('Client disconnected')


@socketio.on('input')
def handle_input(data):
    logger.info(f'Received input: {data}')
    try:
        if data.strip().lower() == 'exit':
            emit('output', '\r\nGoodbye!\r\n')
            return

        output = kubectl_executor.execute(data)
        emit('output', output)
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        emit('output', f"Error: {str(e)}\r\n")


def init_socketio(app):
    socketio.init_app(app)
