from flask import Flask, request, jsonify
from flask_cors import CORS
import re
from datetime import date
from database import init_db, get_conn
from ai_service import get_prediction

app = Flask(__name__)
CORS(app)
init_db()

EMAIL_RE = re.compile(r'^[\w.+-]+@[\w-]+\.[\w.]+$')


def validate(data):
    errors = []
    if not data.get("full_name", "").strip():
        errors.append("Full name is required.")
    try:
        dob = date.fromisoformat(data.get("dob", ""))
        if dob > date.today():
            errors.append("Date of birth cannot be a future date.")
    except ValueError:
        errors.append("Invalid date of birth.")
    if not EMAIL_RE.match(data.get("email", "").strip()):
        errors.append("Invalid email address.")
    for field in ("glucose", "haemoglobin", "cholesterol"):
        try:
            float(data.get(field, ""))
        except (TypeError, ValueError):
            errors.append(f"{field.capitalize()} must be a number.")
    return errors


# ── GET all patients ──────────────────────────────────────────────────────────
@app.route("/api/patients", methods=["GET"])
def list_patients():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM patients ORDER BY id DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])


# ── POST create patient ───────────────────────────────────────────────────────
@app.route("/api/patients", methods=["POST"])
def create_patient():
    data   = request.get_json()
    errors = validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    remarks = get_prediction(
        data["full_name"],
        float(data["glucose"]),
        float(data["haemoglobin"]),
        float(data["cholesterol"]),
    )
    conn = get_conn()
    cur  = conn.execute(
        "INSERT INTO patients (full_name,dob,email,glucose,haemoglobin,cholesterol,remarks) "
        "VALUES (?,?,?,?,?,?,?)",
        (data["full_name"].strip(), data["dob"], data["email"].strip(),
         float(data["glucose"]), float(data["haemoglobin"]),
         float(data["cholesterol"]), remarks),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM patients WHERE id=?", (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201


# ── GET single patient ────────────────────────────────────────────────────────
@app.route("/api/patients/<int:pid>", methods=["GET"])
def get_patient(pid):
    conn = get_conn()
    row  = conn.execute("SELECT * FROM patients WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))


# ── PUT update patient ────────────────────────────────────────────────────────
@app.route("/api/patients/<int:pid>", methods=["PUT"])
def update_patient(pid):
    data   = request.get_json()
    errors = validate(data)
    if errors:
        return jsonify({"errors": errors}), 400

    remarks = get_prediction(
        data["full_name"],
        float(data["glucose"]),
        float(data["haemoglobin"]),
        float(data["cholesterol"]),
    )
    conn = get_conn()
    conn.execute(
        "UPDATE patients SET full_name=?,dob=?,email=?,glucose=?,haemoglobin=?,"
        "cholesterol=?,remarks=? WHERE id=?",
        (data["full_name"].strip(), data["dob"], data["email"].strip(),
         float(data["glucose"]), float(data["haemoglobin"]),
         float(data["cholesterol"]), remarks, pid),
    )
    conn.commit()
    row = conn.execute("SELECT * FROM patients WHERE id=?", (pid,)).fetchone()
    conn.close()
    if not row:
        return jsonify({"error": "Not found"}), 404
    return jsonify(dict(row))


# ── DELETE patient ────────────────────────────────────────────────────────────
@app.route("/api/patients/<int:pid>", methods=["DELETE"])
def delete_patient(pid):
    conn = get_conn()
    conn.execute("DELETE FROM patients WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
