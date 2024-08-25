// Copyright (c) 2024 Robert Cronin
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

document.addEventListener("DOMContentLoaded", () => {
  const scenarioPrompt = document.getElementById("scenario-prompt");
  const generateButton = document.getElementById("generate-scenarios");
  const feelingLuckyButton = document.getElementById("feeling-lucky");
  const scenarioList = document.getElementById("scenario-list");

  function displayScenarios(scenarios) {
    scenarioList.innerHTML = scenarios
      .map(
        (scenario, index) => `
        <div class="scenario-option" data-id="${scenario.id}">
          <h3>Scenario ${index + 1}: ${scenario.title}</h3>
          <div class="description-container">
            <p class="description">${scenario.description.slice(0, 100)}${
          scenario.description.length > 100 ? "..." : ""
        }</p>
            <button class="expand-btn">Show More</button>
          </div>
          ${
            scenario.tasks
              ? `
          <div class="tasks-container">
            <button class="show-tasks-btn">Show Tasks</button>
            <ul class="tasks-list hidden">
              ${scenario.tasks.map((task) => `<li>${task}</li>`).join("")}
            </ul>
          </div>
          `
              : ""
          }
          <div class="button-container">
            <button onclick="selectScenario(${scenario.id})">Select</button>
            <button class="delete-btn" data-id="${scenario.id}">Delete</button>
          </div>
        </div>
      `
      )
      .join("");

    // Add event listeners for expand buttons
    document.querySelectorAll(".expand-btn").forEach((btn) => {
      btn.addEventListener("click", function () {
        const descContainer = this.closest(".description-container");
        const descP = descContainer.querySelector(".description");
        if (this.textContent === "Show More") {
          descP.textContent = scenarios.find(
            (s) =>
              s.id === parseInt(this.closest(".scenario-option").dataset.id)
          ).description;
          this.textContent = "Show Less";
        } else {
          descP.textContent =
            scenarios
              .find(
                (s) =>
                  s.id === parseInt(this.closest(".scenario-option").dataset.id)
              )
              .description.slice(0, 100) + "...";
          this.textContent = "Show More";
        }
      });
    });

    // Add event listeners for show tasks buttons
    document.querySelectorAll(".show-tasks-btn").forEach((btn) => {
      btn.addEventListener("click", function () {
        const tasksList = this.nextElementSibling;
        tasksList.classList.toggle("hidden");
        this.textContent = tasksList.classList.contains("hidden")
          ? "Show Tasks"
          : "Hide Tasks";
      });
    });

    // Add event listeners for delete buttons
    document.querySelectorAll(".delete-btn").forEach((btn) => {
      btn.addEventListener("click", function () {
        const scenarioId = this.dataset.id;
        if (confirm("Are you sure you want to delete this scenario?")) {
          deleteScenario(scenarioId);
        }
      });
    });
  }

  function fetchExistingScenarios() {
    fetch("/api/scenarios")
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((scenarios) => {
        displayScenarios(scenarios);
      })
      .catch((error) => {
        console.error("Error fetching existing scenarios:", error);
        scenarioList.innerHTML =
          "<p>Error loading scenarios. Please try refreshing the page.</p>";
      });
  }

  function generateScenarios(prompt = "") {
    fetch("/api/generate-scenarios", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt }),
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((scenarios) => {
        displayScenarios(scenarios);
      })
      .catch((error) => {
        console.error("Error generating scenarios:", error);
        scenarioList.innerHTML =
          "<p>Error generating scenarios. Please try again.</p>";
      });
  }

  function deleteScenario(id) {
    fetch(`/api/scenarios/${id}`, {
      method: "DELETE",
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(() => {
        fetchExistingScenarios();
      })
      .catch((error) => {
        console.error("Error deleting scenario:", error);
        alert("Error deleting scenario. Please try again.");
      });
  }

  generateButton.addEventListener("click", () => {
    generateScenarios(scenarioPrompt.value);
  });

  feelingLuckyButton.addEventListener("click", () => {
    scenarioPrompt.value = "";
    generateScenarios();
  });

  fetchExistingScenarios();
});

// Define selectScenario in the global scope
window.selectScenario = function (id) {
  window.location.href = `/scenario/${id}`;
};
