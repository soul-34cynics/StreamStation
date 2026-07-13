from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import cv2
import numpy as np
from keras.models import model_from_json
import base64

app = Flask(__name__, static_folder='static', template_folder='templates')

# Load emotion detection model
model_path = 'model/emotiondetector.json'
weights_path = 'model/emotiondetector.h5'

with open(model_path, "r") as json_file:
    loaded_model_json = json_file.read()
model = model_from_json(loaded_model_json)
model.load_weights(weights_path)

# Label mapping
labels = {
    0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy',
    4: 'neutral', 5: 'sad', 6: 'surprise'
}

# ✅ Homepage route with autoplay support
@app.route('/')
def home1():
    return render_template('index.html')

@app.route('/search')
def home():
    autoplay = request.args.get('autoplay')  # autoplay param from URL if any
    songs = []
    songs_folder = 'static/songs'
    covers_folder = 'static/covers'

    song_titles = [
        'Angry', 'Arcade', 'Beat It', 'Before You Go', 'Believer',
        'Blinding Lights', 'Disgust', 'Fear', 'Girls Like You', 'Happier',
        'Kammani Ee Premalekhani', 'Memories', 'Mental Madhilo', 'Neutral',
        'O Cheliya', 'Paper Rings', 'Perfect', 'Sahana', 'Someone You Loved',
        'Sundari Neeve', 'The Nights', 'They Dont Care About Us',
        'Until I Found You', 'Watermelon Sugar', 'Yamuna Thatilo', 'Yedho Adaganaa'
    ]

    for title in song_titles:
        filename = f"{title}.mp3"
        cover = f"{title}.png"
        songs.append({
            'title': title,
            'file': f"{songs_folder}/{filename}",
            'cover': f"{covers_folder}/{cover}"
        })

    return render_template('search.html', songs=songs, autoplay=autoplay)

# 🎭 Mood Detection
@app.route('/detect-mood', methods=['POST'])
def detect_mood():
    data = request.get_json()
    img_data = data['image']
    img_bytes = base64.b64decode(img_data.split(',')[1])
    nparr = np.frombuffer(img_bytes, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)

    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img_np, 1.3, 5)

    if len(faces) == 0:
        return jsonify({'error': 'No face detected'})

    for (x, y, w, h) in faces:
        face = img_np[y:y+h, x:x+w]
        face = cv2.resize(face, (48, 48))
        face = face.reshape(1, 48, 48, 1) / 255.0
        prediction = model.predict(face)
        mood = labels[np.argmax(prediction)]
        break

    mood_songs = {
        'happy': ['static/songs/Happier.mp3', 'static/songs/Paper Rings.mp3'],
        'sad': ['static/songs/Someone You Loved.mp3', 'static/songs/Before You Go.mp3'],
        'angry': ['static/songs/Angry.mp3'],
        'surprise': ['static/songs/The Nights.mp3'],
        'neutral': ['static/songs/Neutral.mp3'],
        'disgust': ['static/songs/Disgust.mp3'],
        'fear': ['static/songs/Fear.mp3']
    }

    return jsonify({'mood': mood, 'songs': mood_songs.get(mood, [])})

# 🎭 Mood Page
@app.route('/mood')
def mood_page():
    return render_template('mood.html')

# 🎬 Videos Page
@app.route('/videos')
def video_page():
    video_folder = 'static/videos'
    thumb_folder = 'static/thumbnails'
    video_list = []

    for filename in os.listdir(video_folder):
        if filename.endswith('.mp4'):
            title = filename[:-4]
            video_list.append({
                'title': title,
                'file': f"{video_folder}/{filename}",
                'thumbnail': f"{thumb_folder}/{title}.png"
            })

    return render_template('videos.html', videos=video_list)

# 🔊 Voice command route to play song by name
@app.route('/play-song/<song_name>')
def play_song(song_name):
    return redirect(url_for('home', autoplay=song_name))

# 🔥 Run Flask
if __name__ == '__main__':
    print("🔥 Flask app is starting...")
    app.run(debug=True, host='0.0.0.0')
