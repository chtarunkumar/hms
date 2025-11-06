import requests

BASE_URL = "http://127.0.0.1:5000"

def menu():
    while True:
        print("\nPatient Management System")
        print("1. Add Patient")
        print("2. View All Patients")
        print("3. Update Patient")
        print("4. Delete Patient")
        print("5. Calculate Batch Average Age")
        print("6. Scrape Hospital Info")
        print("7. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            name = input("Name: ")
            age = int(input("Age: "))
            disease = input("Disease: ")
            payload = {"name": name, "age": age, "disease": disease}
            resp = requests.post(f"{BASE_URL}/patients", json=payload)
            print(resp.json())
        
        elif choice == "2":
            resp = requests.get(f"{BASE_URL}/patients")
            for p in resp.json():
                print(p)
        
        elif choice == "3":
            pid = input("Enter Patient ID to update: ")
            name = input("New Name (leave blank to skip): ")
            age = input("New Age (leave blank to skip): ")
            disease = input("New Disease (leave blank to skip): ")
            payload = {}
            if name: payload['name'] = name
            if age: payload['age'] = int(age)
            if disease: payload['disease'] = disease
            resp = requests.put(f"{BASE_URL}/patients/{pid}", json=payload)
            try:
                data = resp.json()
                if resp.status_code == 404:
                    print("Error: Patient not found.")
                else:
                    print(data)
            except Exception:
                print(f"Error: {resp.status_code} - {resp.text}")
        
        elif choice == "4":
            pid = input("Enter Patient ID to delete: ")
            resp = requests.delete(f"{BASE_URL}/patients/{pid}")
            if resp.status_code == 204:
                print("Deleted")
            else:
                try:
                    data = resp.json()
                    if resp.status_code == 404:
                        print("Error: Patient not found.")
                    else:
                        print(data)
                except Exception:
                    print(f"Error: {resp.status_code} - {resp.text}")
        
        elif choice == "5":
            batch_size = input("Batch size (default 10): ")
            params = {"batch_size": batch_size} if batch_size else {}
            resp = requests.get(f"{BASE_URL}/patients/batch-average-age", params=params)
            print(resp.json())
        
        elif choice == "6":
            resp = requests.get(f"{BASE_URL}/scrape-hospital-info")
            print(resp.json())
        
        elif choice == "7":
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    menu()