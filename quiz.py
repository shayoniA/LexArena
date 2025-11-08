from flask import Blueprint, session, redirect, render_template, request
import pandas as pd
import random
import joblib
import time
import json
from bson import ObjectId
from db import users_collection
from db import descriptions_collection
from db import questions_collection

quiz_bp = Blueprint("quiz", __name__)

CLASSIFIER_FILE = "ml/model.pkl"
SCALER_FILE = "scaler.pkl"

def get_user(username):
    user = users_collection.find_one({"username": username})
    return {
        "username": user["username"],
        "score": int(user.get("score", 0)),
        "level": int(user.get("level", 1)),
        "history": user.get("history", []),
    }

def update_user(username, score, level, history):
    users_collection.update_one(
        {"username": username},
        {"$set": {"score": score, "level": level, "history": history}}
    )

@quiz_bp.route("/home")
def home():
    if "username" not in session:
        return redirect("/auth/login")
    user = users_collection.find_one({"username": session["username"]})
    user_data = get_user(session["username"])
    return render_template("home.html", score=user_data['score'], level=user_data['level'], history=user_data["history"], user_id=str(user["_id"]))
    
@quiz_bp.route("/next")
def next_question():
    if "username" not in session:
        return redirect("/auth/login")

    username = session["username"]
    user = get_user(username)
    level = user['level']
    score = user['score']
    history = user['history']

    filtered = list(questions_collection.find({"IPC_section_number": level}))
    if not filtered:
        return f"No question found for IPC Section {level}", 404
    question_row = filtered[0]

    # Determine question category
    if level <= 3:
        category = 0
    elif level == 4:
        category = 1
    else:
        scaler = joblib.load(SCALER_FILE)
        clf = joblib.load(CLASSIFIER_FILE)
        if not history:
            category = 0
        else:
            prev_q = history[-1]
            prev_cat = prev_q["cat"]
            onehot = [1.0, 0.0] if prev_cat == "hard" else [0.0, 1.0]
            raw_features = [
                score,
                prev_q["avg_time"],
                prev_q["time"],
                prev_q["length"]
            ]
            print(f"The raw features: {raw_features}")
            scaled_features = scaler.transform([raw_features])[0]
            X = [onehot + list(scaled_features)]
            print(f"Here is X: {X}")
            category = int(clf.predict(X)[0])

    session["start-time"] = time.time()
    session["category"] = category

    question_data = json.loads(question_row["hard_question"]) if category == 1 else json.loads(question_row["easy_question"])
    question_text, options, correct_answers = question_data[0], question_data[1], question_data[2]
    session["correct_answers"] = correct_answers
    session["length"] = len(question_text)

    return render_template("question.html", level=level, question=question_text, ipc_section=level, options=options, correct_answers=correct_answers)


@quiz_bp.route("/submit", methods=["POST"])
def submit_answer():
    if "username" not in session:
        return redirect("/auth/login")

    username = session["username"]
    ipc_section = int(request.form["ipc_section"])
    correct_sections = list(map(str, session.get("correct_answers", [])))
    selected_sections = list(map(str, request.form.getlist("selected_answers")))

    correct_numbers = [s.split()[-1] for s in correct_sections]
    explanations = list(descriptions_collection.find({
        "IPC_section_number": {"$in": [int(x) for x in correct_numbers]}
    }))
    
    user = get_user(username)
    level = user['level']
    score = user['score']
    history = user['history']

    # Calculate time taken
    end_time = time.time()
    start_time = session.get("start_time", end_time)
    time_taken = round((end_time - start_time) / 60, 2)

    total_time = sum(h["time"] for h in history) if history else 0
    new_avg = round((total_time + time_taken) / (level), 2)
    category = session.get("category", 0)
    length = session.get("length", 300)

    incorrect_selected = [s for s in selected_sections if s not in correct_sections]
    penalty = 5 * len(incorrect_selected)
    base_points = 50 if category == 0 else 100
    earned_points = max(base_points - penalty, 0)
    score += earned_points
    level += 1

    history.append({
        "level": level-1,
        "cat": "hard" if category == 1 else "easy",
        "time": time_taken,
        "avg_time": new_avg,
        "length": length
    })

    update_user(username, score, level, history)
    print(f"The explanations: {explanations}")
    return render_template("feedback.html", correct=correct_sections, selected=selected_sections, explanations=explanations, level=level-1)


@quiz_bp.route("/youarehere/<user_id>", methods=["GET"])
def you_are_here(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    history = user.get("history", [])
    level = user["level"]
    progress = {}
    for entry in history:
        lvl = entry.get("level")
        cat = entry.get("cat")
        if lvl and cat:
            progress[lvl] = cat  # either "easy" or "hard"
    return render_template("youarehere.html", current_level=level, history=history, progress=progress, level=level)
