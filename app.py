from flask import Flask, render_template, request
import re
import random
import string

app = Flask(__name__)

# ---------------- PASSWORD ANALYSIS ---------------- #

def analyze_password(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 2
    else:
        feedback.append("Password is too short. Short passwords are easier to crack.")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("No uppercase letters detected. This reduces password complexity.")

    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("No lowercase letters detected. A mix of cases improves security.")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("No numbers included. Numbers increase password strength.")

    if re.search(r"[!@#$%^&*]", password):
        score += 2
    else:
        feedback.append("No special characters found. Special symbols make guessing harder.")

    weak_patterns = ["123", "password", "abc", "qwerty"]
    if any(p in password.lower() for p in weak_patterns):
        score -= 2
        feedback.append("Common or predictable patterns detected. Attackers check these first.")

    return score, feedback


def classify_strength(score):
    if score <= 2:
        return "Weak"
    elif score <= 5:
        return "Moderate"
    elif score <= 8:
        return "Strong"
    else:
        return "Very Strong"


# ---------------- SMART PASSWORD GENERATOR ---------------- #

def generate_smart_suggestions(password):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    suggestions = []

    # -------- FIRST TWO → INPUT AT FRONT -------- #

    for _ in range(2):
        strong_suffix = (
            random.choice("!@#$%^&*") +
            str(random.randint(100, 9999)) +
            random.choice("!@#$%^&*")
        )

        suggestions.append(password + strong_suffix)

    # -------- NEXT TWO → FULLY RANDOM -------- #

    for _ in range(2):
        suggestions.append(''.join(random.choice(chars) for _ in range(12)))

    return suggestions

# ---------------- FLASK ROUTE ---------------- #

@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        password = request.form["password"]

        score, feedback = analyze_password(password)
        strength = classify_strength(score)

        # ✅ NEW smart suggestions
        suggestions = generate_smart_suggestions(password)

        result = {
            "strength": strength,
            "score": score,
            "feedback": feedback,
            "suggestions": suggestions
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)