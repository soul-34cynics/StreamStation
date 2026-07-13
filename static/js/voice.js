const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

recognition.continuous = false;
recognition.lang = 'en-US';

function speak(text) {
  const synth = window.speechSynthesis;
  const utterance = new SpeechSynthesisUtterance(text);
  synth.speak(utterance);
}

document.getElementById('voiceBtn').addEventListener('click', () => {
  recognition.start();
});

recognition.onresult = (event) => {
  const command = event.results[0][0].transcript.toLowerCase();
  console.log('Voice command:', command);

  if (command.includes('play')) {
    const songName = command.replace('play', '').trim().toLowerCase();
    const songs = document.querySelectorAll('.card');

    let found = false;
    songs.forEach(song => {
      const title = song.querySelector('h3').innerText.toLowerCase();
      if (title.includes(songName)) {
        song.scrollIntoView({ behavior: 'smooth' });
        song.querySelector('audio').play();
        speak(`Playing ${title}`);
        found = true;
      }
    });

    if (!found) speak("Sorry, I couldn't find that song.");
  } else if (command.includes('mood')) {
    window.location.href = "/mood";
  } else if (command.includes('video')) {
    window.location.href = "/videos";
  } else {
    speak("Sorry, I didn't understand the command.");
  }
};
