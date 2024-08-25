# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import subprocess
import json
import os
from flask_socketio import SocketIO, emit
from app.utils.logger import logger

socketio = SocketIO()


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
            emit('output', json.dumps(
                {'type': 'text', 'content': 'Goodbye!\r\n'}))
            return

        command = data.split()[0]
        if command == 'ls':
            output = handle_ls_command(data)
        elif command == 'cd':
            output = handle_cd_command(data)
        elif command == 'pwd':
            output = handle_pwd_command()
        else:
            output = run_command(data)

        emit('output', json.dumps(output))
    except Exception as e:
        logger.error(f"Error executing command: {e}")
        emit('output', json.dumps(
            {'type': 'error', 'content': f"Error: {str(e)}\r\n"}))


def run_command(command):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    stdout, stderr = process.communicate()

    if stderr:
        return {'type': 'error', 'content': stderr}
    return {'type': 'text', 'content': stdout}


def handle_ls_command(command):
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        files = output.strip().split('\n')
        return {'type': 'ls', 'content': files}
    except subprocess.CalledProcessError as e:
        return {'type': 'error', 'content': str(e)}


def handle_cd_command(command):
    try:
        path = command.split(maxsplit=1)[1] if len(
            command.split()) > 1 else '~'
        os.chdir(os.path.expanduser(path))
        return {'type': 'text', 'content': ''}
    except FileNotFoundError:
        return {'type': 'error', 'content': f"cd: no such file or directory: {path}\n"}
    except Exception as e:
        return {'type': 'error', 'content': str(e)}


def handle_pwd_command():
    return {'type': 'text', 'content': f"{os.getcwd()}\n"}


def init_socketio(app):
    socketio.init_app(app)
