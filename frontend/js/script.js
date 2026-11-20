/* =========================================================
   API NEXUS - FRONTEND SCRIPT
   ========================================================= */

/* ---------------------------------------------------------
   1. SETTINGS
   --------------------------------------------------------- */

const API_URL = "/ask";
const HEALTH_URL = "/health";

const SAMPLE_QUESTIONS = [
    "How many UserEndpoint files are stored?",
    "Explain the POST endpoint.",
    "What parameters are required in GET?",
    "Explain the PUT endpoint.",
    "How does the DELETE endpoint work?",
    "Show the API request and response format."
];

// Page path -> id of the section to scroll to
const SECTION_BY_PATH = {
    "/home": "home",
    "/technology": "technology",
    "/workflow": "workflow"
};


/* ---------------------------------------------------------
   2. PAGE ELEMENTS
   --------------------------------------------------------- */

const chatWindow = document.getElementById("chatWindow");
const chatToggle = document.getElementById("chatToggle");
const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const questionInput = document.getElementById("questionInput");
const sendButton = document.getElementById("sendButton");


/* ---------------------------------------------------------
   3. OPEN / CLOSE THE CHAT WINDOW
   --------------------------------------------------------- */

function openChat() {
    chatWindow.classList.add("active");
    chatToggle.textContent = "×";
    questionInput.focus();
}

function closeChat() {
    chatWindow.classList.remove("active");
    chatToggle.textContent = "✦";
}

function toggleChat() {
    if (chatWindow.classList.contains("active")) {
        closeChat();
    } else {
        openChat();
    }
}


/* ---------------------------------------------------------
   4. CHAT MESSAGES
   --------------------------------------------------------- */

function renderWelcome() {
    chatMessages.replaceChildren();

    const welcome = document.createElement("div");
    welcome.className = "welcome-message";

    const heading = document.createElement("h3");
    heading.textContent = "Welcome to API Nexus AI";

    const subheading = document.createElement("h4");
    subheading.textContent = "Your intelligent API assistant is ready.";

    const intro = document.createElement("p");
    intro.textContent = "You can ask questions about your uploaded Python files:";

    welcome.append(heading, subheading, intro);

    SAMPLE_QUESTIONS.forEach(function (question) {
        const paragraph = document.createElement("p");
        paragraph.textContent = "• " + question;
        welcome.appendChild(paragraph);
    });

    const outro = document.createElement("p");
    outro.textContent = "Ask your question to get started.";
    welcome.appendChild(outro);

    chatMessages.appendChild(welcome);
}

function resetChat() {
    renderWelcome();
}

function addMessage(message, type) {
    const element = document.createElement("div");

    element.className = "message " + type;
    element.textContent = message;

    chatMessages.appendChild(element);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showTyping() {
    const element = document.createElement("div");

    element.className = "typing";
    element.id = "typingMessage";
    element.textContent = "AI Assistant is thinking...";

    chatMessages.appendChild(element);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeTyping() {
    const element = document.getElementById("typingMessage");

    if (element) {
        element.remove();
    }
}


/* ---------------------------------------------------------
   5. ASK A QUESTION (calls POST /ask)
   --------------------------------------------------------- */

async function askQuestion(question) {
    const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: question })
    });

    const data = await response.json();

    if (!response.ok) {
        const detail = typeof data.detail === "string"
            ? data.detail
            : JSON.stringify(data.detail || "Request failed");

        throw new Error(detail);
    }

    return data.answer
        || data.response
        || data.message
        || "No answer was returned by the server.";
}

chatForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    addMessage(question, "user-message");

    questionInput.value = "";
    questionInput.disabled = true;
    sendButton.disabled = true;

    showTyping();

    try {
        const answer = await askQuestion(question);

        removeTyping();
        addMessage(answer, "bot-message");

    } catch (error) {
        removeTyping();

        addMessage(
            "Unable to get an answer. Please check your FastAPI backend "
            + "and Bedrock configuration. Details: " + error.message,
            "bot-message"
        );

    } finally {
        questionInput.disabled = false;
        sendButton.disabled = false;
        questionInput.focus();
    }
});


/* ---------------------------------------------------------
   6. BACKEND STATUS (calls GET /health)
   --------------------------------------------------------- */

async function checkBackend() {
    const backendStatus = document.getElementById("backendStatus");
    const chatStatus = document.getElementById("chatStatus");

    try {
        const response = await fetch(HEALTH_URL);

        if (!response.ok) {
            throw new Error("Backend unavailable");
        }

        backendStatus.innerHTML =
            '<span class="status-indicator">●</span> Backend Connected';

        chatStatus.textContent = "● Online";
        chatStatus.style.color = "#a7ffd8";

    } catch (error) {
        backendStatus.textContent = "● Backend Not Connected";
        backendStatus.style.color = "#ff8585";

        chatStatus.textContent = "● Offline";
        chatStatus.style.color = "#ff8585";
    }
}


/* ---------------------------------------------------------
   7. PAGE NAVIGATION (/technology, /workflow ... scroll to section)
   --------------------------------------------------------- */

function scrollToCurrentSection() {
    const sectionId = SECTION_BY_PATH[window.location.pathname];

    if (!sectionId) {
        return;
    }

    const section = document.getElementById(sectionId);

    if (section) {
        section.scrollIntoView({ behavior: "smooth", block: "start" });
    }
}


/* ---------------------------------------------------------
   8. START
   --------------------------------------------------------- */

window.addEventListener("DOMContentLoaded", function () {
    renderWelcome();
    checkBackend();
    scrollToCurrentSection();
});
