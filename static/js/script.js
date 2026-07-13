function startMoodDetection() {
  navigator.mediaDevices.getUserMedia({ video: true }).then(stream => {
    const video = document.getElementById("videoPreview");
    video.srcObject = stream;
    video.style.display = "block"; // Show the camera preview

    setTimeout(() => {
      const canvas = document.createElement("canvas");
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      const ctx = canvas.getContext("2d");
      ctx.drawImage(video, 0, 0);

      const imageData = canvas.toDataURL("image/png");

      fetch("/detect-mood", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData })
      })
      .then(res => res.json())
      .then(data => {
        const resultDiv = document.getElementById("moodResult");
        if (data.error) {
          resultDiv.innerHTML = `<p>${data.error}</p>`;
        } else {
          let html = `<h2>Detected Mood: ${data.mood}</h2>`;
          data.songs.forEach(song => {
            const title = song.split('/').pop().replace('.mp3', '');
            const cover = song.replace('/songs/', '/covers/').replace('.mp3', '.png');
            html += `
              <div class="song-card">
                <img src="${cover}" alt="Cover" class="album-cover">
                <h3>${title}</h3>
                <audio controls>
                  <source src="${song}" type="audio/mpeg">
                </audio>
              </div>
            `;
          });
          resultDiv.innerHTML = html;
        }
        // Stop camera
        stream.getTracks().forEach(track => track.stop());
        video.style.display = "none"; // Hide preview after detection
      });

    }, 3000); // Wait 3 seconds before capturing image
  });
}
