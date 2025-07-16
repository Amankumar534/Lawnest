// chatbot-script.js

// Global variables
let chatOpen = false;
let messageCount = 0;

// Initialize chatbot when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeChatbot();
});

// Initialize chatbot functionality
function initializeChatbot() {
    // Hide notification badge initially
    const badge = document.getElementById('notification-badge');
    if (badge) {
        badge.style.display = 'none';
    }
    
    // Focus input when chat opens
    setupInputFocus();
    
    // Add enter key handler
    setupEnterKeyHandler();
    
    // Add send button handler
    setupSendButton();
}

// Toggle chat visibility
function toggleChat() {
    const chatbox = document.getElementById('chatbox');
    const badge = document.getElementById('notification-badge');
    
    if (!chatOpen) {
        // Open chat
        chatbox.classList.remove('chatbox-hidden');
        chatbox.classList.add('chatbox-visible');
        chatOpen = true;
        
        // Hide notification badge
        if (badge) {
            badge.style.display = 'none';
        }
        
        // Focus input
        setTimeout(() => {
            document.getElementById('chat-input').focus();
        }, 300);
        
        // Scroll to bottom
        scrollToBottom();
    } else {
        // Close chat
        chatbox.classList.remove('chatbox-visible');
        chatbox.classList.add('chatbox-hidden');
        chatOpen = false;
    }
}

// Setup input focus functionality
function setupInputFocus() {
    const chatInput = document.getElementById('chat-input');
    
    chatInput.addEventListener('focus', function() {
        this.parentElement.style.borderColor = '#667eea';
    });
    
    chatInput.addEventListener('blur', function() {
        this.parentElement.style.borderColor = '#e2e8f0';
    });
}

// Setup enter key handler
function setupEnterKeyHandler() {
    const chatInput = document.getElementById('chat-input');
    chatInput.addEventListener('keydown', handleEnter);
}

// Setup send button
function setupSendButton() {
    const sendBtn = document.getElementById('send-btn');
    sendBtn.addEventListener('click', sendMessage);
}

