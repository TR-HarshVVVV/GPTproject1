// Global variables
let selectedModel = "mistral";
let currentChatId = null;
let chats = [];

// DOM Elements
const messagesContainer = document.querySelector(".messages-container");
const userInput = document.querySelector("#user-input");
const sendButton = document.querySelector("#send-button");
const modelSelector = document.querySelector("#model-selector");
const newChatButton = document.querySelector("#new-chat");
const chatHistoryContainer = document.querySelector(".chat-history");

// Event Listeners
document.addEventListener("DOMContentLoaded", () => {
  initializeChat();
  setupAutoResize();
});

// Setup auto-resize for textarea
function setupAutoResize() {
  userInput.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
  });
}

// Initialize the chat interface
function initializeChat() {
  loadChats();
  loadModels();
  setupEventListeners();
  showWelcomeMessage();
}

// Load available models
async function loadModels() {
  try {
    const response = await fetch("/api/models");
    const models = await response.json();
    if (models && models.length > 0) {
      modelSelector.innerHTML = models
        .map((model) => `<option value="${model}">${model}</option>`)
        .join("");
      selectedModel = models[0];
    } else {
      console.error("No models available");
      modelSelector.innerHTML = '<option value="mistral">mistral</option>';
    }
  } catch (error) {
    console.error("Error loading models:", error);
    modelSelector.innerHTML = '<option value="mistral">mistral</option>';
  }
}

// Load chats from the server
async function loadChats() {
  try {
    const response = await fetch("/api/chats");
    const data = await response.json();
    if (data.chats) {
      chats = data.chats;
      chatHistoryContainer.innerHTML = chats
        .map(
          (chat) => `
        <div class="chat-item ${
          chat.id === currentChatId ? "active" : ""
        }" data-chat-id="${chat.id}">
          <span>${chat.title || "New Chat"}</span>
          <i class="fas fa-trash delete-btn"></i>
        </div>
      `
        )
        .join("");
    }
  } catch (error) {
    console.error("Error loading chats:", error);
    chatHistoryContainer.innerHTML =
      '<div class="error">Failed to load chats</div>';
  }
}

// Create a new chat
async function createNewChat() {
  try {
    const response = await fetch("/api/chats", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: "New Chat",
        model: modelSelector.value,
      }),
    });

    const data = await response.json();
    if (data.chat_id) {
      currentChatId = data.chat_id;
      await loadChats();
      showWelcomeMessage();
    }
  } catch (error) {
    console.error("Error creating chat:", error);
  }
}

// Delete a chat
async function deleteChat(chatId) {
  try {
    const response = await fetch(`/api/chats/${chatId}`, {
      method: "DELETE",
    });

    if (response.ok) {
      if (currentChatId === chatId) {
        currentChatId = null;
        showWelcomeMessage();
      }
      await loadChats();
    }
  } catch (error) {
    console.error("Error deleting chat:", error);
  }
}

// Switch to a different chat
async function switchChat(chatId) {
  try {
    const response = await fetch(`/api/chats/${chatId}`);
    const chat = await response.json();

    if (chat) {
      currentChatId = chatId;
      messagesContainer.innerHTML = chat.messages
        .map((msg) => createMessageHTML(msg))
        .join("");
      await loadChats(); // Update active state
    }
  } catch (error) {
    console.error("Error switching chat:", error);
  }
}

// Create message HTML
function createMessageHTML(message) {
  return `
    <div class="message ${message.role}-message">
      ${message.content}
    </div>
  `;
}

// Show welcome message
function showWelcomeMessage() {
  messagesContainer.innerHTML = `
    <div class="welcome-message">
      <h1>Welcome to Ollama Chat</h1>
      <p>Select a model and start a new conversation!</p>
    </div>
  `;
}

// Send message to the server
async function sendMessage() {
  const message = userInput.value.trim();
  if (!message || !currentChatId) return;

  // Add user message to UI
  const userMessage = { role: "user", content: message };
  messagesContainer.innerHTML += createMessageHTML(userMessage);

  // Clear input
  userInput.value = "";

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message,
        model: modelSelector.value,
        chat_id: currentChatId,
      }),
    });

    const data = await response.json();

    // Add assistant message to UI
    const assistantMessage = { role: "assistant", content: data.response };
    messagesContainer.innerHTML += createMessageHTML(assistantMessage);

    // Reload chats to update the UI
    await loadChats();
  } catch (error) {
    console.error("Error sending message:", error);
    messagesContainer.innerHTML += `
      <div class="message error-message">
        Error: Failed to get response from the server.
      </div>
    `;
  }
}

// Setup event listeners
function setupEventListeners() {
  // Send message on button click
  sendButton.addEventListener("click", sendMessage);

  // Send message on Enter (but allow Shift+Enter for new line)
  userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  // New chat button
  newChatButton.addEventListener("click", createNewChat);

  // Chat history item clicks
  chatHistoryContainer.addEventListener("click", (e) => {
    const chatItem = e.target.closest(".chat-item");
    if (chatItem) {
      if (e.target.classList.contains("delete-btn")) {
        deleteChat(chatItem.dataset.chatId);
      } else {
        switchChat(chatItem.dataset.chatId);
      }
    }
  });
}

modelSelector.addEventListener("change", (e) => {
  selectedModel = e.target.value;
});
