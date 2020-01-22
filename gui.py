"""
GUI for the discogs.py command line app
"""

import sys
from threading import Thread
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.scrolledtext import ScrolledText

from discogs import main


LICENCE = """
MIT License

Copyright (c) 2020 Jaakko Roponen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


class CommandLineArgs(object):
    """Object for storing variables that would be given via command line"""
    def __init__(self, filename='', no_urls=False, no_details=False):
        self.filename = filename
        self.no_urls = no_urls
        self.no_details = no_details


class StdoutRedirector(object):
    """Redirect stdout to GUI text box instead of console"""
    def __init__(self, text_widget):
        self.text_box = text_widget

    def write(self, string):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert('end', string)
        self.text_box.see('end')  # scroll to end
        self.text_box.config(state=tk.DISABLED)


class Window(tk.Frame):
    """Application main frame"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title('Prices from Discogs')
        self.build_menu()
        self.build_widgets()

    def build_menu(self):
        """GUI menu"""
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file_menu = tk.Menu(menu, tearoff=0)
        file_menu.add_command(label="Exit", command=lambda: root.destroy())
        menu.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menu, tearoff=0)
        help_menu.add_command(label="About", command=self.show_about)
        help_menu.add_separator()
        help_menu.add_command(label="Licence", command=self.show_licence)
        menu.add_cascade(label="Help", menu=help_menu)

    def build_widgets(self):
        """GUI widget definitions"""

        # allow the widget to take the full space of the root window
        self.pack(fill='both', expand=True, padx=20, pady=20)

        tk.Label(self, anchor='w', text='Prices from Discogs', font=(44)) \
          .grid(row=0, columnspan=2, sticky='w')

        tk.Label(
            self,
            anchor='w',
            text="Please, provide an excel file with 'Cat', 'Artist' "
                 "and 'Album' columns.") \
            .grid(row=1, columnspan=2, sticky='w', pady=10)

        tk.Button(
            self, text='Choose file...', width=15, command=self.ask_filename) \
            .grid(row=2, column=0, sticky='w', pady=10)

        self.file_box = tk.Text(self, height=1)
        self.file_box.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

        self.no_urls = tk.IntVar()
        tk.Checkbutton(
            self,
            anchor='w',
            text='Skip url search (only searh details for albums, '
                 'which already have Discogs url)',
            variable=self.no_urls) \
            .grid(row=3, columnspan=2, sticky='w', pady=5)

        self.no_details = tk.IntVar()
        tk.Checkbutton(
            self,
            anchor='w',
            text='Skip album detail search (only search Discogs album urls)',
            variable=self.no_details) \
            .grid(row=4, columnspan=2, sticky='w', pady=5)

        tk.Button(self, text='Start', width=15, command=self.start) \
          .grid(row=5, column=0, sticky='w', pady=10)

        self.text_box = ScrolledText(self, state='disabled')
        self.text_box.grid(row=6, columnspan=2, pady=5, sticky='nsew')

        tk.Label(self, text='(c) Jaakko Roponen, 2020') \
          .grid(row=7, columnspan=2, sticky='e')

        # how rows and cols should expand
        self.columnconfigure(1, weight=1)
        self.rowconfigure(6, weight=1)

    def ask_filename(self):
        """get file name"""
        self.filename = askopenfilename(
            filetypes=[('Excel files', '.xlsx .xls')])
        if self.filename:
            self.file_box.delete('1.0', 'end')
            self.file_box.insert('end', self.filename)

    def show_about(self):
        window = tk.Toplevel(self)
        window.resizable(False, False)

        tk.Label(
            window,
            text='About "Prices from Discogs"',
            font=(44)) \
            .pack(pady=20, padx=20)

        tk.Label(
            window,
            text="This app searches prices for albums from discogs.com.",
            wraplength=300) \
            .pack(padx=20)

        tk.Label(
            window,
            text="Please, provide an excel file with 'Cat', 'Artist' "
                 "and 'Album' columns.", wraplength=300) \
            .pack(padx=20)

        tk.Label(
            window,
            text='First searches the exact release based on the catalog '
                 'number. If no results, then searches for the "master" '
                 'by artist and album name.', wraplength=300) \
            .pack(padx=20)

        tk.Label(
            window,
            text="In case of a match, saves the album information, including "
                 "album url and prices, to the source file.", wraplength=300) \
            .pack(padx=20)

        tk.Label(window, text='(c) Jaakko Roponen, 2020', wraplength=300) \
          .pack(pady=20, padx=20)

    def show_licence(self):
        window = tk.Toplevel(self)
        window.resizable(False, False)
        tk.Label(window, text=LICENCE).pack(pady=20, padx=20)

    def disable_widgets(self, disable=True):
        """disable / enable widgets"""
        state = tk.DISABLED if disable else tk.NORMAL
        for widget in self.winfo_children():
            try:
                widget.config(state=state)
            except tk._tkinter.TclError:  # widgets, which don't have state
                pass

    def threader(self, args):
        """wrapper for discogs.py main, where stdout is printed to text box"""
        sys.stdout = StdoutRedirector(self.text_box)  # stdout to text_box
        try:
            main(args)
        except SystemExit as err:
            print(err)
        sys.stdout = sys.__stdout__  # return stdout to original sys.stdout
        self.disable_widgets(False)

    def start(self):
        """get args from GUI and start the main process in a thread"""
        filename = self.file_box.get('1.0', 'end-1c')
        no_urls = bool(self.no_urls.get())
        no_details = bool(self.no_details.get())

        if not filename:
            return None

        args = CommandLineArgs(
            filename=filename,
            no_urls=no_urls,
            no_details=no_details)

        self.disable_widgets(True)

        # run discogs.py main outside of mainloop
        thread = Thread(target=lambda: self.threader(args))
        thread.daemon = True  # daemon, so will die when the main dies
        thread.start()


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('1200x500')

    app = Window(root)

    root.mainloop()
