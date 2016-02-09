#!/usr/bin/env python3

###############################################################
# Urwish lib by Joep Bos-Coenraad (github.com/JoepBC)
# An easy wrapper for making simple menus using \
#  the Urwid library, www.urwid.org
###############################################################

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