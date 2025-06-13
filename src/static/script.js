document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const textarea = chatForm.querySelector('textarea');
    const chatHistory = document.querySelector('.chat-history');
    const botTyping = document.getElementById('bot-typing');
    const sendSound = document.getElementById('send-sound');
    const voiceBtn = document.getElementById('voice-btn');
    const themeToggle = document.getElementById('theme-toggle');
    const clearHistoryBtn = document.getElementById('clear-history');
    let isListening = false;

    chatHistory.scrollTop = chatHistory.scrollHeight;

    if (themeToggle) {
        const savedTheme = localStorage.getItem('theme');
        if (savedTheme === 'light') {
            document.body.classList.add('light-theme');
            themeToggle.textContent = '🌙 Tmavý režim';
        } else {
            themeToggle.textContent = '☀️ Světlý režim';
        }

        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('light-theme');
            const isLightTheme = document.body.classList.contains('light-theme');
            themeToggle.textContent = isLightTheme ? '🌙 Tmavý režim' : '☀️ Světlý režim';
            localStorage.setItem('theme', isLightTheme ? 'light' : 'dark');
        });
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const zprava = textarea.value.trim();
        if (!zprava) {
            console.warn('Zpráva je prázdná, odeslání přeskočeno.');
            return;
        }

        if (sendSound) {
            try {
                sendSound.currentTime = 0;
                sendSound.play();
            } catch (e) {
                console.warn('Nepodařilo se přehrát zvuk:', e.message);
            }
        }

        const timestamp = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        const userMsg = `
            <div class="timestamp">${timestamp}</div>
            <div class="user-message">
                <div class="message-content"><small>${zprava}</small></div>
            </div>
        `;
        chatHistory.insertAdjacentHTML('beforeend', userMsg);
        textarea.value = '';

        if (botTyping) {
            botTyping.classList.remove('d-none');
        }

        try {
            const response = await fetch('/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: `zprava=${encodeURIComponent(zprava)}`
            });

            if (!response.ok) {
                throw new Error(`HTTP chyba: ${response.status}`);
            }

            // Simulace zpoždění na klientovi, aby indikace byla viditelná
            await new Promise(resolve => setTimeout(resolve, 1000)); // 1 sekunda

            const data = await response.json();
            const botMsg = `
                <div class="timestamp">${data.timestamp || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                <div class="chatbot-message">
                    <div class="message-content"><small>${data.bot_response || data.odpoved}</small></div>
                </div>
            `;
            chatHistory.insertAdjacentHTML('beforeend', botMsg);
        } catch (err) {
            const errorMsg = `
                <div class="timestamp">${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</div>
                <div class="chatbot-message error">
                    <div class="message-content"><small>Chyba při komunikaci se serverem.</small></div>
                </div>
            `;
            chatHistory.insertAdjacentHTML('beforeend', errorMsg);
            console.error('Chyba při fetch:', err);
        }

        if (botTyping) {
            botTyping.classList.add('d-none');
        }

        chatHistory.scrollTop = chatHistory.scrollHeight;
    });

    if (clearHistoryBtn) {
        clearHistoryBtn.addEventListener('click', async () => {
            if (confirm('Opravdu chceš vymazat historii chatu?')) {
                try {
                    const response = await fetch('/clear_history', {
                        method: 'POST'
                    });
                    if (!response.ok) {
                        throw new Error(`HTTP chyba: ${response.status}`);
                    }
                    location.reload();
                } catch (err) {
                    console.error('Chyba při mazání historie:', err);
                }
            }
        });
    }

    if (voiceBtn) {
        voiceBtn.addEventListener('click', () => {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (!SpeechRecognition) {
                alert('Tvůj prohlížeč nepodporuje hlasové ovládání.');
                return;
            }

            const recognition = new SpeechRecognition();
            recognition.lang = 'cs-CZ';
            recognition.interimResults = false;

            if (!isListening) {
                recognition.start();
                voiceBtn.classList.add('listening');
                voiceBtn.innerHTML = 'Poslouchám...';
                isListening = true;

                recognition.onresult = (event) => {
                    const transcript = event.results[0][0].transcript;
                    textarea.value = transcript;
                    voiceBtn.classList.remove('listening');
                    voiceBtn.innerHTML = '<img src="/static/firefly-icon.svg" alt="Hlas" class="voice-icon"> Hlas';
                    isListening = false;
                };

                recognition.onerror = (event) => {
                    console.error('Chyba hlasového ovládání:', event.error);
                    voiceBtn.classList.remove('listening');
                    voiceBtn.innerHTML = '<img src="/static/firefly-icon.svg" alt="Hlas" class="voice-icon"> Hlas';
                    isListening = false;
                };

                recognition.onend = () => {
                    voiceBtn.classList.remove('listening');
                    voiceBtn.innerHTML = '<img src="/static/firefly-icon.svg" alt="Hlas" class="voice-icon"> Hlas';
                    isListening = false;
                };
            }
        });
    }
});