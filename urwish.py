#!/usr/bin/env python3

###############################################################
# Urwish lib by Joep Bos-Coenraad (github.com/JoepBC)
# An easy wrapper for making simple menus using \
#  the Urwid library, www.urwid.org
###############################################################

''' EXAMPLE urwish USAGE:
from urwish import *
from collections import OrderedDict

# Create a new urwish form with a title:
wish = Urwish("Just some examples.")

# urwish input parameters order: input_type, assign_key, description, default_value

# Create an edit field:
wish.add_input("edit", "user", "Your name", "Jane Doe")
# Get answer (str) after run: wish.get_value("user")

# Create a set of radiobuttons using a radiolist. The values can be assigned
#    using a list (by default checking the first item) or as a dictionary
#    of keys and booleans (the last "True" will be selected). Use an OrderedDict 
#    when you want the items of the dictionary to be presented in the right order.
#    Study the "checklist" type below for an OrderedDict example.
wish.add_input("radiolist", "drink", "You must choose", ["beer", "wine", "coffee"])
# Get answer (str) after run: wish.get_value("drink")
#    (answer will be "beer", "wine" or "coffee")

# You may add extra submit buttons too:
wish.add_input("button", "btn1", "An extra submit button")
wish.add_input("button", "btn2", "Or try this one", "Click me")
# Find out if button was clicked (bool): wish.get_value(key)

# Add a list of checkboxes. 
wish.add_input("checklist", "programming_languages", "I love to develop", 
	OrderedDict([("python",False), ("Smalltalk",True), ("C++",False), ("Java",False)]))
# Get answer (list of strings): wish.get_value("programming_languages")

# Create a single checkbox with text left and checkbox right, the "edit field" style:
wish.add_input("twocolcheckbox", "terminal", "Loves the terminal", True)
# Get answer (bool) after run: wish.get_value("terminal")

# Create a classic, but layout messing, checkbox: check first, description after:
wish.add_input("checkbox", "checkbox_only", "This classic checkbox should be used\nin checkbox-only forms for layout reasons", False)
# Get answer (bool) after run: wish.get_value("checkbox_only")

# Or no text at all, just a horizontal spacer/divider. Does not return a value, no need for key assignment.
wish.add_input("spacer")

# Add some static text. Does not return a value, no need for key assignment.
wish.add_input("text", descr="Once upon a time...")
wish.add_input("text", descr="... there was just plain text.")

# Add a full row of additional buttons to end the form with:
wish.add_input("buttonrow", "extra_buttons", ['Fin', 'End', 'Schluss'])
# Find out which button was clicked (str): wish.get_value("extra_buttons")
#    (returns one of the values 'Fin', 'End' and 'Schluss', or None if another
#     submit button was used to end the form.)

wish.run();

# (after the run(), start reading the get_value(key) output)
keys = ["user", "terminal", "checkbox_only", "drink", "btn1", "btn2", 
	"programming_languages", "extra_buttons"]
for a_key in keys:
	print(a_key, "produced value:", wish.get_value(a_key))

# Check the implementation of urwish.define_attributes() in urwid.py for 
#    suggestions to change the appearance.
'''


import urwid
import time

__all__ = ['UrwishWidgetsBase', 'Urwish']