// Handle enter key press
function handleEnter(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// Send message function
function sendMessage() {
    const chatInput = document.getElementById('chat-input');
    const message = chatInput.value.trim();
    
    if (message === '') return;
    
    // Clear input
    chatInput.value = '';
    
    // Add user message
    addMessage('user', message);
    
    // Show typing indicator
    showTypingIndicator();
    
    // Simulate API call
    setTimeout(() => {
        hideTypingIndicator();
        sendToServer(message);
    }, 1000 + Math.random() * 2000); // Random delay between 1-3 seconds
}

// Add message to chat
function addMessage(sender, text, isBot = false) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    const currentTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    
    messageDiv.className = `message ${sender === 'user' ? 'user-message' : 'bot-message'}`;
    
    if (sender === 'user') {
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="10" cy="10" r="10" fill="rgb(243, 176, 69)"/>
                    <path d="M10 5C8.34 5 7 6.34 7 8S8.34 11 10 11 13 9.66 13 8 11.66 5 10 5ZM10 13C7.67 13 6 14.34 6 16V17H14V16C14 14.34 12.33 13 10 13Z" fill="white"/>
                </svg>
            </div>
            <div class="message-content">
                <p>${escapeHtml(text)}</p>
                <span class="message-time">${currentTime}</span>
            </div>
        `;
    } else {
        messageDiv.innerHTML = `
            <div class="message-avatar">
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="10" cy="10" r="10" fill="rgb(243, 176, 69)"/>
                    <path d="M10 5C8.34 5 7 6.34 7 8S8.34 11 10 11 13 9.66 13 8 11.66 5 10 5ZM10 13C7.67 13 6 14.34 6 16V17H14V16C14 14.34 12.33 13 10 13Z" fill="white"/>
                </svg>
            </div>
            <div class="message-content">
                <p>${escapeHtml(text)}</p>
                <span class="message-time">${currentTime}</span>
            </div>
        `;
    }
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
    messageCount++;
    
    // Show notification if chat is closed
    if (!chatOpen && sender === 'bot') {
        showNotification();
    }
}

// Show typing indicator
function showTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.classList.add('show');
        scrollToBottom();
    }
}

// Hide typing indicator
function hideTypingIndicator() {
    const typingIndicator = document.getElementById('typing-indicator');
    if (typingIndicator) {
        typingIndicator.classList.remove('show');
    }
}

// Show notification badge
function showNotification() {
    const badge = document.getElementById('notification-badge');
    if (badge && !chatOpen) {
        badge.style.display = 'flex';
        badge.textContent = '!';
        
        // Add shake animation
        const chatToggle = document.getElementById('chat-toggle');
        chatToggle.style.animation = 'shake 0.5s ease-in-out';
        
        setTimeout(() => {
            chatToggle.style.animation = '';
        }, 500);
    }
}

// Scroll to bottom of chat
function scrollToBottom() {
    const chatMessages = document.getElementById('chat-messages');
    setTimeout(() => {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }, 100);
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Send message to server
function sendToServer(message) {
    // Disable send button temporarily
    const sendBtn = document.getElementById('send-btn');
    sendBtn.disabled = true;
    
    fetch('/chatbot-response/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        addMessage('bot', data.response || 'Sorry, I encountered an error. Please try again.');
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('bot', 'Sorry, I encountered an error. Please try again.');
    })
    .finally(() => {
        // Re-enable send button
        sendBtn.disabled = false;
    });
}

// Get CSRF token from cookies
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// Add shake animation to CSS dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
`;
document.head.appendChild(style);

// Auto-resize textarea functionality (optional enhancement)
function autoResizeTextarea(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

// Add some sample automated responses (for demo purposes)
const sampleResponses = [
    "Thank you for your message! How can I help you book an appointment?",
    "I'd be happy to help you schedule an appointment. What service are you interested in?",
    "Great! Let me check our availability. What date works best for you?",
    "Perfect! I'll get that scheduled for you. Is there anything else I can help you with?",
    "I understand. Let me connect you with our booking system for more detailed assistance.",
    "Thank you for choosing our services! Your appointment request has been noted."
];

// Simulate automated responses (for demo - remove in production)
function simulateResponse(userMessage) {
    const responses = sampleResponses;
    const randomResponse = responses[Math.floor(Math.random() * responses.length)];
    
    // Simulate processing time
    setTimeout(() => {
        addMessage('bot', randomResponse);
    }, 1000 + Math.random() * 1500);
}

// Enhanced error handling
window.addEventListener('error', function(e) {
    console.error('Chatbot error:', e);
});

// Add keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // ESC to close chat
    if (e.key === 'Escape' && chatOpen) {
        toggleChat();
    }
    
    // Ctrl/Cmd + Enter to send message
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        sendMessage();
    }
});

// Initialize notification system
function initializeNotifications() {
    // Check if notifications are supported
    if ('Notification' in window) {
        // Request permission if needed
        if (Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }
}

// Show browser notification (optional)
function showBrowserNotification(message) {
    if ('Notification' in window && Notification.permission === 'granted') {
        const notification = new Notification('New Message', {
            body: message,
            icon: '/path/to/icon.png', // Add your icon path
            badge: '/path/to/badge.png' // Add your badge path
        });
        
        notification.onclick = function() {
            window.focus();
            if (!chatOpen) {
                toggleChat();
            }
            notification.close();
        };
        
        // Auto close after 5 seconds
        setTimeout(() => {
            notification.close();
        }, 5000);
    }
}

// Performance optimization: Debounce typing indicator
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Export functions for external use (if needed)
window.ChatbotWidget = {
    toggle: toggleChat,
    sendMessage: sendMessage,
    addMessage: addMessage,
    isOpen: () => chatOpen
};