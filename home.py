from PIL import ImageTk, Image
import pathlib as pathlib
import datetime
import tkinter as tk

from logIn import LoginFrame
from doctorInterface import DoctorFrame
from receptionInterface import ReceptionFrame

class HospitalManagementSystem(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("système de gestion hospitalière")
        self.geometry("1250x700+50+30")
        self.resizable(False, False)
        # set the icon for the window
        icon_image = tk.PhotoImage(file="./hospital_icon.png")
        self.iconphoto(False, icon_image)
        
        # Set background image
        self.background_image = ImageTk.PhotoImage(Image.open("backgroundImage.jpeg"))
        self.background_label = tk.Label(self, image=self.background_image)
        self.background_label.place(relwidth=1, relheight=1)

        # Create label widget for displaying current time
        self.time_label = tk.Label(self,text="", font=("Arial 16"), bd=0, highlightthickness=0, fg="black")
        self.time_label.place(x=1140, y=15, anchor="center")

        # Create login interface
        self.login_frame = LoginFrame(self)
        self.login_frame.pack(expand=True)
        # Start a timer to update the current time label every second
        self.update_time()

    def update_time(self):
      # Get the current time
      current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

      # Update the label with the current time
      self.time_label.configure(text=current_time)

      # Schedule the next update in 1 second
      self.after(1000, self.update_time)

    def switch_to_doctor_interface(self):
        self.doctor_frame = DoctorFrame(self)
        self.doctor_frame.pack(expand=True)
        self.login_frame.destroy()

    def switch_to_reception_interface(self):
        self.reception_frame = ReceptionFrame(self)
        self.reception_frame.pack(expand=True)
        self.login_frame.destroy()

if __name__ == '__main__':
    app = HospitalManagementSystem()
    app.mainloop()