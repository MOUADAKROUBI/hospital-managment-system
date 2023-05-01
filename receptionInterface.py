from tkinter import messagebox
import pathlib as pathlib
import datetime
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from fpdf import FPDF

from HMSdatabase import Database
from logIn import LoginFrame

# init database
db = Database()

class ReceptionFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.config(pady=10)

        results = db.all_reception()
        now = datetime.datetime.now()
        text = ""
        if now.strftime("%p") == "AM":
            text = "bonjour M."
        else:
            text = "bonsoir M."

        self.header = tk.Frame(self)
        self.header.pack()

        # Create widgets for doctor frame
        self.label_title = tk.Label(self.header, text=(text + str(results[0][0])).upper(), font=("Arial 16 bold"))
        self.label_title.grid(row=0, column=0, padx=100)

        # admin title
        self.label_admin = tk.Label(self.header, text="reception", font=("Arial 14 bold"))
        self.label_admin.grid(row=0, column=1, padx=100)

        # Initialize variables
        self.choice = tk.StringVar()

        styleRe = ttk.Style()
        # Configure style for the tabs
        styleRe.configure('TNotebook.Tab',font=('Helvetica', '12', 'bold'), foreground='black', padding=(10, 5))
        # Configure style for the notebook
        styleRe.configure('TNotebook', tabposition = "n",background='#f0f0f0')

        # Create tabs for different functions
        self.notebook = ttk.Notebook(self)
        self.notebook.style = styleRe #type:ignore

        self.tab_patients = ttk.Frame(self.notebook)
        self.tab_appointments = ttk.Frame(self.notebook)
        self.tab_inventory = tk.Frame(self.notebook)

        self.notebook.add(self.tab_patients, text="Patients Et Facteur")
        self.notebook.add(self.tab_appointments, text="les rendez vous")
        self.notebook.add(self.tab_inventory, text="gestion de magazin")

        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Initialize the interface
        self.init_patients()
        self.init_appointments()
        self.init_manage_invontary()

        # button logout
        button_logOut = tk.Button(self, text="déconnection", font=("Arial 12 bold"), bg="red", fg="white", width=20, command=self.logout)
        button_logOut.pack()

    # Initialize the Patients tab
    def init_patients(self):
        # Create the search entry and button for patient records
        self.entry_search_patients = tk.Entry(self.tab_patients, width=20, font=("Arial", 12), justify="center")
        self.entry_search_patients.place(x=60, y=40)

        self.button_search_patients = tk.Button(self.tab_patients, text="Recherche", font=("Arial", 12), bg="blue", fg="white", command=self.search_patients)
        self.button_search_patients.place(x=250, y=35)

        self.button_refresh_patients = tk.Button(self.tab_patients, text="Actualiser", font=("Arial", 12), bg="blue", fg="white", command=self.refresh_patients)
        self.button_refresh_patients.place(x=350, y=35)

        self.button_add_patient = tk.Button(self.tab_patients, text="Ajouter un nouveau patient", font=("Arial 12 bold"), bg="blue", fg="white", command=self.add_patient)
        self.button_add_patient.place(x=470, y=35)

        self.button_delete_patient = tk.Button(self.tab_patients, text="Supprimer le patient", font=("Arial 12 bold"), bg="blue", fg="white", command=self.delete_patient)
        self.button_delete_patient.place(x=700, y=35)

        self.label_frame_patients = tk.LabelFrame(self.tab_patients, text="Dossiers des patients", font=("Arial 12 bold"))
        self.label_frame_patients.place(relx=0.5, y=220, anchor=tk.CENTER, relwidth=0.9, relheight=0.7)

        # Create the treeview widget for patient records
        self.treeview_patients = ttk.Treeview(self.label_frame_patients, columns=("ID", "Nome", "Date De Naissance", "Sexe", "Address", "numéro téléphone"))

        # Create a scrollbar and connect it to the treeview widget
        scrollbar_patients = ttk.Scrollbar(self.label_frame_patients, orient="vertical", command=self.treeview_patients.yview)
        scrollbar_patients.pack(side=tk.RIGHT, fill=tk.Y)
        self.treeview_patients.configure(yscrollcommand=scrollbar_patients.set)

        self.treeview_patients.heading("#0", text="ID")
        self.treeview_patients.heading("#1", text="Nome")
        self.treeview_patients.heading("#2", text="Date De Naissance")
        self.treeview_patients.heading("#3", text="Sexe")
        self.treeview_patients.heading("#4", text="Address")
        self.treeview_patients.heading("#5", text="numéro téléphone")
        self.treeview_patients.column("#0", width=50, anchor="center")
        self.treeview_patients.column("#1", width=150, anchor="center")
        self.treeview_patients.column("#2", width=100, anchor="center")
        self.treeview_patients.column("#3", width=150, anchor="center")
        self.treeview_patients.column("#4", width=200, anchor="center")
        self.treeview_patients.column("#5", width=150, anchor="center")

        self.treeview_patients.place(relx=0, rely=0, relwidth=1, relheight=1)

        # Create the button widget for handling billing
        self.button_handle_billing = tk.Button(self.label_frame_patients, text="Gérer la facturation", font=("Arial 12 bold"), bg="green", fg="white", command=self.handle_billing)
        self.button_handle_billing.place(relx=0.5, rely=0.95, anchor=tk.S)

        # Populate the patient records table
        self.populate_patients()

    def populate_patients(self):
        # Retrieve the patient records from the database
        records = db.all_patient()

        # Insert data into the treeview
        for record in records:
            self.treeview_patients.insert("", tk.END, text=str(record[0]), values=(record[1:6]))

    def add_patient(self):
        # Create a new dialog window for adding a patient
        self.add_patient_dialog = tk.Toplevel(self)
        self.add_patient_dialog.title("Ajouter un nouveau patient")
        self.add_patient_dialog.geometry("500x400")

        # Create widgets for the add patient dialog
        self.label_title_add_patient = tk.Label(self.add_patient_dialog, text="Ajouter un nouveau patient", font=("Arial 16 bold"))
        self.label_title_add_patient.pack(pady=10)

        self.label_name = tk.Label(self.add_patient_dialog, text="Nome:", font=("Arial 12"))
        self.label_name.pack()
        self.entry_name = tk.Entry(self.add_patient_dialog, font=("Arial 12"))
        self.entry_name.pack()

        self.label_dob = tk.Label(self.add_patient_dialog, text="Date De Naissance:", font=("Arial 12"))
        self.label_dob.pack()
        self.entry_dob = DateEntry(self.add_patient_dialog, font=(12), background='gray',foreground='black', borderwidth=2, year= int(datetime.datetime.today().strftime("%y")))
        self.entry_dob.pack()

        genderVal = ["Mâle", "Femelle"]
        self.label_gender = tk.Label(self.add_patient_dialog, text="Sexe:", font=("Arial 12"))
        self.label_gender.pack()
        self.choice_gender = ttk.Combobox(self.add_patient_dialog, font=("Arial 12"), values= genderVal)
        self.choice_gender.pack()

        self.choice_gender.set(genderVal[0])

        self.label_address = tk.Label(self.add_patient_dialog, text="Address:", font=("Arial 12"))
        self.label_address.pack()
        self.entry_address = tk.Entry(self.add_patient_dialog, font=("Arial 12"))
        self.entry_address.pack()

        self.label_phone = tk.Label(self.add_patient_dialog, text="Numéro de telephone:", font=("Arial 12"))
        self.label_phone.pack()
        self.entry_phone = tk.Entry(self.add_patient_dialog, font=("Arial 12"))
        self.entry_phone.pack()

        self.button_submit = tk.Button(self.add_patient_dialog, text="submit", font=("Arial 16 bold"), bg="blue", fg="white", command=self.save_patient)
        self.button_submit.pack(pady=10)
    # Save a new patient record
    def save_patient(self):
        # Get the values from the entry fields
        name = self.entry_name.get()
        gender = self.choice_gender.get()
        dob = self.entry_dob.get()
        address = self.entry_address.get()
        phone = self.entry_phone.get()

        # Valider l'entrée
        if not name:
            messagebox.showerror("Erreur", "Veuillez entrer un nom")
            return
        if not gender:
            messagebox.showerror("Erreur", "Veuillez sélectionner un sexe")
            return
        if not dob:
            messagebox.showerror("Erreur", "Veuillez entrer une date de naissance")
            return

        # Save the patient record to the database
        try:
            dt = datetime.datetime.strptime(dob, '%m/%d/%y')
            date_mysql = datetime.datetime.strftime(dt, '%Y-%m-%d')
            db.add_patient(name, gender, date_mysql, phone, address)
            self.entry_name.delete(0, tk.END)
            self.entry_address.delete(0, tk.END)
            self.entry_phone.delete(0, tk.END)
            self.treeview_patients.delete(*self.treeview_patients.get_children())
            self.populate_patients()
        except Exception as e:
            print(str(e))
            messagebox.showerror("Error", str(e))

    # Search for patients
    def search_patients(self):
        # Get the search term
        search_term = self.entry_search_patients.get().strip()

        # Search for patients with the given name or phone number
        try:
            patients = db.search_patients(search_term)
            self.treeview_patients.delete(*self.treeview_patients.get_children())
            for patient in patients:
                self.treeview_patients.insert("", tk.END, text=str(patient[0]), values=(patient[1:6]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Refresh the patient records table
    def refresh_patients(self):
        self.treeview_patients.delete(*self.treeview_patients.get_children())
        self.populate_patients()

    def delete_patient(self):
        # Get the selected item from the treeview widget
        item = self.treeview_patients.focus()
        item_values = self.treeview_patients.item(item, "values")

        # Check if an item is selected
        if not item:
            messagebox.showerror("Error", "Veuillez sélectionner un patient à supprimer.")
            return

        # Ask the user to confirm the deletion
        confirm = messagebox.askyesno("Supprimer le patient", f"Êtes-vous sûr de vouloir supprimer {item_values[0]} de la base de données?")

        # If the user confirms the deletion, delete the patient from the database and the treeview widget
        if confirm:
            # Delete the patient from the database
            db.delete_patient(item_values[0])

            # Delete the patient from the treeview widget
            self.treeview_patients.delete(item)

    def handle_billing(self):
        # Get the selected item from the treeview widget
        item = self.treeview_patients.focus()
        item_values = self.treeview_patients.item(item, "values")

        # Check if an item is selected
        if not item:
            messagebox.showerror("Error", "Veuillez sélectionner un patient à facturer.")
            return

        # Open a dialog window for billing
        billing_window = tk.Toplevel(self.master)
        billing_window.title("Informations de facturation")
        billing_window.geometry("600x700")
        billing_window.config(bg="white")
        billing_window.resizable(False, False)

        # Définition des données de la facture
        today = datetime.datetime.today()

        self.nom_patient = item_values[0]
        self.num_dossier = "123456789"
        self.date_facture = today.strftime("%d-%m-%Y %H:%M")

        tests = db.all_tests()
        tests_prixs = db.all_tests_types()

        tmp = 0
        for test in tests:
            if test[1] == self.nom_patient:
                for test_prix in tests_prixs:
                    if test[2] == test_prix[0]:
                        tmp += test_prix[1] #type:ignore

        total_frais = tmp

        # Create the labels and entry fields for the patient information
        patient_name_label = tk.Label(billing_window, text="Nom du patient: ", font=("Helvetica 15 underline"), bg="White")
        patient_name_label.place(x=50, y=20)
        patient_name_entry = tk.Label(billing_window, text=f"{self.nom_patient}", font=("Arial 15"), bg="White")
        patient_name_entry.place(x=300, y=20)

        medical_record_number_label = tk.Label(billing_window, text="Numéro de dossier médical :", font=("Helvetica 15 underline"), bg="White")
        medical_record_number_label.place(x=50, y=60)
        medical_record_number_entry = tk.Label(billing_window, text=f"{self.num_dossier}", font=("Arial 15"), bg="White")
        medical_record_number_entry.place(x=350, y=60)

        date_label = tk.Label(billing_window, text="Date de la facture :", font=("Helvetica 15 underline"), bg="White")
        date_label.place(x=50, y=100)
        date_entry = tk.Label(billing_window, text=f"{self.date_facture}", font=("Arial 15"), bg="White")
        date_entry.place(x=300, y=100)

        # Create the labels and values for the medical expenses
        i = 150
        self.items = []
        for test in tests:
            if test[1] == self.nom_patient:
                for test_prix in tests_prixs:
                    if test[2] == test_prix[0]:
                        type_lbl = tk.Label(billing_window, text=f"{test[2]}", font=("Helvetica 15 underline"), bg="White")
                        prix_lbl = tk.Label(billing_window, text=f"{test_prix[1]} DH", font=("Arial 15"), bg="White")
                        type_lbl.place(x=50, y=i)
                        prix_lbl.place(x=350, y=i)
                        self.items.append({
                            "test": test[2],
                            "price": test_prix[1]
                        })
                        i += 40

        total_label = tk.Label(billing_window, text=f"Total des frais : {total_frais} DH", font=("Helvetica 15 underline"))
        total_label.place(x=150, y=i+40)


        # Create the label for payment arrangements
        payment_arrangements_label = tk.Label(billing_window, text="Des arrangements de paiement peuvent être disponibles \n sur demande.", font=("Helvetica 14"), bg="White")
        payment_arrangements_label.place(x=50, y=i+90)

        nom_medcian = db.get_names_doctors()
        # Create the label for the closing statement
        closing_statement_label = tk.Label(billing_window, text=f"Veuillez adresser toutes les questions ou préoccupations \n au Dr. {nom_medcian[0][0]}.", font=("Helvetica 14 italic"), bg="White")
        closing_statement_label.place(x=50, y=i+150)

        # Create the button for printing the bill
        print_button = tk.Button(billing_window, text="Imprimer la facture", font=("Helvetica 14 bold"), command=self.print_bill, bg="green", fg="white")
        print_button.place(x=170, y=i+400)

        # Create the button for closing the billing window
        close_button = tk.Button(billing_window, text="Fermer", font=("Helvetica 14 bold"), command=billing_window.destroy, bg="red", fg="white")
        close_button.place(x=370, y=i+400)

    def print_bill(self):
        # Create a new PDF document
        pdf = FPDF()

        # Set the margins to be equal on all sides
        pdf.set_margins(20, 20, 20)

        # Add a page to the document
        pdf.add_page()

        # Add the logo image and draw a border at the top of the page
        pdf.image('logo.png', 20, 20, 50)
        # pdf.rect(10, 10, 190, 45)

        # Set the font for the document
        pdf.set_font("Arial", size=12)

        # Add the header
        pdf.cell(0, 40, "Relevé de facturation", ln=1, align="C")

        self.currentDate = datetime.datetime.today().strftime("%d-%m-%Y %H:%M")
        pdf.cell(0, 10, f"la date: {self.currentDate}", ln=1)

        # Add the customer information
        pdf.cell(0, 10, f"Nome: {self.nom_patient}", ln=1)
        patients_infos = db.all_patient()
        self.customer_address = ""
        self.customer_phone = ""
        self.date_bird = ""

        for patient_info in patients_infos:
            if patient_info[1] == self.nom_patient:
                self.date_bird = patient_info[2]
                self.customer_address = patient_info[4]
                self.customer_phone = patient_info[5]

        pdf.cell(0, 10, f"date naissance: {self.date_bird}", ln=1)
        pdf.cell(0, 10, f"Address: {self.customer_address}", ln=1)
        pdf.cell(0, 10, f"Phone: {self.customer_phone}", ln=1)

        # Add the items table
        pdf.cell(60, 10, "type de test: ", border=1)
        pdf.cell(30, 10, "Price", border=1)
        pdf.ln()

        for item in self.items:
            pdf.cell(60, 10, item["test"], border=1)
            pdf.cell(30, 10, f"{item['price']:.2f} DH", border=1, align="C")
            pdf.ln()

        # Add the subtotal, and total
        self.total = 0
        for item in self.items:
            self.total += float(item["price"])

        pdf.cell(120, 10, "", border=0)
        pdf.cell(40, 10, "Total:", border=1)
        pdf.cell(40, 10, f"{self.total:.2f} DH", border=1)

        # Add a button with the message at the bottom of the page
        pdf.cell(70, 10, "Nous vous remercions d'avoir choisi notre établissement pour vos soins de santé.\nVeuillez noter que les paiements doivent être effectués dans les 30 jours suivant la réception de cette facture.", ln=1)
        pdf.cell(120, 10, "Caché et Signateur: ", ln=1, align="C")

        # Output the PDF to a file
        pdf.output(f"relevé de facturation de {self.nom_patient}.pdf")

    # Initialize the Appointments tab
    def init_appointments(self):
        # Create widgets for the Appointments tab
        self.btns_frame = tk.Frame(self.tab_appointments)

        self.button_add_appointment = tk.Button(self.btns_frame, text="ajouter nevaux rendez_vous", font=("Arial 12 bold"), bg="blue", fg="white", command=self.add_appointment)
        self.button_delete_appointment = tk.Button(self.btns_frame, text="supprimer rendez_vous", font=("Arial 12 bold"), bg="red", fg="white", command=self.delete_appointment)

        self.button_add_appointment.grid(row=0, column=0, padx=10)
        self.button_delete_appointment.grid(row=0, column=1)

        self.btns_frame.pack(pady=10)

        self.label_frame_appointments = tk.LabelFrame(self.tab_appointments, text="Dossiers de rendez-vous", font=("Arial 12 bold"))
        self.label_frame_appointments.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Create the treeview widget for appointment records
        self.treeview_appointments = ttk.Treeview(self.label_frame_appointments, columns=("ID", "Nome De Patient", "Date", "Temps", "Doctor"))
        self.treeview_appointments.heading("#0", text="ID")
        self.treeview_appointments.heading("#1", text="Nome De Patient")
        self.treeview_appointments.heading("#2", text="Date")
        self.treeview_appointments.heading("#3", text="Temps")
        self.treeview_appointments.heading("#4", text="Doctor")
        self.treeview_appointments.column("#0", width=50)
        self.treeview_appointments.column("#1", width=150)
        self.treeview_appointments.column("#2", width=100)
        self.treeview_appointments.column("#3", width=100)
        self.treeview_appointments.column("#4", width=150)
        self.treeview_appointments.pack(expand=True, fill=tk.BOTH)

        # Populate the appointment records table
        self.populate_appointments()

    def delete_appointment(self):
        # Get the selected item in the treeview
        selected_item = self.treeview_appointments.focus()
        if not selected_item:
            messagebox.showwarning("Avertissement", "Veuillez sélectionner un élément à supprimer.")
            return

        # Retrieve the details of the selected item
        item_id = self.treeview_appointments.item(selected_item, "text")
        item_name = self.treeview_appointments.item(selected_item, "values")[0]

        # Confirm if the user wants to remove the selected item
        if not messagebox.askyesno("Confirmer", f"Êtes-vous sûr de vouloir supprimer le rendez-vous de {item_name} ?"):
            return

        # Remove the selected item from the database
        db.delete_appointment(item_id)

        # Remove the selected item from the treeview
        self.treeview_appointments.delete(selected_item)

    def add_appointment(self):
        # Create a new window for adding an appointment
        self.window_add_appointment = tk.Toplevel(self)
        self.window_add_appointment.title("Ajouter Rendez vous")
        self.window_add_appointment.geometry("500x400")

        self.patients = db.get_names_patients()
        self.doctors = db.get_names_doctors()

        # Create widgets for the window
        label_title = tk.Label(self.window_add_appointment, text="Ajouter un nouveau rendez-vous", font=("Arial 16 bold"))
        label_title.pack(pady=10)

        label_patient = tk.Label(self.window_add_appointment, text="Patient:")
        label_patient.pack(pady=5)

        # Create a combobox to select the patient for the appointment
        self.combobox_patient = ttk.Combobox(self.window_add_appointment, values=[patient[0] for patient in self.patients]) # type: ignore
        self.combobox_patient.pack()

        self.combobox_patient.set(self.patients[0][0])

        label_doctor = tk.Label(self.window_add_appointment, text="Doctor:")
        label_doctor.pack(pady=5)

        # Create a combobox to select the doctor for the appointment
        self.combobox_doctor = ttk.Combobox(self.window_add_appointment, values=[doctor for doctor in self.doctors]) # type: ignore
        self.combobox_doctor.pack()

        self.combobox_doctor.set(self.doctors[0][0])

        label_date = tk.Label(self.window_add_appointment, text="Date (YYYY-MM-DD):")
        label_date.pack(pady=5)

        # Create an entry for the appointment date
        self.entry_date = DateEntry(self.window_add_appointment, font=(12), background='gray',foreground='black', borderwidth=2, year= int(datetime.datetime.today().strftime("%y")))
        self.entry_date.pack()

        label_time = tk.Label(self.window_add_appointment, text="Temp (HH:MM):")
        label_time.pack(pady=5)

        # Create an entry for the appointment time
        # create a StringVar to store the selected time
        self.time_var = tk.StringVar()

        self.time_frame = tk.Frame(self.window_add_appointment)
        # create a Spinbox widget for selecting hours
        self.hour_spinbox = tk.Spinbox(self.time_frame, from_=0, to=23, width=5, wrap=True)
        self.hour_spinbox.grid(row=0, column=0, padx=5)

        # create a Spinbox widget for selecting minutes
        self.minute_spinbox = tk.Spinbox(self.time_frame, from_=0, to=59, width=5, wrap=True)
        self.minute_spinbox.grid(row=0, column=1)

        self.time_frame.pack()
        
        button_add = tk.Button(self.window_add_appointment, text="ajouter rendez_vous", font=("Arial 12 bold"), bg="blue", fg="white", command=self.save_appointment)
        button_add.pack(pady=10)

    def save_appointment(self):
        # Get the user's inputs
        patient_id = self.combobox_patient.get().strip()
        date = self.entry_date.get()
        heure = self.hour_spinbox.get().zfill(2)  # pad with leading zeros if necessary
        minute = self.minute_spinbox.get().zfill(2)  # pad with leading zeros if necessary
        self.time_var.set(f"{heure}:{minute}")
        heure_complete = f"{heure}:{minute}"
        doctor = self.combobox_doctor.get()

        # Validate the inputs
        if not (patient_id and date and heure_complete and doctor):
            messagebox.showerror("Error", "Veuillez remplir tous les champs.")
            return

        # Get the appointments from the database
        appointments = db.all_appointments()

        # # Save the appointment to the database
        dt = datetime.datetime.strptime(date, "%m/%d/%y")
        sql_date = datetime.datetime.strftime(dt, "%Y-%m-%d")

        time = datetime.datetime.strptime(heure_complete, "%H:%M").time()

        # # Check if the appointment already exists
        appointment_exists = False
        for appointment in appointments:
            if (appointment[1] == patient_id and appointment[2] == date and appointment[3] == time):
                appointment_exists = True
                break

        if appointment_exists:
            messagebox.showerror("Error", "Ce rendez-vous existe déjà.")
            return

        db.add_appointment(patient_id, sql_date, heure_complete, doctor)

        # Clear the input fields
        self.combobox_patient.set("sélectionner le patient")

        # Refresh the appointments table
        self.populate_appointments()

    def populate_appointments(self):
        # Clear the current appointments
        self.treeview_appointments.delete(*self.treeview_appointments.get_children())

        # Get the appointments from the database
        appointments = db.all_appointments()

        # Insert the appointments into the treeview widget
        for appointment in appointments:
            self.treeview_appointments.insert("", tk.END, text=str(appointment[0]), values=(appointment[1:5]))

    def init_manage_invontary(self):
        # Créer les widgets pour l'onglet "Gérer l'inventaire"
        self.label_title_inventory = tk.Label(self.tab_inventory, text="Gérer l'inventaire", font=("Arial 16 bold"))
        self.label_title_inventory.pack(pady=10)

        self.label_frame_inventory = tk.LabelFrame(self.tab_inventory, text="Inventaire", font=("Arial 12 bold"))
        self.label_frame_inventory.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        # Créer le widget treeview pour les enregistrements d'inventaire
        self.treeview_inventory = ttk.Treeview(self.label_frame_inventory, columns=("ID", "Nom de l'article", "Quantité", "Prix ​​unitaire", "Prix total", "Description"))
        self.treeview_inventory.heading("#0")
        self.treeview_inventory.heading("#1", text="ID")
        self.treeview_inventory.heading("#2", text="Nom de l'article")
        self.treeview_inventory.heading("#3", text="Quantité")
        self.treeview_inventory.heading("#4", text="Prix ​​unitaire")
        self.treeview_inventory.heading("#5", text="Prix total")
        self.treeview_inventory.heading("#6", text="Description")
        self.treeview_inventory.column("#0", width=0,stretch= tk.NO)
        self.treeview_inventory.column("#1", width=150,anchor="center")
        self.treeview_inventory.column("#2", width=150,anchor="center")
        self.treeview_inventory.column("#3", width=150,anchor="center")
        self.treeview_inventory.column("#4", width=150,anchor="center")
        self.treeview_inventory.column("#5", width=150,anchor="center")
        self.treeview_inventory.column("#6", width=150,anchor="center")
        self.treeview_inventory.pack(expand=True, fill=tk.BOTH)

        # Créer le widget de barre de défilement pour les enregistrements d'inventaire
        self.scrollbar_inventory = tk.Scrollbar(self.label_frame_inventory, orient=tk.VERTICAL, command=self.treeview_inventory.yview)
        self.treeview_inventory.configure(yscroll=self.scrollbar_inventory.set) #type:ignore
        self.scrollbar_inventory.pack(side=tk.RIGHT, fill=tk.Y)

        # Créer les widgets de bouton pour ajouter et supprimer des articles de l'inventaire
        self.button_add_item = tk.Button(self.label_frame_inventory, text="Ajouter un article", font=("Arial 12 bold"), bg="blue", fg="white", command=self.add_item)
        self.button_add_item.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_remove_item = tk.Button(self.label_frame_inventory, text="Supprimer un article", font=("Arial 12 bold"), bg="red", fg="white", command=self.remove_item)
        self.button_remove_item.pack(side=tk.RIGHT, padx=10, pady=10)

        # Refresh inventory records
        self.refresh_inventory()

    def refresh_inventory(self):
        # Clear the current inventory list
        for item in self.treeview_inventory.get_children():
            self.treeview_inventory.delete(item)

        # Retrieve the latest inventory data from the database
        inventory = db.all_invontry()

        # Update the inventory list in the GUI
        for record in inventory:
            self.treeview_inventory.insert("", tk.END, text=str(record[0]), values=(record[0:6]))


    def add_item(self):
        # Ouvrir une fenêtre de dialogue pour ajouter un nouvel élément au stock
        add_item_window = tk.Toplevel(self)
        add_item_window.title("Ajouter un élément")
        add_item_window.geometry("500x400")

        # Créer les champs de saisie et les étiquettes pour le nouvel élément du stock
        label_item_name = tk.Label(add_item_window, text="Nom de l'élément :")
        label_item_name.grid(row=0, column=0, padx=10, pady=10)
        entry_item_name = tk.Entry(add_item_window)
        entry_item_name.grid(row=0, column=1, padx=10, pady=10)

        label_item_quantity = tk.Label(add_item_window, text="Quantité :")
        label_item_quantity.grid(row=1, column=0, padx=10, pady=10)
        entry_item_quantity = tk.Entry(add_item_window)
        entry_item_quantity.grid(row=1, column=1, padx=10, pady=10)

        label_item_unit_price = tk.Label(add_item_window, text="Prix unitaire :")
        label_item_unit_price.grid(row=2, column=0, padx=10, pady=10)
        entry_item_unit_price = tk.Entry(add_item_window)
        entry_item_unit_price.grid(row=2, column=1, padx=10, pady=10)

        label_item_description = tk.Label(add_item_window, text="Description :")
        label_item_description.grid(row=3, column=0, padx=10, pady=10)
        entry_item_description = tk.Entry(add_item_window)
        entry_item_description.grid(row=3, column=1, padx=10, pady=10)

        # Fonction pour ajouter le nouvel élément au stock
        def add_to_database():
            item_name = entry_item_name.get()
            quantity = entry_item_quantity.get()
            unit_price = entry_item_unit_price.get()
            description = entry_item_description.get()

            # Vérifier si l'un des champs est vide
            if not item_name or not quantity or not unit_price or not description:
                messagebox.showerror("Erreur", "Tous les champs sont requis")
                return

            # Vérifier si la quantité et le prix unitaire sont des nombres valides
            try:
                quantity = int(quantity)
                unit_price = float(unit_price)
            except ValueError:
                messagebox.showerror("Erreur", "Quantité ou prix unitaire invalide")
                return

            # Insérer le nouvel élément dans la table de stock
            db.add_invontry(item_name, quantity, unit_price, description)

            # Fermer la fenêtre après avoir ajouté le nouvel élément
            add_item_window.destroy()

            # Mettre à jour la table de stock dans l'interface graphique
            self.show_inventory()

        # Créer le bouton pour ajouter le nouvel élément au stock
        button_add_item = tk.Button(add_item_window, text="Ajouter un élément", font=("Arial 12 bold"), bg="blue", fg="white",command=add_to_database)
        button_add_item.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def show_inventory(self):
        # Clear the treeview
        for record in self.treeview_inventory.get_children():
            self.treeview_inventory.delete(record)

        # Fetch all the records from the inventory table
        records = db.all_invontry()

        # Insert the fetched records into the treeview
        for record in records:
            self.treeview_inventory.insert("", tk.END, text=str(record[0]), values=(record[0:6]))

    def remove_item(self):
        # Obtenir l'élément sélectionné dans la treeview
        selected_item = self.treeview_inventory.focus()
        if not selected_item:
            messagebox.showwarning("Attention", "Veuillez sélectionner un élément à supprimer.")
            return

        # Récupérer les détails de l'élément sélectionné
        item_id = self.treeview_inventory.item(selected_item, "text")
        item_name = self.treeview_inventory.item(selected_item, "values")[0]

        # Confirmer si l'utilisateur souhaite supprimer l'élément sélectionné
        if not messagebox.askyesno("Confirmer", f"Êtes-vous sûr de vouloir supprimer {item_name} ?"):
            return

        # Supprimer l'élément sélectionné de la base de données
        db.remove_item(item_id)

        # Supprimer l'élément sélectionné de la treeview
        self.treeview_inventory.delete(selected_item)

    def logout(self):
        # Switch back to login interface
        self.master.login_frame = LoginFrame(self.master)# type: ignore
        self.master.login_frame.pack(expand=True)# type: ignore
        self.destroy()
