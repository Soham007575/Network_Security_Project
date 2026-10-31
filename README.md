## 🚀 Live Demo

**Try the deployed application:** [Phishing Website Detection System](https://network-security-project-94m5.vercel.app)

Upload a CSV file containing website features to classify websites as **Phishing** or **Legitimate**.

## 📂 Source Code

[View the project on GitHub](https://github.com/Soham007575/Network_Security_Project)




# 🛡️ Phishing Website Detection System

### Machine Learning-Based Network Security Application

A machine learning-powered web application that analyzes website features and classifies websites as **Phishing** or **Legitimate**. The project combines a trained ML model with a FastAPI backend and an interactive web dashboard to make phishing detection easier to understand.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Machine%20Learning-Classification-orange" alt="Machine Learning">
  <img src="https://img.shields.io/badge/HTML-CSS-JavaScript-E34F26?logo=html5" alt="Frontend">
</p>

---

## 📌 Project Overview

Phishing attacks use fraudulent websites to trick users into revealing sensitive information such as passwords, banking details, and personal data.

This project uses machine learning to analyze website-related features and predict whether a website is likely to be phishing or legitimate.

The application provides a simple web interface where users can upload a CSV dataset and receive readable prediction results.

### 🎯 Objectives

- Detect potentially phishing websites using machine learning.
- Process website feature datasets through a trained model.
- Convert numerical model predictions into understandable labels.
- Display prediction summaries and individual results.
- Provide an interactive web application for demonstration and analysis.

---

## ✨ Features

- **CSV Upload:** Upload a dataset containing website features.
- **Machine Learning Prediction:** Classify each record using the trained model.
- **Readable Results:** Display `Phishing` and `Legitimate` instead of raw numeric labels.
- **Dashboard Statistics:** View total scanned, phishing detected, and legitimate websites.
- **Prediction Table:** Review the result for each record.
- **FastAPI Backend:** Process uploaded data and return prediction results through an API.
- **Interactive Web Interface:** Access the application through a browser.

---

## 🧠 How It Works

1. The user uploads a CSV file containing website features.
2. The FastAPI backend reads and validates the uploaded dataset.
3. The saved preprocessing object transforms the input features.
4. The trained machine learning model generates predictions.
5. Numeric predictions are converted into readable labels.
6. The dashboard displays summary statistics and individual results.

```text
          User
           |
           v
      Web Dashboard
           |
           v
      CSV Upload
           |
           v
       FastAPI
           |
           v
     Preprocessor
           |
           v
    Trained ML Model
           |
           v
   Prediction Results
           |
           v
  Phishing / Legitimate
           |
           v
   Results Dashboard
```

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Backend | FastAPI |
| API Server | Uvicorn |
| Frontend | HTML, CSS, JavaScript |
| Model Serialization | Pickle |
| Version Control | Git and GitHub |
| Deployment | Vercel (planned/configured) |

---

## 📂 Project Structure

```text
Network_Security_Project/
│
├── app.py
├── requirements.txt
├── README.md
│
├── final_model/
│   ├── model.pkl
│   └── preprocessor.pkl
│
├── templates/
│   ├── index.html
│   └── table.html
│
├── networksecurity/
│   ├── exception/
│   ├── utils/
│   └── ...
│
└── ...
```

The project may contain additional training, logging, and utility modules.

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Soham007575/Network_Security_Project.git
```

### 2. Navigate to the project directory

```bash
cd Network_Security_Project
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the environment

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the application

```bash
uvicorn app:app --reload
```

### 7. Open the application

Web Dashboard:

```text
http://127.0.0.1:8000/
```

FastAPI Swagger Documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 📊 Prediction Output

The API returns readable predictions and summary statistics.

Example response:

```json
{
  "total_scanned": 2,
  "phishing_count": 1,
  "legitimate_count": 1,
  "results": [
    {
      "website": "Website #1",
      "prediction": "Phishing",
      "message": "Potentially malicious website detected"
    },
    {
      "website": "Website #2",
      "prediction": "Legitimate",
      "message": "Classified as legitimate"
    }
  ]
}
```

If the input CSV contains a `URL`, `Website`, or `Domain` column, the application can display that value. Otherwise, records are identified using labels such as `Website #1`.

---

## 📁 Dataset

The model expects a CSV file containing the website features used during model training.

**Important:** The input feature names, data types, and column order must match the requirements of the saved preprocessing pipeline.

The application removes a `Result` column from the uploaded CSV when present, so that the target label is not passed into the model as an input feature.

---

## 🔒 Important Notes

- A prediction is a machine learning classification, not a guarantee that a website is safe or malicious.
- The application analyzes the provided website features. It does not automatically browse or verify the live website.
- The dataset must contain the expected model features.
- The mapping between numeric predictions and labels must match the model's training configuration.

---

## 🚀 Future Enhancements

- Direct URL input and automatic feature extraction.
- Real-time website analysis.
- Improved model evaluation and explainability.
- Prediction confidence visualization.
- User authentication and scan history.
- Enhanced responsive dashboard.
- Cloud deployment and production API configuration.

---

## 👨‍💻 Author

**Soham Antre**

Computer Engineering Student | Machine Learning | Network Security

- GitHub: [Soham007575](https://github.com/Soham007575)

---

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub.

This project was developed as an educational and practical application of machine learning in cybersecurity.
