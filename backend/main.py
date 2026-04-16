from fastapi import FastAPI
from pydantic import BaseModel
import re
import socket

app = FastAPI(title="Password Strength Checker API")


class PasswordRequest(BaseModel):
    password: str


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

    return {
        "length": length,
        "score": score,
        "strength": strength_map[score],
        "instance": socket.gethostname()  # 🔥 важно для балансировки
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/check-password")
def check_password(data: PasswordRequest):
    return evaluate_password(data.password)