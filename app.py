import streamlit as st
import pickle
import numpy as np

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Turbidity Removal Efficiency Predictor",
    page_icon="💧",
    layout="wide",
)

# -----------------------------
# LOAD MODEL
# -----------------------------
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# -----------------------------
# SESSION STATE
# -----------------------------
default_values = {
    "dda": 0.0,
    "mw": 0.0,
    "dose": 0.0,
    "ph": 0.0,
    "settling_time": 0.0,
    "initial_turbidity": 0.0,
    "rapid_mix_speed": 0.0,
    "residual_turbidity": 0.0,
    "prediction": None,
    "show_confirm": False
}

for key, value in default_values.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# CUSTOM CSS
# -----------------------------
st.markdown("""
<style>

/* Main background */
.stApp{
    background: linear-gradient(135deg, #020617, #0f172a, #111827);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

/* Remove default top spacing */
.block-container{
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Title styling */
.main-title{
    text-align:center;
    font-size:55px;
    font-weight:800;
    color:#38bdf8;
    margin-bottom:5px;
}

.sub-title{
    text-align:center;
    font-size:20px;
    color:#cbd5e1;
    margin-bottom:40px;
}

/* Input container */
.input-box{
    background: rgba(255,255,255,0.05);
    padding:30px;
    border-radius:25px;
    border:1px solid rgba(255,255,255,0.08);
    box-shadow:0px 0px 25px rgba(0,0,0,0.4);
}

/* LABELS */
label{
    color:white !important;
    font-size:17px !important;
    font-weight:600 !important;
}

/* Input fields */
.stNumberInput input{
    background-color: rgba(255,255,255,0.95);
    color:black;
    border-radius:12px;
    border:2px solid #38bdf8;
    font-size:17px;
    padding:10px;
}

/* Predict button */
div.stButton > button:first-child{
    width:100%;
    height:50px;
    border:none;
    border-radius:15px;
    background: linear-gradient(to right, #0ea5e9, #2563eb);
    color:white;
    font-size:20px;
    font-weight:bold;
    transition:0.3s;
    margin-top:5px;
}

div.stButton > button:first-child:hover{
    transform:scale(1.02);
    background: linear-gradient(to right, #0284c7, #1d4ed8);
}

/* Prediction card */
.prediction-card{
    margin-top:35px;
    background: linear-gradient(135deg, #06b6d4, #2563eb);
    padding:35px;
    border-radius:25px;
    text-align:center;
    box-shadow:0px 0px 30px rgba(37,99,235,0.5);
}

.prediction-title{
    color:white;
    font-size:30px;
    font-weight:700;
}

/* Footer */
.footer{
    text-align:center;
    color:#94a3b8;
    margin-top:40px;
    font-size:14px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown(
    '<div class="main-title">💧 Turbidity Removal Efficiency Predictor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Advanced Machine Learning Prediction System for Water Treatment Analysis</div>',
    unsafe_allow_html=True
)

# -----------------------------
# INPUT SECTION
# -----------------------------
st.markdown('<div class="input-box">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:

    st.session_state.dda = st.number_input(
        "Degree of Deacetylation (DDA) (%)",
        value=st.session_state.dda,
        format="%.2f"
    )

    st.session_state.mw = st.number_input(
        "Molecular Weight (kDa)",
        value=st.session_state.mw,
        format="%.2f"
    )

    st.session_state.dose = st.number_input(
        "Dose (mg/L)",
        value=st.session_state.dose,
        format="%.2f"
    )

    st.session_state.ph = st.number_input(
        "pH",
        value=st.session_state.ph,
        format="%.2f"
    )

with col2:

    st.session_state.settling_time = st.number_input(
        "Settling Time (minutes)",
        value=st.session_state.settling_time,
        format="%.2f"
    )

    st.session_state.initial_turbidity = st.number_input(
        "Initial Turbidity (NTU)",
        value=st.session_state.initial_turbidity,
        format="%.2f"
    )

    st.session_state.rapid_mix_speed = st.number_input(
        "Rapid Mix Speed (rpm)",
        value=st.session_state.rapid_mix_speed,
        format="%.2f"
    )

    st.session_state.residual_turbidity = st.number_input(
        "Residual Turbidity (NTU)",
        value=st.session_state.residual_turbidity,
        format="%.2f"
    )

# -----------------------------
# BUTTONS
# -----------------------------
btn1, btn2 = st.columns(2)

with btn1:
    predict = st.button("🔮 Predict Efficiency")

with btn2:
    clear = st.button("🗑️ Clear Inputs")

st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# PREDICT
# -----------------------------
if predict:

    features = np.array([[
        st.session_state.dda,
        st.session_state.mw,
        st.session_state.dose,
        st.session_state.ph,
        st.session_state.settling_time,
        st.session_state.initial_turbidity,
        st.session_state.residual_turbidity,
        st.session_state.rapid_mix_speed
    ]])

    prediction = model.predict(features)[0]

    st.session_state.prediction = round(prediction, 2)

# -----------------------------
# CLEAR CONFIRMATION
# -----------------------------
if clear:
    st.session_state.show_confirm = True

if st.session_state.show_confirm:

    st.warning("⚠️ Are you sure you want to clear all inputs and predictions?")

    yes_col, no_col = st.columns(2)

    with yes_col:
        yes = st.button("✅ Yes, Clear Everything")

    with no_col:
        no = st.button("❌ No, Keep Values")

    if yes:

        st.session_state.dda = 0.0
        st.session_state.mw = 0.0
        st.session_state.dose = 0.0
        st.session_state.ph = 0.0
        st.session_state.settling_time = 0.0
        st.session_state.initial_turbidity = 0.0
        st.session_state.rapid_mix_speed = 0.0
        st.session_state.residual_turbidity = 0.0
        st.session_state.prediction = None
        st.session_state.show_confirm = False

        st.rerun()

    if no:
        st.session_state.show_confirm = False
        st.rerun()

# -----------------------------
# DISPLAY PREDICTION
# -----------------------------
if st.session_state.prediction is not None:

    st.markdown(f"""
    <div class="prediction-card">
        <div class="prediction-title">
            Predicted Turbidity Removal Efficiency:
            <br><br>
            {st.session_state.prediction}%
        </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown(
    '<div class="footer">Developed with Streamlit & Machine Learning</div>',
    unsafe_allow_html=True
)