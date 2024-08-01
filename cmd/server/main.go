// Copyright (c) 2024 Robert Cronin
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

package server

import (
	"html/template"
	"log"
	"net/http"
	"os"

	"github.com/robert-cronin/kpa/internal/ai"
	"github.com/robert-cronin/kpa/internal/api"
	"github.com/robert-cronin/kpa/internal/db"
	"github.com/robert-cronin/kpa/internal/kubectl"
)

func Run() {
	err := db.InitDB("kpa.db")
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}

	log.Println("Database initialized")

	kubectlExecutor := kubectl.NewExecutor()

	aiChat := ai.NewChatHandler(kubectlExecutor)

	mux := http.NewServeMux()

	log.Println("Setting up routes...")

	// Set up API routes
	api.SetupRoutes(mux, kubectlExecutor, aiChat)

	// Serve static files
	fs := http.FileServer(http.Dir("web/static"))
	mux.Handle("GET /static/", http.StripPrefix("/static/", fs))

	// Parse templates
	templates := template.Must(template.ParseFiles(
		"web/templates/index.html",
		"web/templates/scenario_select.html",
	))

	// Handle the root route (scenario selection)
	mux.HandleFunc("GET /", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			log.Printf("Path not found: %s", r.URL.Path)
			http.NotFound(w, r)
			return
		}
		err := templates.ExecuteTemplate(w, "scenario_select.html", nil)
		if err != nil {
			log.Printf("Failed to execute template: %v", err)
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}
	})

	// Handle the scenario route
	mux.HandleFunc("GET /scenario/{id}", func(w http.ResponseWriter, r *http.Request) {
		err := templates.ExecuteTemplate(w, "index.html", nil)
		if err != nil {
			log.Printf("Failed to execute template: %v", err)
			http.Error(w, err.Error(), http.StatusInternalServerError)
		}
	})

	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
		log.Printf("Defaulting to port %s", port)
	}

	log.Printf("Starting server on :%s", port)
	if err := http.ListenAndServe(":"+port, mux); err != nil {
		log.Fatalf("Server failed to start: %v", err)
	}
}
