class JokeBot {
    constructor() {
        this.batteryLevel = 100;
        this.isRecording = false;
        this.recognition = null;
        this.barInterval = null;
        this.currentJoke = '';
        this.currentResponse = '';
        this.speechSynth = window.speechSynthesis;
        
        this.init();
    }

    async init() {
        this.loadBattery();
        this.cacheDOM();
        this.setupEventListeners();
        this.updateBatteryDisplay();
        console.log('🤖 JokeBot initialized - ✅ Pure Web Speech Voice');
    }

    cacheDOM() {
        this.batteryPercent = document.getElementById('batteryPercent');
        this.batteryFill = document.getElementById('batteryFill');
        this.batteryStatus = document.getElementById('batteryStatus');
        this.responseText = document.getElementById('responseText');
        this.speakBtn = document.getElementById('speakBtn');
        this.jokeInput = document.getElementById('jokeInput');
        this.evaluateBtn = document.getElementById('evaluateBtn');
        this.charCount = document.getElementById('charCount');
        this.textTab = document.getElementById('textTab');
        this.voiceTab = document.getElementById('voiceTab');
        this.textSection = document.getElementById('textSection');
        this.voiceSection = document.getElementById('voiceSection');
        this.recordBtn = document.getElementById('recordBtn');
        this.voiceStatus = document.getElementById('voiceStatus');
        this.transcriptText = document.getElementById('transcriptText');
        this.useTranscriptBtn = document.getElementById('useTranscriptBtn');
        this.exampleBtns = document.querySelectorAll('.example-btn');
        this.resetBtn = document.getElementById('resetBtn');
        this.helpBtn = document.getElementById('helpBtn');
        // Modal elements
        this.modal = document.getElementById('evaluationModal');
        this.modalResult = document.getElementById('modalResult');
        this.closeModalBtn = document.getElementById('closeModalBtn');
        this.modalSpeakBtn = document.getElementById('modalSpeakBtn');
        this.robotMouth = document.getElementById('robotMouth');
    }