class UrwishWidgetsBase(object):
	
	def revMapItem(self, item):
		'''Edit-fields should change colour when selected. This method
		   will add the focus map 'reversed' to the widget using 
		   an AttrMap wrapper.'''
		return urwid.AttrMap(item, None, focus_map='reversed')

	def urwid_listbox_window(self, title_string):
		body = [urwid.Text(title_string, align='center'), urwid.Divider()]
		listwalker = urwid.SimpleFocusListWalker(body)
		listbox = urwid.ListBox(listwalker)
		pad = urwid.LineBox(urwid.Padding(listbox, left=1, right=1))
		top = urwid.Overlay(pad, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
		    align='center', width=('relative', 80),
		    valign='middle', height=('relative', 80),
		    min_width=20, min_height=24)
		return top, listwalker

	def urwid_twocol_field(self, widget, leftcol_text, equal_space=True, width_first_col=None, leftcol_suffix=": "):
		cols = urwid.Columns([])
		#set default space options
		space_options = cols.options() 
		#and override when necessary
		if not equal_space:
			space_options = cols.options(width_type="pack")
		if width_first_col is not None:
			space_options = cols.options(width_type="given", width_amount=width_first_col)
		cols.contents.append((urwid.Text(leftcol_text+leftcol_suffix), space_options))
		# Use (default) cols.options for second column, as we want this one to be as large as allowed, based on the size of the first column.
		cols.contents.append((self.revMapItem(widget), cols.options()))
		cols.focus_position = len(cols.contents) - 1
		return cols, widget


	def urwid_multicol_field(self, widget_list, equal_space=True, width_first_col=None):
		cols = urwid.Columns([])
		#set default space options
		space_options = cols.options() 
		#and override when necessary
		if not equal_space:
			space_options = cols.options(width_type="pack")
		if width_first_col is not None:
			space_options = cols.options(width_type="given", width_amount=width_first_col)
		#cols.contents.append((urwid.Text(leftcol_text+leftcol_suffix), space_options))
		for widget in widget_list:
			cols.contents.append((self.revMapItem(widget), space_options))
		#cols.focus_position = len(cols.contents) - 1
		return cols, widget_list


	def urwid_buttonrow(self, caption_list=["OK", "Cancel"], equal_space=True, width_first_col=None):
		buttons = []
		for caption in caption_list:
			buttons.append(urwid.Button(caption))
		return self.urwid_multicol_field(buttons)

	def urwid_twocol_edit(self, leftcol_text, defval="", equal_space=True, width_first_col=None, leftcol_suffix=": "):
		widget = urwid.Edit("", defval, edit_pos=0)
		return self.urwid_twocol_field(widget, leftcol_text, 
			equal_space=equal_space, width_first_col=width_first_col, 
			leftcol_suffix = leftcol_suffix)



	def urwid_twocol_button(self, leftcol_text="", defval="Submit", equal_space=True, width_first_col=None, leftcol_suffix=": "):
		widget = urwid.Button(defval)
		return self.urwid_twocol_field(widget, leftcol_text, 
			equal_space=equal_space, width_first_col=width_first_col, 
			leftcol_suffix = leftcol_suffix)

	def urwid_twocol_checkbox(self, leftcol_text, defval="", equal_space=True, width_first_col=None, leftcol_suffix=": "):
		widget = urwid.CheckBox("", defval)
		return self.urwid_twocol_field(widget, leftcol_text, 
			equal_space=equal_space, width_first_col=width_first_col, 
			leftcol_suffix = leftcol_suffix)


