from tkinter import messagebox
from PIL import ImageTk, Image
import pathlib as pathlib
import tkinter as tk

from HMSdatabase import Database

# init database
db = Database()

class LoginFrame(tk.Frame):
  def __init__(self, master):
      super().__init__(master)

      self.config(highlightthickness=0, highlightbackground=self["bg"], highlightcolor=self["bg"])

      # Load the image and create a label for it
      self.image = ImageTk.PhotoImage(Image.open("logo.png"))
      self.label_image = tk.Label(self, image=self.image)

      # Create widgets for login frame
      self.label_title = tk.Label(self, text="Hôpital Ángeles LÉON", font=("Arial", 20))
      self.label_title.config(highlightthickness=0, highlightbackground=self.label_title["bg"], highlightcolor=self.label_title["bg"])
      self.label_username = tk.Label(self, text="Username:", font=("Arial", 14))
      self.entry_username = tk.Entry(self, font=("Arial", 14), justify="center")
      self.label_password = tk.Label(self, text="Mot de pass:", font=("Arial", 14))
      self.entry_password = tk.Entry(self, show="*", font=("Arial", 14), justify="center")
      self.button_login = tk.Button(self, text="Connexion", width=30, bg="#3c7ade", fg="white",font=("Arial", 14), command=self.login)

      # Layout widgets using grid
      self.label_image.grid(row=0, column=0, columnspan=4)
      self.label_title.grid(row=1, column=0, columnspan=4, padx=20, pady=20)
      self.label_username.grid(row=2, column=0, padx=10, pady=10, sticky="e")
      self.entry_username.grid(row=2, column=1, padx=10, pady=10, sticky="w")
      self.label_password.grid(row=3, column=0, padx=10, pady=10, sticky="e")
      self.entry_password.grid(row=3, column=1, padx=10, pady=10, sticky="w")
      self.button_login.grid(row=4, column=0, columnspan=2, padx=10, pady=20)

  def login(self):
    doctors = db.all_doctors()
    records = db.all_reception()
    # Verify credentials and switch to appropriate interface
    if self.entry_username.get() == doctors[0][0] and self.entry_password.get() == doctors[0][5]:
        self.master.switch_to_doctor_interface() #type:ignore
    elif self.entry_username.get() == records[0][0] and self.entry_password.get() == records[0][5]:
        self.master.switch_to_reception_interface() #type:ignore
    else:
        messagebox.showerror('Error', "votre nome ou mot de pass est incorrect")
