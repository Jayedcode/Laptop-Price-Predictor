import streamlit as st
import pickle
import numpy as np
from io import StringIO
from datetime import datetime

# Load model and data
try:
    pipe = pickle.load(open('pipe.pkl', 'rb'))
    df = pickle.load(open('df.pkl', 'rb'))
except Exception as e:
    st.error(f"🚨 Error loading model or data: {e}")
    st.stop()

# Sidebar: Branding and Dark Mode
st.sidebar.markdown("## 💻 Laptop Price App")
dark_mode = st.sidebar.toggle("🌙 Enable Dark Mode")

# Apply dynamic CSS
st.markdown(f"""
    <style>
    body {{
        font-family: 'Segoe UI', sans-serif;
        transition: background-color 0.4s ease;
    }}

    [data-testid="stAppViewContainer"] {{
        background-color: {"#121212" if dark_mode else "#f4f8fb"};
        transition: all 0.3s ease-in-out;
        padding: 1rem;
        color: {"#FFFFFF" if dark_mode else "#000000"};
    }}

    .card {{
        max-width: 900px;
        margin: auto;
        background: {"#1e1e1eaa" if dark_mode else "#ffffffdd"};
        border-radius: 20px;
        padding: 2rem 3rem;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15);
        backdrop-filter: blur(8px);
        color: {"#FFFFFF" if dark_mode else "#000000"};
        transition: all 0.4s ease-in-out;
    }}

    h1, h3 {{
        color: {"#00FFAB" if dark_mode else "#007BFF"};
        text-align: center;
    }}

    .stButton>button {{
        background: {"#00FFAB" if dark_mode else "#007BFF"};
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: none;
        margin-top: 1rem;
    }}

    .stButton>button:hover {{
        background: {"#00cc88" if dark_mode else "#3399ff"};
        transition: 0.3s;
    }}

    .footer {{
        margin-top: 3rem;
        text-align: center;
        color: {"#bbbbbb" if dark_mode else "#666666"};
        font-size: 14px;
        padding-top: 20px;
    }}
    </style>
""", unsafe_allow_html=True)

# Main card
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.title("🔮 Laptop Price Predictor")
st.markdown("Customize your configuration to get an estimated market price.")

# Input layout
col1, col2 = st.columns(2)

with col1:
    company = st.selectbox('Brand', sorted(df['Company'].unique()))
    laptop_type = st.selectbox('Type', sorted(df['TypeName'].unique()))
    ram = st.selectbox('RAM (GB)', [2, 4, 6, 8, 12, 16, 24, 32, 64])
    weight = st.number_input('Weight (kg)', format="%.2f")
    touchscreen = st.selectbox('Touchscreen', ['No', 'Yes'])
    ips = st.selectbox('IPS Display', ['No', 'Yes'])

with col2:
    screen_size = st.slider('Screen Size (inches)', 10.0, 18.0, 13.3)
    resolution = st.selectbox('Screen Resolution', [
        '1920x1080', '1366x768', '1600x900',
        '3840x2160', '3200x1800', '2880x1800',
        '2560x1600', '2560x1440', '2304x1440'
    ])
    cpu = st.selectbox('CPU', sorted(df['Cpu brand'].unique()))
    hdd = st.selectbox('HDD (GB)', [0, 128, 256, 512, 1024, 2048])
    ssd = st.selectbox('SSD (GB)', [0, 8, 128, 256, 512, 1024])
    gpu = st.selectbox('GPU', sorted(df['Gpu brand'].unique()))
    os = st.selectbox('Operating System', sorted(df['os'].unique()))

# Predict button
if st.button("💰 Predict Price"):
    try:
        # Preprocess inputs
        touchscreen_val = 1 if touchscreen == 'Yes' else 0
        ips_val = 1 if ips == 'Yes' else 0
        X_res, Y_res = map(int, resolution.split('x'))
        ppi = ((X_res**2 + Y_res**2) ** 0.5) / screen_size

        input_data = np.array([company, laptop_type, ram, weight, touchscreen_val, ips_val, ppi,
                               cpu, hdd, ssd, gpu, os]).reshape(1, -1)

        predicted_price = int(np.exp(pipe.predict(input_data)[0]))

        # Styled price output
        price_html = f"""
            <div style='
                font-size: 36px;
                font-weight: 800;
                color: {"#00FFAB" if dark_mode else "#007BFF"};
                padding: 1rem;
                border-radius: 12px;
                background-color: {"#003322" if dark_mode else "#e6f7ff"};
                text-align: center;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1);
                margin-top: 20px;
            '>
            ✅ Estimated Price: ₹{predicted_price:,}
            </div>
        """
        st.markdown(price_html, unsafe_allow_html=True)

        # 📄 Download quote content
        quote_text = f"""Laptop Price Estimate

🖥️ Brand: {company}
💻 Type: {laptop_type}
🧠 RAM: {ram} GB
⚖️ Weight: {weight:.2f} kg
🖲️ Touchscreen: {touchscreen}
🖼️ IPS: {ips}
📏 Screen Size: {screen_size} inches
🔢 Resolution: {resolution}
⚙️ CPU: {cpu}
💾 HDD: {hdd} GB
💽 SSD: {ssd} GB
🎮 GPU: {gpu}
🖥️ OS: {os}

📈 PPI: {ppi:.2f}

💸 Estimated Price: ₹{predicted_price:,}
📅 Date: {datetime.now().strftime('%d %B %Y, %I:%M %p')}
"""

        # ✅ Download button with string data
        st.download_button(
            label="📄 Download Quote as TXT",
            data=quote_text,
            file_name="laptop_price_quote.txt",
            mime="text/plain"
        )

    except Exception as e:
        st.error(f"⚠️ Prediction failed: {e}")

# Footer
st.markdown("</div>", unsafe_allow_html=True)
st.markdown(f"""
    <div class='footer'>
        Made with ❤️ by <strong>Jayed Akhtar</strong>
    </div>
""", unsafe_allow_html=True)
