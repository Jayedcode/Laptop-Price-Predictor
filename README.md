# 💻 Laptop Price Predictor

This is a Streamlit web app that predicts the price of a laptop based on various input features using a machine learning model.

---

## 📂 Project Structure
Laptop-Price-Predictor/
├── app.py # Streamlit app file
├── pipe.pkl # Trained ML pipeline
├── df.pkl # Dataset used for reference (e.g., for dropdowns)
├── requirements.txt # Required Python packages
└── data/ # (Optional) Additional dataset folder

---

## 🚀 How to Run the App

### 🔹 Option 1: Streamlit Cloud (Recommended)

1. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
2. Link your GitHub repo
3. Set `app.py` as the main file
4. Deploy 🚀

### 🔹 Option 2: Run Locally

```bash
git clone https://github.com/Jayedcode/Laptop-Price-Predictor.git
cd Laptop-Price-Predictor
pip install -r requirements.txt
streamlit run app.py
🔍 Features
Predicts laptop price based on specs:

Brand

RAM

Processor

Operating System

GPU

HDD/SSD

Built using a machine learning pipeline

User-friendly interface with Streamlit

🧠 Technologies Used
Python 🐍

Pandas, NumPy

Scikit-learn

Streamlit

Joblib (for model persistence)

📌 Author
Made with ❤️ by Jayed Akhtar

