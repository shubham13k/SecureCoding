import bcrypt
import json
import os
import base64
import hashlib
from cryptography.fernet import Fernet
 
USER_FILE = "admins.json"
PATIENT_FILE = "patients.json"
LOCKOUT_THRESHOLD = 3
SECRET_KEY = base64.urlsafe_b64encode(hashlib.sha256(b"my_secret_key").digest())  # Generate a key for Fernet
encryption_suite = Fernet(SECRET_KEY)
 
def encrypt_data(data):
    return encryption_suite.encrypt(data.encode()).decode()
 
def decrypt_data(data):
    return encryption_suite.decrypt(data.encode()).decode()
 
def load_data(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)
 
def save_data(filename, data):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
 
def hash_passcode(passcode):
    return bcrypt.hashpw(passcode.encode(), bcrypt.gensalt()).decode()
 
def verify_passcode(stored_hash, passcode):
    return bcrypt.checkpw(passcode.encode(), stored_hash.encode())
 
def register_admin():
    admins = load_data(USER_FILE)
    username = input("Enter new admin username: ")
    if username in admins:
        print("Username already exists. Try a different one.")
        return
    passcode = input("Enter passcode: ")
    hashed_passcode = hash_passcode(passcode)
    admins[username] = {"passcode": hashed_passcode, "failed_attempts": 0}
    save_data(USER_FILE, admins)
    print("Admin registered successfully!")
 
def login_admin():
    admins = load_data(USER_FILE)
    username = input("Enter username: ")
    if username not in admins:
        print("Invalid username.")
        return None
   
    if admins[username]["failed_attempts"] >= LOCKOUT_THRESHOLD:
        print("Account locked due to multiple failed attempts. Contact support.")
        return None
   
    passcode = input("Enter passcode: ")
    if verify_passcode(admins[username]["passcode"], passcode):
        admins[username]["failed_attempts"] = 0  # Reset failed attempts on success
        save_data(USER_FILE, admins)
        print("Login successful!")
        return username
    else:
        admins[username]["failed_attempts"] += 1
        save_data(USER_FILE, admins)
        print(f"Incorrect passcode. Attempts left: {LOCKOUT_THRESHOLD - admins[username]['failed_attempts']}")
        return None
 
def manage_patients(admin):
    patients = load_data(PATIENT_FILE)
    while True:
        print("\nPatient Management System")
        print("1. Add Patient")
        print("2. View Patients")
        print("3. Logout")
        choice = input("Choose an option: ")
       
        if choice == "1":
            patient_name = input("Enter patient name: ")
            patient_age = input("Enter patient age: ")
            patient_email = input("Enter patient email: ")
            patient_ssn = input("Enter patient SSN: ")
            patient_history = input("Enter history of illness: ")
            patient_id = str(len(patients) + 1)
           
            encrypted_data = {
                "name": encrypt_data(patient_name),
                "age": encrypt_data(patient_age),
                "email": encrypt_data(patient_email),
                "ssn": encrypt_data(patient_ssn),
                "history": encrypt_data(patient_history)
            }
           
            patients[patient_id] = encrypted_data
            save_data(PATIENT_FILE, patients)
            print("Patient added successfully!")
        elif choice == "2":
            if patients:
                print("\nPatient List:")
                for pid, data in patients.items():
                    print(f"ID: {pid}, Name: {decrypt_data(data['name'])}, Age: {decrypt_data(data['age'])}, Email: {decrypt_data(data['email'])}, SSN: {decrypt_data(data['ssn'])}, History: {decrypt_data(data['history'])}")
            else:
                print("No patients found.")
        elif choice == "3":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")
 
def main():
    while True:
        print("\nHospital Admin System")
        print("1. Register Admin")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option: ")
       
        if choice == "1":
            register_admin()
        elif choice == "2":
            admin = login_admin()
            if admin:
                manage_patients(admin)
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")
 
if __name__ == "__main__":
    main()
 