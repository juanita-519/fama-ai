# FAMA AI – Permanent Cloud Deployment Guide

Follow these step-by-step instructions to deploy your FAMA AI platform permanently to the cloud for free. Once deployed, anyone anywhere in the world will be able to access the dashboard 24/7, even when your local computer is powered off.

---

## 🛠️ Prerequisites
1. A **GitHub** account ([Sign up here](https://github.com/)).
2. A **Render** account ([Sign up here](https://render.com/) - completely free tier).
3. **Git** installed on your local computer.

---

## 📂 Step 1: Initialize Git and Push to GitHub

To deploy to Render, you need to have your code hosted in a GitHub repository.

1. Open **Command Prompt** or **PowerShell** on your computer.
2. Navigate to your project directory:
   ```cmd
   cd C:\Users\Saira\Desktop\AntiGravity-AI
   ```
3. Initialize a local Git repository:
   ```cmd
   git init
   ```
4. Create a `.gitignore` file to avoid uploading local temporary files:
   ```cmd
   echo .system_generated/ > .gitignore
   echo __pycache__/ >> .gitignore
   echo .gemini/ >> .gitignore
   echo *.log >> .gitignore
   ```
5. Add all project files:
   ```cmd
   git add .
   ```
6. Commit the files:
   ```cmd
   git commit -m "Initialize FAMA AI with OLS, Random Forest, and XGBoost Comparison"
   ```
7. Go to [GitHub](https://github.com/) and create a new **public or private repository** named `fama-ai`. Leave "Initialize this repository with" unchecked.
8. Link your local codebase to the GitHub repository and push:
   ```cmd
   git remote add origin https://github.com/YOUR_GITHUB_USERNAME/fama-ai.git
   git branch -M main
   git push -u origin main
   ```
   *(Replace `YOUR_GITHUB_USERNAME` with your actual GitHub username).*

---

## 🚀 Step 2: Deploy to Render for Free

Render is a modern cloud hosting provider with a generous free tier that is perfect for hosting Python FastAPI servers.

1. Log in to [Render Dashboard](https://dashboard.render.com/).
2. Click the **New +** button in the top right and select **Web Service**.
3. Choose **Connect Repository** and link your GitHub account. Select your `fama-ai` repository.
4. Configure the Web Service settings as follows:
   * **Name:** `fama-ai` (or any name you prefer)
   * **Region:** Choose the region closest to you (e.g., `Singapore` or `Frankfurt`)
   * **Branch:** `main`
   * **Runtime:** `Python`
   * **Build Command:** `pip install -r requirements.txt`
   * **Start Command:** `python -m uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Scroll down to the **Instance Type** section and select the **Free** tier.
6. Click **Deploy Web Service** at the bottom of the page.

---

## 🌐 Step 3: Accessing Your Website
Render will take 1-3 minutes to download your files, install Python dependencies (including `pandas`, `statsmodels`, `scikit-learn`, and `xgboost`), and start your server.

Once the build is complete, you will see a green **"Live"** badge in the Render console, and a permanent public URL will be displayed at the top left (e.g., `https://fama-ai.onrender.com`).

* Anyone globally can now access this URL from their phone, tablet, or PC!
* The database, backend engine, and frontend assets are all packaged together, ensuring a secure and seamless HTTPS connection without needing local SSH tunnels.
