// Copyright (c) 2024 Robert Cronin
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

package api

import (
	"encoding/json"
	"log"
	"net/http"
	"strconv"

	"github.com/robert-cronin/kpa/internal/ai"
	"github.com/robert-cronin/kpa/internal/db"
	"github.com/robert-cronin/kpa/internal/kubectl"
	"github.com/robert-cronin/kpa/internal/models"
)

type Handler struct {
	kubectlExecutor *kubectl.Executor
	aiChat          *ai.ChatHandler
}

func NewHandler(kubectlExecutor *kubectl.Executor, aiChat *ai.ChatHandler) *Handler {
	return &Handler{
		kubectlExecutor: kubectlExecutor,
		aiChat:          aiChat,
	}
}

func (h *Handler) HandleGenerateScenarios(w http.ResponseWriter, r *http.Request) {
	var request struct {
		Prompt string `json:"prompt"`
	}
	if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
		log.Printf("Failed to decode request: %v", err)
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Use AI to generate scenarios based on the prompt
	generatedScenarios, err := h.aiChat.GenerateScenarios(request.Prompt)
	if err != nil {
		log.Printf("Failed to generate scenarios: %v", err)
		http.Error(w, "Failed to generate scenarios", http.StatusInternalServerError)

		return
	}

	// Store scenarios in the database and get their IDs
	storedScenarios := make([]models.Scenario, len(generatedScenarios))
	for i, scenario := range generatedScenarios {
		id, err := db.StoreScenario(models.Scenario{
			Name:        scenario.Name,
			Description: scenario.Description,
			Tasks:       scenario.Tasks,
			Validation:  scenario.Validation,
		})
		if err != nil {
			log.Printf("Failed to store scenarios: %v", err)
			http.Error(w, "Failed to store scenarios", http.StatusInternalServerError)
			return
		}
		storedScenarios[i] = models.Scenario{
			ID:          id,
			Name:        scenario.Name,
			Description: scenario.Description,
			Tasks:       scenario.Tasks,
			Validation:  scenario.Validation,
		}
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(storedScenarios)
}

func (h *Handler) HandleGetScenario(w http.ResponseWriter, r *http.Request) {
	idStr := r.URL.Path[len("/api/scenarios/"):]
	id, err := strconv.Atoi(idStr)
	if err != nil {
		log.Printf("Invalid scenario ID: %v", err)
		http.Error(w, "Invalid scenario ID", http.StatusBadRequest)
		return
	}

	scenario, err := db.GetScenario(id)
	if err != nil {
		log.Printf("Failed to get scenario: %v", err)
		http.Error(w, "Failed to get scenario", http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(scenario)
}

func (h *Handler) HandleValidate(w http.ResponseWriter, r *http.Request) {
	// Implementation for validating a scenario
}

func (h *Handler) HandleAIChat(w http.ResponseWriter, r *http.Request) {
	// Implementation for AI chat
}
