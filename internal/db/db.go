// Copyright (c) 2024 Robert Cronin
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

package db

import (
	"database/sql"
	"encoding/json"
	"fmt"

	_ "github.com/mattn/go-sqlite3"
	"github.com/robert-cronin/kpa/internal/models"
)

var DB *sql.DB

func InitDB(dbPath string) error {
	var err error
	DB, err = sql.Open("sqlite3", dbPath)
	if err != nil {
		return fmt.Errorf("error opening database: %v", err)
	}

	err = createTables()
	if err != nil {
		return fmt.Errorf("error creating tables: %v", err)
	}

	return nil
}

func createTables() error {
	_, err := DB.Exec(`
		CREATE TABLE IF NOT EXISTS scenarios (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT,
			description TEXT,
			tasks TEXT,
			validation TEXT
		);
		CREATE TABLE IF NOT EXISTS learner_notes (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			scenario_id INTEGER,
			note TEXT,
			timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (scenario_id) REFERENCES scenarios(id)
		);
	`)
	return err
}

func StoreScenario(scenario models.Scenario) (int64, error) {
	tasksJSON, err := json.Marshal(scenario.Tasks)
	if err != nil {
		return 0, fmt.Errorf("failed to marshal tasks: %w", err)
	}

	result, err := DB.Exec(
		"INSERT INTO scenarios (name, description, tasks, validation) VALUES (?, ?, ?, ?)",
		scenario.Name,
		scenario.Description,
		tasksJSON,
		scenario.Validation,
	)
	if err != nil {
		return 0, err
	}
	return result.LastInsertId()
}

func GetScenario(id int) (models.Scenario, error) {
	var scenario models.Scenario
	var tasksJSON string

	err := DB.QueryRow(
		"SELECT id, name, description, tasks, validation FROM scenarios WHERE id = ?",
		id,
	).Scan(&scenario.ID, &scenario.Name, &scenario.Description, &tasksJSON, &scenario.Validation)
	if err != nil {
		return models.Scenario{}, err
	}

	err = json.Unmarshal([]byte(tasksJSON), &scenario.Tasks)
	if err != nil {
		return models.Scenario{}, fmt.Errorf("failed to unmarshal tasks: %w", err)
	}

	return scenario, nil
}

func StoreLearnerNote(scenarioId int, note string) error {
	_, err := DB.Exec(
		"INSERT INTO learner_notes (scenario_id, note) VALUES (?, ?)",
		scenarioId,
		note,
	)
	return err
}

func GetLearnerNotes(scenarioId int) ([]string, error) {
	rows, err := DB.Query(
		"SELECT note FROM learner_notes WHERE scenario_id = ? ORDER BY timestamp",
		scenarioId,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var notes []string
	for rows.Next() {
		var note string
		if err := rows.Scan(&note); err != nil {
			return nil, err
		}
		notes = append(notes, note)
	}
	return notes, nil
}