    setupEventListeners() {
        this.jokeInput.addEventListener('input', () => this.updateCharCount());
        this.evaluateBtn.addEventListener('click', () => this.evaluateJoke());
        this.textTab.addEventListener('click', () => this.switchTab('text'));
        this.voiceTab.addEventListener('click', () => this.switchTab('voice'));
        this.recordBtn.addEventListener('click', () => this.toggleRecording());
        this.useTranscriptBtn.addEventListener('click', () => this.useTranscript());
        
        this.exampleBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const joke = e.currentTarget.getAttribute('data-joke');
                this.jokeInput.value = joke;
                this.switchTab('text');
                this.updateCharCount();
                this.showNotification('Example joke loaded!');
            });
        });
        
        this.resetBtn.addEventListener('click', () => this.resetBattery());
        this.helpBtn.addEventListener('click', () => this.showHelp());
        this.speakBtn.addEventListener('click', () => this.speakResponse());
        
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                this.evaluateJoke();
            }
        });

        // Modal close event
        this.closeModalBtn.addEventListener('click', () => {
            this.modal.classList.remove('active');
        });
        // Modal speak button
        this.modalSpeakBtn.addEventListener('click', () => {
            this.speakResponseWithMouth(this.robotMouth);
        });
        // Click outside modal to close
        window.addEventListener('click', (e) => {
            if (e.target === this.modal) {
                this.modal.classList.remove('active');
            }
        });
    }

    // ========== VOICE RECORDING (Web Speech API) ==========
    toggleRecording() {
        if (!this.isRecording) {
            this.startVoiceRecording();
        } else {
            this.stopVoiceRecording();
        }
    }

    startVoiceRecording() {
        if (!('webkitSpeechRecognition' in window)) {
            this.showNotification('❌ Speech recognition not supported in this browser.');
            return;
        }

        this.recognition = new webkitSpeechRecognition();
        this.recognition.continuous = true;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 1;

        this.recognition.onstart = () => {
            this.isRecording = true;
            this.recordBtn.classList.add('recording');
            this.recordBtn.innerHTML = '<i class="fas fa-stop"></i> Stop Recording';
            this.voiceStatus.textContent = '🎤 Listening... Speak your joke!';
            this.transcriptText.textContent = '';
            this.useTranscriptBtn.disabled = true;
            this.animateVoiceBars(true);
        };

        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript + ' ';
                } else {
                    interimTranscript += transcript;
                }
            }

            // Show interim + final in transcript box
            this.transcriptText.textContent = finalTranscript + interimTranscript;
            
            // Enable "Use This Joke" if we have any final text
            if (finalTranscript.trim().length > 0) {
                this.useTranscriptBtn.disabled = false;
            }
        };

        this.recognition.onerror = (event) => {
            this.showNotification(`🎤 Error: ${event.error}`);
            this.stopVoiceRecording();
        };

        this.recognition.onend = () => {
            if (this.isRecording) {
                // Recognition ended unexpectedly – keep UI in stopped state
                this.voiceStatus.textContent = '⚠️ Recognition ended. Press button to retry.';
            }
            this.animateVoiceBars(false);
            this.isRecording = false;
            this.recordBtn.classList.remove('recording');
            this.recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Record Joke';
        };

        this.recognition.start();
    }

    stopVoiceRecording() {
        if (this.recognition) {
            this.recognition.stop();
            this.isRecording = false;
            this.recordBtn.classList.remove('recording');
            this.recordBtn.innerHTML = '<i class="fas fa-microphone"></i> Record Joke';
            this.voiceStatus.textContent = '✅ Recording stopped. Ready to use.';
            this.animateVoiceBars(false);
        }
    }

    animateVoiceBars(active) {
        const bars = document.querySelectorAll('.voice-bars .bar');
        if (!bars.length) return;
        
        if (active) {
            this.barInterval = setInterval(() => {
                bars.forEach(bar => {
                    const height = Math.floor(Math.random() * 30) + 10;
                    bar.style.height = height + 'px';
                });
            }, 150);
        } else {
            clearInterval(this.barInterval);
            bars.forEach(bar => bar.style.height = '10px');
        }
    }

    useTranscript() {
        let joke = this.transcriptText.textContent.trim();
        if (joke && joke.length > 2) {
            this.jokeInput.value = joke;
            this.switchTab('text');
            this.updateCharCount();
            this.showNotification(`🎤 Loaded: "${joke.substring(0, 40)}..."`);
            this.jokeInput.focus();
            this.jokeInput.select();
        } else {
            this.showNotification('❌ No valid speech detected.');
        }
    }

    // ========== BATTERY SYSTEM ==========
    loadBattery() {
        const saved = localStorage.getItem('jokebot_battery');
        if (saved !== null) {
            this.batteryLevel = parseInt(saved);
        } else {
            this.batteryLevel = 100;
            this.saveBattery();
        }
    }

    saveBattery() {
        localStorage.setItem('jokebot_battery', this.batteryLevel.toString());
    }

    updateBatteryBasedOnScore(score) {
        if (this.batteryLevel <= 0) {
            this.showNotification("🔋 Battery empty! Reset to continue.");
            return false;
        }

        const oldLevel = this.batteryLevel;
        let batteryChange = 0;
        
        if (score >= 90) { batteryChange = 20; this.batteryStatus.textContent = "⚡ LEGENDARY JOKE! +20%!"; }
        else if (score >= 80) { batteryChange = 15; this.batteryStatus.textContent = "🤩 EXCELLENT! +15%!"; }
        else if (score >= 70) { batteryChange = 10; this.batteryStatus.textContent = "😄 GREAT! +10%!"; }
        else if (score >= 60) { batteryChange = 5; this.batteryStatus.textContent = "🙂 GOOD! +5%!"; }
        else if (score >= 50) { batteryChange = 0; this.batteryStatus.textContent = "😐 AVERAGE. No change."; }
        else if (score >= 40) { batteryChange = -5; this.batteryStatus.textContent = "😕 WEAK. -5%!"; }
        else if (score >= 30) { batteryChange = -10; this.batteryStatus.textContent = "😬 POOR. -10%!"; }
        else if (score >= 20) { batteryChange = -15; this.batteryStatus.textContent = "💀 BAD! -15%!"; }
        else { batteryChange = -20; this.batteryStatus.textContent = "🚫 TERRIBLE! -20%!"; }

        this.batteryLevel += batteryChange;
        this.batteryLevel = Math.max(0, Math.min(100, this.batteryLevel));
        this.saveBattery();
        this.updateBatteryDisplay();
        this.animateBatteryChange(oldLevel, this.batteryLevel);
        
        if (batteryChange > 0) this.showNotification(`🔋 +${batteryChange}%`);
        else if (batteryChange < 0) this.showNotification(`🔋 ${batteryChange}%`);
        
        return true;
    }

    updateBatteryDisplay() {
        this.batteryFill.style.width = `${this.batteryLevel}%`;
        this.batteryPercent.textContent = `${this.batteryLevel}%`;
        
        if (this.batteryLevel >= 70) {
            this.batteryFill.style.background = 'linear-gradient(90deg, #10b981, #22c55e)';
            this.batteryPercent.style.color = '#10b981';
        } else if (this.batteryLevel >= 30) {
            this.batteryFill.style.background = 'linear-gradient(90deg, #f59e0b, #fbbf24)';
            this.batteryPercent.style.color = '#f59e0b';
        } else {
            this.batteryFill.style.background = 'linear-gradient(90deg, #ef4444, #dc2626)';
            this.batteryPercent.style.color = '#ef4444';
        }
        
        this.evaluateBtn.disabled = this.batteryLevel <= 0;
        if (this.batteryLevel <= 0) {
            this.evaluateBtn.innerHTML = '<i class="fas fa-battery-empty"></i> BATTERY EMPTY';
            this.batteryStatus.textContent = '⚠️ Reset to continue.';
        } else {
            this.evaluateBtn.innerHTML = '<i class="fas fa-brain"></i> Evaluate Joke';
        }
    }

    animateBatteryChange(oldLevel, newLevel) {
        this.batteryFill.style.transition = 'none';
        this.batteryFill.style.width = `${oldLevel}%`;
        this.batteryFill.offsetHeight;
        setTimeout(() => {
            this.batteryFill.style.transition = 'width 0.8s cubic-bezier(0.34, 1.56, 0.64, 1)';
            this.batteryFill.style.width = `${newLevel}%`;
        }, 10);
    }

    resetBattery() {
        if (confirm('Reset battery to 100%?')) {
            this.batteryLevel = 100;
            this.updateBatteryDisplay();
            this.saveBattery();
            this.batteryStatus.textContent = 'Battery reset!';
            this.showNotification('🔋 Reset complete!');
        }
    }

    // ========== JOKE EVALUATION ==========
    async evaluateJoke() {
        const joke = this.jokeInput.value.trim();
        if (!joke) { this.showNotification('Enter a joke first!'); return; }
        if (joke.split(' ').length < 3) { this.showNotification('3+ words minimum!'); return; }
        if (this.batteryLevel <= 0) { this.showNotification('Battery empty!'); return; }
        
        this.currentJoke = joke;
        this.evaluateBtn.disabled = true;
        const originalText = this.evaluateBtn.innerHTML;
        this.evaluateBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Evaluating...';
        
        try {
            let result;
            try {
                const response = await fetch('http://localhost:5000/evaluate', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ joke })
                });
                if (response.ok) result = await response.json();
                else throw new Error('API failed');
            } catch {
                result = this.evaluateLocally(joke);
            }
            
            this.showBotResponse(result);
            this.updateBatteryBasedOnScore(result.quality_score);
            this.showEvaluationModal(result);
            this.jokeInput.value = '';
            this.updateCharCount();
            
        } catch (error) {
            this.showNotification('Evaluation failed.');
        } finally {
            this.evaluateBtn.disabled = false;
            this.evaluateBtn.innerHTML = originalText;
        }
    }

    evaluateLocally(joke) {
        let score = 50;
        const hasQuestion = joke.includes('?');
        const hasExclamation = joke.includes('!');
        const hasBecause = joke.toLowerCase().includes('because');
        const hasWhy = joke.toLowerCase().includes('why');
        const words = joke.split(' ');
        const hasPun = this.detectPun(joke);
        
        if (words.length > 6 && (hasQuestion || hasBecause)) score += 20;
        if (hasQuestion && hasExclamation) score += 15;
        if (hasPun) score += 15;
        if (words.length > 5 && words.length < 30) score += 10;
        
        score += (Math.random() * 20 - 10);
        score = Math.max(0, Math.min(100, Math.round(score)));
        
        const feedback = score >= 80 ? "😂 HILARIOUS!" : 
                        score >= 60 ? "😄 VERY GOOD!" :
                        score >= 40 ? "🙂 GOOD!" : "😬 Needs work...";
        
        return { quality_score: score, feedback, rating: this.getRating(score) };
    }

    detectPun(joke) {
        const punWords = ['bear', 'bare', 'son', 'sun', 'flower', 'flour', 'see', 'sea'];
        return punWords.some(word => joke.toLowerCase().includes(word));
    }

    getRating(score) {
        if (score >= 80) return "EXCELLENT";
        if (score >= 60) return "GOOD";
        if (score >= 40) return "AVERAGE";
        return "POOR";
    }

    showBotResponse(result) {
        const score = result.quality_score;
        const responseHTML = `
            <div style="margin-bottom: 10px;">
                <span style="font-size: 0.9rem; color: #94a3b8;">JOKE SCORE</span><br>
                <span style="font-size: 2rem; font-weight: bold; color: ${this.getScoreColor(score)}">${score}%</span>
            </div>
            <div style="font-size: 1.1rem; margin: 15px 0;">${result.feedback}</div>
            <div style="font-style: italic; color: #cbd5e1; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px;">
                "${this.currentJoke}"
            </div>
        `;
        
        this.responseText.innerHTML = responseHTML;
        this.currentResponse = `${result.feedback} Score: ${score}%`;
        this.speakBtn.disabled = false;
        setTimeout(() => this.speakResponse(), 800);
    }

    getScoreColor(score) {
        return score >= 80 ? '#10b981' : score >= 60 ? '#3b82f6' : score >= 40 ? '#f59e0b' : '#ef4444';
    }

    // ========== SPEECH SYNTHESIS ==========
    speakResponse() {
        if (!this.currentResponse || !('speechSynthesis' in window)) return;
        this.speechSynth.cancel();
        const utterance = new SpeechSynthesisUtterance(this.currentResponse);
        utterance.rate = 1.0;
        
        // Animate mouth if modal is open
        if (this.modal.classList.contains('active')) {
            this.robotMouth.classList.add('speaking');
            utterance.onend = () => this.robotMouth.classList.remove('speaking');
        }
        
        this.speechSynth.speak(utterance);
    }

    speakResponseWithMouth(mouthElement) {
        if (!this.currentResponse || !('speechSynthesis' in window)) return;
        this.speechSynth.cancel();
        const utterance = new SpeechSynthesisUtterance(this.currentResponse);
        utterance.rate = 1.0;

        mouthElement.classList.add('speaking');
        utterance.onend = () => mouthElement.classList.remove('speaking');

        this.speechSynth.speak(utterance);
    }

    // ========== EVALUATION MODAL ==========
    showEvaluationModal(result) {
        const score = result.quality_score;
        const scoreColor = this.getScoreColor(score);
        
        this.modalResult.innerHTML = `
            <div class="score-display" style="color: ${scoreColor}">${score}%</div>
            <div class="feedback-text">${result.feedback}</div>
            <div class="joke-quote">"${this.currentJoke}"</div>
        `;

        this.modal.classList.add('active');
    }

    // ========== UI HELPERS ==========
    switchTab(tab) {
        if (tab === 'text') {
            this.textTab.classList.add('active');
            this.voiceTab.classList.remove('active');
            this.textSection.classList.add('active');
            this.voiceSection.classList.remove('active');
            this.jokeInput.focus();
        } else {
            this.textTab.classList.remove('active');
            this.voiceTab.classList.add('active');
            this.textSection.classList.remove('active');
            this.voiceSection.classList.add('active');
        }
    }

    updateCharCount() {
        const count = this.jokeInput.value.length;
        this.charCount.textContent = `${count} chars`;
        this.charCount.style.color = count < 20 ? '#ef4444' : count < 50 ? '#f59e0b' : '#10b981';
    }

    showNotification(message) {
        const existing = document.querySelector('.custom-notification');
        if (existing) existing.remove();
        
        const notification = document.createElement('div');
        notification.className = 'custom-notification';
        notification.innerHTML = `<div style="display: flex; align-items: center; gap: 10px;">
            <i class="fas fa-info-circle"></i><span>${message}</span>
        </div>`;
        
        notification.style.cssText = `
            position: fixed; top: 20px; right: 20px; background: linear-gradient(135deg, #6366f1, #4f46e5);
            color: white; padding: 15px 25px; border-radius: 12px; z-index: 10000;
            box-shadow: 0 10px 25px rgba(0,0,0,0.3); max-width: 400px;
        `;
        
        document.body.appendChild(notification);
        setTimeout(() => notification.remove(), 3000);
    }

    showHelp() {
        alert(`🤖 JOKEBOT - ✅ NO APIs NEEDED!

🎤 VOICE (FIXED):
• Record → Stop → Auto-transcribes live
• Uses browser Web Speech API only
• Works in Chrome/Edge

⚡ TEXT: Type → Ctrl+Enter
🔋 BATTERY: Good jokes charge!
        
Try: "Why don't programmers like nature? It has too many bugs!"`);
    }
}

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    window.jokeBot = new JokeBot();
});