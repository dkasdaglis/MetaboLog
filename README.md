# Metabolog: Health Data Management & Analytics System ⚕️📊

## Overview
Metabolog is a Python-based backend system designed for medical clinics to manage patient data and automatically extract health analytics. Built with an object-oriented approach, it seamlessly integrates with an SQLite database to store patient records and perform targeted data analysis for clinical decision-making.

## Key Features
* **Relational Database Management:** Utilizes `SQLite3` to safely store and retrieve patient metrics (Age, Weight, Fasting Glucose, Sleep Hours).
* **Automated Health Analytics:** Runs SQL queries to instantly identify high-risk patients (e.g., Fasting Glucose > 100 mg/dL) and sleep deficiency (< 6 hours).
* **Automated Reporting:** Generates a daily text-based clinical report (`.txt`) summarizing average clinic metrics and high-risk alerts.
* **Data Export:** Features a built-in module to export the entire database into a clean, structured `.csv` file for further analysis in Excel or BI tools.

## Technology Stack
* **Language:** Python 3
* **Database:** SQLite
* **Libraries:** `sqlite3`, `csv`, `os`
* **Architecture:** Object-Oriented Programming (OOP)

## Why I Built This
As an aspiring **Health Data Engineer**, I built Metabolog to bridge the gap between raw medical data and actionable clinical insights. This project demonstrates my ability to design database schemas, write efficient SQL queries, and build Python backends that process health information securely and efficiently.

## Future Updates (Version 2.0 Roadmap)
- [ ] Database schema expansion (adding Gender, Height, BMI calculation, and Target Weight tracking).
- [ ] Integration with a graphical user interface (GUI).
- [ ] Advanced temporal data analysis for weight tracking over time.
