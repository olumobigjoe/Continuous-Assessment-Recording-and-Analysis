import streamlit as st
import pandas as pd
import random
import time
import json
import os
from datetime import datetime

# ── PAGE CONFIG ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GLT 302 – General Instrumentation Test",
    page_icon="📡",
    layout="centered",
)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
DURATION_SEC   = 600          # 10 minutes
NUM_QUESTIONS  = 40           # questions per student
PASS_MARK      = 49           # pass if score > 49
SCORES_CSV     = "glt302_scores.csv"
ATTEMPTS_JSON  = "glt302_attempts.json"
DEPARTMENTS    = [
    "Microbiology - Morning Class",
    "Microbiology - Evening Class",
    "Physics",
]

# ── QUESTION BANK (60 questions) ──────────────────────────────────────────────
ALL_QUESTIONS = [
    # ── Chapter 1: Introduction to Measurement ──────────────────────────────
    {
        "q": "Which of the following best defines 'instrumentation'?",
        "options": [
            "The science of building musical instruments",
            "The science and technology of measuring and controlling physical quantities",
            "The study of electrical circuits only",
        ],
        "answer": "The science and technology of measuring and controlling physical quantities",
    },
    {
        "q": "The difference between the measured value and the true value of a quantity is called:",
        "options": ["Precision", "Error", "Sensitivity"],
        "answer": "Error",
    },
    {
        "q": "Which term describes the ability of an instrument to give the same reading repeatedly under the same conditions?",
        "options": ["Accuracy", "Repeatability", "Linearity"],
        "answer": "Repeatability",
    },
    {
        "q": "The smallest change in input that produces a detectable change in output is called:",
        "options": ["Threshold", "Resolution", "Span"],
        "answer": "Resolution",
    },
    {
        "q": "Which type of error is caused by changes in the environment such as temperature and humidity?",
        "options": ["Gross error", "Systematic error", "Environmental error"],
        "answer": "Environmental error",
    },
    {
        "q": "Accuracy of a measuring instrument is defined as:",
        "options": [
            "The closeness of a measured value to the true value",
            "The ability to produce the same result every time",
            "The range of values the instrument can measure",
        ],
        "answer": "The closeness of a measured value to the true value",
    },
    {
        "q": "A zero error in an instrument is an example of which type of error?",
        "options": ["Random error", "Systematic error", "Gross error"],
        "answer": "Systematic error",
    },
    {
        "q": "Which of the following is the SI unit of electric current?",
        "options": ["Volt", "Ampere", "Watt"],
        "answer": "Ampere",
    },
    {
        "q": "The ratio of change in output to change in input of a measuring instrument is called:",
        "options": ["Sensitivity", "Accuracy", "Drift"],
        "answer": "Sensitivity",
    },
    {
        "q": "Calibration of an instrument refers to:",
        "options": [
            "Adjusting the zero of the instrument only",
            "Comparing the instrument reading against a known standard",
            "Replacing worn parts of the instrument",
        ],
        "answer": "Comparing the instrument reading against a known standard",
    },

    # ── Chapter 2: Electronic Instruments ────────────────────────────────────
    {
        "q": "An oscilloscope is primarily used to:",
        "options": [
            "Measure resistance",
            "Display waveforms and measure voltage vs time",
            "Measure frequency only",
        ],
        "answer": "Display waveforms and measure voltage vs time",
    },
    {
        "q": "The time base of an oscilloscope controls:",
        "options": [
            "The vertical sensitivity",
            "The horizontal sweep speed",
            "The brightness of the display",
        ],
        "answer": "The horizontal sweep speed",
    },
    {
        "q": "On an oscilloscope, the Y-axis represents:",
        "options": ["Time", "Voltage", "Frequency"],
        "answer": "Voltage",
    },
    {
        "q": "Which control on an oscilloscope is used to adjust the height of the displayed waveform?",
        "options": [
            "Time/div",
            "Volts/div",
            "Trigger level",
        ],
        "answer": "Volts/div",
    },
    {
        "q": "A digital multimeter (DMM) can measure all of the following EXCEPT:",
        "options": ["Voltage", "Resistance", "Magnetic flux"],
        "answer": "Magnetic flux",
    },
    {
        "q": "When measuring current with a multimeter, the meter should be connected:",
        "options": [
            "In parallel with the load",
            "In series with the load",
            "Across the power supply",
        ],
        "answer": "In series with the load",
    },
    {
        "q": "When measuring voltage with a multimeter, the meter should be connected:",
        "options": [
            "In series with the circuit",
            "In parallel across the component",
            "Between ground and neutral only",
        ],
        "answer": "In parallel across the component",
    },
    {
        "q": "The input impedance of a voltmeter should be:",
        "options": [
            "Very low to minimise circuit loading",
            "Very high to minimise circuit loading",
            "Equal to the source impedance",
        ],
        "answer": "Very high to minimise circuit loading",
    },
    {
        "q": "Which type of oscilloscope stores and recalls waveforms for later analysis?",
        "options": [
            "Analog oscilloscope",
            "Digital Storage Oscilloscope (DSO)",
            "Cathode Ray Oscilloscope (CRO) only",
        ],
        "answer": "Digital Storage Oscilloscope (DSO)",
    },
    {
        "q": "The trigger function of an oscilloscope is used to:",
        "options": [
            "Increase the amplitude of the signal",
            "Stabilise the waveform display on screen",
            "Filter out noise from the signal",
        ],
        "answer": "Stabilise the waveform display on screen",
    },

    # ── Chapter 3: Multimeter & Oscilloscope Use ─────────────────────────────
    {
        "q": "Before measuring a high voltage with a multimeter, you should:",
        "options": [
            "Start at the lowest range and work up",
            "Start at the highest range and work down",
            "Set the range to resistance first",
        ],
        "answer": "Start at the highest range and work down",
    },
    {
        "q": "The deflection sensitivity of a CRT oscilloscope is expressed in:",
        "options": ["Volts per division", "Amps per division", "Ohms per metre"],
        "answer": "Volts per division",
    },
    {
        "q": "To measure the frequency of a waveform on an oscilloscope, you need to know:",
        "options": [
            "The amplitude and phase of the signal",
            "The period of the waveform and the time/div setting",
            "The voltage and current simultaneously",
        ],
        "answer": "The period of the waveform and the time/div setting",
    },
    {
        "q": "A Lissajous figure displayed on an oscilloscope is used to determine:",
        "options": [
            "The amplitude of a DC signal",
            "The frequency ratio and phase difference between two signals",
            "The internal resistance of a battery",
        ],
        "answer": "The frequency ratio and phase difference between two signals",
    },
    {
        "q": "Which probe is commonly used with an oscilloscope to reduce loading effects?",
        "options": [
            "1:1 probe",
            "10:1 attenuating probe",
            "50-ohm direct probe",
        ],
        "answer": "10:1 attenuating probe",
    },

    # ── Chapter 4: Thermocouple & Potentiometer ───────────────────────────────
    {
        "q": "A thermocouple operates on the principle of:",
        "options": [
            "Change in resistance with temperature",
            "The Seebeck effect – an EMF generated by a junction of two dissimilar metals",
            "Thermal expansion of a bimetallic strip",
        ],
        "answer": "The Seebeck effect – an EMF generated by a junction of two dissimilar metals",
    },
    {
        "q": "A Type K thermocouple is made from:",
        "options": [
            "Platinum and Rhodium",
            "Chromel and Alumel",
            "Iron and Constantan",
        ],
        "answer": "Chromel and Alumel",
    },
    {
        "q": "Cold junction compensation in a thermocouple system is required because:",
        "options": [
            "The reference junction temperature must be accounted for",
            "The hot junction must be cooled to work properly",
            "Thermocouples only work at sub-zero temperatures",
        ],
        "answer": "The reference junction temperature must be accounted for",
    },
    {
        "q": "A potentiometer in instrumentation is primarily used for:",
        "options": [
            "Amplifying small voltages",
            "Precisely measuring or comparing EMF/voltage",
            "Converting current to voltage",
        ],
        "answer": "Precisely measuring or comparing EMF/voltage",
    },
    {
        "q": "In a Wheatstone bridge, balance condition is achieved when:",
        "options": [
            "The galvanometer reads maximum deflection",
            "The product of opposite arms are equal (no current flows through galvanometer)",
            "All four resistors have the same value only",
        ],
        "answer": "The product of opposite arms are equal (no current flows through galvanometer)",
    },
    {
        "q": "Which thermocouple type has the highest temperature range and is used in high-temperature furnaces?",
        "options": [
            "Type J (Iron-Constantan)",
            "Type R or S (Platinum-Rhodium)",
            "Type T (Copper-Constantan)",
        ],
        "answer": "Type R or S (Platinum-Rhodium)",
    },

    # ── Chapter 5: Signal Generator ───────────────────────────────────────────
    {
        "q": "A signal generator is used primarily to:",
        "options": [
            "Measure unknown resistance",
            "Produce test signals of specific frequency and amplitude",
            "Display waveforms on a screen",
        ],
        "answer": "Produce test signals of specific frequency and amplitude",
    },
    {
        "q": "A function generator differs from a basic signal generator in that it can produce:",
        "options": [
            "Only sine waves",
            "Sine, square, and triangular waveforms",
            "DC voltage only",
        ],
        "answer": "Sine, square, and triangular waveforms",
    },
    {
        "q": "The output impedance of a typical signal generator is:",
        "options": ["600 ohms or 50 ohms", "1 Mega-ohm", "0 ohms"],
        "answer": "600 ohms or 50 ohms",
    },
    {
        "q": "Frequency modulation (FM) in a signal generator means:",
        "options": [
            "The amplitude of the carrier varies with the modulating signal",
            "The frequency of the carrier varies with the modulating signal",
            "The phase of the signal is fixed",
        ],
        "answer": "The frequency of the carrier varies with the modulating signal",
    },
    {
        "q": "A sweep generator is used in:",
        "options": [
            "Measuring DC voltage",
            "Testing the frequency response of circuits and filters",
            "Generating only audio frequencies",
        ],
        "answer": "Testing the frequency response of circuits and filters",
    },

    # ── Chapter 6: Pressure Measurement ──────────────────────────────────────
    {
        "q": "Gauge pressure is defined as:",
        "options": [
            "Pressure measured relative to absolute zero pressure",
            "Pressure measured relative to atmospheric pressure",
            "The pressure of a perfect vacuum",
        ],
        "answer": "Pressure measured relative to atmospheric pressure",
    },
    {
        "q": "Absolute pressure equals:",
        "options": [
            "Gauge pressure minus atmospheric pressure",
            "Gauge pressure plus atmospheric pressure",
            "Atmospheric pressure only",
        ],
        "answer": "Gauge pressure plus atmospheric pressure",
    },
    {
        "q": "A manometer measures pressure by:",
        "options": [
            "The deflection of a diaphragm",
            "The height difference of a liquid column",
            "The change in electrical resistance",
        ],
        "answer": "The height difference of a liquid column",
    },
    {
        "q": "A Bourdon tube pressure gauge works on the principle that:",
        "options": [
            "Pressure causes a liquid to rise in a tube",
            "Internal pressure causes a curved tube to straighten and deflect a pointer",
            "Magnetic force deflects the measuring element",
        ],
        "answer": "Internal pressure causes a curved tube to straighten and deflect a pointer",
    },
    {
        "q": "The SI unit of pressure is:",
        "options": ["Bar", "Pascal (Pa)", "psi"],
        "answer": "Pascal (Pa)",
    },
    {
        "q": "A piezoresistive pressure sensor operates by:",
        "options": [
            "Generating a voltage from a piezoelectric crystal under pressure",
            "Changing electrical resistance of a material when pressure is applied",
            "Measuring the temperature rise caused by pressure",
        ],
        "answer": "Changing electrical resistance of a material when pressure is applied",
    },
    {
        "q": "Vacuum pressure refers to pressure that is:",
        "options": [
            "Greater than atmospheric pressure",
            "Below atmospheric pressure (negative gauge pressure)",
            "Equal to standard atmospheric pressure",
        ],
        "answer": "Below atmospheric pressure (negative gauge pressure)",
    },

    # ── Chapter 7: Recorder & Reproducer ─────────────────────────────────────
    {
        "q": "A strip chart recorder is used to:",
        "options": [
            "Measure instantaneous values only",
            "Produce a continuous graphical record of a variable against time",
            "Store digital data in binary format",
        ],
        "answer": "Produce a continuous graphical record of a variable against time",
    },
    {
        "q": "In a magnetic tape recorder, information is stored as:",
        "options": [
            "Optical patterns on the tape",
            "Variations in magnetisation of the tape coating",
            "Mechanical indentations in the tape",
        ],
        "answer": "Variations in magnetisation of the tape coating",
    },
    {
        "q": "Which type of recorder uses a heated stylus on heat-sensitive paper?",
        "options": [
            "Ink pen recorder",
            "Thermal recorder",
            "UV recorder",
        ],
        "answer": "Thermal recorder",
    },
    {
        "q": "The primary advantage of a digital data logger over an analog chart recorder is:",
        "options": [
            "It can only record one channel",
            "Data can be stored, retrieved, and analysed on a computer",
            "It requires no power supply",
        ],
        "answer": "Data can be stored, retrieved, and analysed on a computer",
    },

    # ── Chapter 8: Power Supply ────────────────────────────────────────────────
    {
        "q": "A regulated power supply maintains:",
        "options": [
            "A constant output regardless of load or input variation",
            "A varying output proportional to the load",
            "Only AC output voltage",
        ],
        "answer": "A constant output regardless of load or input variation",
    },
    {
        "q": "Line regulation of a power supply is the ability to maintain output voltage when:",
        "options": [
            "The load changes",
            "The input (mains) voltage changes",
            "The ambient temperature changes",
        ],
        "answer": "The input (mains) voltage changes",
    },
    {
        "q": "Load regulation of a power supply refers to:",
        "options": [
            "Keeping the output stable as the load current changes",
            "Keeping the input voltage constant",
            "Protecting the supply from overheating",
        ],
        "answer": "Keeping the output stable as the load current changes",
    },
    {
        "q": "A linear power supply uses which component to regulate voltage?",
        "options": [
            "A switching transistor",
            "A series pass transistor or zener diode",
            "An inductor and capacitor only",
        ],
        "answer": "A series pass transistor or zener diode",
    },
    {
        "q": "A switched-mode power supply (SMPS) is more efficient than a linear supply because:",
        "options": [
            "It uses a transformer with fewer windings",
            "The pass transistor operates in switching (on/off) mode, minimising power dissipation",
            "It only supplies DC at fixed voltage",
        ],
        "answer": "The pass transistor operates in switching (on/off) mode, minimising power dissipation",
    },
    {
        "q": "Ripple voltage in a DC power supply is caused by:",
        "options": [
            "Incorrect grounding of the chassis",
            "Incomplete filtering of the rectified AC waveform",
            "Too high an input voltage",
        ],
        "answer": "Incomplete filtering of the rectified AC waveform",
    },

    # ── Chapter 9: Electronic Troubleshooting ─────────────────────────────────
    {
        "q": "The first step in systematic electronic troubleshooting is usually:",
        "options": [
            "Replace all capacitors immediately",
            "Observe and define the fault symptoms carefully",
            "Apply maximum voltage to locate the fault",
        ],
        "answer": "Observe and define the fault symptoms carefully",
    },
    {
        "q": "Signal tracing in a faulty amplifier involves:",
        "options": [
            "Measuring resistance through each stage with power off",
            "Injecting a test signal and following it stage by stage to find where it disappears",
            "Replacing transistors one at a time",
        ],
        "answer": "Injecting a test signal and following it stage by stage to find where it disappears",
    },
    {
        "q": "A short circuit in an electronic component means:",
        "options": [
            "An open path that blocks current flow",
            "An unintended low-resistance path that allows excessive current",
            "The component value has drifted out of tolerance",
        ],
        "answer": "An unintended low-resistance path that allows excessive current",
    },
    {
        "q": "An open circuit fault means:",
        "options": [
            "Current flows freely through the component",
            "The circuit path is broken and no current can flow",
            "The resistance has decreased to zero",
        ],
        "answer": "The circuit path is broken and no current can flow",
    },
    {
        "q": "When using an oscilloscope for fault diagnosis, a flat line (no waveform) at a test point suggests:",
        "options": [
            "The signal is too large for the probe",
            "The signal is absent — indicating a possible open circuit or no drive to that stage",
            "The time/div is set too slow",
        ],
        "answer": "The signal is absent — indicating a possible open circuit or no drive to that stage",
    },
    {
        "q": "ESD (Electrostatic Discharge) precautions are important because:",
        "options": [
            "Static electricity can damage sensitive semiconductor components",
            "Static makes solder joints cold",
            "ESD only affects large power components",
        ],
        "answer": "Static electricity can damage sensitive semiconductor components",
    },
    {
        "q": "The half-split method in troubleshooting involves:",
        "options": [
            "Testing every component in order from first to last",
            "Dividing the circuit in half and testing the midpoint to narrow down the fault location",
            "Replacing the most expensive component first",
        ],
        "answer": "Dividing the circuit in half and testing the midpoint to narrow down the fault location",
    },
]

