
# Voicestack - Dental Call Analytics Dashboard

An AI-powered **Streamlit dashboard** that analyzes dental call logs to provide actionable insights on **front desk performance**, **patient communication**, and **business efficiency**.

![Overview](https://img.shields.io/badge/Status-Ready-green) ![Python](https://img.shields.io/badge/Python-3.8%2B-blue) ![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)

## 🚀 Overview

This dashboard helps dental practices:
- Track **call volumes**, **answered vs missed calls**, and **average durations**
- Understand **new vs existing patient interactions**
- Identify **peak call hours** for better staffing decisions
- Generate **business insights** for improved efficiency and revenue
- Explore raw call data interactively

The dataset includes call metadata such as time, direction, duration, call type, and transcripts (with all PHI/PII redacted).

## 🧠 Key Features

- 📊 **Interactive Analytics:** Real-time filters for date, direction, and category
- 📈 **Dynamic Visualizations:** Line charts, pie charts, and bar charts with trend tracking
- 💬 **AI Call Classification:** Classifies transcripts into categories (Appointment, Billing, Insurance, Emergency, etc.)
- 💡 **Insight Generation:** Automatic recommendations for front desk and management decisions
- 🧾 **Data Explorer:** Filter and view raw call data directly inside the app

## 🧩 Tech Stack

| Category | Tools |
|-----------|--------|
| **Frontend** | Streamlit |
| **Backend / Data** | Python, Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn |
| **Styling** | Custom CSS |
| **Optional Integration** | Google Sheets as data source |

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/dental-call-analytics.git
cd dental-call-analytics
```

### 2️⃣ Create a Virtual Environment (Optional but Recommended)
```bash
python -m venv venv
source venv/bin/activate    # For macOS/Linux
venv\Scripts\activate       # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the App
```bash
streamlit run app.py
```

## 📋 Requirements

The `requirements.txt` file includes:
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.21.0
matplotlib>=3.5.0
seaborn>=0.11.0
plotly>=5.13.0
```
## 🔬 Google Colab Notebook

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/187wVaUEuRromdobXVqlIuVw_ggthAt6C?usp=sharing)

For data preprocessing and model training, check out our interactive Colab notebook:
- **Data cleaning and analysis**
- **AI model training**
- **Visualization experiments**
