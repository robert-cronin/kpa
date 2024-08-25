# Copyright (c) 2024 Robert Cronin
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sqlite3
import json
from contextlib import contextmanager
from typing import List, Dict, Any
from datetime import datetime

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
        db.executescript('''
            CREATE TABLE IF NOT EXISTS scenarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                setup_commands TEXT NOT NULL,
                tasks TEXT NOT NULL,
                hints TEXT NOT NULL,
                solution TEXT NOT NULL,
                verification_commands TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_id INTEGER,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
            );

            CREATE TABLE IF NOT EXISTS scenario_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scenario_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                completed_tasks TEXT NOT NULL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
            );
        ''')
        db.commit()


def store_scenario(scenario: Dict[str, Any]) -> int:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO scenarios 
            (title, description, setup_commands, tasks, hints, solution, verification_commands)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            scenario['title'],
            scenario['description'],
            json.dumps(scenario['setup_commands']),
            json.dumps(scenario['tasks']),
            json.dumps(scenario['hints']),
            # Convert KubernetesScenarioSolution to dict
            json.dumps(scenario['solution']),
            json.dumps(scenario['verification_commands'])
        ))
        db.commit()
        return cursor.lastrowid


def get_scenario(scenario_id: int) -> Dict[str, Any]:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM scenarios WHERE id = ?", (scenario_id,))
        row = cursor.fetchone()
        if row:
            scenario = dict(row)
            for field in ['setup_commands', 'tasks', 'hints', 'solution', 'verification_commands']:
                if field in scenario and scenario[field]:
                    scenario[field] = json.loads(scenario[field])
                else:
                    scenario[field] = []
            return scenario
    return None


def store_note(content: str) -> int:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO notes (content) VALUES (?)",
            (content,)
        )
        db.commit()
        return cursor.lastrowid


def get_notes() -> List[Dict[str, Any]]:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]


def store_chat_message(scenario_id: int, role: str, content: str) -> int:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO chat_history (scenario_id, role, content) VALUES (?, ?, ?)",
            (scenario_id, role, content)
        )
        db.commit()
        return cursor.lastrowid


def get_chat_history(scenario_id: int) -> List[Dict[str, Any]]:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM chat_history WHERE scenario_id = ? ORDER BY timestamp",
            (scenario_id,)
        )
        return [dict(row) for row in cursor.fetchall()]


def update_scenario_progress(scenario_id: int, status: str, completed_tasks: List[str]) -> None:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO scenario_progress 
            (scenario_id, status, completed_tasks, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (
            scenario_id,
            status,
            json.dumps(completed_tasks),
            datetime.now().isoformat()
        ))
        db.commit()


def get_scenario_progress(scenario_id: int) -> Dict[str, Any]:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM scenario_progress WHERE scenario_id = ?",
            (scenario_id,)
        )
        row = cursor.fetchone()
        if row:
            progress = dict(row)
            progress['completed_tasks'] = json.loads(
                progress['completed_tasks'])
            return progress
    return None


def get_all_scenarios() -> List[Dict[str, Any]]:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, title, description FROM scenarios ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]


def get_last_scenario_id() -> int:
    with get_db() as db:
        cursor = db.cursor()
        cursor.execute("SELECT MAX(id) FROM scenarios")
        result = cursor.fetchone()
        return result[0] if result[0] is not None else 0
