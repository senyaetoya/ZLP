# -*- coding: utf-8 -*-
# GUI module generated by PAGE version 4.21
#  in conjunction with Tcl version 8.6
#    Mar 19, 2019 02:27:57 PM MSK  platform: Linux
import ctypes
import sys
import tkinter.font as tkFont
from PIL import Image, ImageTk as itk
from numpy import linspace
import app.user_form_support
from app.int_linear_main import integer_lp
from tkinter import ttk, filedialog
import tkinter as tk
from tkinter import messagebox
import os.path


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    global prog_location
    if sys.platform == 'win32':
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    sys.stdout.flush()
    root = tk.Tk()
    top = Toplevel1(root)
    app.user_form_support.init(root, top)
    root.iconbitmap('img/icon.ico')
    root.mainloop()


w = None


def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    global prog_location
    prog_call = sys.argv[0]
    prog_location = os.path.split(prog_call)[0]
    rt = root
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    app.user_form_support.init(w, top, *args, **kwargs)
    return w, top


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = 'white'  #
        _fgcolor = 'black'  #
        _compcolor = 'white'  #
        _ana1color = 'white'  #
        _ana2color = 'white'  # light-gray

        self.style = ttk.Style()
        self.style.configure('.', background=_bgcolor)
        self.style.configure('.', foreground=_fgcolor)
        self.style.configure('.', font="TkDefaultFont")
        self.style.map('.', background=
        [('selected', _compcolor), ('active', _ana2color)])
        # Gets the requested values of the height and widht.
        window_width = 1020
        window_height = 680
        # Gets both half the screen width/height and window width/height
        position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
        # Positions the window in the center of the page.
        top.geometry("{}x{}+{}+{}".format(window_width, window_height, position_right, position_down))
        top.resizable(width=False, height=False)
        top.title("Поиск оптимального портфеля закупок")
        top.configure(highlightcolor="black")

        self.style.layout("ClosetabNotebook", [("ClosetabNotebook.client",
                                                {"sticky": "nswe"})])
        self.style.layout("ClosetabNotebook.Tab", [
            ("ClosetabNotebook.tab",
             {"sticky": "nswe",
              "children": [
                  ("ClosetabNotebook.padding", {
                      "side": "top",
                      "sticky": "nswe",
                      "children": [
                          ("ClosetabNotebook.focus", {
                              "side": "top",
                              "sticky": "nswe",
                              "children": [
                                  ("ClosetabNotebook.label", {"side":
                                                                  "left", "sticky": ''}),
                                  ("ClosetabNotebook.close", {"side":
                                                                  "left", "sticky": ''}), ]})]})]})])

        PNOTEBOOK = "ClosetabNotebook"

        '''tk classes'''
        class CoeffEntry(tk.Entry):
            def __init__(self, master, var_type, *args, **kwargs):
                tk.Entry.__init__(self, master, *args, **kwargs)
                self.bind('<FocusOut>', focus_out)
                self.var_type = var_type

        '''tk callbacks'''
        def focus_out(e):
            value = e.widget.get()
            var_type = e.widget.var_type
            try:
                if var_type == 'int':
                    int(value)
                else:
                    float(value)
                e.widget['background'] = 'white'
            except ValueError:
                e.widget['background'] = '#FF6347'

        def open_file():
            file = filedialog.askopenfilename(initialdir=(prog_location + "/excel"),
                                              filetypes=(('excel file', '*.xls'), ('excel file', '*.xlsx'),
                                                         ('excel file', '*.xlsm')))
            if file is not None:
                filename.set(file.rpartition('/')[2])
                filepath.set(file)

        def call_linear_prog(filepath, zadacha):
            if filepath == '':
                raise Exception(
                messagebox.showinfo('Ошибка', 'Вы не загрузили таблицу исходных данных')
                )
            else:
                coeffs = {'sort': self.sort_var.get(),
                          'zadacha': zadacha}
                if zadacha == 1:
                    try:
                        coeffs['T'] = int(self.T_entry_p1.get())
                        coeffs['F'] = float(self.F_entry_p1.get())
                        coeffs['stable'] = self.sol_stability.get()
                        coeffs['dummy'] = self.dummy_line.get()
                    except ValueError:
                        messagebox.showinfo('Ошибка', 'Неверное введены коэффициенты')
                        raise
                elif zadacha == 2:
                    try:
                        coeffs['T'] = int(self.T_entry_p2.get())
                        coeffs['F'] = float(self.F_entry_p2.get())
                        coeffs['y'] = float(self.y_entry_p2.get())
                        if self.auto_D.get() == 1:
                            Ds = [k * coeffs['F'] for k in linspace(0.1, 1.5, 15)]
                            coeffs['auto_D'] = Ds
                        else:
                            coeffs['D'] = float(self.D_entry_p2.get())
                    except ValueError:
                        messagebox.showinfo('Ошибка', 'Неверное введены коэффициенты')
                        raise
                integer_lp(filepath, **coeffs)

        def block_D_entry():
            if self.auto_D.get():
                self.D_entry_p2.configure(state='disabled')
            else:
                self.D_entry_p2.configure(state='normal')

        def block_dummy_line():
            if self.sol_stability.get():
                self.check_dummy_stability_p1.configure(state='normal')
            else:
                self.check_dummy_stability_p1.configure(state='disabled')
                self.dummy_line.set(0)

        '''tk variables'''
        #  кнопки открытия файла и запуска расчетов
        filename = tk.StringVar()
        filepath = tk.StringVar()
        #  коэффициенты в форме
        self.sort_var = tk.StringVar()
        self.sort_var.set('b/a')
        F1 = tk.DoubleVar()
        F2 = tk.DoubleVar()
        T1 = tk.IntVar()
        T2 = tk.IntVar()
        D = tk.DoubleVar()
        y = tk.DoubleVar()
        F1.set(100000)
        F2.set(30000)
        T1.set(30)
        T2.set(10)
        D.set(0.4 * F2.get())
        y.set(0.125)
        self.auto_D = tk.BooleanVar()
        self.auto_D.set(0)
        self.sol_stability = tk.BooleanVar()
        self.sol_stability.set(1)
        self.dummy_line = tk.BooleanVar()
        self.dummy_line.set(0)

        self.customFont = tkFont.Font(family="Cambria", size=12, weight='bold')
        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        '''window elements'''
        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
        [('selected', _compcolor), ('active', _ana2color)])
        self.PNotebook1 = ttk.Notebook(top)
        self.PNotebook1.place(relx=0.0, rely=0.0, relheight=1.0, relwidth=1.0)
        self.PNotebook1.configure(style=PNOTEBOOK)

        self.PNotebook1_t0 = tk.Frame(takefocus='1', background='white')
        self.PNotebook1.add(self.PNotebook1_t0)
        self.PNotebook1.tab(0, text=" Базовая стратегия ")

        self.PNotebook1_t1 = tk.Frame(takefocus='1', background='white')
        self.PNotebook1.add(self.PNotebook1_t1)
        self.PNotebook1.tab(1, text=" Кредитная стратегия ")

        '''1 PAGE'''
        self.formula_p1 = ttk.Label(self.PNotebook1_t0)
        image = Image.open('img/1.png')
        factor = 0.5
        width, height = map(lambda x: int(x * factor), image.size)
        image_sized = image.resize((width, height), Image.ANTIALIAS)
        self.image1 = itk.PhotoImage(image_sized)
        self.formula_p1.configure(image=self.image1)
        self.formula_p1.place(anchor='n', relx=0.7, rely=0.03)

        self.label_file_p1 = ttk.Label(self.PNotebook1_t0)
        self.label_file_p1.place(relx=0.05, rely=0.06, anchor='w')
        self.label_file_p1.configure(text='1) Загрузите таблицу\nисходных данных:',
                                     font=self.customFont)

        self.file_button_p1 = tk.Button(self.PNotebook1_t0, command=open_file)
        self.file_button_p1.place(relx=0.2, rely=0.15, anchor='center', height=50, width=240)
        self.file_button_p1.configure(background="#ffffff", cursor='hand2')
        self.file_button_p1.configure(relief='sunken', textvariable=filename)

        self.label_coeffs_p1 = ttk.Label(self.PNotebook1_t0)
        self.label_coeffs_p1.place(relx=0.05, rely=0.23, anchor='w')
        self.label_coeffs_p1.configure(text='2) Введите исходные данные:', font=self.customFont)

        self.Label_F = ttk.Label(self.PNotebook1_t0)
        self.Label_F.place(relx=0.05, rely=0.3, anchor='w')
        self.Label_F.configure(text='Свободные средства (F)')

        self.F_entry_p1 = CoeffEntry(self.PNotebook1_t0, var_type='float', textvariable=F1)
        self.F_entry_p1.place(relx=0.33, rely=0.305, anchor='center', relheight=0.06, relwidth=0.1)

        self.Label_T = ttk.Label(self.PNotebook1_t0)
        self.Label_T.place(relx=0.05, rely=0.38, anchor='w')
        self.Label_T.configure(text='Время в целых днях (T)')

        self.T_entry_p1 = CoeffEntry(self.PNotebook1_t0, var_type='int', textvariable=T1)
        self.T_entry_p1.place(relx=0.33, rely=0.38, anchor='center', relheight=0.06, relwidth=0.1)

        self.label_sort_p1 = ttk.Label(self.PNotebook1_t0)
        self.label_sort_p1.place(relx=0.05, rely=0.48, anchor='w')
        self.label_sort_p1.configure(text='3) Выберите стратегию поиска \nначального приближения:', font=self.customFont)

        self.radio_sort_ba_p1 = tk.Radiobutton(self.PNotebook1_t0)
        self.radio_sort_ba_p1.place(relx=0.05, rely=0.56, anchor='w')
        self.radio_sort_ba_p1.configure(justify='left')
        self.radio_sort_ba_p1.configure(text='По наибольшей марже', background='white')
        self.radio_sort_ba_p1.configure(variable=self.sort_var, value='b/a')

        self.radio_sort_teta_p1 = tk.Radiobutton(self.PNotebook1_t0)
        self.radio_sort_teta_p1.place(relx=0.05, rely=0.62, anchor='w')
        self.radio_sort_teta_p1.configure(justify='left', background='white')
        self.radio_sort_teta_p1.configure(text='По оборачиваемости запасов')
        self.radio_sort_teta_p1.configure(variable=self.sort_var, value='teta')

        self.check_sol_stability_p1 = ttk.Checkbutton(self.PNotebook1_t0)
        self.check_sol_stability_p1.place(relx=0.53, rely=0.68, anchor='w')
        self.check_sol_stability_p1.configure(text='Рассчитать устойчивость решения',
                                              var=self.sol_stability, command=block_dummy_line)

        self.exe_button_p1 = ttk.Button(self.PNotebook1_t0)
        self.exe_button_p1.configure(command=lambda: call_linear_prog(filepath.get(), zadacha=1))
        self.exe_button_p1.place(relx=0.53, rely=0.78, anchor='w', relheight=0.1, relwidth=0.34)
        self.exe_button_p1.configure(text='''Рассчитать''')

        self.check_dummy_stability_p1 = ttk.Checkbutton(self.PNotebook1_t0)
        self.check_dummy_stability_p1.place(relx=0.53, rely=0.87, anchor='w')
        self.check_dummy_stability_p1.configure(text='Добавить тестовую линию в график\n'
                                                     'устойчивости решения',
                                                var=self.dummy_line)

        '''2 PAGE'''
        self.formula_p2 = ttk.Label(self.PNotebook1_t1)
        image = Image.open('img/2.png')
        factor = 0.5
        width, height = map(lambda x: int(x * factor), image.size)
        image_sized = image.resize((width, height), Image.ANTIALIAS)
        self.image2 = itk.PhotoImage(image_sized)
        self.formula_p2.configure(image=self.image2)
        self.formula_p2.place(anchor='n', relx=0.7, rely=0.03)

        self.label_file_p2 = ttk.Label(self.PNotebook1_t1)
        self.label_file_p2.place(relx=0.05, rely=0.06, anchor='w')
        self.label_file_p2.configure(text='1) Загрузите таблицу\nисходных данных:',
                                     font=self.customFont)

        self.file_button_p2 = tk.Button(self.PNotebook1_t1, command=open_file)
        self.file_button_p2.place(relx=0.2, rely=0.15, anchor='center', height=50, width=240)
        self.file_button_p2.configure(background="#ffffff", cursor='hand2')
        self.file_button_p2.configure(relief='sunken', textvariable=filename)

        self.label_coeffs_p2 = ttk.Label(self.PNotebook1_t1)
        self.label_coeffs_p2.place(relx=0.05, rely=0.23, anchor='w')
        self.label_coeffs_p2.configure(text='2) Введите исходные данные:', font=self.customFont)

        self.Label_F = ttk.Label(self.PNotebook1_t1)
        self.Label_F.place(relx=0.05, rely=0.3, anchor='w')
        self.Label_F.configure(text='Свободные средства (F)')

        self.F_entry_p2 = CoeffEntry(self.PNotebook1_t1, var_type='float', textvariable=F2)
        self.F_entry_p2.place(relx=0.33, rely=0.305, anchor='center', relheight=0.06, relwidth=0.1)

        self.Label_T = ttk.Label(self.PNotebook1_t1)
        self.Label_T.place(relx=0.05, rely=0.38, anchor='w')
        self.Label_T.configure(text='Время в целых днях (T)')

        self.T_entry_p2 = CoeffEntry(self.PNotebook1_t1, var_type='int', textvariable=T2)
        self.T_entry_p2.place(relx=0.33, rely=0.38, anchor='center', relheight=0.06, relwidth=0.1)

        self.Label_y_p2 = ttk.Label(self.PNotebook1_t1)
        self.Label_y_p2.place(relx=0.05, rely=0.455, anchor='w')
        self.Label_y_p2.configure(text='Ставка по кредиту (y)')

        self.y_entry_p2 = CoeffEntry(self.PNotebook1_t1, var_type='float', textvariable=y)
        self.y_entry_p2.place(relx=0.33, rely=0.455, anchor='center', relheight=0.06, relwidth=0.1)

        self.Label_D_p2 = ttk.Label(self.PNotebook1_t1)
        self.Label_D_p2.place(relx=0.05, rely=0.53, anchor='w')
        self.Label_D_p2.configure(text='Заёмные средства (D)')

        self.D_entry_p2 = CoeffEntry(self.PNotebook1_t1, var_type='float', textvariable=D)
        self.D_entry_p2.place(relx=0.33, rely=0.53, anchor='center', relheight=0.06, relwidth=0.1)

        self.D_auto_checkbutton = ttk.Checkbutton(self.PNotebook1_t1, variable=self.auto_D,
                                                  text='Автоподбор D', onvalue=1, offvalue=0,
                                                  command=block_D_entry)
        self.D_auto_checkbutton.place(relx=0.25, rely=0.595, anchor='w')

        self.label_sort_p2 = ttk.Label(self.PNotebook1_t1)
        self.label_sort_p2.place(relx=0.05, rely=0.67, anchor='w')
        self.label_sort_p2.configure(text='3) Выберите стратегию поиска \nначального приближения:', font=self.customFont)

        self.radio_sort_ba_p2 = tk.Radiobutton(self.PNotebook1_t1)
        self.radio_sort_ba_p2.place(relx=0.05, rely=0.75, anchor='w')
        self.radio_sort_ba_p2.configure(justify='left')
        self.radio_sort_ba_p2.configure(text='По наибольшей марже', background='white')
        self.radio_sort_ba_p2.configure(variable=self.sort_var, value='b/a')

        self.radio_sort_teta_p2 = tk.Radiobutton(self.PNotebook1_t1)
        self.radio_sort_teta_p2.place(relx=0.05, rely=0.81, anchor='w')
        self.radio_sort_teta_p2.configure(justify='left', background='white')
        self.radio_sort_teta_p2.configure(text='По оборачиваемости запасов')
        self.radio_sort_teta_p2.configure(variable=self.sort_var, value='teta')

        # self.check_sol_stability_p2 = ttk.Checkbutton(self.PNotebook1_t1)
        # self.check_sol_stability_p2.place(relx=0.53, rely=0.68, anchor='w')
        # self.check_sol_stability_p2.configure(text='Рассчитать устойчивость решения',
        #                                      var=self.sol_stability)

        self.exe_button_p2 = ttk.Button(self.PNotebook1_t1)
        self.exe_button_p2.configure(command=lambda: call_linear_prog(filepath.get(), zadacha=2))
        self.exe_button_p2.place(relx=0.53, rely=0.78, anchor='w', relheight=0.1, relwidth=0.34)
        self.exe_button_p2.configure(text='''Рассчитать''')


if __name__ == '__main__':
    vp_start_gui()
