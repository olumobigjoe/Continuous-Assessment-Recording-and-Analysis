# 📡 GLT 302 — General Instrumentation Online Test System

> **Secure, timed, randomised multi-choice test platform for university students**  
> Built with Python · Streamlit · Pandas · 60-question bank · Anti-cheat · Live scoreboard

[![Python](https://img.shields.io/badge/Python-3.x-blue?style=flat-square&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-≥1.28-red?style=flat-square&logo=streamlit)](https://streamlit.io)
[![Questions](https://img.shields.io/badge/Question_Bank-60_questions-green?style=flat-square)]()
[![Served](https://img.shields.io/badge/Per_Student-40_questions-orange?style=flat-square)]()
[![Duration](https://img.shields.io/badge/Duration-10_minutes-yellow?style=flat-square)]()
[![Pass Mark](https://img.shields.io/badge/Pass_Mark->50%25-informational?style=flat-square)]()
[![License](https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square)]()

---

## 📌 Overview

The **GLT 302 General Instrumentation Online Test System** is a fully featured, browser-based examination platform designed for the Department of Science Laboratory Technology. It delivers a randomised, timed, anti-cheat test to university students — with instant feedback on every answer, a live real-time scoreboard, and automatic CSV export of all results.

Each student is served **40 randomly selected questions** drawn from a **bank of 60**, ensuring that no two students receive the same test while all questions come from the same GLT 302 course syllabus.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔐 **Student login** | Full name (max 60 chars), 4-digit Application Number, Department |
| 🎲 **Randomised questions** | 40 questions drawn randomly from a bank of 60 per session |
| 🔀 **Shuffled options** | Answer option order is randomised per student per session |
| ⏱️ **10-minute countdown** | Auto-submits and locks the test when time expires |
| ✅ **Instant feedback** | Correct: green tick · Wrong: red alert with correct answer revealed |
| 🔒 **Answer lock** | Once an option is selected, it cannot be changed |
| 🗂️ **Question navigator** | Grid showing ✅/❌/number for all 40 questions at a glance |
| 🛡️ **Triple anti-cheat** | Blocks re-attempts by device, name, and application number |
| 📊 **Live scoreboard** | Real-time table of all submissions visible on every page |
| 🏆 **Pass/Fail result** | Score over 100, correct count, PASS/FAIL banner |
| 💾 **CSV export** | Every result saved automatically to `glt302_scores.csv` |
| 🔢 **Numbered questions** | All questions labelled Q1 to Q40 on screen |

---

## 🏫 Departments Supported

- Microbiology — Morning Class
- Microbiology — Evening Class
- Physics and Glass Technology

---

## 📚 Question Bank — 60 Questions Across 9 Chapters

| Chapter | Topic | Questions |
|---|---|---|
| 1 | Introduction to Measurement | 10 |
| 2 | Electronic Instruments | 10 |
| 3 | Multimeter & Oscilloscope Use | 5 |
| 4 | Thermocouple & Potentiometer | 6 |
| 5 | Signal Generator | 5 |
| 6 | Pressure Measurement | 7 |
| 7 | Recorder & Reproducer | 4 |
| 8 | Power Supply | 6 |
| 9 | Electronic Troubleshooting | 7 |
| | **Total** | **60** |

Every question has exactly **3 answer options** and a single correct answer. Options are shuffled on every login so students cannot share answers by option position (e.g. "Option B").

---

## 🛡️ Anti-Cheat System — Three Independent Locks

The system enforces one attempt per student using three simultaneous checks, all stored persistently in `glt302_attempts.json`:

```
Attempt blocked if ANY of these match a previous submission:
  1. Device fingerprint  → 64-bit random ID stored in Streamlit session state
  2. Application Number  → exact 4-digit match
  3. Student Full Name   → case-insensitive match
```

Both the device fingerprint AND the student credentials are checked — so using a different device with the same name/application number is also blocked, and using the same device with different credentials is equally blocked.

The attempt record is written to disk **immediately at submission**, surviving app restarts.

---

## ⏱️ Timer Behaviour

- Timer starts the moment the student passes login
- Counts down from **10:00** (600 seconds) in real time
- **Turns red** when less than 60 seconds remain
- A progress bar mirrors the countdown
- When the timer reaches zero, the test **auto-submits** whatever has been answered and transitions to the result page — no student action required

---

## 🎯 Scoring

| Metric | Value |
|---|---|
| Total questions served | 40 |
| Score formula | (Correct answers ÷ 40) × 100 |
| Pass mark | **Score > 50** |
| Unanswered questions | Count as 0 (no negative marking) |

Skipped or unanswered questions simply receive no marks. Students are free to navigate between questions and can answer in any order before submitting.

---

## 📋 App Pages

| Page | Trigger | Description |
|---|---|---|
| **Login** | App start | Name, App No, Department entry; live scoreboard visible |
| **Test** | Successful login | 40 questions with timer, navigator, navigation buttons |
| **Result** | Submit or timeout | PASS/FAIL banner, score, correct count, live scoreboard |
| **Blocked** | Duplicate attempt detected | Access denied message with reason and live scoreboard |

---

## 🖥️ Test Page Walkthrough

```
┌─────────────────────────────────────────────────────┐
│  📡 GLT 302 – General Instrumentation Test          │
│  Student: [Name] | Q1 of 40                         │
├─────────────────────────────────────────────────────┤
│  ⏱ Time remaining:  09:42        [progress bar]     │
│  Answered: 0 / 40 | Correct so far: 0               │
├─────────────────────────────────────────────────────┤
│  Q1. Which of the following best defines ...?       │
│                                                     │
│  ▸ Multiselect (pick 1):                            │
│    [ ] Option A                                     │
│    [ ] Option B   ← student selects                 │
│    [ ] Option C                                     │
│                                                     │
│  ✅ Correct!   ── or ──   ❌ Wrong! Answer is: ...  │
├─────────────────────────────────────────────────────┤
│  [← Previous]              [Next →]                 │
│                                                     │
│  ▸ Submit test early (expander)                     │
│  ▸ Question navigator (expander)                    │
│    1  2  3  ✅  ❌  6  7  8 ...                     │
└─────────────────────────────────────────────────────┘
```

---

## 💾 Data Files

### `glt302_scores.csv` — Student Results

Created automatically on first submission; new rows are appended.

| Column | Type | Description |
|---|---|---|
| `Timestamp` | String | `YYYY-MM-DD HH:MM:SS` of submission |
| `Name` | String | Student's full name |
| `App_No` | String | 4-digit application number |
| `Department` | String | Selected department |
| `Score (%)` | Float | Score as percentage (0–100) |
| `Result` | String | `PASS` or `FAIL` |

**Example row:**
```
2026-03-15 10:23:44, Okonkwo Chidinma Grace, 1234, Microbiology - Morning Class, 72.5, PASS
```

### `glt302_attempts.json` — Anti-Cheat Store

Maps device fingerprints to student credentials. Survives app restarts.

```json
{
  "8291048576392847362": {
    "name": "Okonkwo Chidinma Grace",
    "app_no": "1234"
  }
}
```

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/glt302-test-system.git
cd glt302-test-system
```

### 2. Install dependencies

```bash
pip install streamlit pandas
```

### 3. Run the app

```bash
streamlit run glt302_test.py
```

The app opens at `http://localhost:8501`.

### 4. Share with students

Share the **Network URL** shown in your terminal with students connected to the same Wi-Fi network:

```
Local URL:   http://localhost:8501
Network URL: http://192.168.x.x:8501
```

For students outside the local network, deploy to Streamlit Cloud (see below).

---

## 🌐 Deploy to Streamlit Cloud (Free)

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **New app** → select this repo → set the main file to `glt302_test.py`.
4. Click **Deploy** — you receive a public URL to share with all students.

> **Note:** On Streamlit Cloud, `glt302_scores.csv` and `glt302_attempts.json` live in the app's ephemeral filesystem and reset on each deployment. For a persistent run, host the app on a dedicated machine or mount persistent storage.

---

## 📁 Repository Structure

```
glt302-test-system/
├── glt302_test.py          ← entire application (single file)
├── README.md               ← this file
├── requirements.txt        ← Python dependencies
└── data/                   (auto-created at runtime)
    ├── glt302_scores.csv   ← student results (appended each submission)
    └── glt302_attempts.json← anti-cheat device/name/app-no store
```

### `requirements.txt`

```
streamlit>=1.28.0
pandas>=2.0.0
```

---

## ⚙️ Configuration

All adjustable constants are at the top of `glt302_test.py`:

| Constant | Default | Controls |
|---|---|---|
| `DURATION_SEC` | `600` | Test duration in seconds (600 = 10 min) |
| `NUM_QUESTIONS` | `40` | Questions served per student |
| `PASS_MARK` | `50` | Pass threshold — score must be **above** this |
| `SCORES_CSV` | `"glt302_scores.csv"` | Output path for results |
| `ATTEMPTS_JSON` | `"glt302_attempts.json"` | Path for anti-cheat store |
| `DEPARTMENTS` | 3 departments | List of selectable departments |

---

## 📖 Adding or Editing Questions

All 60 questions live in the `ALL_QUESTIONS` list in `glt302_test.py`. Each question follows this structure:

```python
{
    "q": "Your question text here?",
    "options": [
        "Option A text",
        "Option B text",
        "Option C text",
    ],
    "answer": "Option A text",   # must match one of the options exactly
},
```

**Rules:**
- Each question must have **exactly 3 options**
- The `answer` value must exactly match one of the strings in `options`
- The bank must contain **at least 40 questions** (currently 60)
- Options are automatically shuffled per student session — do not rely on order

---

## 🔄 Resetting Between Test Sessions

To clear all records and allow a new cohort to take the test:

```bash
rm glt302_scores.csv glt302_attempts.json
```

Then restart the app:

```bash
streamlit run glt302_test.py
```

---

## 📊 Viewing Results During the Test

The **live scoreboard** is visible on three pages:
- Login page (scroll down below the login form)
- Result page (after submission)
- Blocked page (for students who attempt twice)

The table updates automatically with each new submission, showing all students' names, departments, scores, and pass/fail status in real time.

To download results as a CSV after the test, simply retrieve the `glt302_scores.csv` file from the server.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3 | Core language |
| Streamlit | Web UI framework, session state, page routing |
| Pandas | CSV read/write for scoreboard |
| json | Persistent anti-cheat device store |
| random | Question selection and option shuffling |
| time | Countdown timer logic |
| datetime | Timestamping submissions |

---

## 📄 License

MIT — free to use, modify, and deploy for academic purposes.

---

## ⚠️ Disclaimer

This system is designed for supervised academic testing. The anti-cheat mechanism uses a browser session fingerprint (not hardware identification) — it is robust against casual re-attempts but not against determined circumvention in an unsupervised environment. For high-stakes examinations, additional invigilation is recommended.

---

*GLT 302 — General Instrumentation · Department of Science Laboratory Technology · Built with Python + Streamlit*
