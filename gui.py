import tkinter as tk
import customtkinter as ctk
import CTkMenuBar 
import time
import threading
import os
from PIL import Image
from main import main


class DehydrationApp(ctk.CTk):
	def __init__(self):
		super().__init__()
		self.title('DryFit') # Add title
		self.geometry('500x400') 
		self.resizable(False, False) # Make app Non-resizable

		ctk.set_appearance_mode('Dark')
		
		color = '#2b2b2b'

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
		dropdown.add_option(option="Documentation")
		dropdown.add_separator() 
		dropdown.add_option(option="Report a Bug")
		dropdown.add_separator() 
		dropdown.add_option(option="About DryFit")

		
		self.upload_frame = ctk.CTkFrame(master=self)
		self.upload_frame.pack(padx=20, pady=50, fill='x')

		self.file_label = ctk.CTkLabel(
			self.upload_frame, 
			text='No File Selected',
			font=("Roboto", 14),
			anchor='center',
			width=250,
		)

		self.file_label.pack(side='right', padx=10)


		
		try:
			icon_image = Image.open('share.png')
		except FileNotFoundError:
			print('Error: Upload Icon not found')
			icon_image = None
		
		# Add upload Button
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
			self,
			text="Start Analysis",
			font = ('Calibri', 20),
			width=220,
			corner_radius=3.5,
			state='disabled',
			command=lambda: main(self.file_path)
		)

		self.start_button.pack(pady=70)


	def open_dialog(self):
		# get path to selected file
		self.file_path = tk.filedialog.askopenfilename(
            title="Select Moisture Ratio Data File",
            filetypes=[("All Files", "*.*")]
        )

		if self.file_path:
			self.start_button.configure(state='normal')
			
			filename = os.path.basename(self.file_path)[:30] \
					+ "..." if len(os.path.basename(self.file_path)) > 30 else os.path.basename(self.file_path)
			
			print(self.file_path)
			self.file_label.configure(text=filename)	
	
		else:
			print('Kindly select a File')
		return


	# def simulate_progress(self):
	# 	self.upload_button.configure(state='disabled')
	# 	self.start_button.configure(state='disabled')

	# 	self.progress = ctk.CTkProgressBar(self, width=400, height=5)
	# 	self.progress.pack(pady=5)
		
	# 	def run_progress():
	# 		self.progress.set(0)
	# 		for i in range(101):
	# 			self.progress.set(i / 100)
	# 			time.sleep(0.01)
	# 			# self.update_idletasks()
		
	# 	threading.Thread(target=run_progress).start()




if __name__ == '__main__':
	app = DehydrationApp()
	app.mainloop()