// Copyright (c) 2024 Robert Cronin
//
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT

document.addEventListener("DOMContentLoaded", async () => {
  const scenarioTitle = document.getElementById("scenario-title");
  const scenarioDescription = document.getElementById("scenario-description");
  const taskList = document.getElementById("task-list");
  const checkButton = document.getElementById("check-button");
  const checkOutput = document.getElementById("check-output");
  const chatMessages = document.getElementById("chat-messages");
  const userInput = document.getElementById("user-input");
  const sendButton = document.getElementById("send-button");

  let currentScenarioId = null;
  let term = null;
  let socket = null;

  function initializeTerminal() {
    const terminalElement = document.getElementById("terminal");
    term = new Terminal({
      cursorBlink: true,
      fontSize: 14,
      fontFamily: 'Consolas, "Courier New", monospace',
      theme: {
        background: "#1e1e1e",
      },
    });
    term.open(terminalElement);

    function fitTerminal() {
      const CHAR_WIDTH = 9;
      const CHAR_HEIGHT = 17;

      const cols = Math.floor(terminalElement.clientWidth / CHAR_WIDTH);
      const rows = Math.floor(terminalElement.clientHeight / CHAR_HEIGHT);

      term.resize(cols, rows);
    }

    fitTerminal();
    window.addEventListener("resize", fitTerminal);

    socket = io();

    socket.on("connect", () => {
      term.write("\r\n*** Connected to server ***\r\n");
      term.write("$ ");
    });

    socket.on("output", (data) => {
      term.write(data);
      term.write("\r\n$ ");
    });

    let currentLine = "";
    term.onKey(({ key, domEvent }) => {
      const printable =
        !domEvent.altKey && !domEvent.ctrlKey && !domEvent.metaKey;

      if (domEvent.keyCode === 13) {
        socket.emit("input", currentLine);
        currentLine = "";
        term.write("\r\n");
      } else if (domEvent.keyCode === 8) {
        if (currentLine.length > 0) {
          currentLine = currentLine.slice(0, -1);
          term.write("\b \b");
        }
      } else if (printable) {
        currentLine += key;
        term.write(key);
      }
    });
  }

  function loadScenario() {
    const urlParams = new URLSearchParams(window.location.search);
    const scenarioId = urlParams.get("id");

    if (scenarioId) {
      fetch(`/api/scenarios/${scenarioId}`)
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((scenario) => {
          console.log("Scenario loaded:", scenario);
          currentScenarioId = scenario.id;
          scenarioTitle.textContent = scenario.title;
          scenarioDescription.textContent = scenario.description;
          taskList.innerHTML = scenario.tasks
            .map((task) => `<li>${task}</li>`)
            .join("");
          addMessage(
            "ai",
            "Welcome to the new scenario! How can I assist you?"
          );
        })
        .catch((error) => {
          console.error("Error loading scenario:", error);
          scenarioTitle.textContent = "Error loading scenario";
          scenarioDescription.textContent = "Please try refreshing the page.";
        });
    } else {
      scenarioTitle.textContent = "No scenario selected";
      scenarioDescription.textContent =
        "Please select a scenario from the home page.";
    }
  }

  function addMessage(sender, content) {
    const messageElement = document.createElement("div");
    messageElement.classList.add("message", `${sender}-message`);
    messageElement.textContent = content;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
  }

  function sendMessage() {
    const message = userInput.value.trim();
    if (message) {
      addMessage("user", message);
      userInput.value = "";

      fetch("/api/ai-chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message, scenarioId: currentScenarioId }),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
          return response.json();
        })
        .then((data) => {
          addMessage("ai", data.response);
        })
        .catch((error) => {
          console.error("Error sending message:", error);
          addMessage(
            "ai",
            "Sorry, there was an error processing your message. Please try again."
          );
        });
    }
  }

  checkButton.addEventListener("click", () => {
    fetch(`/api/scenarios/${currentScenarioId}/validate`, { method: "POST" })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        checkOutput.textContent = data.message;
      })
      .catch((error) => {
        console.error("Error validating scenario:", error);
        checkOutput.textContent =
          "Error validating scenario. Please try again.";
      });
  });

  sendButton.addEventListener("click", sendMessage);

  userInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  loadScenario();
  initializeTerminal();
});

console.log("main.js loaded");
