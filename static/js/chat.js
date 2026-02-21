// Chat functionality
let messageCount = 0;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadDocuments();
    setupEventListeners();
});

function setupEventListeners() {
    const questionInput = document.getElementById('questionInput');
    const sendBtn = document.getElementById('sendBtn');
    const clearBtn = document.getElementById('clearBtn');

    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);

    // Send message on Enter (but Shift+Enter for new line)
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    // Clear chat
    if (clearBtn) {
        clearBtn.addEventListener('click', clearChat);
    }

    // Suggestion cards
    document.querySelectorAll('.suggestion-card').forEach(card => {
        card.addEventListener('click', function() {
            const question = this.querySelector('p').textContent;
            questionInput.value = question;
            sendMessage();
        });
    });
}

async function sendMessage() {
    const questionInput = document.getElementById('questionInput');
    const question = questionInput.value.trim();
    
    if (!question) return;

    // Disable input while processing
    toggleInput(false);

    // Hide welcome message
    const welcome = document.querySelector('.welcome-message');
    if (welcome) {
        welcome.style.display = 'none';
    }

    // Add user message
    addMessage('user', question);

    // Clear input
    questionInput.value = '';

    // Show loading
    showLoading(true);

    try {
        const response = await fetch('/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question: question })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Hide loading
        showLoading(false);

        // Add assistant message with sources
        addMessage('assistant', data.answer, data.sources, data.overall_confidence);

        // Update stats
        messageCount += 2;
        updateStats();

    } catch (error) {
        console.error('Error:', error);
        showLoading(false);
        addMessage('assistant', 'Sorry, I encountered an error. Please try again later.', [], 0);
    } finally {
        toggleInput(true);
    }
}

function addMessage(role, content, sources = [], confidence = 0) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = role === 'user' ? 'U' : 'AI';
    const time = new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });

    let sourcesHTML = '';
    if (sources && sources.length > 0) {
        sourcesHTML = `
            <div class="sources">
                <div class="sources-title">
                    📚 Sources:
                </div>
                ${sources.map(source => `
                    <div class="source-item">
                        <span>
                            <strong>${source.document_name}</strong>
                            ${source.section_number ? ` - Section ${source.section_number}` : ''}
                        </span>
                        <span class="confidence-badge ${getConfidenceClass(source.confidence_score)}">
                            ${(source.confidence_score * 100).toFixed(0)}%
                        </span>
                    </div>
                `).join('')}
            </div>
        `;
    }

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">
            <div class="message-bubble">
                ${content}
                ${sourcesHTML}
            </div>
            <div class="message-time">${time}</div>
        </div>
    `;

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function getConfidenceClass(score) {
    if (score >= 0.7) return 'confidence-high';
    if (score >= 0.4) return 'confidence-medium';
    return 'confidence-low';
}

function showLoading(show) {
    const loading = document.querySelector('.loading');
    if (loading) {
        loading.classList.toggle('active', show);
    }
}

function toggleInput(enabled) {
    const questionInput = document.getElementById('questionInput');
    const sendBtn = document.getElementById('sendBtn');
    
    questionInput.disabled = !enabled;
    sendBtn.disabled = !enabled;
}

function clearChat() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <h3>👋 Welcome to the Central Bank Regulatory Assistant</h3>
            <p>Ask me anything about Sri Lankan banking regulations, monetary policies, and financial stability.</p>
            
            <div class="welcome-suggestions">
                <div class="suggestion-card">
                    <h4>💰 Capital Requirements</h4>
                    <p>What are capital adequacy requirements?</p>
                </div>
                <div class="suggestion-card">
                    <h4>📊 Financial Stability</h4>
                    <p>What is the current financial stability outlook?</p>
                </div>
                <div class="suggestion-card">
                    <h4>📈 Monetary Policy</h4>
                    <p>What are the recent monetary policy changes?</p>
                </div>
                <div class="suggestion-card">
                    <h4>🏦 Banking Regulations</h4>
                    <p>What are the key banking regulations?</p>
                </div>
            </div>
        </div>
    `;
    messageCount = 0;
    updateStats();
    setupEventListeners();
}

async function loadDocuments() {
    try {
        const response = await fetch('/documents');
        const data = await response.json();
        
        const documentList = document.getElementById('documentList');
        if (documentList && data.documents) {
            documentList.innerHTML = data.documents.map(doc => `
                <div class="document-item">
                    <span class="document-icon">📄</span>
                    ${doc.replace(/_/g, ' ')}
                </div>
            `).join('');
            
            // Update document count
            const docCount = document.getElementById('docCount');
            if (docCount) {
                docCount.textContent = data.documents.length;
            }
        }
    } catch (error) {
        console.error('Error loading documents:', error);
    }
}

function updateStats() {
    const msgCount = document.getElementById('msgCount');
    if (msgCount) {
        msgCount.textContent = messageCount;
    }
}