# ── PERSISTENCE HELPERS ────────────────────────────────────────────────────────
def load_attempts() -> dict:
    if os.path.exists(ATTEMPTS_JSON):
        with open(ATTEMPTS_JSON) as f:
            return json.load(f)
    return {}

def save_attempts(data: dict):
    with open(ATTEMPTS_JSON, "w") as f:
        json.dump(data, f)

def record_score(name: str, app_no: str, dept: str, score: float, result: str):
    row = pd.DataFrame([{
        "Timestamp":  datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Name":       name,
        "App_No":     app_no,
        "Department": dept,
        "Score (%)":  round(score, 1),
        "Result":     result,
    }])
    if os.path.exists(SCORES_CSV):
        row.to_csv(SCORES_CSV, mode="a", header=False, index=False)
    else:
        row.to_csv(SCORES_CSV, index=False)

def load_scores() -> pd.DataFrame:
    if os.path.exists(SCORES_CSV):
        return pd.read_csv(SCORES_CSV)
    return pd.DataFrame(columns=["Timestamp","Name","App_No","Department","Score (%)","Result"])

# ── SESSION STATE DEFAULTS ─────────────────────────────────────────────────────
_defaults = {
    "page":        "login",
    "name":        "",
    "app_no":      "",
    "dept":        "",
    "device_id":   str(random.getrandbits(64)),
    "questions":   [],
    "current_q":   0,
    "answers":     {},        # {q_idx: chosen_option}
    "correct":     {},        # {q_idx: True/False}
    "start_time":  None,
    "submitted":   False,
    "final_score": 0.0,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.stApp { background-color: #f0f4fb; }
.header-box {
    background: linear-gradient(90deg, #0a3d62, #1a6bbf);
    color: white; padding: 18px 24px; border-radius: 12px;
    margin-bottom: 20px;
}
.header-box h1 { margin: 0; font-size: 1.3rem; }
.header-box p  { margin: 5px 0 0; font-size: .85rem; opacity: .85; }
.q-card {
    background: white; border-radius: 12px;
    padding: 20px 22px; border: 1px solid #dee2e6;
    margin-bottom: 16px;
}
.q-text { font-size: 1rem; font-weight: 600; margin-bottom: 14px; color: #1a1a2e; }
.correct-banner {
    background: #d1e7dd; border: 1.5px solid #0f5132; color: #0f5132;
    border-radius: 8px; padding: 10px 14px; font-weight: 600;
    margin-top: 10px;
}
.wrong-banner {
    background: #f8d7da; border: 1.5px solid #842029; color: #842029;
    border-radius: 8px; padding: 10px 14px; margin-top: 10px;
}
.timer-box {
    background: #fff3cd; border: 1.5px solid #ffc107; color: #856404;
    border-radius: 8px; padding: 10px 18px; font-size: 1.1rem;
    font-weight: 700; text-align: center;
}
.timer-red {
    background: #f8d7da; border: 1.5px solid #842029; color: #842029;
    border-radius: 8px; padding: 10px 18px; font-size: 1.2rem;
    font-weight: 700; text-align: center;
}
.pass-banner {
    background: #d1e7dd; border: 2px solid #0f5132; color: #0f5132;
    border-radius: 12px; padding: 22px; text-align: center;
    font-size: 1.2rem; font-weight: 700; margin-bottom: 14px;
}
.fail-banner {
    background: #f8d7da; border: 2px solid #842029; color: #842029;
    border-radius: 12px; padding: 22px; text-align: center;
    font-size: 1.2rem; font-weight: 700; margin-bottom: 14px;
}
.blocked-box {
    background: #f8d7da; border: 2px solid #842029; color: #842029;
    border-radius: 12px; padding: 26px; text-align: center;
}
div.stButton > button {
    background-color: #1a6bbf !important;
    color: white !important; border-radius: 7px !important;
    font-weight: 600 !important;
}
div.stButton > button:hover {
    background-color: #0a3d62 !important;
}
/* multiselect pills */
.stMultiSelect [data-baseweb="tag"] {
    background-color: #1a6bbf !important;
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ── SHARED HEADER ──────────────────────────────────────────────────────────────
def render_header(sub=""):
    extra = f"&nbsp;&nbsp;|&nbsp;&nbsp;{sub}" if sub else ""
    st.markdown(f"""
    <div class="header-box">
        <h1>📡 GLT 302 – General Instrumentation Test</h1>
        <p>Department of Science Laboratory Technology{extra}</p>
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: LOGIN
# ══════════════════════════════════════════════════════════════════════════════
if st.session_state.page == "login":
    render_header("Student Login")

    st.markdown("### 📋 Enter your details to begin the test")

    name = st.text_input("Full Name (max 60 characters):", max_chars=60,
                         placeholder="e.g. Olumodeji Ibukun Ayodeji")

    app_no = st.text_input("Application Number :", max_chars=4,
                           placeholder="LAST 4 DIGITS OF YOUR APPLICATION NUMBER e.g. 1234")

    dept = st.selectbox("Department:", options=["-- Select Department --"] + DEPARTMENTS)

    st.markdown("**Test information:** 40 questions · 10 minutes · Pass mark: 50%")

    if st.button("Start Test", type="primary", use_container_width=True):
        name    = name.strip()
        app_no  = app_no.strip()

        # Validation
        if not name or len(name) < 3:
            st.error("Please enter your full name (at least 3 characters).")
        elif not app_no.isdigit() or len(app_no) != 4:
            st.error("Application Number must be exactly 4 digits.")
        elif dept == "-- Select Department --":
            st.error("Please select your department.")
        else:
            attempts     = load_attempts()
            dev_id       = st.session_state.device_id
            used_apps    = {v["app_no"] for v in attempts.values()}
            used_names   = {v["name"].lower() for v in attempts.values()}

            blocked = False
            if dev_id in attempts:
                blocked = True
                reason  = "This device has already been used for the test."
            elif app_no in used_apps:
                blocked = True
                reason  = f"Application number {app_no} has already taken this test."
            elif name.lower() in used_names:
                blocked = True
                reason  = f"A student with the name '{name}' has already taken this test."

            if blocked:
                st.session_state.page = "blocked"
                st.session_state.name = name
                st.rerun()
            else:
                # Select 40 random questions; shuffle option order per student
                pool = random.sample(ALL_QUESTIONS, NUM_QUESTIONS)
                for q in pool:
                    opts = q["options"].copy()
                    random.shuffle(opts)
                    q["shuffled_options"] = opts

                st.session_state.name       = name
                st.session_state.app_no     = app_no
                st.session_state.dept       = dept
                st.session_state.questions  = pool
                st.session_state.start_time = time.time()
                st.session_state.page       = "test"
                st.rerun()

    st.divider()

    # Real-time scoreboard
    st.markdown("#### 📊 Live Scoreboard")
    scores_df = load_scores()
    if scores_df.empty:
        st.info("No submissions yet.")
    else:
        st.dataframe(
            scores_df[["Timestamp","Name","App_No","Department","Score (%)","Result"]],
            use_container_width=True, hide_index=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: TEST
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "test":

    elapsed   = time.time() - st.session_state.start_time
    remaining = max(0, DURATION_SEC - int(elapsed))

    # ── Auto-submit on timeout ────────────────────────────────────────────────
    if remaining == 0 and not st.session_state.submitted:
        st.session_state.submitted = True
        # Calculate score from answered questions
        correct_count = sum(1 for v in st.session_state.correct.values() if v)
        answered      = len(st.session_state.answers)
        score         = (correct_count / NUM_QUESTIONS) * 100
        result        = "PASS" if score > PASS_MARK else "FAIL"
        st.session_state.final_score = score

        record_score(st.session_state.name, st.session_state.app_no,
                     st.session_state.dept, score, result)

        attempts = load_attempts()
        attempts[st.session_state.device_id] = {
            "name":   st.session_state.name,
            "app_no": st.session_state.app_no,
        }
        save_attempts(attempts)
        st.session_state.page = "result"
        st.rerun()

    q_idx = st.session_state.current_q
    total = NUM_QUESTIONS

    render_header(f"Student: {st.session_state.name} | Q{q_idx + 1} of {total}")

    # ── Timer ─────────────────────────────────────────────────────────────────
    mins = remaining // 60
    secs = remaining % 60
    timer_class = "timer-red" if remaining < 60 else "timer-box"
    st.markdown(
        f'<div class="{timer_class}">⏱ Time remaining: {mins:02d}:{secs:02d}</div>',
        unsafe_allow_html=True
    )
    st.progress(remaining / DURATION_SEC)

    # ── Progress ──────────────────────────────────────────────────────────────
    answered_count = len(st.session_state.answers)
    st.caption(f"Answered: {answered_count} / {total} | "
               f"Correct so far: {sum(1 for v in st.session_state.correct.values() if v)}")

    # ── Question card ─────────────────────────────────────────────────────────
    q_data = st.session_state.questions[q_idx]
    opts   = q_data["shuffled_options"]

    st.markdown(f"""
    <div class="q-card">
        <div class="q-text">Q{q_idx + 1}. {q_data['q']}</div>
    </div>""", unsafe_allow_html=True)

    # ── Already answered this question ────────────────────────────────────────
    if q_idx in st.session_state.answers:
        chosen = st.session_state.answers[q_idx]
        was_correct = st.session_state.correct[q_idx]

        # Show options as disabled multiselect (read-only look)
        st.multiselect(
            "Your selection (locked):",
            options=opts,
            default=[chosen],
            disabled=True,
            key=f"ms_locked_{q_idx}",
        )

        if was_correct:
            st.markdown('<div class="correct-banner">✅ Correct!</div>',
                        unsafe_allow_html=True)
        else:
            st.markdown(
                f'<div class="wrong-banner">❌ Wrong!&nbsp; '
                f'The correct answer is: <strong>{q_data["answer"]}</strong></div>',
                unsafe_allow_html=True,
            )

    else:
        # ── Selection widget ──────────────────────────────────────────────────
        selection = st.multiselect(
            "Select ONE answer:",
            options=opts,
            default=[],
            max_selections=1,
            key=f"ms_{q_idx}",
            placeholder="Click to choose your answer...",
        )

        if selection:
            chosen = selection[0]
            is_correct = (chosen == q_data["answer"])

            st.session_state.answers[q_idx] = chosen
            st.session_state.correct[q_idx] = is_correct

            if is_correct:
                st.markdown('<div class="correct-banner">✅ Correct!</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="wrong-banner">❌ Wrong!&nbsp; '
                    f'The correct answer is: <strong>{q_data["answer"]}</strong></div>',
                    unsafe_allow_html=True,
                )

    st.write("")

    # ── Navigation ────────────────────────────────────────────────────────────
    col_prev, col_next = st.columns(2)

    with col_prev:
        if q_idx > 0:
            if st.button("← Previous", use_container_width=True):
                st.session_state.current_q -= 1
                st.rerun()

    with col_next:
        if q_idx < total - 1:
            btn_label = "Next →"
            if q_idx not in st.session_state.answers:
                btn_label = "Skip →"
            if st.button(btn_label, use_container_width=True, type="primary"):
                st.session_state.current_q += 1
                st.rerun()

    # ── Early submit ──────────────────────────────────────────────────────────
    st.write("")
    with st.expander("⚠️ Submit test early"):
        st.warning("This will end your test immediately and submit your current answers.")
        if st.button("✅ Submit Now", type="primary", use_container_width=True):
            correct_count = sum(1 for v in st.session_state.correct.values() if v)
            score  = (correct_count / NUM_QUESTIONS) * 100
            result = "PASS" if score > PASS_MARK else "FAIL"
            st.session_state.final_score = score
            st.session_state.submitted   = True

            record_score(st.session_state.name, st.session_state.app_no,
                         st.session_state.dept, score, result)

            attempts = load_attempts()
            attempts[st.session_state.device_id] = {
                "name":   st.session_state.name,
                "app_no": st.session_state.app_no,
            }
            save_attempts(attempts)
            st.session_state.page = "result"
            st.rerun()

    # ── Question navigator grid ───────────────────────────────────────────────
    with st.expander("🗂️ Question navigator"):
        cols = st.columns(10)
        for i in range(total):
            with cols[i % 10]:
                label = str(i + 1)
                if i in st.session_state.correct:
                    label = "✅" if st.session_state.correct[i] else "❌"
                if st.button(label, key=f"nav_{i}", use_container_width=True):
                    st.session_state.current_q = i
                    st.rerun()

    # ── Auto-refresh every second ─────────────────────────────────────────────
    time.sleep(1)
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: RESULT
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "result":
    render_header("Test Complete")

    score  = st.session_state.final_score
    result = "PASS" if score > PASS_MARK else "FAIL"
    banner = "pass-banner" if score > PASS_MARK else "fail-banner"
    icon   = "🎉" if score > PASS_MARK else "📋"

    correct_count = sum(1 for v in st.session_state.correct.values() if v)

    st.markdown(f"""
    <div class="{banner}">
        {icon} {result}<br>
        <span style="font-size:1.5rem">{score:.1f} / 100</span>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Score", f"{score:.1f}%")
    c2.metric("Correct", f"{correct_count} / {NUM_QUESTIONS}")
    c3.metric("Result", result)

    st.markdown(f"""
    **Student:** {st.session_state.name}  
    **App No:** {st.session_state.app_no}  
    **Department:** {st.session_state.dept}
    """)

    st.divider()
    st.markdown("#### 📊 Live Scoreboard")
    scores_df = load_scores()
    if not scores_df.empty:
        st.dataframe(
            scores_df[["Timestamp","Name","App_No","Department","Score (%)","Result"]],
            use_container_width=True, hide_index=True
        )

# ══════════════════════════════════════════════════════════════════════════════
# PAGE: BLOCKED
# ══════════════════════════════════════════════════════════════════════════════
elif st.session_state.page == "blocked":
    render_header()
    st.markdown(f"""
    <div class="blocked-box">
        <div style="font-size:2.5rem">🚫</div>
        <div style="font-size:1.2rem; font-weight:700; margin:10px 0">Access Denied</div>
        <div>This device, name, or application number has already been used to take this test.<br>
        Each student is permitted <strong>one attempt only</strong>.<br><br>
        If you believe this is an error, please contact your lecturer.</div>
    </div>""", unsafe_allow_html=True)

    st.divider()
    st.markdown("#### 📊 Live Scoreboard")
    scores_df = load_scores()
    if not scores_df.empty:
        st.dataframe(
            scores_df[["Timestamp","Name","App_No","Department","Score (%)","Result"]],
            use_container_width=True, hide_index=True
        )
