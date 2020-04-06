import numpy as np



class Input_files:

	def __init__(self, relative_path):
		file_in_data = open(relative_path + 'simulations_input.txt','r')

		file_in_data_lines = file_in_data.readlines()
		self.project = file_in_data_lines[0].strip()
		self.network_file = relative_path + file_in_data_lines[1].strip()
		self.codes_file = relative_path + file_in_data_lines[2].strip()

	def get_project_name(self):
		return self.project
	
	def get_network_file_name(self):
		return self.network_file

	def get_codes_file_name(self):
		return self.codes_file