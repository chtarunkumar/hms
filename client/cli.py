# client/cli.py

import requests
import json
# from app.emailer import send_gmail
# from app.config import to_address

BASE_URL = "http://127.0.0.1:5000"

def print_json(data):
    """Helper to pretty print JSON responses."""
    print(json.dumps(data, indent=2))

def menu():
    while True:
        print("\n--- Patient Management System ---")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Get Patient by ID") # Added for completeness
        print("4. Update Patient")
        print("5. Delete Patient")
        print("6. Calculate Batch Average Age")
        # print("7. Scrape Hospital Info")
        # print("8. Scrape Disease Info")
        print("7. Delete All Patients")
        choice = int(input("Enter your choice: "))

        if choice == 1:
            name = input("Name: ")
            age = int(input("Age: "))
            disease = input("Disease: ")
            payload = {"name": name, "age": age, "disease": disease}
            resp = requests.post(f"{BASE_URL}/patients", json=payload)
            print("Patient added successfully.")
            # send_gmail(to_address, "New Patient Added", f"Patient {name} has been added.")
            # print_json(resp.json())

        elif choice == 2:
            resp = requests.get(f"{BASE_URL}/patients")
            print_json(resp.json())

        elif choice == 3: # New: Get Patient by ID
            pid = input("Enter Patient ID to view: ")
            resp = requests.get(f"{BASE_URL}/patients/{pid}")
            print_json(resp.json())

        elif choice == 4:
            pid = input("Enter Patient ID to update: ")
            name = input("New Name (leave blank to skip): ")
            age = input("New Age (leave blank to skip): ")
            disease = input("New Disease (leave blank to skip): ")
            payload = {}
            if name: payload['name'] = name
            if age: payload['age'] = int(age) if age.isdigit() else None
            if disease: payload['disease'] = disease
            
            # Remove None values from payload
            payload = {k: v for k, v in payload.items() if v is not None}

            if not payload:
                print("No update data provided.")
                continue

            resp = requests.put(f"{BASE_URL}/patients/{pid}", json=payload)
            print_json(resp.json())

        elif choice == 5:
            pid = input("Enter Patient ID to delete: ")
            resp = requests.delete(f"{BASE_URL}/patients/{pid}")
            if resp.status_code == 204:
                print("Deleted successfully.")
            else:
                print_json(resp.json())

        elif choice == 6:
            # method = input("Calculation method (thread/async, default thread): ") or 'thread'
            # batch_size = input("Batch size (default 10): ")
            # params = {"method": method}
            # if batch_size.isdigit():
            #     params["batch_size"] = batch_size
            # resp = requests.get(f"{BASE_URL}/patients/average-age", params=params)
            # print_json(resp.json())
            resp = requests.get(f"{BASE_URL}/patients")
            sum = 0
            count = 0
            for e in resp.json():
                count += 1
                sum += e['age']

            print(sum / count if count > 0 else 0)



        elif choice == 7:
            resp = requests.delete(f"{BASE_URL}/patients")
            if resp.status_code == 204:
                print("All patients deleted successfully.")
            else:
                print_json(resp.json())

        elif choice == 8:
            print("Exiting.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    menu()