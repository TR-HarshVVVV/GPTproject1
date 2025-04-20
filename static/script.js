// Global variables
let selectedModel = "mistral";
let currentChatId = null;
let chatHistory = [];
let chats = JSON.parse(localStorage.getItem("chats") || "[]");

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
    if (models) {
      modelSelector.innerHTML = models
        .map((model) => `<option value="${model}">${model}</option>`)
        .join("");
      selectedModel = models[0];
    }
  } catch (error) {
    console.error("Error loading models:", error);
  }
}

// Load chats from localStorage
function loadChats() {
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

// Save chats to localStorage
function saveChats() {
  localStorage.setItem("chats", JSON.stringify(chats));
}

// Create a new chat
function createNewChat() {
  currentChatId = Date.now().toString();
  const newChat = {
    id: currentChatId,
    title: "New Chat",
    messages: [],
  };
  chats.unshift(newChat);
  saveChats();
  loadChats();
  showWelcomeMessage();
}

// Delete a chat
function deleteChat(chatId) {
  chats = chats.filter((chat) => chat.id !== chatId);
  if (currentChatId === chatId) {
    currentChatId = null;
    showWelcomeMessage();
  }
  saveChats();
  loadChats();
}

// Switch to a different chat
function switchChat(chatId) {
  currentChatId = chatId;
  const chat = chats.find((c) => c.id === chatId);
  if (chat) {
    messagesContainer.innerHTML = chat.messages
      .map((msg) => createMessageHTML(msg))
      .join("");
    loadChats(); // Update active state
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

  // Add user message to UI and chat history
  const userMessage = { role: "user", content: message };
  messagesContainer.innerHTML += createMessageHTML(userMessage);
  const chat = chats.find((c) => c.id === currentChatId);
  chat.messages.push(userMessage);

  // Update chat title if it's the first message
  if (chat.title === "New Chat") {
    chat.title = message.slice(0, 30) + (message.length > 30 ? "..." : "");
    loadChats();
  }

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

    // Add assistant message to UI and chat history
    const assistantMessage = { role: "assistant", content: data.response };
    messagesContainer.innerHTML += createMessageHTML(assistantMessage);
    chat.messages.push(assistantMessage);

    saveChats();
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
