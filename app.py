from flask import Flask, render_template, request, jsonify
import joblib
from gtts import gTTS
import os
from pydub import AudioSegment

# Set the path to the FFmpeg binary
os.environ["PYDUB_FFMPEG_PATH"] = "C:\\path_sih"  # Replace with the actual path

app = Flask(__name__)

# Load your trained model (replace 'your_model.pkl' with your model file)
model = joblib.load('sih_model.pkl')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input from the form
        Num_bedrooms = float(request.form['Num_bedrooms'])
        Num_bathrooms = float(request.form['Num_bathrooms'])
        Area = float(request.form['Area'])
        grade_house = float(request.form['grade_house'])
        furniture_grade = float(request.form['furniture_grade'])
        floors = float(request.form['floors'])

        # Check if any of the input fields are empty
        if any(val is None or val == '' for val in [Num_bedrooms, Num_bathrooms, Area, grade_house, furniture_grade, floors]):
            return jsonify({'error': 'Please fill in all input fields'})

        # Make predictions using the model
        prediction = model.predict([[Num_bedrooms, Num_bathrooms, Area, grade_house, furniture_grade, floors]])

        # Convert prediction to speech
        text = f"The prediction is {prediction[0]}"
        tts = gTTS(text, lang='en')
        tts.save('prediction.mp3')

        # Create a silent MP3 file (1 second)
        silence = AudioSegment.silent(duration=1000)

        # Concatenate the silent file with the prediction audio
        silent_prediction = silence + AudioSegment.from_mp3('prediction.mp3')
        silent_prediction.export('silent_prediction.mp3', format='mp3')

        # Play the audio in the background
        os.system('"C:\\Users\\AAVINASH\\vlc-3.0.18-win64.exe" E:\\sih_virtual_ass')

        # Return the prediction as JSON
        result = {'prediction': prediction[0]}
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
