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
      fontFamily: 'Menlo, Monaco, "Courier New", monospace',
      theme: {
        background: "#282a36",
        foreground: "#f8f8f2",
        cursor: "#f8f8f2",
        selection: "rgba(248,248,242,0.3)",
        black: "#000000",
        red: "#ff5555",
        green: "#50fa7b",
        yellow: "#f1fa8c",
        blue: "#bd93f9",
        magenta: "#ff79c6",
        cyan: "#8be9fd",
        white: "#bfbfbf",
        brightBlack: "#4d4d4d",
        brightRed: "#ff6e67",
        brightGreen: "#5af78e",
        brightYellow: "#f4f99d",
        brightBlue: "#caa9fa",
        brightMagenta: "#ff92d0",
        brightCyan: "#9aedfe",
        brightWhite: "#e6e6e6",
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
      term.write(
        "\r\n\x1b[1;32m➜ \x1b[1;36mKubernetes Practice Assistant\x1b[0m\r\n"
      );
      writePrompt();
    });

    socket.on("output", (data) => {
      // Improve output formatting
      const formattedOutput = formatOutput(data);
      term.write(formattedOutput);
      writePrompt();
    });

    // Update the socket.on('output') handler
    socket.on("output", (data) => {
      const formattedOutput = formatOutput(data);
      term.write(formattedOutput);
      writePrompt();
    });



    let currentLine = "";
    let commandHistory = [];
    let historyIndex = -1;

    term.onKey(({ key, domEvent }) => {
      const printable = !domEvent.altKey && !domEvent.ctrlKey && !domEvent.metaKey;

      if (domEvent.keyCode === 13) { // Enter key
        term.write("\r\n");
        if (currentLine.trim()) {
          processCommand(currentLine);
          commandHistory.push(currentLine);
          historyIndex = commandHistory.length;
        }
        currentLine = "";
      } else if (domEvent.keyCode === 8) { // Backspace
        if (currentLine.length > 0) {
          currentLine = currentLine.slice(0, -1);
          term.write("\b \b");
        }
      } else if (domEvent.keyCode === 38) { // Up arrow
        if (historyIndex > 0) {
          historyIndex--;
          currentLine = commandHistory[historyIndex];
          term.write('\r\x1B[K' + getPrompt() + currentLine);
        }
      } else if (domEvent.keyCode === 40) { // Down arrow
        if (historyIndex < commandHistory.length - 1) {
          historyIndex++;
          currentLine = commandHistory[historyIndex];
          term.write('\r\x1B[K' + getPrompt() + currentLine);
        } else if (historyIndex === commandHistory.length - 1) {
          historyIndex = commandHistory.length;
          currentLine = '';
          term.write('\r\x1B[K' + getPrompt());
        }
      } else if (printable) {
        currentLine += key;
        term.write(key);
      }
    });

    function processCommand(command) {
      if (command.trim() === 'clear') {
        term.clear();
      } else if (command.startsWith('k ') || command.startsWith('kubectl ')) {
        // Handle kubectl commands
        const kubectlCommand = command.replace(/^k /, 'kubectl ');
        socket.emit("input", kubectlCommand);
      } else {
        socket.emit("input", command);
      }
    }

    socket.on("output", (data) => {
      const formattedOutput = formatOutput(data);
      term.writeln(formattedOutput);
      writePrompt();
    });

    function writePrompt() {
      term.write(getPrompt());
    }

    function getPrompt() {
      return "\r\n\x1B[1;32m➜\x1B[0m \x1B[1;34m~/kubernetes\x1B[0m \x1B[1;36m(main)\x1B[0m $ ";
    }

    writePrompt();
  }

  // function writePrompt() {
  //   const username = "user";
  //   const hostname = "kpa";
  //   const currentDir = "~/kubernetes";
  //   const gitBranch = "main";
  //   term.write(
  //     `\r\n\x1b[1;32m➜ \x1b[1;36m${username}@${hostname}\x1b[0m:\x1b[1;34m${currentDir}\x1b[0m \x1b[1;33m(${gitBranch})\x1b[0m `
  //   );
  // }
  //
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


  function formatOutput(outputData) {
    try {
      const data = JSON.parse(outputData);
      switch (data.type) {
        case "ls":
          return formatLsOutput(data.content);
        case "error":
          return `\x1B[1;31m${data.content}\x1B[0m`;
        case "text":
          return data.content;
        default:
          return outputData;
      }
    } catch (e) {
      console.error("Error parsing output:", e);
      return outputData;
    }
  }

  function formatLsOutput(files) {
    const columns = 4; // Number of columns for ls output
    const formattedFiles = files.map(file => {
      if (file.endsWith("/")) {
        // Blue for directories
        return `\x1B[1;34m${file.padEnd(20)}\x1B[0m`;
      } else if (file.match(/\.(exe|sh|bat)$/)) {
        // Green for executables
        return `\x1B[1;32m${file.padEnd(20)}\x1B[0m`;
      }
      return file.padEnd(20);
    });

    let output = "";
    for (let i = 0; i < formattedFiles.length; i += columns) {
      output += formattedFiles.slice(i, i + columns).join("") + "\r\n";
    }
    return output;
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
