// Function to add a message to the chat
function addMessage(message, isUser) {
  const chatMessages = document.getElementById("chat-messages");
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${isUser ? "user-message" : "ai-message"}`;
  messageDiv.textContent = message;
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to send a message
async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();

  if (message === "") return;

  // Add user message to chat
  addMessage(message, true);
  input.value = "";

  try {
    // Send message to server
    const response = await fetch("/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: message }),
    });

    const data = await response.json();

    if (data.error) {
      addMessage("Sorry, there was an error processing your request.", false);
    } else {
      addMessage(data.response, false);
    }
  } catch (error) {
    addMessage("Sorry, there was an error connecting to the server.", false);
  }
}

// Allow sending message with Enter key
document
  .getElementById("user-input")
  .addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
