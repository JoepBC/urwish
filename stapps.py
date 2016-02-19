#!/usr/bin/env python3

#########################################################################
# StoredApplicationSettings lib by Joep Bos-Coenraad (github.com/JoepBC)
#########################################################################

import json
import atexit
import re
import os
from appdirs import AppDirs

__all__ = ["StoredApplicationSettings", "VerboseWriter"]

class VerboseWriter(object):
	def __init__(self, verbose_level=1):
		# Integer: The level of output to be generated.
		## -1: no output at all. 
		##  0: only very important output (errors, critical warnings etc.)
		##  1: warnings, suggestions
		##  2: debug info
		self.verbose_level = verbose_level

	def print(self, comment_level, *args):
		''' Output arguments if the verbose_level is higher or equal to the comment_level priveded with the verbose call. '''
		if self.verbose_level >= comment_level:
			print(*args)


class StoredApplicationSettings(object):

	def __init__(self, application_name=None, filename = None, application_developer="", use_local_path=False, 
			config_file_prefix="default", config_file_suffix="-settings.conf", verbose_level=1, verbosewriter=None,
			base=None, static_base_settings=False):

		self.v = verbosewriter if verbosewriter is not None else VerboseWriter(verbose_level)

		# String: The actual filename that will be used to store data
		self.filename = filename
		# Boolean: Should the file be stored at the pwd or in the user config dir?
		self.use_local_path = use_local_path
		# String: What should the exported file start/end with? (only relevant if no [full]filename is given)
		self.config_file_prefix = config_file_prefix
		self.config_file_suffix = config_file_suffix

		# Base is another StoredApplicationSettings object (or alike) whose settings will be loaded, and which is also affected when this object is updated.
		self.base = base
		self.static_base_settings = static_base_settings

		self.set_application_name(application_name, application_developer)
		# Create default settings dictionary
		self.default_settings()
		# In case of a base, add these settings too
		self.add_base_settings()
		# Define filenames for reading/writing settings
		self.set_filenames()
		# Make sure the directory exists
		self.verify_config_dir()
		# If present, load settings from self.user_settings_filename
		self.load_settings()
		atexit.register(self.close_settings)
		self.store_settings_on_close = True

	def update(self, key, value):
		''' Store/overwrite setting, also in base settings if available and if base is not marked static. '''
		if not self.static_base_settings and not self.base == None:
			self.base.update(key,value)
		self.settings[key] = value


	def set_application_name(self, application_name, application_developer):
		''' Perform validation check on application name and set attributes '''
		self.application_name = application_name
		if self.use_local_path:
			if self.application_name == None:
				self.application_name = "local"
			return
		if not re.match(r'[\w-]+$', application_name):
			raise ValueError("Invalide application name ("+application_name+"). It may only contain letters, digits, underscores and dashes (and at least one of them).")
		self.author = application_developer


	def default_settings(self):
		''' Override this method with default values when creating a StoredApplicationSettings subclass '''
		# Create dictionary to store application settings
		self.settings = {}

	def add_base_settings(self):
		''' If base settings are present, add/overwrite them to the default settings values '''
		if not self.base == None:
			for key, value in self.base.settings.items():
				self.settings[key] = value

	def set_filenames(self):
		''' Define the filenames used for loading and storing the application settings data '''
		if self.filename == None:
			self.filename = self.config_file_prefix+self.config_file_suffix
		self.user_config_dirname = os.getcwd() if self.use_local_path else AppDirs(self.application_name, self.author).user_config_dir
		self.user_settings_filename = os.path.join(self.user_config_dirname, self.filename);

	def verify_config_dir(self):
		''' Make sure that the user directory for the configuration file exists '''
		if self.use_local_path:
			return None
		os.makedirs(self.user_config_dirname, exist_ok=True)

	def load_settings(self):
		''' If settings have been saved previously, load (and set) them now. '''
		try:
			fp = open(self.user_settings_filename, 'r')
		except:
			#Couldn't open file. That's OK. No settings loaded from file.
			return
		else:
			with fp:
				self.set_settings_from_file(fp)

	def set_settings_from_file(self, infile):
		''' Read JSON dictionary data from opened filehandler 'infile' and update the values in self.settings with its contents '''
		settings_dictionary  = json.load(infile)
		for key, value in settings_dictionary.items():
			self.update(key,value)
			# self.settings[key] = value #this was before "self.base" was implemented.
		self.v.print(1, ("Local" if self.use_local_path else "User"), "settings read from file", self.user_settings_filename)

	def close_settings(self):
		''' This method is called upon closing the application '''
		if self.store_settings_on_close:
			self.store_settings()

	def store_settings(self):
		''' Store the settings in dictionary self.settings in self.user_settings_filename using JSON serialisation '''
		with open(self.user_settings_filename, 'w') as outfile:
			json.dump(self.settings, outfile)
		self.v.print(1,"Current",self.application_name, "settings stored at '"+self.user_settings_filename+"'.")
		self.v.print(1,"Remove this file to reset to the default settings at a next run.")

# End of StoredApplicationSettings
