# TkToolTip

TkToolTip is a library for adding ToolTips to Tkinter widgets in an easy and sophisticated way.

## Installation

To install TkToolTip, you can use pip:

```
pip install TkToolTip
```

## Usage Example:

```
import tkinter as tk
from TkToolTip import ToolTip

root = tk.Tk()

button = tk.Button(root, text="Hover here")
button.pack(padx=10, pady=10)
ToolTip(button, text="This is a tooltip", delay=1.5, font=('Helvetica', 12, 'italic'), text_color='#FF5733', background="#ffffe0", borderwidth=2 , relief='raised', show_duration=5)

root.mainloop()
```