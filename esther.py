from flask import Flask, request, render_template
from zxcvbn import zxcvbn
import random
import string

app = Flask(__name__)

# Predefined strong passwords
strong_passwords = [
    "Tr0ub4dor&3",
    "correcthorsebatterystaple",
    "X3@mp!ePa$$w0rd",
    "D0g.....................",
    "tH!sIsAV3ry$tr0nGP@$$w0rd",
    "c0rr3ctH0rs3b@tt3rY5taple",
    "myF@v0r!t3F00dI$P!zz@",
    "3@tM0reFrU!t$"
]

# Function to enhance password strength
def enhance_password(password):
    while True:
        result = zxcvbn(password)
        if result['score'] >= 4:
            break
        # Add complexity to the password
        password += random.choice(string.ascii_letters + string.digits + string.punctuation)
    return password

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_password', methods=['POST'])
def check_password():
    password = request.form['password']
    result = zxcvbn(password)
    score = result['score']
    feedback = result['feedback']
    suggestions = []
    if score < 4:
        enhanced_password = enhance_password(password)
        suggestions.append(enhanced_password)
    return render_template('result.html', score=score, feedback=feedback, suggestions=suggestions, strong_passwords=strong_passwords)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

