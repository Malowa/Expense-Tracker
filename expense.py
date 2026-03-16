import csv
import os
import tkinter as tk
from tkinter import filedialog    
from tkinter import messagebox,ttk
from datetime import datetime
import matplotlib.pyplot as plt
from collections import defaultdict



FILE_NAME = 'expenses_tracker.csv'

def init_file():
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Date','Category','Description', 'Amount'])

def add_expense():
    date=date_entry.get()
    category=category_entry.get()
    description=description_entry.get()
    amount=amount_entry.get()

    if not (date and category and description and amount):
        messagebox.showerror("Error", "All fields are required.")
        return
    try:
        datetime.strptime(date, '%Y-%m-%d') # Validate date format
    except ValueError:
        messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
        return
    try:
        float(amount)  # Validate amount is a number
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number.")
        return
    messagebox.showinfo("Expense added", f"Expense on {date} added successfully.")
    
    
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])
        print("Expense added successfully.")

    
    clear_entries()
    load_expenses()

def clear_entries():
    #date_entry.delete(0, tk.END)
    category_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)

def load_expenses():
    for row in expense_table.get_children():
        expense_table.delete(row)

    total = 0.0

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                expense_table.insert("", tk.END, values=(row["Date"], row["Category"], row["Description"], row["Amount"]))
                total += float(row["Amount"])
        print("Expenses loaded successfully.")
    else:
        messagebox.showerror("Error", "No expenses found.")
    total_label.config(text=f"Total Spent: KES {total:.2f}")

def search_expenses(query):
    for row in expense_table.get_children():
        expense_table.delete(row)

    total = 0.0
    found = False

    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if query.lower() in row["Category"].lower() or query.lower() in row["Description"].lower():
                    expense_table.insert("", tk.END, values=(row["Date"], row["Category"], row["Description"], row["Amount"]))
                    total += float(row["Amount"])
                    found = True
                
        if not found:
            messagebox.showinfo("Search Result", "No expenses found matching your search.")
    else:
        messagebox.showerror("Error", "No expenses found.")

    total_label.config(text=f"Total Spent: KES {total:.2f}")

