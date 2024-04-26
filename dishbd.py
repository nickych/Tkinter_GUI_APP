import tkinter as tk

def update_label():
    label_text.set(entry.get())

def clear_entry():
    entry.delete(0, tk.END)

# Create main window
root = tk.Tk()
root.title("Dashboard App")

# Create and add widgets
label_text = tk.StringVar()
label = tk.Label(root, textvariable=label_text, font=("Helvetica", 16))
label.pack(pady=20)

entry = tk.Entry(root, font=("Helvetica", 14))
entry.pack(pady=10)

update_button = tk.Button(root, text="Update Label", command=update_label)
update_button.pack(pady=5)

clear_button = tk.Button(root, text="Clear Entry", command=clear_entry)
clear_button.pack(pady=5)

# Run the application
root.mainloop()