from tkinter import messagebox
import pathlib as pathlib
import mysql.connector as connection
from datetime import timedelta, date
import calendar

class Database:
    def __init__(self):
        self.conn = connection.connect(
            host = "localhost",
            user = "mouadakroubi",
            password = "mouad0612738376",
            database = "HMS"
        )
        self.cursor = self.conn.cursor()
    
    def add_patient(self, name, gender, dob, phone, address):
        sql = "INSERT INTO patients (name, date_bird, gender, address, phone_number) VALUES (%s, %s, %s, %s, %s)"
        values = (name, dob, gender, address, phone)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def all_patient(self):
        # Retrieve the patient records from the database
        sql = 'SELECT * FROM patients'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def search_patients(self, search_term):
      sql = "SELECT * FROM patients WHERE name LIKE %s"
      val  = ("%" + search_term + "%", )
      self.cursor.execute(sql, val)
      result = self.cursor.fetchall()
      return result

    def delete_patient(self, id_patient):
        sql = "DELETE FROM patients WHERE name = %s"
        val  = (id_patient, )
        self.cursor.execute(sql, val)
        self.conn.commit()
    
    def get_names_patients(self):
        sql = "SELECT name FROM patients"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def all_reception(self):
        # Retrieve the patient records from the database
        sql = 'SELECT * FROM reception'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def all_doctors(self):
        sql = 'SELECT * FROM doctor'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results
    
    def get_names_doctors(self):
        sql = "SELECT name FROM doctor"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def all_appointments(self):
        sql = 'SELECT * FROM appointments'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def add_appointment(self, patient_name, date, time, doctor):
        sql = "INSERT INTO appointments (patient_name, date, time, doctor) VALUES (%s,%s,%s,%s)"
        val = (patient_name, date, time, doctor)
        self.cursor.execute(sql, val)
        self.conn.commit()

        messagebox.showinfo('success', f'the appointment is registred')

    def get_all_times_appointment(self):
        sql = 'SELECT time FROM appointments'
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def day_appointments(self):
        # Query the database to retrieve appointments for the selected day
        sql = "SELECT * FROM appointments WHERE date = %s"
        currentDate = date.today()
        self.cursor.execute(sql, (currentDate,))
        results = self.cursor.fetchall()
        return results if results else []
    
    def week_appointments(self):
        today = date.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)
        sql = "SELECT * FROM appointments WHERE date BETWEEN %s AND %s"
        self.cursor.execute(sql, (start_week, end_week))
        results = self.cursor.fetchall()
        return results if results else []

    def month_appointments(self):
        today = date.today()
        start_month = today.replace(day=1)
        end_month = today.replace(day=calendar.monthrange(today.year, today.month)[1])
        sql = "SELECT * FROM appointments WHERE date BETWEEN %s AND %s"
        self.cursor.execute(sql, (start_month, end_month))
        results = self.cursor.fetchall()  
        return results if results else []

    def year_appointments(self):
        today = date.today()
        start_year = today.replace(month=1, day=1)
        end_year = today.replace(month=12, day=31)
        sql = "SELECT * FROM appointments WHERE date BETWEEN %s AND %s"
        self.cursor.execute(sql, (start_year, end_year))
        results = self.cursor.fetchall()  
        return results if results else []
    
    def delete_appointment(self, item_id):
        sql = "DELETE FROM appointments WHERE id = %s"
        val = (item_id, )
        self.cursor.execute(sql, val)
        self.conn.commit()

    def all_tests(self):
        sql = "SELECT * FROM tests"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results
    
    def add_order(self, patient_name, test_type, date, time, status):
        sql = "INSERT INTO tests (patient_name, test_type, date, time, status) VALUES (%s, %s, %s, %s, %s)"
        val = (patient_name, test_type, date, time, status)
        self.cursor.execute(sql, val)
        self.conn.commit()
        
        # Display success message
        success_message = f"le test {test_type} est enregestrie."
        messagebox.showinfo("Success", success_message)

    def all_tests_types(self):
        sql = "SELECT * FROM test_prix"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def add_reception(self, name, mysql_date, adress, tel, email, password):
        sql = "insert into reception (name, year_bird, address, phone_number, email ,password) values (%s,%s,%s,%s,%s,%s)"
        val = (name, mysql_date, adress, tel, email, password)
        self.cursor.execute(sql, val)
        self.conn.commit()

        messagebox.showinfo("success", f"la reception {name} is enregestrie")
    
    def delete_reception(self, name):
        query = "DELETE FROM reception WHERE name = %s"
        self.cursor.execute(query, (name,))
        self.conn.commit()

        messagebox.showinfo('success', f'{name} is deleted')

    def all_invontry(self):
        sql = "SELECT id, item_name, quantity, unit_price, quantity * unit_price as total_price, description FROM inventory"
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results
    
    def add_invontry(self, item_name, quantity, unit_price, description):
        sql = "INSERT INTO inventory (item_name, quantity, unit_price, description) VALUES (%s, %s, %s, %s)"
        values = (item_name, quantity, unit_price, description)
        self.cursor.execute(sql, values)
        self.conn.commit()

    def remove_item(self, item_id):
        sql = "DELETE FROM inventory WHERE id = %s"
        val = (item_id,)
        self.cursor.execute(sql, val)
        self.conn.commit()

        # Show a success message
        messagebox.showinfo("Success", f"{item_id} has been removed from the inventory.")
