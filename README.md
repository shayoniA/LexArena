# LexArena ⚖️  
An adaptive law-learning gamified quiz platform, designed to help users learn IPC sections in a personalized way, such that learning is structured, interactive, and progressively challenging.

---

## How to Run

### Create and activate virtual environment
```
python -m venv venv
venv\Scripts\activate   # MacOS/Linux: source venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Setup environment variables
```
MONGO_URI = your_mongodb_atlas_connection_string
SECRET_KEY = your_secret_key
```

### Train the ML model
```
python train_model.py
```

### Run the application
```
python app.py
```

---

## Key Features

1. **User Authentication**  -  Secure signup and login using hashed passwords.
2. **Adaptive Difficulty System**  -  ML model predicts whether the next question should be easy or hard, based on current score, response time, question length, and past performance.
3. **Progressive Learning**  -  Users level up through IPC sections, and difficulty adapts as the user improves.
4. **Detailed Feedback**  -  Shows correct vs selected answers, and displays corresponding IPC section explanations after each question.
5. **Visual Progress Tracker**  -  “Where Am I?” page to visualize completed, current, and upcoming levels.

---

## Tech Stack

1. **Frontend**  -  HTML, CSS, JavaScript (React.js), Jinja2 Templates
2. **Backend**  -  Python, Flask
3. **Database**  -  MongoDB
4. **Machine Learning**  -  Scikit-learn, Random Forest Classifier
5. **Deployment**  -  Render

---

## Why I Built LexArena
Knowledge about laws is very important. The motivation behind LexArena is to make users legally aware. Also, most quiz platforms follow a one-size-fits-all approach, which can overwhelm beginners and bore advanced learners. I built LexArena to:

- Implement adaptive learning systems via ML
- Simulate how real-world educational platforms personalize content
- Make users legally aware

---

## Future Improvements
Leaderboards and user-ranking system can be implemented. There may also be more granular difficulty levels beyond easy/hard

---

## Author
**Sayani Adhikary**