class Urwish(UrwishWidgetsBase):

	def __init__(self, title):
		self.window, self.listwalker = self.urwid_listbox_window('Configuration setup')
		
		# CREATE MAIN COLLECTIONS:
		#   The descriptive data (a list: descr, value, widgettype, urwidget) is stored here
		self.widget_specs = {}
		#   The order of the list by keys
		self.widgetlist = []
		
		# PERFORM SOME INITIALISATION
		self.define_attributes()

	def define_attributes(self):
		# End every value on the left column with this string.
		self.leftcol_default_suffix = ":"		

		# Should there be a default submit button at the bottom of the form?
		self.show_default_button = True
		
		# What should the submit-button look like?
		self.submit_twocol = True
		self.submit_button_leftcol_text = "Submit"
		self.submit_button_caption = u"OK"

		# A (static) list of types that help define the length of the first column.		
		self.twocol_types = ["edit", "twocolcheckbox", "radiolist", "checklist"]		

		# This attribute collects the widget_key of the button pressed to
		# submit the form (buttonrow clicks excluded). If the default
		# button is pressed, this value will be set to "default".
		self.button_pressed = None

	def add_input(self, widget_type, assign_key=None, descr="", value=""):
		if assign_key == None:
			assign_key = time.time()
			# But using fast systems, two equal timestamps might be created
			# Make sure this is prevented.
			while (assign_key in self.widgetlist):
				assign_key = time.time()
		if assign_key in self.widgetlist:
			print("WARNING: Key {",assign_key,"} already present in widgetlist. Now overwriting, might cause errors.")
		self.widget_specs[assign_key] = {"descr":descr, "value":value, "type":widget_type}
		# The list has all the widgets in the urwid menu in the right order (whereas dictionaries are unordered)
		self.widgetlist.append(assign_key)

	def set_widget(self, widkey, widget):
		self.widget_specs[widkey]["urwidget"] = widget
	def get_widget(self, widkey):
		return self.widget_specs[widkey]["urwidget"]

	def get_widget_type(self, key):
		return self.widget_specs[key]["type"]

	def get_widget_descr(self, key):
		return self.widget_specs[key]["descr"]

	def get_widget_value(self, key):
		return self.widget_specs[key]["value"]
	def set_widget_value(self, key, value):
		self.widget_specs[key]["value"] = value

	def create_fields(self):
		self.descr_colwidth = self.get_descr_col_width()
		for widkey in self.widgetlist:
			self.listwalker.append(self.create_widget(widkey))

	def create_widget(self, widget_key):
		create_method = self.get_createwidget_method(self.widget_specs[widget_key]["type"])
		return create_method(widget_key)

	def get_createwidget_method(self, widget_type):
		if widget_type == "edit":
			return self.create_input
		if widget_type == "checkbox":
			return self.create_checkbox
		if widget_type=="twocolcheckbox":
			return self.create_twocol_checkbox
		if widget_type == "radiolist":
			return self.create_radiolist
		if widget_type=="checklist":
			return self.create_checklist
		if widget_type=="button":
			return self.create_button
		if widget_type=="buttonrow":
			return self.create_buttonrow
		if widget_type=="spacer":
			return self.create_spacer
		if widget_type=="text":
			return self.create_text
		raise ValueError("Unknown Urwish widget_type", widget_type, 
			"See Urwish::get_createwidget_method for valid options.")

	def create_spacer(self, widget_key):
		return urwid.Divider()

	def create_text(self, widget_key):
		return urwid.Text(self.get_widget_descr(widget_key))

	def create_input(self, widget_key):
		list_columns_item, edit_widget = \
			self.urwid_twocol_edit(self.widget_specs[widget_key]["descr"], self.widget_specs[widget_key]["value"], 
				equal_space=True, width_first_col=self.descr_colwidth, leftcol_suffix = self.leftcol_default_suffix)
		self.set_widget(widget_key, edit_widget)
		return list_columns_item


	def button_firstcol_text(self, widget_key):
		if (not self.widget_specs[widget_key]["value"]):
			return self.widget_specs[widget_key]["value"]
		return self.widget_specs[widget_key]["descr"]


	def button_secondcol_text(self, widget_key):
		if (not self.widget_specs[widget_key]["value"]):
			return self.widget_specs[widget_key]["descr"]
		return self.widget_specs[widget_key]["value"]


	def create_button(self, widget_key):
		leftcol_suffix = self.leftcol_default_suffix

		first_col_text = self.button_firstcol_text(widget_key)
		button_text = self.button_secondcol_text(widget_key)

		if not first_col_text:
			# Don't show a suffix on an empty left column...
			leftcol_suffix = ""

		# Button text MUST be set. If not, use the description on the button instead
		if (first_col_text == None):
			first_col_text = ""
		if (button_text == None):
			button_text = ""
		list_columns_item, button_widget = \
			self.urwid_twocol_button(first_col_text, button_text , 
				equal_space=True, width_first_col=self.descr_colwidth, 
				leftcol_suffix = leftcol_suffix)
		self.set_widget_value(widget_key, False)
		urwid.connect_signal(button_widget, 'click', self.manual_button_click, widget_key)
		return list_columns_item

	def create_buttonrow(self, widget_key):
		button_caption_list = self.widget_specs[widget_key]["value"]
		unused_description = self.widget_specs[widget_key]["descr"]
		# Button captions MUST be set. If not, they have probably been assigned to the unused description instead. That's OK.
		if (not button_caption_list):
			button_caption_list = unused_description
		columns, button_list = \
			self.urwid_buttonrow(button_caption_list)
		for button in button_list:
			self.set_widget_value(widget_key, None)
			urwid.connect_signal(button, 'click', self.buttonrow_click, widget_key)
		return columns


	def create_twocol_checkbox(self, widget_key):
		list_columns_item, checkbox_widget = \
			self.urwid_twocol_checkbox(self.widget_specs[widget_key]["descr"], self.widget_specs[widget_key]["value"], 
				equal_space=True, width_first_col=self.descr_colwidth, leftcol_suffix = self.leftcol_default_suffix)
		self.set_widget(widget_key, checkbox_widget)
		return list_columns_item

	def create_checkbox(self, widget_key):
		cb = urwid.CheckBox(self.get_widget_descr(widget_key), state=bool(self.get_widget_value(widget_key)))
		self.set_widget(widget_key, cb)
		return cb

	def ensure_radiobutton_state_values(self, an_iterable, list_value = False):
		if not hasattr(an_iterable, '__iter__'):
			raise TypeError("RadioButton values are not iterable. Cannot create Urwish radiolist.")
		# This is probably a dictionary-type already:
		if hasattr(an_iterable, 'items'):
			return an_iterable
		# If not, an_iterable is probably a list.
		retdict = {}
		for key in an_iterable:
			# Since no values are set, set to "first true"
			retdict[key] = list_value
		return retdict


	def create_checklist(self, widget_key):
		checkgroup = []
		checkbox_values = self.ensure_radiobutton_state_values(self.get_widget_value(widget_key))
		for key, value in checkbox_values.items():
			checkgroup.append(urwid.CheckBox(key, bool(value)))
		pile = urwid.Pile(checkgroup)
		list_columns_item, checklist_widget = self.urwid_twocol_field(pile, 
			self.get_widget_descr(widget_key), equal_space=False, width_first_col=self.descr_colwidth,
			leftcol_suffix = self.leftcol_default_suffix)
		self.set_widget(widget_key, checkgroup)
		return list_columns_item


	def create_radiolist(self, widget_key):
		radiogroup = []
		radio_values = self.ensure_radiobutton_state_values(self.get_widget_value(widget_key), "first True")
		for key, value in radio_values.items():
			urwid.RadioButton(radiogroup, key, value)
		pile = urwid.Pile(radiogroup)
		#return pile
		list_columns_item, radio_widget = self.urwid_twocol_field(pile, 
			self.get_widget_descr(widget_key), equal_space=False, width_first_col=self.descr_colwidth,
			leftcol_suffix = self.leftcol_default_suffix)
		self.set_widget(widget_key, radiogroup)
		return list_columns_item
		
	def get_value(self, key):
		widget_type = self.get_widget_type(key)
		if (widget_type == "edit"):
			return self.get_input_value(key)
		if (widget_type == "checkbox" or widget_type=="twocolcheckbox"):
			return self.get_checkbox_value(key)
		if (widget_type == "radiolist"):
			return self.get_radiolist_value(key)
		if (widget_type == "checklist"):
			return self.get_checklist_values(key)
		if (widget_type == "button"):
			return self.get_button_value(key)
		if (widget_type == "buttonrow"):
			return self.get_buttonrow_value(key)
		# Default behaviour, return "value" from widget_specs dictionary.
		return self.get_widget_value(key)

	def get_button_value(self, key):
		return self.button_pressed == key

	def get_buttonrow_value(self, key):
		return self.get_widget_value(key)

	def get_input_value(self, key):		
		return self.get_widget(key).get_edit_text()

	def get_checkbox_value(self, key):		
		return self.get_widget(key).get_state()

	def get_checklist_values(self, key):
		values = []
		for a_checkbox in self.get_widget(key):
			if a_checkbox.get_state():
				values.append(a_checkbox.label)
		return values

	def get_radiolist_value(self, key):		
		for a_radiobutton in self.get_widget(key):
			if a_radiobutton.get_state():
				return a_radiobutton.label
		
	def add_ok_button(self):
		self.listwalker.append(urwid.Divider())
		if self.submit_twocol:
			list_widget, okbtn = self.urwid_twocol_button(self.submit_button_leftcol_text, 
				self.submit_button_caption, equal_space=False, width_first_col=self.descr_colwidth,
				leftcol_suffix = self.leftcol_default_suffix)
		else:
			okbtn = urwid.Button(self.submit_button_caption)
			list_widget = okbtn
		## Tell the Urwid screen what to do on pressing OK
		urwid.connect_signal(okbtn, 'click', self.ok_click)
		self.listwalker.append(list_widget)

	def buttonrow_click(self, button, widkey):
		self.set_widget_value(widkey, button.label)
		raise urwid.ExitMainLoop()

	def manual_button_click(self, button, widkey):
		self.button_pressed = widkey
		raise urwid.ExitMainLoop()

	def ok_click(self, button):
		self.button_pressed = "default"
		raise urwid.ExitMainLoop()
		
	def get_line_len(self, description):
		maxlen = 0
		# Check for lists first, some fields may produce a list with descriptions.
		if hasattr(description, '__iter__') and not type(description) is str:
			# Parse recursively
			for an_item in description:
				maxlen = max(maxlen, self.get_line_len(an_item))
			return maxlen
		# The "normal" routine, split at linebreaks, return longest line-string.
		for a_line in description.splitlines():
			maxlen = max(maxlen, len(a_line))
		return maxlen
		
	def get_descr_col_width(self):
		maxlen = 0
		for widkey in self.widgetlist:
			if self.get_widget_type(widkey) in self.twocol_types:
				maxlen = max(maxlen, self.get_line_len(self.widget_specs[widkey]["descr"]))
			if self.get_widget_type(widkey) == "button":
				maxlen = max(maxlen, self.get_line_len(self.button_firstcol_text(widkey)))
		# Add 2 as a spacer between description and field.
		return (maxlen + 2)

	def final_list(self):
		self.create_fields()
		if self.show_default_button:
			self.add_ok_button()

	def show(self):
		urwid.MainLoop(self.window, palette=[('reversed', 'standout', 'dark cyan')]).run()
		return self

	def run(self):
		self.final_list()
		return self.show()
