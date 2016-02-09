# urwish, a python3 library for creating linear text-based forms
A **wrapper for urwid** (www.urwid.org) to create forms easily and efficiently. The original urwid library can do way much more in a powerful way, but for the creation of simple/linear data management forms it can be quite a struggle to address. **urwish** is rather limited, but _VERY_ easy.

_Requires library: urwid_

More details (and comments) on the **example below** in *urwish_example.py* (https://github.com/JoepBC/urwish/blob/master/urwish_example.py).

![Example screenshot](https://github.com/JoepBC/urwish/blob/master/urwish_example_screenshot.png "Screenshot")

_The screenshot above is created using the following python3 code:_

```
from urwish import *
from collections import OrderedDict

wish = Urwish("Just some examples.")
wish.add_input("edit", "user", "Your name", "Jane Doe")
wish.add_input("radiolist", "drink", "You must choose", ["beer", "wine", "coffee"])
wish.add_input("button", "btn1", "An extra submit button")
wish.add_input("button", "btn2", "Or try this one", "Click me")
wish.add_input("checklist", "programming_languages", "I love to develop", 
	OrderedDict([("python",False), ("Smalltalk",True), ("C++",False), ("Java",False)]))
wish.add_input("twocolcheckbox", "terminal", "Loves the terminal", True)
wish.add_input("checkbox", "checkbox_only", 
  "This classic checkbox should be used\nin checkbox-only forms for layout reasons", False)
wish.add_input("spacer")
wish.add_input("text", descr="Once upon a time...")
wish.add_input("text", descr="... there was just plain text.")
wish.add_input("buttonrow", "extra_buttons", ['Fin', 'End', 'Schluss'])
wish.run();
```

**Reading the user input is even easier! (see example source)**
