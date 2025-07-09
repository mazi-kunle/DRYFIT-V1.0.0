import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import CTkMenuBar 
import time
import threading
import webbrowser
import os
from PIL import Image
from main import main
from thin_layer_models.model_fitter import resource_path



class DehydrationApp(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title('DryFit') # Add title
		self.geometry('500x400') 
		self.resizable(False, False) # Make app Non-resizable

		ctk.set_appearance_mode('Dark')
		
		color = '#3c3f41'

		# Create menu
		self.menu = CTkMenuBar.CTkMenuBar(master=self, bg_color=color)
	
		# Add help menu
		help_menu = self.menu.add_cascade(
			'Help',
			corner_radius=0,
		)

		# Add dropdown
		dropdown = CTkMenuBar.CustomDropdownMenu(
			help_menu,
			text_color='white',
			corner_radius=0,
			border_width=0.345,
			border_color='#808080',
		)

		# Add options under menu
		dropdown.add_option(option="Documentation", command=self.open_docs)
		dropdown.add_separator() 
		dropdown.add_option(option="Report a Bug", command=self.open_contact)
		# dropdown.add_separator() 
		# dropdown.add_option(option="About DryFit")

		# Container frame for all other widgets
		self.main_container = ctk.CTkFrame(master=self)
		self.main_container.pack(fill='both', expand=True)


		# initialize ui
		self.init_ui()

	def init_ui(self):
		'''
		Create user interface.
		'''
		# Clear existing widgets in main_container
		for widget in self.main_container.winfo_children():
			if widget:
				widget.destroy()

		# Create upload_frame
		self.upload_frame = ctk.CTkFrame(master=self.main_container)
		self.upload_frame.pack(padx=20, pady=50, fill='x')

		self.file_label = ctk.CTkLabel(
			self.upload_frame, 
			text='No File Selected',
			font=("Roboto", 14),
			anchor='center',
			width=250,
		)

		self.file_label.pack(side='right', padx=10)

		# Add upload icon
		try:
			icon_image = Image.open(resource_path('Upload_icon.png'))
		except FileNotFoundError:
			print('Error: Upload Icon not found')
			icon_image = None
		
		# Add upload button
		self.upload_button = ctk.CTkButton(
			self.upload_frame,
			text="Select M.R History Data  ",
			image=ctk.CTkImage(dark_image=icon_image),
			font = ('Calibri', 15),
			width=100,
			corner_radius=3.5,
			command=self.open_dialog,
		)

		self.upload_button.pack(side='left', padx=(0, 10))
		
		# Add start analysis Button
		self.start_button = ctk.CTkButton(
			self.main_container,
			text="Start Analysis",
			font = ('Calibri', 20),
			width=220,
			corner_radius=3.5,
			state='disabled',
			command=lambda: self.simulate_progress()
		)

		self.start_button.pack(pady=70)

		self.file_path = None
		self.update_idletasks()


	def open_dialog(self):
		'''
		create file dialog to upload M.R history data
		'''
		# get path to selected file
		self.file_path = tk.filedialog.askopenfilename(
            title="Select Moisture Ratio Data File",
            filetypes=[("Excel files", "*.xlsx *.xls")]
        )

		if self.file_path:
			self.start_button.configure(state='normal') # Enable start button
			
			# Truncate long filenames
			filename = os.path.basename(self.file_path)[:25] \
					+ "..." if len(os.path.basename(self.file_path)) > 30 else os.path.basename(self.file_path)
			
			# print(self.file_path)
			self.file_label.configure(text=filename)	
	
		else:
			print('Kindly select a File')
		return

	def reset(self):
		'''
		Reset the GUI after Success or Error
		'''
		# Destroy progress bar if it exists
		if hasattr(self, 'progress'):
			self.progress.destroy()
			del self.progress


		if hasattr(self, 'progress_label'):
			self.progress_label.destroy()
			del self.progress_label

		# Reinitialize ui
		self.init_ui()

	def show_success(self, result):
		'''
		Display success message
		'''
		if hasattr(self, 'progress'):
			self.progress.stop()

		messagebox.showinfo(
			'Success',
			f'Results have been saved to {result}'
		)

		# Reset GuI to home page
		self.reset()

		return 0

	def show_error(self, message):
		'''
		Display error message
		'''
		if hasattr(self, 'progress'):
			self.progress.stop()

		messagebox.showerror(
			'Error', 
			message
		)

		# Reset GuI to home page
		self.reset()

		return 0

	def simulate_progress(self):
		'''
		This function performs the analysis of the data
		'''
		# Disable upload and start button
		self.upload_button.configure(command=None)
		self.start_button.configure(state='disabled')
		self.update_idletasks()
	
		# Add a label and progress bar
		self.progress_label = ctk.CTkLabel(
        	self.main_container,
        	text="Processing...",
        	font=("Calibri", 14)
    	)
		self.progress_label.pack(pady=(0, 5))
		
		self.progress = ctk.CTkProgressBar(
        	self.main_container,
        	width=350,
       		height=5,
        	mode='indeterminate'  # Indeterminate since we don’t know exact duration
    	)

		self.progress.pack(pady=(0, 10))
		self.progress.start()  # Start moving the indeterminate bar
		
		def thread_func(file_path):
			try:
				result = main(file_path)

			except ValueError as ve:
				# catch errors from backend
				msg = str(ve)

				# Schedule the GUI update on the main thread
				self.after(0, lambda: self.show_error(msg))

			else:
				# Schedule the GUI update on the main thread
				self.after(0, lambda: self.show_success(result))

		
		# Run function in background to prevent freezing of GUI
		threading.Thread(
				target=thread_func,
				args=(self.file_path, ),
				daemon=True
		).start()

	def open_docs(self):
		'''
		Opens the documentation on a web browser
		'''
		url = 'https://mazi-kunle.github.io/DRYFIT-V1.0.0/'
		webbrowser.open(url)

		return 0

	def open_contact(self):
		'''
		Opens the contact docs on a web browser
		'''
		url = 'https://mazi-kunle.github.io/DRYFIT-V1.0.0/#-contact-us'
		webbrowser.open(url)

		return 0



app = DehydrationApp()
app.mainloop()