// Copyright (c) 2024 Robert Cronin
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

package api

import (
	"net/http"

	"github.com/robert-cronin/kpa/internal/ai"
	"github.com/robert-cronin/kpa/internal/kubectl"
)

func SetupRoutes(mux *http.ServeMux, kubectlExecutor *kubectl.Executor, aiChat *ai.ChatHandler) {
	handler := NewHandler(kubectlExecutor, aiChat)

	mux.HandleFunc("GET /api/scenarios/{id}", handler.HandleGetScenario)
	mux.HandleFunc("POST /api/scenarios/{id}/validate", handler.HandleValidate)
	mux.HandleFunc("POST /api/ai-chat", handler.HandleAIChat)
	mux.HandleFunc("POST /api/generate-scenarios", handler.HandleGenerateScenarios)
}
