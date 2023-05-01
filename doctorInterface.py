from tkinter import messagebox
import pathlib as pathlib
import datetime
import tkinter as tk
from tkinter import ttk
from datetime import  date
from tkcalendar import DateEntry

from HMSdatabase import Database
from logIn import LoginFrame

# init database
db = Database()

class DoctorFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.config(pady=10)

        # Initialize variables
        self.choice = tk.StringVar()

        # Retrieve the results
        results = db.all_doctors()

        now = datetime.datetime.now()
        text = ""
        if now.strftime("%p") == "AM":
            text = "bonjour D."
        else:
            text = "bonsoir D."

        self.header = tk.Frame(self)
        self.header.pack(pady=20)

        # Create widgets for doctor frame
        self.label_title = tk.Label(self.header, text=(text + str(results[0][0])).upper(), font=("Arial 16 bold"))
        self.label_title.grid(row=0, column=0, padx=100)

        # admin title
        self.label_admin = tk.Label(self.header, text="Admin", font=("Arial 14 bold"))
        self.label_admin.grid(row=0, column=1, padx=100)

        # Create a notebook widget and add it to the frame
        styleRe = ttk.Style()
        # Configure style for the tabs
        styleRe.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'), foreground='black', padding=(10, 5))
        # Configure style for the notebook
        styleRe.configure('TNotebook', tabposition='n', background='#f0f0f0')

        # Create tabs for different functions
        self.notebook = ttk.Notebook(self, width=1000, padding=(5, 10))
        self.notebook.style = styleRe #type:ignore

        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Create frames for each tab
        self.patient_tab = tk.Frame(self.notebook)
        self.appt_tab = tk.Frame(self.notebook)
        self.test_tab = tk.Frame(self.notebook)
        self.reception_tab = tk.Frame(self.notebook)

        # Add the frames to the notebook with appropriate labels
        self.notebook.add(self.patient_tab, text="Dossier du patient")
        self.notebook.add(self.appt_tab, text="Planifier des rendez-vous")
        self.notebook.add(self.test_tab, text="Demande test")
        self.notebook.add(self.reception_tab, text="Réception")

        self.view_patient_record()
        self.schedule_appointments()
        self.order_test()
        self.inscreption_reception()

        self.logout_button = tk.Button(self, text="Déconnexion", bg= "red", font=("Arial 16 bold"), fg="white",command=self.logout)
        self.logout_button.pack()

    def view_patient_record(self):
        #create the search bar
        self.entry_search_patients = tk.Entry(self.patient_tab, width=40, font=("Arial", 12), justify="center")
        self.entry_search_patients.place(x=200, y=40)

        self.button_search_patients = tk.Button(self.patient_tab, text="Rechercher", font=("Arial", 12), bg="blue", fg="white", command=self.search_patients)
        self.button_search_patients.place(x=590, y=35)

        self.button_refresh_patients = tk.Button(self.patient_tab, text="Actualiser", font=("Arial", 12), bg="blue", fg="white", command=self.refresh_patients)
        self.button_refresh_patients.place(x=700, y=35)
        
        # Créer le widget treeview
        self.treeview_pat = ttk.Treeview(self.patient_tab, columns=("ID", "Nom", "Année de naissance", "Genre", "Adresse", "Téléphone"), show="headings")
        self.treeview_pat.place(x=120, y=85)

        # Définir les en-têtes de colonnes et leurs propriétés
        self.treeview_pat.heading("ID", text="ID")
        self.treeview_pat.column("ID", width=50, anchor="center")
        self.treeview_pat.heading("Nom", text="Nom")
        self.treeview_pat.column("Nom", width=200, anchor="center")
        self.treeview_pat.heading("Année de naissance", text="Année de naissance")
        self.treeview_pat.column("Année de naissance", width=100, anchor="center")
        self.treeview_pat.heading("Genre", text="Genre")
        self.treeview_pat.column("Genre", width=75, anchor="center")
        self.treeview_pat.heading("Adresse", text="Adresse")
        self.treeview_pat.column("Adresse", width=200, anchor="center")
        self.treeview_pat.heading("Téléphone", text="Téléphone")
        self.treeview_pat.column("Téléphone", width=150, anchor="center")

        self.populate_patients()

    def populate_patients(self):
        # Retrieve the patient records from the database
        records = db.all_patient()

        # Insert data into the treeview
        for record in records:
            self.treeview_pat.insert("", tk.END, text=str(record[0]), values=record)

    def search_patients(self):
        # Get the search term
        search_term = self.entry_search_patients.get().strip()

        # Search for patients with the given name or phone number
        try:
            patients = db.search_patients(search_term)
            self.treeview_pat.delete(*self.treeview_pat.get_children())
            for patient in patients:
                self.treeview_pat.insert("", tk.END, values=patient)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def refresh_patients(self):
        self.treeview_pat.delete(*self.treeview_pat.get_children())
        self.populate_patients()

    def schedule_appointments(self):
        self.frame_radio_buttons = tk.Frame(self.appt_tab, width=700, height=450)
        self.frame_radio_buttons.pack(pady=30)

        self.choice = tk.StringVar(value="day")
        self.radio_day = tk.Radiobutton(self.frame_radio_buttons, text="Aujourd'hui", value="day", variable=self.choice, font=("Arial 12"))
        self.radio_week = tk.Radiobutton(self.frame_radio_buttons, text="Semain", value="week", variable=self.choice, font=("Arial 12"))
        self.radio_month = tk.Radiobutton(self.frame_radio_buttons, text="Moin", value="month", variable=self.choice, font=("Arial 12"))
        self.radio_year = tk.Radiobutton(self.frame_radio_buttons, text="Annee", value="year", variable=self.choice, font=("Arial 12"))

        self.radio_day.grid(row=0, column=0, padx=10, pady=10)
        self.radio_week.grid(row=0, column=1, padx=10, pady=10)
        self.radio_month.grid(row=0, column=2, padx=10, pady=10)
        self.radio_year.grid(row=0, column=3, padx=10, pady=10)

        self.button_show = tk.Button(self.appt_tab, text="Montrer", font=("Arial 14 bold"), bg="green", fg="white", command=self.show_appointments)
        self.button_show.pack(pady=10)

        self.treeview_app = ttk.Treeview(self.appt_tab, columns=("ID", "Nom du patient", "Date", "Heure", "Nom du médecin"), show="headings")
        self.treeview_app.pack()

        # Définir les en-têtes de colonnes et leurs propriétés
        self.treeview_app.heading("ID", text="ID")
        self.treeview_app.column("ID", width=50, anchor="center")
        self.treeview_app.heading("Nom du patient", text="Nom du patient")
        self.treeview_app.column("Nom du patient", width=150)
        self.treeview_app.heading("Date", text="Date")
        self.treeview_app.column("Date", width=100, anchor="center")
        self.treeview_app.heading("Heure", text="Heure")
        self.treeview_app.column("Heure", width=100, anchor="center")
        self.treeview_app.heading("Nom du médecin", text="Nom du médecin")
        self.treeview_app.column("Nom du médecin", width=150)

        # Call the show_appointments function to insert the data into the treeview
        self.show_appointments()

    def show_appointments(self):
        # Delete all rows from the tree
        self.treeview_app.delete(*self.treeview_app.get_children())

        # Determine the selected time frame
        time_frame = self.choice.get()
        records = []
        if time_frame == "day":
            # Query the database to retrieve appointments for the selected day
            records = db.day_appointments()

        elif time_frame == "week":
            # Query the database to retrieve appointments for the selected week
            records = db.week_appointments()

        elif time_frame == "month":
            # Query the database to retrieve appointments for the selected month
            records = db.month_appointments()

        elif time_frame == "year":
            # Query the database to retrieve appointments for the selected year
            records = db.year_appointments()

        # Insert the appointment records into the treeview
        for record in records:
            self.treeview_app.insert("", tk.END, text=str(record[0]), values=(record[0:5]))

    def order_test(self):
        self.fram_test = tk.Frame(self.test_tab)
        self.fram_test.pack(pady=30)

        self.label_patient_name = tk.Label(self.fram_test, text="nom Patient:", font=("Arial 14"))
        self.entry_patient_name = ttk.Combobox(self.fram_test, font=("Arial 12"), values= [patient[0] for patient in db.get_names_patients()]) #type:ignore
        self.label_test_type = tk.Label(self.fram_test, text="Type de Test: ", font=("Arial 14"))
        self.entry_test_type = ttk.Combobox(self.fram_test, font=("Arial 12"), values = [test_type[0] for test_type in db.all_tests_types()]) #type:ignore
        self.entry_patient_name.set(db.get_names_patients()[0][0])
        self.entry_test_type.set(db.all_tests_types()[0][0])
        self.label_status = tk.Label(self.fram_test, text="Status:", font=("Arial 14"))
        val = ["En Cours", "Complete"]
        self.entry_status = ttk.Combobox(self.fram_test, font=("Arial 12"), values=val)
        self.entry_status.set("Select Un Statu")

        self.label_patient_name.grid(row=0, column=0 ,pady=10, padx=15)
        self.entry_patient_name.grid(row=0, column=1, pady=10, padx=15)
        self.label_test_type.grid(row=1, column=0 ,pady=10, padx=15)
        self.entry_test_type.grid(row=1, column=1, pady=10, padx=15)
        self.label_status.grid(row=2, column=0, pady=10, padx=15)
        self.entry_status.grid(row=2, column=1 ,pady=10, padx=15)

        self.button_submit = tk.Button(self.fram_test, text="Enregistrer", font=("Arial 12 bold"), bg="blue", fg="white", command=self.submit_test_order)
        self.button_submit.grid(row=4, column=0, columnspan=2, pady=10)

    def submit_test_order(self):
        # Get the values entered in the form
        patient_name = self.entry_patient_name.get()
        test_type = self.entry_test_type.get()
        currentDate = date.today()
        currentTime = datetime.datetime.now().strftime("%H:%M")
        status = self.entry_status.get()

        if patient_name != "" and test_type != "" and status != "":
            # Insert the test order into the database
            db.add_order(patient_name, test_type, currentDate, currentTime, status)
            # Clear the form fields
            self.entry_patient_name.delete(0, tk.END)
            self.entry_test_type.delete(0, tk.END)
            self.entry_status.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Tout les champt est obliger")

    def inscreption_reception(self):
        style = ttk.Style()
        # Configure style for the tabs
        style.configure('TNotebook.Tab', font=('Helvetica', '12', 'bold'), foreground='black', padding=(10, 5))
        # Configure style for the notebook
        style.configure('TNotebook', background='#f0f0f0')

        menu_reception = ttk.Notebook(self.reception_tab)
        menu_reception.pack(pady=30)
        menu_reception.style = style # type: ignore

        new_rece = tk.Frame(menu_reception, bg="white")
        delete_rece = tk.Frame(menu_reception, bg="white")

        menu_reception.add(new_rece, text="nouveau reception")
        menu_reception.add(delete_rece, text="supprimer reception")

        # new reception
        new_rece_frame = tk.Frame(new_rece, bg="white")
        new_rece_frame.pack()

        self.name_lable = tk.Label(new_rece_frame, text="nome de reception", font=("Arial 12"), bg="white")
        self.date_lable = tk.Label(new_rece_frame, text="date de naissance", font=("Arial 12"), bg="white")
        self.adress_lable = tk.Label(new_rece_frame, text="adress", font=("Arial 12"), bg="white")
        self.tel_lable = tk.Label(new_rece_frame, text="numéro de téléphone", font=("Arial 12"), bg="white")
        self.email_lable = tk.Label(new_rece_frame, text="email", font=("Arial 12"), bg="white")
        self.password_lable = tk.Label(new_rece_frame, text="mot de pass", font=("Arial 12"), bg="white")
        self.name_lable.grid(row=0, column=0, pady=10)
        self.date_lable.grid(row=1, column=0, pady=10)
        self.adress_lable.grid(row=2, column=0, pady=10)
        self.tel_lable.grid(row=3, column=0, pady=10)
        self.email_lable.grid(row=4, column=0, pady=10)
        self.password_lable.grid(row=5, column=0, pady=10)

        self.name_entry = tk.Entry(new_rece_frame, font=("Arial 12"))
        self.date_entry = DateEntry(new_rece_frame, font=(12), background='gray',foreground='black', borderwidth=2, year= int(datetime.datetime.today().strftime("%y")))
        self.adress_entry = tk.Entry(new_rece_frame, font=("Arial 12"))
        self.tel_entry = tk.Entry(new_rece_frame, font=("Arial 12"))
        self.email_entry = tk.Entry(new_rece_frame, font=("Arial 12"))
        self.password_entry = tk.Entry(new_rece_frame, font=("Arial 12"), show="*")
        self.name_entry.grid(row=0, column=1)
        self.date_entry.grid(row=1, column=1)
        self.adress_entry.grid(row=2, column=1)
        self.tel_entry.grid(row=3, column=1)
        self.email_entry.grid(row=4, column=1)
        self.password_entry.grid(row=5, column=1)

        self.submit_button = tk.Button(new_rece_frame, text="Enregistrer", font=("Arial 12 bold"), bg="blue", fg="white", command=self.submit_inscre_rece)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Create treeview
        delete_rec_frame = tk.Frame(delete_rece)
        delete_rec_frame.pack()

        tree_scroll = tk.Scrollbar(delete_rece)
        tree_scroll.pack(side=tk.RIGHT,fill=tk.Y)

        self.treeview_rec = ttk.Treeview(delete_rec_frame, yscrollcommand=tree_scroll.set , columns=("nome", "Date Naissance", "address", "Numéro De Téléphone", "email", "Mot De Pass"))

        tree_scroll.config(command=self.treeview_rec.yview)

        self.treeview_rec.heading("#0", text="Name")
        self.treeview_rec.column("#0", width=0, minwidth=0, stretch=tk.NO)

        self.treeview_rec.heading("#1", text="Name")
        self.treeview_rec.column("#1", width=100, minwidth=150, stretch=tk.NO)

        self.treeview_rec.heading("#2", text="Year Bird")
        self.treeview_rec.column("#2", width=100, minwidth=100, stretch=tk.NO)

        self.treeview_rec.heading("#3", text="Address")
        self.treeview_rec.column("#3", width=100, minwidth=200, stretch=tk.NO)

        self.treeview_rec.heading("#4", text="Phone Number")
        self.treeview_rec.column("#4", width=100, minwidth=150, stretch=tk.NO)

        self.treeview_rec.heading("#5", text="Email")
        self.treeview_rec.column("#5", width=150, minwidth=200, stretch=tk.NO)

        self.treeview_rec.heading("#6", text="Password")
        self.treeview_rec.column("#6", width=100, minwidth=150, stretch=tk.NO)

        self.treeview_rec.grid(row=0, column=0, sticky="nsew")
        
        # Load reception data into the treeview
        self.load_reception_data()
        
        # Bind a function to handle row deletion when a row is selected
        self.treeview_rec.bind("<Double-Button-1>", self.delete_row)

    def submit_inscre_rece(self):
      name = self.name_entry.get()
      date_str = self.date_entry.get_date()
      adress = self.adress_entry.get()
      email = self.email_entry.get()
      tel = self.tel_entry.get()
      password = self.password_entry.get()

      # convert the date to a string in the format of MySQL's DATE type
      mysql_date = date_str.strftime('%Y-%m-%d')

      if name != "" and date_str != "" and adress != "" and email != "" and tel != "" and password != "":
          db.add_reception(name, mysql_date, adress, tel, email, password)

          self.name_entry.delete(0, tk.END)
          self.date_entry.delete(0, tk.END)
          self.tel_entry.delete(0, tk.END)
          self.email_entry.delete(0, tk.END)
          self.adress_entry.delete(0, tk.END)
          self.password_entry.delete(0, tk.END)
      else:
          messagebox.showerror("Error", "Tout les champt est obliger")
    
    def load_reception_data(self):
        # Clear the treeview
        for row in self.treeview_rec.get_children():
            self.treeview_rec.delete(row)
        
        # Select all rows from the reception table
        rows = db.all_reception()
        
        # Insert the rows into the treeview
        for row in rows:
            self.treeview_rec.insert("", tk.END, text=str(row[0]), values=row[0:6])

    def delete_row(self, event):
        selected_item = self.treeview_rec.selection()[0]
        if selected_item:
            # Get the ID of the selected row
            name = self.treeview_rec.item(selected_item)['text']
            
            # Delete the row from the reception table
            db.delete_reception(name)
            
            # Remove the row from the treeview
            self.treeview_rec.delete(selected_item)

    def logout(self):
        # Switch back to login interface
        self.master.login_frame = LoginFrame(self.master) #type:ignore
        self.master.login_frame.pack(expand=True) #type:ignore
        self.destroy()
