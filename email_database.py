import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from cryptography.fernet import Fernet
import os

# Gera uma chave do algoritmo de criptografia
key = Fernet.generate_key()
cipher_suite = Fernet(key)


# Criptografa determinada string usando a chave do algoritmo
def encrypt_string(text):
    return cipher_suite.encrypt(text.encode()).decode()


# Descriptografa determinada string usando a chave do algoritmo
def decrypt_string(text):
    return cipher_suite.decrypt(text.encode()).decode()


# Adicionar um novo e-mail ao banco de dados
def add_email():
    # Criptografa os dados
    name = name_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    encrypted_data = encrypt_string(f"{name}, {email}, {password}")
    
    # Anexa os dados criptografados ao arquivo
    with open("emails.txt", "a") as f:
        f.write(encrypted_data + "\n")
        
    # Atualiza a lista de e-mails salvos
    display_emails()


# Remove um e-mail do banco de dados
def erase_email(index):
    # Lê o arquivo de banco de dados e remova a linha especificada
    with open("emails.txt", "r") as f:
        lines = f.readlines()
    del lines[index]
    
    # Substitui o banco de dados com os emails atualizados
    with open("emails.txt", "w") as f:
        f.writelines(lines)
        
    # Atualiza a lista de e-mails salvos
    display_emails()


# Atualiza a lista de e-mails salvos exibidos
def display_emails():
    for widget in email_frame.winfo_children():
        widget.destroy()
        
    # Cria o banco de dados se ele não existir
    if not os.path.exists("emails.txt"):
        with open("emails.txt", "w") as f:
            pass
            
    # Le o banco de dados e descriptografa o conteúdo
    with open("emails.txt", "r") as f:
        lines = f.readlines()
    decrypted_lines = [decrypt_string(line.strip()) for line in lines]
    
    # Cria uma linha para cada e-mail salvo
    for i, line in enumerate(decrypted_lines):
        name, email, _ = line.split(",")  # Ignorar a senha!!
        label = ttk.Label(email_frame, text=f"{i+1}. {name}, {email}", font=("Helvetica", 14))
        label.grid(row=i, column=0, sticky="w")
        erase_button = ttk.Button(email_frame, text="Erase", command=lambda index=i: erase_email(index))
        erase_button.grid(row=i, column=1, padx=5)
        

# Cria a janela principal
root = ThemedTk(theme="black")
root.geometry("500x600")
root.title("Email Database - Dark Theme")


# Define a aparência da janela
style = ttk.Style(root)
style.configure('.', font=("Helvetica", 12))
style.configure('TLabel', background="#1F1F1F", foreground="#E8E8E8", padx=10, pady=10)
style.configure('TEntry', background="#1F1F1F", foreground="black", insertbackground="#E8E8E8", padx=5, pady=5)
style.configure('TButton', background="#0080FF", foreground="#E8E8E8", padx=5, pady=5)

title_label = ttk.Label(root, text="Email Database", font=("Helvetica", 16, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=20)

name_label = ttk.Label(root, text="Name:", font=("Helvetica", 14))
name_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
name_entry = ttk.Entry(root, font=("Helvetica", 14))
name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

email_label = ttk.Label(root, text="Email:", font=("Helvetica", 14))
email_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
email_entry = ttk.Entry(root, font=("Helvetica", 14))
email_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

password_label = ttk.Label(root, text="Password:", font=("Helvetica", 14))
password_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
password_entry = ttk.Entry(root, show="*", font=("Helvetica", 14))
password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")

add_email_button = ttk.Button(root, text="Add Email", command=add_email)
add_email_button.grid(row=4, column=1, padx=10, pady=10)

email_display_label = ttk.Label(root, text="Saved Emails:", font=("Helvetica", 14))
email_display_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")

email_frame = ttk.Frame(root)
email_frame.grid(row=6, column=0, columnspan=2, padx=10, pady=10)

display_emails()

root.mainloop()

