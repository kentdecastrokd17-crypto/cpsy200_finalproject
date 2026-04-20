import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
import os

# 1. MODELS
class Customer:
    def __init__(self, customer_id, first_name, last_name):
        self.id = customer_id
        self.first_name = first_name
        self.last_name = last_name

class Equipment:
    def __init__(self, equipment_id, name, daily_rate, status="Available"):
        self.id = equipment_id
        self.name = name
        self.daily_rate = daily_rate
        self.status = status

# 2. FILE PERSISTENCE LOGIC
CLIENT_FILE = "clients.csv"
EQUIP_FILE = "equipment.csv"

def load_data():
    """Reads CSV files and populates the database dictionaries."""
    clients = {}
    if os.path.exists(CLIENT_FILE):
        with open(CLIENT_FILE, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                clients[row['id']] = Customer(row['id'], row['first_name'], row['last_name'])
    
    equipment = {}
    if os.path.exists(EQUIP_FILE):
        with open(EQUIP_FILE, mode='r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Ensure daily_rate is treated as a float for calculations
                equipment[row['id']] = Equipment(row['id'], row['name'], row['daily_rate'], row['status'])
    
    return clients, equipment

def save_data():
    """Writes the current state of dictionaries back to CSV files."""
    # Save Clients
    with open(CLIENT_FILE, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'first_name', 'last_name'])
        writer.writeheader()
        for c in clients_db.values():
            writer.writerow({'id': c.id, 'first_name': c.first_name, 'last_name': c.last_name})
            
    # Save Equipment
    with open(EQUIP_FILE, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'name', 'daily_rate', 'status'])
        writer.writeheader()
        for e in equipment_db.values():
            writer.writerow({'id': e.id, 'name': e.name, 'daily_rate': e.daily_rate, 'status': e.status})

# Initialize DBs from files on startup
clients_db, equipment_db = load_data()


# 3. UPDATED BUSINESS LOGIC
def add_equipment():
    e_id = simpledialog.askstring("New Equipment", "Enter Equipment ID:")
    name = simpledialog.askstring("New Equipment", "Enter Equipment Name:")
    rate = simpledialog.askstring("New Equipment", "Enter Daily Rate ($):")
    
    if e_id and name and rate:
        equipment_db[e_id] = Equipment(e_id, name, rate)
        save_data()  # PERSIST TO FILE
        messagebox.showinfo("Success", f"Equipment '{name}' added successfully!")

def delete_equipment():
    e_id = simpledialog.askstring("Delete Equipment", "Enter Equipment ID to delete:")
    if e_id in equipment_db:
        deleted_item = equipment_db.pop(e_id)
        save_data()  # PERSIST TO FILE
        messagebox.showinfo("Success", f"Equipment '{deleted_item.name}' removed.")
    else:
        messagebox.showwarning("Not Found", "Equipment ID does not exist.")

def add_client():
    c_id = simpledialog.askstring("New Client", "Enter Client ID:")
    f_name = simpledialog.askstring("New Client", "Enter First Name:")
    l_name = simpledialog.askstring("New Client", "Enter Last Name:")
    
    if c_id and f_name:
        clients_db[c_id] = Customer(c_id, f_name, l_name)
        save_data()  # PERSIST TO FILE
        messagebox.showinfo("Success", f"Client '{f_name}' added successfully!")

def display_equipment():
    lines = [f"ID: {e.id} | {e.name} | Rate: ${e.daily_rate} | Status: {e.status}" 
             for e in equipment_db.values()]
    output = "\n".join(lines) if lines else "No equipment in inventory."
    messagebox.showinfo("Equipment Inventory", output)

def display_clients():
    lines = [f"ID: {c.id} | {c.first_name} {c.last_name}" 
             for c in clients_db.values()]
    output = "\n".join(lines) if lines else "No clients registered."
    messagebox.showinfo("Client List", output)

def process_rental():
    c_id = simpledialog.askstring("Process Rental", "Enter Client ID:")
    e_id = simpledialog.askstring("Process Rental", "Enter Equipment ID:")
    
    if c_id not in clients_db:
        messagebox.showerror("Error", "Invalid Client ID.")
        return
        
    if e_id not in equipment_db:
        messagebox.showerror("Error", "Invalid Equipment ID.")
        return

    item = equipment_db[e_id]
    client = clients_db[c_id]

    if item.status == "Available":
        item.status = "Rented"
        save_data()  # PERSIST UPDATED STATUS
        messagebox.showinfo("Success", f"Rented {item.name} to {client.first_name}.")
    else:
        messagebox.showwarning("Unavailable", f"Sorry, {item.name} is currently {item.status}.")


# 4. MAIN APPLICATION WINDOW
root = tk.Tk()
root.title("Village Rentals - Data Integrated")
root.geometry("350x300")
root.configure(padx=20, pady=20)

tk.Label(root, text="Village Rentals Management", font=("Arial", 14, "bold")).pack(pady=(0, 15))

# Buttons
tk.Button(root, text="1. Add Equipment", command=add_equipment, width=25).pack(pady=3)
tk.Button(root, text="   Delete Equipment", command=delete_equipment, width=25).pack(pady=3)
tk.Button(root, text="2. Add New Client", command=add_client, width=25).pack(pady=3)
tk.Button(root, text="3. Display All Equipment", command=display_equipment, width=25).pack(pady=3)
tk.Button(root, text="4. Display All Clients", command=display_clients, width=25).pack(pady=3)
tk.Button(root, text="5. Process Rental", command=process_rental, width=25, bg="lightblue").pack(pady=10)

root.mainloop()