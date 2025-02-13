import rsa
import json
import os
 
PATIENT_FILE = "patients.json"
 
# Load the private key
if not os.path.exists("private_key.pem"):
    print("Private key not found! Please ensure it exists.")
    exit()
 
with open("private_key.pem", "rb") as priv_file:
    private_key = rsa.PrivateKey.load_pkcs1(priv_file.read())
 
def decrypt_data(data):
    """Decrypts encrypted data using the private key"""
    return rsa.decrypt(bytes.fromhex(data), private_key).decode()
 
def view_decrypted_patients():
    """Reads encrypted patient data and decrypts it"""
    if not os.path.exists(PATIENT_FILE):
        print("No patient data found.")
        return
 
    with open(PATIENT_FILE, "r") as file:
        patients = json.load(file)
 
    if not patients:
        print("No patients found.")
        return
 
    print("\nDecrypted Patient Records:")
    for pid, data in patients.items():
        try:
            print(f"ID: {pid}, Name: {decrypt_data(data['name'])}, Age: {decrypt_data(data['age'])}, Email: {decrypt_data(data['email'])}, SSN: {decrypt_data(data['ssn'])}, History: {decrypt_data(data['history'])}")
        except Exception as e:
            print(f"Error decrypting patient {pid}: {e}")
 
# Run the doctor's console
if __name__ == "__main__":
    print("\nDoctor's Secure Patient Viewer")
    view_decrypted_patients()