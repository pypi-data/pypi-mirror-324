import tkinter as tk

class ToolTip(object):
    def __init__(self, 
                 widget, 
                 relief: str | tuple | None = None, 
                 borderwidth: int = 1,  
                 background : str | tuple | None = None, 
                 text : str | tuple | None = None, 
                 delay: float = 1.0,
                 show_duration: float = 10.0,
                 font: tuple | None = None, 
                 text_color: str | tuple | None = None, 
                 justify: str = 'left',
                 **kwargs: any):

    
        
    
        self.widget = widget
        self.text = text
        self.delay = int(delay * 1000)
        self.show_duration = int(show_duration * 1000)
        self.font = font
        self.text_color = text_color
        self.widget.bind("<Enter>", self.schedule_show)
        self.widget.bind("<Leave>", self.leave)
        self.tw = None
        self.id_after = None
        self.id_duration = None
        self.background = background
        self.borderwidth = borderwidth
        self.relief = relief
        self.justify = justify
        

    def schedule_show(self, event=None):
        self.id_after = self.widget.after(self.delay, self.enter)

    def enter(self, event=None):
        x = y = 0
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify=self.justify, background=self.background, relief=self.relief, borderwidth=self.borderwidth, font=('Arial', 10), fg=self.text_color)
        label.pack(ipadx=1)

    # Agendar a destruição após o tempo de duração
        self.id_duration = self.tw.after(self.show_duration, self.leave)

    def leave(self, event=None):
        if self.id_after:
            self.widget.after_cancel(self.id_after)
            self.id_after = None
        if self.id_duration:
            self.tw.after_cancel(self.id_duration)
            self.id_duration = None
        if self.tw:
            self.tw.destroy()
