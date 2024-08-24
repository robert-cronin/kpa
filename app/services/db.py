# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sqlite3
import json
from contextlib import contextmanager

DATABASE = None


@contextmanager
def get_db():
    global DATABASE
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    try:
        yield db
    finally:
        db.close()


def init_db(db_path):
    global DATABASE
    DATABASE = db_path
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                description TEXT,
                tasks TEXT,
                validation TEXT
            )
        ''')
        db.execute('''
            CREATE TABLE IF NOT EXISTS learner_notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_id INTEGER,
                note TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
            )
        ''')
        db.commit()


def store_scenario(scenario):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO scenarios (name, description, tasks, validation) VALUES (?, ?, ?, ?)",
            (scenario['name'], scenario['description'], json.dumps(
                scenario['tasks']), scenario['validation'])
        )
        db.commit()
        return cursor.lastrowid


def get_scenario(id):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM scenarios WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            scenario = dict(row)
            scenario['tasks'] = json.loads(scenario['tasks'])
            return scenario
    return None


def store_learner_note(scenario_id, note):
    with get_db() as db:
        db.execute(
            "INSERT INTO learner_notes (scenario_id, note) VALUES (?, ?)",
            (scenario_id, note)
        )
        db.commit()


def get_learner_notes(scenario_id):
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT note FROM learner_notes WHERE scenario_id = ? ORDER BY timestamp",
            (scenario_id,)
        )
        return [row['note'] for row in cursor.fetchall()]
