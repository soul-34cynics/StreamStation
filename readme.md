✅ 0.
Create the virtual environment (if it doesn't exist)
Run this:

python -m venv venv
This will create the venv folder with the necessary scripts inside.

✅ 1. Activate the virtual environment
If you haven’t already, activate it in PowerShell:

.\venv\Scripts\Activate.ps1
You’ll know it worked when your prompt changes to show something like:

(venv) PS C:\Users\sujay\Desktop\auraflows_final>
✅ 2. Install required packages (if needed)
If your project uses external libraries (like Flask, OpenCV, etc.), install them:

If you have a requirements.txt file:

pip install -r requirements.txt
Or install manually:

pip install flask opencv-python keras
(Replace with whatever your project needs)

✅ 3. Run your main Python file
Find the file that starts your project (for example, app.py, main.py, etc.). Then run it like this:

python app.py
Replace app.py with the actual filename.

✅ 4. Access your app (if it's a web app)
If it's a web project (like Flask), after running it, you’ll see something like:

Running on http://127.0.0.1:5000/
Just open that URL in your browser.

✅ 5. Deactivate when you're done
When you finish working, deactivate the virtual environment by running:

deactivate



IF VENV EXIST RUN....
DIRECTLY RUN python app.py