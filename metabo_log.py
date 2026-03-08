import csv
import os
import sqlite3

class Patient:
    def __init__(self, name, age, gender, height, weight, target_weight, sleep_hours, fasting_glucose):
        self.name = name
        self.age = age
        self.gender = gender
        self.height = height   
        self.weight = weight
        self.target_weight = target_weight
        self.weight_history = [weight]
        self.sleep_hours = sleep_hours
        self.fasting_glucose = fasting_glucose
    def update_weight(self, new_weight):
        self.weight = new_weight
        self.weight_history.append(new_weight)
    def check_plateau(self):
        if len(self.weight_history) >= 2:
            today_weight = self.weight_history[-1]
            previous_weight = self.weight_history[-2]
            difference = round(previous_weight - today_weight, 1)

            if difference <= 0.2:
                return "Weight loss plateau detected!"
            else:
                return "Bravo, weight loss is on track!"
    def distance_to_target(self):
        distance = self.weight - self.target_weight
        return round(distance, 1)
    def calculate_bmi(self):
        bmi = self.weight / (self.height ** 2)
        return round(bmi, 1)  

class Clinic:
    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.patients_db = []
    def add_patient(self, patient):
        self.patients_db.append(patient)
        import sqlite3
        import os
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "metabolog.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            weight REAL,
            glucose INTEGER,
            sleep_hours REAL
        )
        """)
        cursor.execute("""
        INSERT INTO Patients (name, age, weight, glucose, sleep_hours) 
        VALUES (?, ?, ?, ?, ?)
        """, (patient.name, patient.age, patient.weight, patient.fasting_glucose, patient.sleep_hours)) 
        conn.commit()
        conn.close()
        print(f"Success! Patient {patient.name} saved to the database.")
    def get_high_glucose_patients(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "metabolog.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, glucose FROM Patients WHERE glucose > 100")
        high_risk_patients = cursor.fetchall()
        
        print("\n--- HIGH GLUCOSE ALERT (>100 mg/dL) ---")
        if not high_risk_patients:
            print("No high risk patients found.")
        else:
            for patient in high_risk_patients:
                print(f"Patient: {patient[0]} | Glucose: {patient[1]} mg/dL")
        conn.close()
        return high_risk_patients
    def get_patients_with_sleep_issues(self):
        import sqlite3
        import os
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "metabolog.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, sleep_hours FROM Patients WHERE sleep_hours < 6")
        sleep_issue_patients = cursor.fetchall()       
        print("\n--- LOW SLEEP HOURS ALERT (< 6 hours) ---")
        if not sleep_issue_patients:
            print("No patients with sleep issues found.")
        else:
            for patient in sleep_issue_patients:
                print(f"Patient: {patient[0]} | Sleep: {patient[1]} hrs")
        conn.close()
        return sleep_issue_patients
    def get_average_sleep(self):
        import sqlite3
        import os
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "metabolog.db")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT AVG(sleep_hours) FROM Patients")
        result = cursor.fetchone() 
        average_sleep = result[0] if result[0] is not None else 0
        conn.close()
        return round(average_sleep, 1)
    def generate_daily_report(self):
        with open("metabolog_report.txt", "w", encoding="utf-8") as file:
            file.write(f"--- CLINIC DAILY REPORT: {self.name} ---\n\n")
            file.write(f"Average Clinic Sleep: {self.get_average_sleep()} hours\n\n")
            file.write("HIGH GLUCOSE ALERT (>100 mg/dL):\n")
            high_glucose_list = self.get_high_glucose_patients()
            if high_glucose_list:
                for patient in high_glucose_list:
                    file.write(f"- Patient: {patient[0]} | Glucose: {patient[1]} mg/dL\n")
        print("\n--- SUCCESS: Daily report generated in metabolog_report.txt ---")
        return "Daily report generated successfully!"
    def export_patients_to_csv(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "metabolog.db")
        csv_path = os.path.join(BASE_DIR, "patients_export.csv")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name, age, weight, glucose, sleep_hours FROM Patients")
        rows = cursor.fetchall()
        with open(csv_path, "w", newline='', encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Age", "Weight", "Glucose", "Sleep Hours"])
            writer.writerows(rows)
        conn.close()
        print(f"\n--- SUCCESS: Database exported to patients_export.csv ---")
        return "CSV export completed successfully!"

    def import_patients_from_csv(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(BASE_DIR, "patients_export.csv")
        try:
            with open(csv_path, "r", encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)
                for row in reader:
                    try:
                        name = row[0]
                        age = int(row[1])
                        weight = float(row[2])
                        glucose = float(row[3])
                        sleep_hours = float(row[4])
                        new_patient = Patient(name, age, "Unknown", 1.70, weight, weight, sleep_hours, glucose)
                        self.add_patient(new_patient)
                    except (ValueError, IndexError):
                        print(f"WARNING: Error in row {row}! Skipped.")
                        continue
            print("\n--- SUCCESS: Data imported from CSV to Database ---")
            return "CSV import completed successfully!"
        except FileNotFoundError:
            print("\n--- ERROR: No CSV file found to import. ---")
            return "File not found."

if __name__ == "__main__":
    # 1. Δημιουργία Κλινικής
    my_clinic = Clinic("HealthData Center", "210-123", "info@hc.com")
    
    # 2. Δημιουργία 3 Ασθενών
    patient_1 = Patient("George", 45, "Male", 1.75, 85.0, 75.0, 5.0, 110)
    patient_2 = Patient("Maria", 38, "Female", 1.65, 65.0, 60.0, 7.5, 95)
    patient_3 = Patient("Nikos", 55, "Male", 1.80, 95.0, 85.0, 4.5, 125)
    
    # 3. Εισαγωγή στη Βάση Δεδομένων
    print("--- 1. SAVING PATIENTS TO DATABASE ---")
    my_clinic.add_patient(patient_1)
    my_clinic.add_patient(patient_2)
    my_clinic.add_patient(patient_3)
    
    # 4. Εκτέλεση Analytics (SQL)
    print("\n--- 2. RUNNING DATABASE ANALYTICS ---")
    my_clinic.get_high_glucose_patients()
    my_clinic.get_patients_with_sleep_issues()
    avg_sleep = my_clinic.get_average_sleep()
    print(f"\n--- AVERAGE CLINIC SLEEP: {avg_sleep} hours ---")
    
    # 5. Εξαγωγή Αναφορών (CSV & TXT)
    print("\n--- 3. EXPORTING DATA & REPORTS ---")
    my_clinic.export_patients_to_csv()
    my_clinic.generate_daily_report()