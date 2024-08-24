import tkinter as tk
from tkinter import messagebox
import sqlite3

# Function to create the assets table
def create_assets_table():
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS assets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 name TEXT,
                 description TEXT)''')
    conn.commit()
    conn.close()

# Function to add a new asset to the database
def add_asset():
    name = entry_name.get()
    description = entry_description.get('1.0', tk.END).strip()

    if name and description:
        conn = sqlite3.connect('assets.db')
        c = conn.cursor()
        c.execute("INSERT INTO assets (name, description) VALUES (?, ?)", (name, description))
        conn.commit()
        conn.close()
        label_status.config(text="Asset added successfully!", fg="green")
        # Clear entry fields after adding asset
        entry_name.delete(0, tk.END)
        entry_description.delete('1.0', tk.END)
    else:
        label_status.config(text="Please enter both name and description", fg="red")

# Function to view all assets in the database
def view_assets():
    conn = sqlite3.connect('assets.db')
    c = conn.cursor()
    c.execute("SELECT * FROM assets")
    assets = c.fetchall()
    conn.close()
    if assets:
        for asset in assets:
            messagebox.showinfo("Asset Info", f"ID: {asset[0]}\nName: {asset[1]}\nDescription: {asset[2]}")
    else:
        messagebox.showinfo("Asset Info", "No assets found")

# Function to delete an asset from the database
def delete_asset():
    asset_id = entry_delete_id.get()
    if asset_id:
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this asset?")
        if confirmation:
            conn = sqlite3.connect('assets.db')
            c = conn.cursor()
            c.execute("DELETE FROM assets WHERE id=?", (asset_id,))
            conn.commit()
            conn.close()
            label_status.config(text="Asset deleted successfully!", fg="green")
            # Clear entry field after deleting asset
            entry_delete_id.delete(0, tk.END)
    else:
        label_status.config(text="Please enter an asset ID", fg="red")

# Function to exit the application
def exit_app():
    root.destroy()

# Function to check login credentials and open appropriate window
def login():
    username = entry_username.get()
    password = entry_password.get()
    # Check if username and password match "admin"
    if username == "admin" and password == "admin":
        root.withdraw()  # Hide the login window
        open_asset_manager()
    # Check if username and password match "customer"
    elif username == "customer" and password == "password":
        root.withdraw()  # Hide the login window
        open_customer_review()
    else:
        label_status.config(text="Incorrect username or password!", fg="red")

# Function to open asset manager window
def open_asset_manager():
    asset_manager = tk.Toplevel(root)
    asset_manager.title("Asset Manager")

    asset_manager.configure(bg='#333333')

    label_header = tk.Label(asset_manager, text="🔒 Asset Manager 🔒", bg='#333333', fg='white', font=("Helvetica", 24))
    label_header.pack(pady=20)

    # the asset name label
    label_name = tk.Label(asset_manager, text="Asset Name:", bg='#333333', fg='white', font=("Helvetica", 14))
    label_name.pack()

    # the asset name entry
    global entry_name
    entry_name = tk.Entry(asset_manager, bg='#444444', fg='white', font=("Helvetica", 14), relief=tk.FLAT)
    entry_name.pack(pady=5)

    # the asset description label
    label_description = tk.Label(asset_manager, text="Asset Description:", bg='#333333', fg='white', font=("Helvetica", 14))
    label_description.pack()

    # the asset description text area with scrollbar
    scrollbar = tk.Scrollbar(asset_manager)
    global entry_description
    entry_description = tk.Text(asset_manager, bg='#444444', fg='white', font=("Helvetica", 14), relief=tk.FLAT, height=5, yscrollcommand=scrollbar.set)
    scrollbar.config(command=entry_description.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    entry_description.pack(pady=5)

    # the status label
    global label_status
    label_status = tk.Label(asset_manager, text="", bg='#333333', fg='white', font=("Helvetica", 12))
    label_status.pack(pady=10)

    # the add asset button
    button_add_asset = tk.Button(asset_manager, text="Add Asset", bg='#0077cc', fg='white', font=("Helvetica", 14), relief=tk.FLAT, command=add_asset)
    button_add_asset.pack(pady=5)

    # the view assets button
    button_view_assets = tk.Button(asset_manager, text="View Assets", bg='#0077cc', fg='white', font=("Helvetica", 14), relief=tk.FLAT, command=view_assets)
    button_view_assets.pack(pady=5)

    # the delete asset label
    label_delete_id = tk.Label(asset_manager, text="Asset ID to delete:", bg='#333333', fg='white', font=("Helvetica", 14))
    label_delete_id.pack()

    # the delete asset entry
    global entry_delete_id
    entry_delete_id = tk.Entry(asset_manager, bg='#444444', fg='white', font=("Helvetica", 14), relief=tk.FLAT)
    entry_delete_id.pack(pady=5)

    # the delete asset button
    button_delete_asset = tk.Button(asset_manager, text="Delete Asset", bg='#0077cc', fg='white', font=("Helvetica", 14), relief=tk.FLAT, command=delete_asset)
    button_delete_asset.pack(pady=5)

    # the exit button
    button_exit = tk.Button(asset_manager, text="Exit", bg='#cc0000', fg='white', font=("Helvetica", 14), relief=tk.FLAT, command=exit_app)
    button_exit.pack(pady=5)

    # the assets table
    create_assets_table()

# Function to open customer review window
def open_customer_review():
    def search_asset():
        search_term = entry_search.get()
        conn = sqlite3.connect('assets.db')
        c = conn.cursor()
        c.execute("SELECT * FROM assets WHERE name LIKE ?", ('%' + search_term + '%',))
        assets = c.fetchall()
        conn.close()
        if assets:
            for asset in assets:
                messagebox.showinfo("Asset Info", f"ID: {asset[0]}\nName: {asset[1]}\nDescription: {asset[2]}")
        else:
            messagebox.showinfo("Asset Info", "No matching assets found")

    def exit_review():
        customer_review.destroy()

    customer_review = tk.Toplevel(root)
    customer_review.title("Customer Review")

    customer_review.configure(bg='#333333')

    label_header = tk.Label(customer_review, text="📝 Customer Review 📝", bg='#333333', fg='white', font=("Helvetica", 24))
    label_header.pack(pady=20)

    # the search label
    label_search = tk.Label(customer_review, text="Search Asset by Name:", bg='#333333', fg='white', font=("Helvetica", 14))
    label_search.pack()

    # the search entry
    entry_search = tk.Entry(customer_review, bg='#444444', fg='white', font=("Helvetica", 14), relief=tk.FLAT)
    entry_search.pack(pady=5)

    # the search button
    button_search = tk.Button(customer_review, text="Search", bg='#0077cc', fg='white', font=("Helvetica", 14), relief=tk.FLAT, command=search_asset)
    button_search.pack(pady=5)

    # the asset list label
    label_asset_list = tk.Label(customer_review, text="Asset List:", bg='#333333', fg='white', font=("Helvetica", 14))
    label_asset_list.pack(pady=(20, 10))

    # the asset listbox with scrollbar
    scrollbar = tk.Scrollbar(customer_review)
    asset_listbox = tk.Listbox(customer_review, bg='#444444', fg='white', font=("Helvetica", 14), relief=tk.FLAT, height=10, yscrollcommand=scrollbar.set)
    scrollbar.config(command=asset_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    asset_listbox.pack(pady=(0, 20))

    # Function to populate asset listbox
    def populate_asset_list():
        conn = sqlite3.connect('assets.db')
        c = conn.cursor()
        c.execute("SELECT * FROM assets")
        assets = c.fetchall()
        conn.close()
        for asset in assets:
            asset_listbox.insert(tk.END, f"Name: {asset[1]}")

    populate_asset_list()

    # the exit button
    button_exit = tk.Button(customer_review, text="Exit", bg='#cc0000', fg='white', font=("Helvetica", 14), relief=tk.FLAT, command=exit_review)
    button_exit.pack(pady=5)


# main window
root = tk.Tk()
root.title("Login")

# background color
root.configure(bg='#333333')

# header label
label_header = tk.Label(root, text="🔒 Login 🔒", bg='#333333', fg='white', font=("Helvetica", 24))
label_header.pack(pady=20)

# username label
label_username = tk.Label(root, text="Username:", bg='#333333', fg='white', font=("Helvetica", 14))
label_username.pack()

# username entry with placeholder text
entry_username = tk.Entry(root, bg='#444444', fg='white', font=("Helvetica", 14), relief=tk.FLAT)
entry_username.pack(pady=5)

# password label
label_password = tk.Label(root, text="Password:", bg='#333333', fg='white', font=("Helvetica", 14))
label_password.pack()

# password entry with placeholder text
entry_password = tk.Entry(root, bg='#444444', fg='white', font=("Helvetica", 14), show="*", relief=tk.FLAT)
entry_password.pack(pady=5)

# little label for status
label_status = tk.Label(root, text="", bg='#333333', fg='white', font=("Helvetica", 12))
label_status.pack(pady=10)

# login button
button_login = tk.Button(root, text="Login", bg='#0077cc', fg='white', font=("Helvetica", 14), relief=tk.FLAT, command=login)
button_login.pack(pady=20)

# Run the main loop
root.mainloop()
