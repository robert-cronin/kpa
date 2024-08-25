// Copyright (c) 2024 Robert Cronin
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

document.addEventListener("DOMContentLoaded", () => {
  const scenarioPrompt = document.getElementById("scenario-prompt");
  const generateButton = document.getElementById("generate-scenarios");
  const feelingLuckyButton = document.getElementById("feeling-lucky");
  const scenarioList = document.getElementById("scenario-list");

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
        scenarioList.innerHTML = scenarios
          .map(
            (scenario, index) => `
            <div class="scenario-option">
              <h3>Scenario ${index + 1}: ${scenario.title}</h3>
              <p>${scenario.description}</p>
              <button onclick="selectScenario(${scenario.id})">Select</button>
            </div>
          `
          )
          .join("");
      })
      .catch((error) => {
        console.error("Error generating scenarios:", error);
        scenarioList.innerHTML =
          "<p>Error generating scenarios. Please try again.</p>";
      });
  }

  generateButton.addEventListener("click", () => {
    generateScenarios(scenarioPrompt.value);
  });

  feelingLuckyButton.addEventListener("click", () => {
    scenarioPrompt.value = "";
    generateScenarios();
  });
});

// Define selectScenario in the global scope
window.selectScenario = function (id) {
  window.location.href = `/scenario/${id}`;
};
