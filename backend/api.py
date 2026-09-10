from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from pathlib import Path
from backend.database import get_connection, create_tables


app = FastAPI(title="Dementia Care API")

# Database tables create karna
create_tables()


# ---------------- HOME ----------------

@app.get("/")
def home():
    return {
        "message": "Dementia Care Backend is running"
    }


# ---------------- DATA MODELS ----------------

class Patient(BaseModel):
    patient_id: str
    name: str
    language: str
    last_active: str


class GameResult(BaseModel):
    patient_id: str
    game: str
    score: int
    accuracy: float
    response_time: float
    mistakes: int


class Reminder(BaseModel):
    patient_id: str
    reminder_type: str
    reminder_text: str
    reminder_time: str


# ---------------- PATIENT ----------------

@app.post("/patient")
def add_patient(data: Patient):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR REPLACE INTO patients
        (patient_id, name, language, last_active)
        VALUES (?, ?, ?, ?)
    """, (
        data.patient_id,
        data.name,
        data.language,
        data.last_active
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Patient added successfully"
    }


@app.get("/patient/{patient_id}")
def get_patient(patient_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE patient_id = ?",
        (patient_id,)
    )

    patient = cursor.fetchone()
    conn.close()

    if patient is None:
        return {
            "message": "Patient not found"
        }

    return {
        "patient_id": patient[0],
        "name": patient[1],
        "language": patient[2],
        "last_active": patient[3]
    }


# ---------------- GAME RESULT ----------------

@app.post("/game-result")
def save_game_result(data: GameResult):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO game_results
        (patient_id, game, score, accuracy, response_time, mistakes)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data.patient_id,
        data.game,
        data.score,
        data.accuracy,
        data.response_time,
        data.mistakes
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Game result saved successfully"
    }


# ---------------- GAME HISTORY ----------------

@app.get("/games/{patient_id}")
def get_games(patient_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT game, score, accuracy, response_time, mistakes
        FROM game_results
        WHERE patient_id = ?
    """, (patient_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "game": row[0],
            "score": row[1],
            "accuracy": row[2],
            "response_time": row[3],
            "mistakes": row[4]
        }
        for row in rows
    ]


# ---------------- REMINDER ----------------

@app.post("/reminder")
def add_reminder(data: Reminder):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO reminders
        (patient_id, reminder_type, reminder_text, reminder_time, status)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.patient_id,
        data.reminder_type,
        data.reminder_text,
        data.reminder_time,
        "Upcoming"
    ))

    conn.commit()
    conn.close()

    return {
        "message": "Reminder added successfully"
    }


# ---------------- NER / LOCALIZATION ----------------

@app.get("/languages")
def get_languages():

    return {
        "languages": [
            "English",
            "Assamese",
            "Manipuri",
            "Bengali",
            "Hindi"
        ]
    }
@app.get("/progress/{patient_id}")
def get_progress(patient_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            COUNT(*),
            AVG(score),
            AVG(accuracy),
            AVG(response_time),
            SUM(mistakes),
            MAX(score)
        FROM game_results
        WHERE patient_id = ?
    """, (patient_id,))

    result = cursor.fetchone()
    conn.close()

    if result[0] == 0:
        return {
            "message": "No game data found"
        }

    return {
        "games_played": result[0],
        "average_score": round(result[1], 2),
        "average_accuracy": round(result[2], 2),
        "average_response_time": round(result[3], 2),
        "total_mistakes": result[4],
        "best_score": result[5]
    }
@app.get("/reminders/{patient_id}")
def get_reminders(patient_id: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT reminder_type, reminder_text, reminder_time, status
        FROM reminders
        WHERE patient_id = ?
    """, (patient_id,))

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "reminder_type": row[0],
            "reminder_text": row[1],
            "reminder_time": row[2],
            "status": row[3]
        }
        for row in rows
    ]
@app.get("/localization/{language}")
def get_localization(language: str):

    content = {
        "English": {
            "welcome": "Welcome",
            "memory_game": "Memory Game",
            "reminder": "Reminder",
            "score": "Your Score"
        },

        "Hindi": {
            "welcome": "स्वागत है",
            "memory_game": "याददाश्त खेल",
            "reminder": "अनुस्मारक",
            "score": "आपका स्कोर"
        },

        "Assamese": {
            "welcome": "স্বাগতম",
            "memory_game": "স্মৃতি খেল",
            "reminder": "সোঁৱৰণী",
            "score": "আপোনাৰ স্ক'ৰ"
        },

        "Bengali": {
            "welcome": "স্বাগতম",
            "memory_game": "স্মৃতি খেলা",
            "reminder": "অনুস্মারক",
            "score": "আপনার স্কোর"
        },

        "Manipuri": {
            "welcome": "Welcome",
            "memory_game": "Memory Game",
            "reminder": "Reminder",
            "score": "Your Score"
        }
    }

    if language not in content:
        return {
            "message": "Language not supported"
        }

    return {
        "language": language,
        "content": content[language]
    }

# ---------------- M1 AI PERFORMANCE ----------------

@app.get("/ai-performance/{patient_id}")
def get_ai_performance(patient_id: str):

    file_path = Path(__file__).resolve().parent.parent / "model train" / "model_predictions.csv"

    if not file_path.exists():
        return {
            "message": "M1 prediction file not found"
        }

    df = pd.read_csv(file_path)

    patient_data = df[
        df["patient_id"] == patient_id
    ]

    if patient_data.empty:
        return {
            "message": "No M1 prediction found for this patient"
        }

    latest = patient_data.iloc[-1]

    return {
        "patient_id": patient_id,
        "performance_score": round(float(latest["performance_score"]), 2),
        "performance_level": latest["performance_level"],
        "predicted_performance": latest["predicted_performance"]
    }