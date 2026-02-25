# 🎭 AI Joke Generator — NLP Powered Comedy

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

> **An AI-powered joke generator** that uses Natural Language Processing (NLP) to analyze and serve jokes from a curated dataset. Built with a Python backend and a clean web frontend, deployed on Vercel.

**🌐 Live Demo:** [joke.vercel.app](https://joke-liart.vercel.app/)  
**📁 GitHub Repo:** [github.com/asgharghanghro/Joke](https://github.com/AsgharGhanghro/Joke)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [How It Works](#-how-it-works)
- [Dataset](#-dataset)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🌟 Overview

This project combines **NLP with a lightweight web app** to generate jokes on demand. The machine learning model is developed and trained in a Jupyter Notebook using a jokes dataset (CSV), and the results are served through a Python backend to a fun, responsive frontend.

Perfect for learning how to connect an NLP pipeline to a real web application!

---

## ✨ Features

- 🤖 **NLP-Based Generation** — Processes and serves jokes using trained patterns from the dataset
- 🌐 **Web Interface** — Clean, responsive frontend built with HTML, CSS, and JavaScript
- ⚡ **Fast Backend** — Python server (`start_app.py`) handles requests efficiently
- 📓 **Jupyter Notebook** — Full ML development and experimentation in `NLP.ipynb`
- 📊 **Rich Dataset** — Trained on 1000+ jokes across multiple categories
- 🚀 **Vercel Deployment** — One-click deployable to the web

---

## 📁 Project Structure

```
JOKES/
│
├── client/                      # Frontend (web interface)
│   ├── index.html               # Main webpage
│   ├── style.css                # Styling & layout
│   └── script.js                # Frontend logic & API calls
│
├── data/
│   └── jokes.csv                # Joke dataset (training data)
│
├── notebook/
│   ├── NLP.ipynb                # ML model development & training
│   └── dataset_examples.json   # Sample joke data examples
│
|               
├── server/       
|   |--app.py                    # Backend server files
|   |--config.py
|   |---more..  
│
├── launch.py                    # App launcher script
├── start_app.py                 # Main Python backend entry point
├── vercel.json                  # Vercel deployment configuration
├── .gitignore                   # Git ignored files
└── README.md                    # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.8 or higher**
- pip (Python package manager)
- Git
- A modern web browser

### 1. Clone the Repository

```bash
git clone https://github.com/asgharghanghro/Joke.git
cd Joke
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install pandas numpy jupyter matplotlib scikit-learn flask
```

### 4. Start the Application

```bash
python start_app.py
```

Or use the launcher:

```bash
python launch.py
```

Then open your browser at **http://localhost:5000**

### 5. (Optional) Explore the Notebook

```bash
jupyter notebook notebook/NLP.ipynb
```

---

## 🧠 How It Works

```
jokes.csv (Dataset)
      │
      ▼
NLP.ipynb (Jupyter Notebook)
  - Load & clean the dataset
  - Tokenize joke text
  - Extract patterns & features
  - Train the NLP model
      │
      ▼
start_app.py (Python Backend)
  - Loads the trained model
  - Handles API requests from frontend
      │
      ▼
client/ (Web Frontend)
  - User clicks "Generate Joke"
  - JavaScript calls the backend
  - Joke is displayed on screen
```

### NLP Pipeline Steps

1. **Data Loading** — Read `jokes.csv` with pandas
2. **Text Cleaning** — Remove special characters, normalize text
3. **Tokenization** — Split jokes into tokens/words
4. **Feature Extraction** — Convert text to numerical vectors
5. **Model Training** — Learn patterns from the joke dataset
6. **Joke Generation** — Retrieve or generate jokes based on learned patterns

---

## 📊 Dataset

The dataset lives in `data/jokes.csv` and contains:

| Field | Description |
|---|---|
| `text` | The joke content |
| `category` | Type of joke (pun, dad joke, general, etc.) |
| `rating` | Quality score |

Sample examples are available in `notebook/dataset_examples.json` for quick reference without loading the full CSV.

---

## 🌐 Deployment

This project is deployed on **Vercel** using the `vercel.json` config file.

### Deploy Your Own Copy

1. Fork this repository
2. Go to [vercel.com](https://vercel.com) → **New Project**
3. Import your forked GitHub repo
4. Vercel auto-detects the config and deploys
5. Your app is live! 🎉

### Manual Deploy via CLI

```bash
npm install -g vercel
vercel login
vercel --prod
```

---

## 🔮 Future Improvements

- [ ] Category filter (puns, dad jokes, dark humor)
- [ ] User ratings & feedback system
- [ ] Text-to-speech for jokes
- [ ] Dark mode toggle
- [ ] Joke sharing (Twitter / WhatsApp)
- [ ] Multi-language support
- [ ] Expand dataset with more joke categories
- [ ] REST API with public endpoints

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. Create a feature branch
   ```bash
   git checkout -b feature/YourFeature
   ```
3. Commit your changes
   ```bash
   git commit -m "feat: add YourFeature"
   ```
4. Push to your branch
   ```bash
   git push origin feature/YourFeature
   ```
5. Open a **Pull Request**

---

## 📄 License

MIT License — Copyright (c) 2024 Asghar Ghanghro

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.

---

## 👤 Author

**Asghar Ghanghro**

- 🐙 GitHub: [@asgharghanghro](https://github.com/asgharghanghro)
- 📧 Email: asgharghanghro@gmail.com
- 🔗 Project: [github.com/asgharghanghro/Joke](https://github.com/asgharghanghro/Joke)

---

## 🙏 Acknowledgments

- Open-source NLP and ML community
- Joke dataset contributors
- Vercel for free hosting

---

⭐ **If this project made you laugh (or learn), give it a star!**

---

*Made with Python, NLP, and a sense of humor 😄*
