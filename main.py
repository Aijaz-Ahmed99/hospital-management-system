from collections import Counter
import csv
import os
import datetime

def input_non_empty(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Try again")

def input_valid_age():
    while True:
        age = input("Enter patient age: ").strip()
        if age.isdigit() and int(age) > 0:
            return int(age)
        print("Invalid age. Enter a positive number")

def id_exists(patient_id, patients):
    return any(p.patient_id == patient_id for p in patients)

def save_to_csv(patients, filename="store.csv"):
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(["patient_id", "name", "age", "gender", "disease", "admit_date"])

        for patient in patients:
            writer.writerow([
                patient.patient_id,
                patient.name,
                patient.age,
                patient.gender,
                patient.disease,
                patient.admit_date

            ])
        
def load_from_csv(filename="store.csv"):
    patients = []
    if not os.path.exists(filename):
        return patients
    
    with open(filename, "r", newline="") as file:
        reader = csv.reader(file)

        next(reader,None)

        for row in reader:
            if len(row) == 6:
                patient_id, name, age, gender, disease, admit_date = row
                patient = Patient(patient_id, name, age, gender, disease, admit_date)
                patients.append(patient)
    return patients

def append_patient_to_csv(patient, filename="store.csv"):
    file_exists = os.path.exists(filename)
    write_header = not file_exists or os.stat(filename).st_size == 0

    with open(filename, "a", newline="") as file:
        writer = csv.writer(file)

        if write_header:
            writer.writerow(["patient_id", "name", "age", "gender", "disease", "admit_date"])

        writer.writerow([
            patient.patient_id,
            patient.name,
            patient.age,
            patient.gender,
            patient.disease,
            patient.admit_date
        ])

def statistics(patients):
    print("\n📊 Hospital Statistics")
    print("-" * 30)

    total = len(patients)
    print(f"Total Patients          : {total}")

    male_count = 0
    female_count = 0
    for p in patients:
        if p.gender == "male".lower():
            male_count += 1

        elif p.gender == "female".lower():
            female_count += 1
            
    print(f"Male Patients           : {male_count}")
    print(f"Female Patients         : {female_count}")

    diseases = []
    for p in patients:
        diseases.append(p.disease.lower())
    
    disease_counter = Counter(diseases)
    if disease_counter:
        most_common = disease_counter.most_common(1)[0]
        print(f"Most Common Disease: {most_common[0].title()} ({most_common[1]} cases)")
    else:
        print("Most Common Disease    : N/A")     

class Patient:
    def __init__(self, patient_id, name, age, gender, disease, admit_date):
        """Initialize a new patient with ID, name, age, gender, and disease."""
        self.patient_id = patient_id
        self.name = name
        self.age = age
        self.gender = gender
        self.disease = disease
        self.admit_date = admit_date

    def display_info(self):
        """Display patient information."""
        print(f"{'ID':15}: {self.patient_id}")
        print(f"{'Name':15}: {self.name}")
        print(f"{'Age':15}: {self.age}")
        print(f"{'Gender':15}: {self.gender}")
        print(f"{'Disease':15}: {self.disease}")
        print(f"{'Admission Date':15}: {self.admit_date}")

class Hospital:
    def __init__(self):
        """Initialize a new hospital with an empty list of patients"""
        self.patients = [] 
    

    def add_patient(self, patient):
        """Add a new patient to the hospital"""
        self.patients = load_from_csv()
        self.patients.append(patient)
        print(f"Patient {patient.name} has been added successfully")
        append_patient_to_csv(patient)
    
    def update_patient(self, patient_id, update_info):
        """Update patient by ID"""
        self.patients = load_from_csv()
        found = False
        for i, patient in enumerate(self.patients):
            if patient.patient_id == patient_id:
                self.patients[i] = update_info
                found = True
                print(f"Patient with ID: {patient_id} has been updated")
                break
                
        if not found:
            print("Patient not found")
            return
        
        save_to_csv(self.patients)
    
    def delete_patient(self, patient_id,):
        """Delete patient by ID"""
        self.patients = load_from_csv()
        found = False
        for patient in self.patients:
            if patient.patient_id == patient_id:
                self.patients.remove(patient)
                found = True
                print(f"Patient with ID '{patient_id}' has been deleted")
                break

        if not found:
            print("Patient not found with that ID")
            return

        save_to_csv(self.patients)    


    def display_all_patients(self):
        """Display information for all patients in the hospital."""
        self.patients = load_from_csv()
        if not self.patients:
            print("No patients found")
        else:
            for patient in self.patients:
                patient.display_info()
                print("-" * 27)

    def find_patient_by_id(self, patient_id):
        """Find a patient by their ID and display their information."""
        self.patients = load_from_csv()
        for patient in self.patients:
            if patient.patient_id == patient_id:
                patient.display_info()
                return
        print("Patient not found")
    
    def searh_by_name(self, name):
        """Search patient by name"""
        self.patients = load_from_csv()
        for patient in self.patients:
            if patient.name == name:
                patient.display_info()
                return
        print("Patient not found with that name")

    def search_by_disease(self, disease):
        self.patients = load_from_csv()
        for patient in self.patients:
            if patient.disease == disease:
                patient.display_info()
                return
        print("Patient not found with that disease")

    def show_statistics(self):
        self.patients = load_from_csv()
        statistics(self.patients)

def main():
    hospital = Hospital()

    while True:
        print("\n--- Hospital Management System ---")
        print("1. Add Patient")
        print("2. Display All Patients")
        print("3. Update patient")
        print("4. Delete patient")
        print("5. Find Patient by ID")
        print("6. Search Patient by Name")
        print("7. Search Patient by Disease")
        print("8. Show Statistics")
        print("9. Exit")

        while True:
            try:
                choice = int(input_non_empty("Enter your choice between (1-9): "))
            except ValueError:
                print("Invalid input. Please enter a number")
                continue
            break

        if choice == 1:
            while True:
                patient_id = input_non_empty("Enter patient ID: ")

                if id_exists(patient_id, load_from_csv()):
                    print("Patient ID already exists. Enter a unique ID")
                else:
                    break
            
            name = input_non_empty("Enter patient name: ")
            age = input_valid_age()
            gender = input_non_empty("Enter patient gender: ")
            disease = input_non_empty("Enter patient disease: ")

            admit_date = datetime.date.today().isoformat()
            new_patient= Patient(patient_id, name, age, gender, disease, admit_date)
            hospital.add_patient(new_patient)

        elif choice == 2:
            hospital.display_all_patients()

        elif choice == 3:
            patient_id = input_non_empty("Enter the patient ID you want to update: ")
            new_name = input_non_empty("Enter new name: ")
            new_age = input_valid_age()
            new_gender = input_non_empty("Enter new gender: ")
            new_disease = input_non_empty("Enter new disease: ")

            update_info = Patient(patient_id, new_name, new_age, new_gender, new_disease, admit_date)
            hospital.update_patient(patient_id, update_info)

        elif choice == 4:
            patient_id = input_non_empty("Enter the patient Id you want to delete: ")
            hospital.delete_patient(patient_id)
            
        elif choice == 5:
            patient_id = input_non_empty("Enter patient ID to find: ")
            hospital.find_patient_by_id(patient_id)

        elif choice == 6:
            name = input_non_empty("Enter the patient name you want to search: ")
            hospital.searh_by_name(name)

        elif choice == 7:
            disease = input_non_empty("Enter the disease you want to search: ")
            hospital.search_by_disease(disease)

        elif choice == 8:
            hospital.show_statistics()

        elif choice == 9:
            print("---Closing the system. Thank you!")
            break

        else:
            print("Invalid choice. Please try again")

if __name__ == "__main__":
    main()



