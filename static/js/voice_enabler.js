const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();
recognition.lang = 'en-US';
recognition.continuous = false;

let initialized = false;
let isListening = false;  // To manage re-triggering

function speak(text) {
  const utterance = new SpeechSynthesisUtterance(text);
  speechSynthesis.speak(utterance);
}

function listenCommand() {
  if (isListening) return;  // Prevent multiple listens happening at once
  isListening = true;

  recognition.start();
  recognition.onresult = function(event) {
    const command = event.results[0][0].transcript.toLowerCase();
    console.log("🎤 Command:", command);

    // Check if the command contains the expected phrases
    if (command.includes("play perfect")) {
        console.log("Command recognized: Play Perfect");
        window.location.href = "/play-song/Perfect";
    }// Navigate to play the song
    } else if (command.includes("detect mood")) {
      console.log("Command recognized: Detect Mood");
      window.location.href = "/mood";  // Navigate to mood detection page
    } else if (command.includes("show videos")) {
      console.log("Command recognized: Show Videos");
      window.location.href = "/videos";  // Navigate to video page
    } else {
      speak("Sorry, I didn't understand that.");
      console.log("Unrecognized command:", command);
    }
  };

  recognition.onerror = function(event) {
    console.warn("🎙️ Recognition error:", event.error);
    recognition.stop();
    speak("I encountered an error, please try again.");
  };

  recognition.onend = () => {
    console.log("🎙️ Recognition ended.");
    isListening = false;
    setTimeout(() => listenCommand(), 1500);  // Restart listening after a delay
  };
}

function initVoiceAssistant() {
  if (!initialized) {
    initialized = true;
    speak("Voice Assistant Ready! Say 'Play Perfect', 'Detect mood now', or 'Show videos'.");
    listenCommand();
  }
}

// 🧠 Wait for user tap to enable mic and audio
window.onload = () => {
  // Check if mic access has already been granted
  if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
    navigator.mediaDevices.enumerateDevices().then(devices => {
      const hasMic = devices.some(device => device.kind === 'audioinput');
      if (!hasMic) {
        // If no microphone is detected, prompt user to check their device
        alert("No microphone detected. Please check your device.");
        return;
      }
    });
  }

  // Create the popup for enabling microphone access
  const popup = document.createElement("div");
  popup.innerHTML = `
    <div style="
      position: fixed;
      top: 0; left: 0; width: 100%; height: 100%;
      background-color: rgba(0,0,0,0.75); display: flex;
      align-items: center; justify-content: center; z-index: 9999;
    ">
      <div style="
        background: white; padding: 30px; border-radius: 10px;
        text-align: center; max-width: 400px;
      ">
        <h2>🎙️ Enable Voice Control</h2>
        <p>This app needs microphone access to start the voice assistant.</p>
        <button id="enableVoice" style="
          margin-top: 10px; padding: 10px 20px;
          background: #111; color: white; border: none;
          border-radius: 5px; font-size: 16px; cursor: pointer;
        ">OK</button>
      </div>
    </div>
  `;
  document.body.appendChild(popup);

  // Button click to enable voice control
  document.getElementById("enableVoice").addEventListener("click", () => {
    popup.remove();  // Remove the popup
    initVoiceAssistant();  // Initialize voice assistant and start listening
  });
};
