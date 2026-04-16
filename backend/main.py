from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re
import socket
import hashlib
import os
import time
import psycopg2

DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_DB", "app")
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "password")


app = FastAPI(title="Password Strength Checker API")


class PasswordRequest(BaseModel):
    password: str


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )


def wait_for_db():
    for _ in range(10):
        try:
            conn = get_connection()
            conn.close()
            return
        except Exception:
            time.sleep(2)
    raise Exception("Database not available")


@app.on_event("startup")
def startup():
    wait_for_db()


def evaluate_password(password: str):
    length = len(password)
    has_uppercase = bool(re.search(r"[A-Z]", password))
    has_lowercase = bool(re.search(r"[a-z]", password))
    has_digit = bool(re.search(r"\d", password))
    has_special = bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password))

    score = sum([
        length >= 8,
        has_uppercase,
        has_lowercase,
        has_digit,
        has_special
    ])

    strength_map = {
        0: "very weak",
        1: "very weak",
        2: "weak",
        3: "medium",
        4: "strong",
        5: "very strong"
    }

    return score, strength_map[score]


@app.get("/health")
def health():
    try:
        conn = get_connection()
        conn.close()
        return {"status": "ok"}
    except Exception:
        raise HTTPException(status_code=503, detail="DB unavailable")


@app.post("/api/check-password")
def check_password(data: PasswordRequest):

    score, strength = evaluate_password(data.password)

    password_hash = hashlib.sha256(data.password.encode()).hexdigest()

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO password_checks (password_hash, score, strength)
            VALUES (%s, %s, %s)
            RETURNING id;
            """,
            (password_hash, score, strength)
        )

        record_id = cur.fetchone()[0]

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "id": record_id,
        "score": score,
        "strength": strength,
        "instance": socket.gethostname()
    }