import tkinter as tk
import csv
from tkinter import messagebox, ttk

users = []

#calculation logic
def calculate_bmi(weight, height, unit):
    if unit == 'm':
        height_m = height / 100
        return round(weight / (height_m ** 2), 2)
    elif unit == 'i':
        return round(703 * weight / (height ** 2), 2)
    return None

def bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    return "Obese"

#user adding
def add_user():
    name = name_entry.get()
    age = age_entry.get()
    unit = unit_var.get().lower()
    weight = weight_entry.get()
    height = height_entry.get()

    try:
        age = int(age)
        weight = float(weight)
        height = float(height)

        bmi = calculate_bmi(weight, height, unit)
        category = bmi_category(bmi)

        users.append({
            'name': name,
            'age': age,
            'unit': unit,
            'weight': weight,
            'height': height,
            'bmi': bmi,
            'category': category
        })

        user_list.insert(tk.END, f"{name} - BMI: {bmi} ({category})")
        clear_fields()
        messagebox.showinfo("User Added", f"{name}'s BMI is {bmi} ({category})")

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

#clear field method
def clear_fields():
    name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    weight_entry.delete(0, tk.END)
    height_entry.delete(0, tk.END)

# generate reports
def generate_reports():
    if users:
        # User data CSV
        with open('bmi_users.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["name", "age", "unit", "weight", "height", "bmi", "category"])
            writer.writeheader()
            writer.writerows(users)

        # Analytics
        total_users = len(users)
        avg_bmi = round(sum(user["bmi"] for user in users) / total_users, 2)
        highest = max(users, key=lambda x: x["bmi"])
        lowest = min(users, key=lambda x: x["bmi"])

        category_count = {"Underweight": 0, "Normal weight": 0, "Overweight": 0, "Obese": 0}
        for user in users:
            category_count[user["category"]] += 1

        # Analytics CSV
        with open('bmi_analytics.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Total Users", total_users])
            writer.writerow(["Average BMI", avg_bmi])
            writer.writerow(["Highest BMI", f"{highest['name']} ({highest['bmi']})"])
            writer.writerow(["Lowest BMI", f"{lowest['name']} ({lowest['bmi']})"])
            writer.writerow([])
            writer.writerow(["Category", "Count"])
            for cat, count in category_count.items():
                writer.writerow([cat, count])

        messagebox.showinfo("Reports Generated", "Data saved: 'bmi_users.csv'\n- 'bmi_analytics.csv'")
    else:
        messagebox.showerror("No Users", "Please add users before generating reports!")

# gui
window = tk.Tk()
window.title("BMI Calculator ")
window.geometry("550x550")
window.configure(bg="#f0f4f7")

title = tk.Label(window, text="BMI Calculator", bg="#f0f4f7", fg="#333")
title.pack(pady=10)

form_frame = tk.Frame(window, bg="#f0f4f7")
form_frame.pack(pady=10)

def form_label(text):
    return tk.Label(form_frame, text=text,  bg="#f0f4f7", anchor='w')

name_label = form_label("Name:")
name_label.grid(row=0, column=0, sticky='w', padx=10, pady=5)
name_entry = tk.Entry(form_frame, width=30)
name_entry.grid(row=0, column=1, padx=10)

age_label = form_label("Age:")
age_label.grid(row=1, column=0, sticky='w', padx=10, pady=5)
age_entry = tk.Entry(form_frame, width=30)
age_entry.grid(row=1, column=1, padx=10)

unit_label = form_label("System (metric/imperial):")
unit_label.grid(row=2, padx=10, pady=5)
unit_var = tk.StringVar(value='m')
unit_menu = ttk.Combobox(form_frame, textvariable=unit_var, values=["m", "i"], state="readonly", width=27)
unit_menu.grid(row=2, column=1, padx=10)

height_label = form_label("Height (cm/inch):")
height_label.grid(row=3, column=0, sticky='w', padx=10, pady=5)
height_entry = tk.Entry(form_frame, width=30)
height_entry.grid(row=3, column=1, padx=10)

weight_label = form_label("Weight (kg/lbs):")
weight_label.grid(row=4, column=0, sticky='w', padx=10, pady=5)
weight_entry = tk.Entry(form_frame, width=30)
weight_entry.grid(row=4, column=1, padx=10)


button_frame = tk.Frame(window, bg="#f0f4f7")
button_frame.pack(pady=15)

tk.Button(button_frame, text="Add User", command=add_user, bg="#1976d2", fg="white", width=15).grid(row=0, column=0, padx=10)
tk.Button(button_frame, text="Generate Reports", command=generate_reports, bg="#388e3c", fg="white", width=15).grid(row=0, column=1, padx=10)


tk.Label(window, text="Users Added:", font= 12, bg="#f0f4f7").pack()
user_list = tk.Listbox(window, width=60, height=10, font=10)
user_list.pack(pady=5)

window.mainloop()