def show_bar_chart():
    if not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", "No expenses found to display.")
        return
    category_totals=defaultdict(float)
    with open(FILE_NAME, mode='r') as file:
        reader=csv.DictReader(file)
        for row in reader:
            category=row['Category']
            amount=float(row['Amount'])
            category_totals[category] += amount
    if not category_totals:
            messagebox.showinfo('Info','No data to display')
            return
    categories=list(category_totals.keys())
    totals=list(category_totals.values())

    plt.figure(figsize=(10,5))
    plt.bar(categories,totals,color='skyblue')
    plt.xlabel("Category")
    plt.ylabel("Total spent (KES)")
    plt.title("Total spending by category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def show_pie_chart():
    if not os.path.exists(FILE_NAME):
        messagebox.showinfo("Info err","No data to display")
        return
    category_totals=defaultdict(float)
    with open(FILE_NAME, mode='r') as file:
        reader=csv.DictReader(file)
        for row in reader:
            category=row["Category"]
            amount=float(row["Amount"])
            category_totals[category] += amount
    if not category_totals:
        messagebox.showinfo('Info','No data to plot')
        return
    categories=list(category_totals.keys())
    totals=list(category_totals.values())

    plt.figure(figsize=(6, 6))
    plt.pie(totals, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Spending Distribution by Category")
    plt.axis('equal')
    plt.show()

def delete_expense():
    selected_item = expense_table.selection()
    if not selected_item:
        messagebox.showerror("Error", "No expense selected.")
        return
    
    confirm=messagebox.askyesno('Delete','Are you sure you want to delete the record')
    if not confirm:
        return

    values= expense_table.item(selected_item,'values')
    date,category,description,amount=values

    expense_table.delete(selected_item)
    messagebox.showinfo("Expense Deleted", "Selected expense has been deleted.")
    
    # Reload expenses to update the total
    updated_rows=[]
    with open(FILE_NAME,mode='r') as file:
        reader=csv.DictReader(file)
        for row in reader:
            if not(row['Date']==date and row['Category']==category and row['Description']==description and row['Amount']==amount):
                updated_rows.append(row)
    
    with open(FILE_NAME,mode='w',newline='') as file:
        fieldnames=['Date','Category','Description','Amount']
        writer=csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(updated_rows)
    
    messagebox.showinfo('Deleted','Expense deleted successfully')

    load_expenses()

def show_monthly_summarry():
    if not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", "No expenses found to display.")
        return

    monthly_totals = defaultdict(float  )
    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = datetime.strptime(row['Date'], '%Y-%m-%d')
            month_year = date.strftime('%Y-%m')
            amount = float(row['Amount'])
            monthly_totals[month_year] += amount
    if not monthly_totals:
        messagebox.showinfo('Info', 'No data to display')
        return
    months = list(monthly_totals.keys())
    totals = list(monthly_totals.values())
    plt.figure(figsize=(10, 5))
    plt.bar(months, totals, color='lightgreen')
    plt.xlabel("Month")
    plt.ylabel("Total Spent (KES)")
    plt.title("Monthly Spending Summary")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def export_monthly_summary():
    if not os.path.exists(FILE_NAME):
        messagebox.showerror("Error", "No expenses found to export.")
        return

    monthly_totals = defaultdict(float)
    with open(FILE_NAME, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            date = datetime.strptime(row['Date'], '%Y-%m-%d')
            month_year = date.strftime('%Y-%m')
            amount = float(row['Amount'])
            monthly_totals[month_year] += amount

    if not monthly_totals:
        messagebox.showinfo('Info', 'No data to export')
        return

    with open('monthly_summary.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Month', 'Total Spent (KES)'])
        for month, total in monthly_totals.items():
            writer.writerow([month, total]) 
    
    messagebox.showinfo('Exported', 'Monthly summary exported successfully as monthly_summary.csv') 

init_file()
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("1100x600")
root.resizable(False, False)

#input frame
input_frame = tk.Frame(root,padx=10, pady=10)
input_frame.pack(fill=tk.X)
# Date input
date_label= tk.Label(input_frame, text="Date (YYYY-MM-DD):")
date_label.grid(row=0, column=0, padx=5, pady=5)
date_entry = tk.Entry(input_frame)
date_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))  # Default to today's date
date_entry.grid(row=0, column=1, padx=5, pady=5)
# Category input
category_label = tk.Label(input_frame, text="Category:")
category_label.grid(row=1, column=0, padx=5, pady=5)
category_entry = tk.Entry(input_frame)
category_entry.grid(row=1, column=1, padx=5, pady=5)
# Description input
description_label = tk.Label(input_frame, text="Description:")
description_label.grid(row=2, column=0, padx=5, pady=5)
description_entry = tk.Entry(input_frame)  # Initialize description_entry
description_entry.grid(row=2, column=1, padx=5, pady=5)
# Amount input
amount_label = tk.Label(input_frame, text="Amount:")
amount_label.grid(row=3, column=0, padx=5, pady=5)
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=3, column=1, padx=5, pady=5)
# Add Expense Button
add_button = tk.Button(input_frame, text="Add Expense", command=add_expense)
add_button.grid(row=4, columnspan=2, pady=10)
#search frame
search_frame = tk.Frame(root, padx=10, pady=10)
search_frame.pack(fill=tk.X)
search_label = tk.Label(search_frame, text="Search by Category:")
search_label.pack(side=tk.LEFT, padx=5, pady=5)
search_entry = tk.Entry(search_frame)
search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)
search_button = tk.Button(search_frame, text="Search", command=lambda: search_expenses(search_entry.get()))
search_button.pack(side=tk.LEFT, padx=5, pady=5)


chart_frame = tk.Frame(root)
chart_frame.pack(pady=10)

bar_btn=tk.Button(chart_frame, text="📊 Bar Chart (Category Totals)", command=show_bar_chart)
bar_btn.pack(side=tk.LEFT, padx=5)


pie_btn=tk.Button(chart_frame, text="🥧 Pie Chart (Spending Share)", command=show_pie_chart)
pie_btn.pack(side=tk.LEFT, padx=5)

# Add monthly summary button
monthly_summary_btn = tk.Button(chart_frame, text="📅 Monthly Summary", command=show_monthly_summarry)
monthly_summary_btn.pack(side=tk.LEFT, padx=5)

export_btn=tk.Button(chart_frame, text="📥 Export Monthly Summary", command=export_monthly_summary)
export_btn.pack(side=tk.LEFT, padx=5)

#delete button
delete_button = tk.Button(chart_frame, text="Delete Selected Expense", command=delete_expense)
delete_button.pack(padx=5)

# Expense Table
expense_table = ttk.Treeview(root, columns=("Date", "Category", "Description", "Amount"), show="headings")
expense_table.heading("Date", text="Date")
expense_table.heading("Category", text="Category")
expense_table.heading("Description", text="Description")
expense_table.heading("Amount", text="Amount")
expense_table.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
# Total Label
total_label = tk.Label(root,text="Total Spent: KES 0.00", font=("Arial", 14))
total_label.pack(pady=5)

#delete_button = tk.Button(root, text="Delete Selected Expense", command=delete_expense)
#delete_button.pack(pady=10)

#load existing expenses
load_expenses()

# Start the GUI event loop
root.mainloop()
# No need to close the file explicitly as it is handled by the context manager
 