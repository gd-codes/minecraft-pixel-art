"""
tkoptiondialog.py

Module to use tkinter to create a window that shows multiple user-specified
RadioButtons or CheckButtons to select and returns values, like simpledialog
returns strings, integers or floats

To create a dialog with radiobuttons, use
>>> askradio(choicelist, title='', prompt="", parent=None, **options)

Gautam D
April 2020"""

from tkinter import *
from tkinter import messagebox

class RadioOptions:
    """Create a window to display radiobuttons and allow user to select a choice"""
    
    def __init__(self, title='', text="", opts=[],
                 parent=None, mustselect=False, **kwargs):
        """Create the tkinter GUI and variables"""
        self.parent = parent
        self.title = title
        self.text = text
        self.opts = opts
        self.value = None
        self.mustselect = mustselect
        """If parent is not given, creates a 1x1 Tk window in the monitor
            to act as the parent, so that the transient() function can be used"""
        if self.parent is not None :
            self.dialog = Toplevel(self.parent)
            self.dialog.transient(self.parent)
        else :
            self._root = Tk()
            self._root.overrideredirect(1)
            self._root.geometry('1x1+1+1')
            self.dialog = Toplevel(self._root)
            self.dialog.transient(self._root)
        self.dialog.protocol('WM_DELETE_WINDOW', self.close)
        self._var = IntVar()
        self._var.set(-1)
        if self.title :
            self.dialog.title(self.title)
        self.label = Label(self.dialog, text=self.text)
        self.label.pack(padx=20, pady=10, expand=YES, fill=X)
        self._oframe = Frame(self.dialog)
        self._oframe.pack(pady=5, padx=10, expand=YES, fill=BOTH)
        self._widgets = []
        #try :
        for i in range(len(self.opts)) :
            self._widgets.append(
                Radiobutton(self._oframe, text=str(self.opts[i]),
                            var=self._var, value=i, **kwargs))
            self._widgets[i].pack(padx=3,pady=3,expand=YES)
        #except TypeError :
        #    raise ValueError("'opts' must be a list or tuple containing \
#text for the radiobutton messages")
        self._bframe = Frame(self.dialog)
        self._bframe.pack(padx=10, pady=10, expand=YES, fill=X, anchor='c')
        self._bframei = Frame(self._bframe)
        self._bframei.pack(anchor='c')
        self.okbtn = Button(self._bframei, text='OK', width=10,
                            command=self.ok)
        self.okbtn.grid(column=0, row=0, padx=3, pady=3, sticky='e')
        self.canbtn = Button(self._bframei, text='Cancel', width=10,
                             command=self.cancel)
        self.canbtn.grid(column=1, row=0, padx=3, pady=3, sticky='w')
        self.okbtn.focus_set()


    def close(self):
        """Protocol to close the window"""
        if self._var.get() == -1:
            self.value = None
            if self.mustselect :
                messagebox.showwarning('Empty', "You must select one of the \
options.", parent=self.dialog)
                return
        self.dialog.destroy()
        if self.parent is None :
            self._root.destroy()
        return None

    def ok(self):
        self.value = self._var.get()
        self.close()

    def cancel(self):
        self.value = None
        self.close()


class CheckOptions:
    """Create a window to display checkbuttons and allow user to select choices"""
    
    def __init__(self, title='', text="", opts=[],
                 parent=None, mustselect=False, **kwargs):
        """Create the tkinter GUI and variables"""
        self.parent = parent
        self.title = title
        self.text = text
        self.opts = opts
        self.value = None
        self.mustselect = mustselect
        """If parent is not given, creates a 1x1 Tk window in the monitor
            to act as the parent, so that the transient() function can be used"""
        if self.parent is not None :
            self.dialog = Toplevel(self.parent)
            self.dialog.transient(self.parent)
        else :
            self._root = Tk()
            self._root.overrideredirect(1)
            self._root.geometry('1x1+1+1')
            self.dialog = Toplevel(self._root)
            self.dialog.transient(self._root)
        self.dialog.protocol('WM_DELETE_WINDOW', self.close)
        self._varlist = []
        if self.title :
            self.dialog.title(self.title)
        self.label = Label(self.dialog, text=self.text)
        self.label.pack(padx=20, pady=10, expand=YES, fill=X)
        self._oframe = Frame(self.dialog)
        self._oframe.pack(pady=5, padx=10, expand=YES, fill=BOTH)
        self._widgets = []
        #try :
        for i in range(len(self.opts)) :
            v = BooleanVar()
            self._varlist.append(v)
            self._widgets.append(
                Checkbutton(self._oframe, text=str(self.opts[i]), onvalue=True,
                            offvalue=False, var=self._varlist[i], **kwargs))
            self._widgets[i].pack(padx=3,pady=3,expand=YES)
        #except TypeError :
        #    raise ValueError("'opts' must be a list or tuple containing \
#text for the radiobutton messages")
        self._bframe = Frame(self.dialog)
        self._bframe.pack(padx=10, pady=10, expand=YES, fill=X, anchor='c')
        self._bframei = Frame(self._bframe)
        self._bframei.pack(anchor='c')
        self.okbtn = Button(self._bframei, text='OK', width=10,
                            command=self.ok)
        self.okbtn.grid(column=0, row=0, padx=3, pady=3, sticky='e')
        self.canbtn = Button(self._bframei, text='Cancel', width=10,
                             command=self.cancel)
        self.canbtn.grid(column=1, row=0, padx=3, pady=3, sticky='w')
        self.okbtn.focus_set()


    def close(self):
        """Protocol to close the window"""
        if type(self.value)==list and not any(self.value) :
            if self.mustselect :
                messagebox.showwarning('Empty', "You must select one of the \
options.", parent=self.dialog)
                return
        self.dialog.destroy()
        if self.parent is None :
            self._root.destroy()
        return None

    def ok(self):
        self.value = [v.get() for v in self._varlist]
        self.close()

    def cancel(self):
        self.value = None
        self.close()



"""Functions to implement the prompt and return a value after waiting"""       

def askradio(choicelist, title='', prompt="", parent=None, mustselect=False,
             **options):
    """Create an instance of RadioOptions and wait for the user to choose one.
Specify radiobuttons by giving the text for each in the choices list,
If a button is selected, returns the integer corresponding to its index.
Return None if not selected or cancelled"""
    x = RadioOptions(title, prompt, choicelist, parent, mustselect, **options)
    x.dialog.wait_window(x.dialog)
    v = x.value
    return v
        
def askcheckbox(choicelist, title='', prompt="", parent=None, mustselect=False,
             **options):
    """Create an instance of CheckOptions and wait for the user to choose one 
or more. Specify checkbuttons by giving the text for each in the choices list, 
Return a list of boolean values corresponding to each checkbutton's state,
or return None if cancelled"""
    x = CheckOptions(title, prompt, choicelist, parent, mustselect, **options)
    x.dialog.wait_window(x.dialog)
    v = x.value
    return v

