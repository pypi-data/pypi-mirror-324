import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import requests

# Set a default version for standalone execution
try:
	# For PyPI package usage
	from . import __version__  
	from . import __author__  
except ImportError:
	# Fallback version for standalone script/executable
	__version__ = "0.2"
	__author__ = "Benevant Mathew"

class PostRequestApp:
	def __init__(self, root):
		self.root = root
		self.root.title("Post Request Application")

		# URL Entry
		tk.Label(root, text="URL:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
		self.url_entry = tk.Entry(root, width=50)
		self.url_entry.grid(row=0, column=1, padx=5, pady=5, columnspan=2)

		# Form Data Entry
		tk.Label(root, text="Form Data (key=value, separated by commas):").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
		self.form_data_entry = tk.Entry(root, width=50)
		self.form_data_entry.grid(row=1, column=1, padx=5, pady=5, columnspan=2)

		# File Selection
		tk.Label(root, text="File:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
		self.file_path = tk.StringVar()
		tk.Entry(root, textvariable=self.file_path, width=40).grid(row=2, column=1, padx=5, pady=5)
		tk.Button(root, text="Browse", command=self.browse_file).grid(row=2, column=2, padx=5, pady=5)

		# Submit Button
		tk.Button(root, text="Send Request", command=self.send_request).grid(row=3, column=1, pady=10)

	def browse_file(self):
		file_path = filedialog.askopenfilename()
		if file_path:
			self.file_path.set(file_path)

	def send_request(self):
		url = self.url_entry.get()
		form_data = self.form_data_entry.get()
		file_path = self.file_path.get()

		if not url:
			messagebox.showerror("Error", "URL is required.")
			return

		# Parse form data into a dictionary
		data = {}
		if form_data:
			try:
				for item in form_data.split(","):
					key, value = item.split("=")
					data[key.strip()] = value.strip()
			except ValueError:
				messagebox.showerror("Error", "Invalid form data format. Use key=value pairs separated by commas.")
				return

		files = None
		if file_path:
			try:
				files = {"file": open(file_path, "rb")}
			except Exception as e:
				messagebox.showerror("Error", f"Unable to open file: {e}")
				return

		try:
			response = requests.post(url, json=data, files=files)
			if files:
				files["file"].close()
			messagebox.showinfo("Response", f"Status Code: {response.status_code}\nResponse Text: {response.text}")
		except Exception as e:
			messagebox.showerror("Error", f"Request failed: {e}")

# Function to display help
def print_help():
	help_message = """
	Usage: postmansub [OPTIONS]

	A small package to sent post requests.

	Options:
	--version, -v      Show the version of postmansub and exit
	--author, -a       Show the Author name and exit
	--help, -h         Show this help message and exit
	(No arguments)     Launch the GUI application
	"""
	print(help_message)
	sys.exit(0)

def create_gui():
	# Check for command-line arguments
	if "--version" in sys.argv or "-v" in sys.argv:
		print(f"version {__version__}")
		sys.exit(0)
	elif "--help" in sys.argv or "-h" in sys.argv:
		print_help()
		sys.exit(0) 
	elif "--author" in sys.argv or "-a" in sys.argv:
		print(f"Author {__author__}")
		sys.exit(0)
	#######################################################
	root = tk.Tk()
	app = PostRequestApp(root)
	root.mainloop()
	
if __name__ == "__main__":
	# Check for command-line arguments
	if "--version" in sys.argv or "-v" in sys.argv:
		print(f"version {__version__}")
		sys.exit(0)
	elif "--help" in sys.argv or "-h" in sys.argv:
		print_help()
		sys.exit(0)
	elif "--author" in sys.argv or "-a" in sys.argv:
		print(f"Author {__author__}")
		sys.exit(0)
	else:
		create_gui()
