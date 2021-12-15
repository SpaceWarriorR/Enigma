import re
import tkinter as tk
from tkinter import messagebox
from string import ascii_uppercase
from file_processing import *
from enigma import enigma


# custom text box class with edit detection
class CustomText(tk.Text):
    def __init__(self, *args, **kwargs):
        """A text widget that report on internal widget commands"""
        tk.Text.__init__(self, *args, **kwargs)

        # create a proxy for the underlying widget
        self._orig = self._w + "_orig"
        self.tk.call("rename", self._w, self._orig)
        self.tk.createcommand(self._w, self._proxy)

    def _proxy(self, command, *args):
        cmd = (self._orig, command) + args
        result = self.tk.call(cmd)

        if command in ("insert", "delete", "replace"):
            self.event_generate("<<TextModified>>")

        return result


# plugboard editing GUI
def plugboard_editor():
    # function for saving plugboard settings to a file
    def save_plugboard():

        # getting settings from text box and preparing for checks
        txt = txt_edit.get(1.0, tk.END).strip() + ' '

        # testing if file is in the right format and there are no repeated letters
        plugboard_regex = re.compile(r'(\b[A-Z]{2} )*')
        if (len(set(txt.replace(' ', ''))) != len(txt.replace(' ', '')) or plugboard_regex.search(
                txt).group() != txt) and txt.strip() != '':
            messagebox.showerror('Invalid Format', 'Please enter a valid set of characters')  # error dialogue box
        else:
            # if check passed, file changed and window closed
            set_plugs(txt, 'plugboard.enigma')
            win_plugboard.destroy()

    # function to close the window
    def cancel_plugboard():
        win_plugboard.destroy()

    # creating window
    win_plugboard = tk.Tk()
    win_plugboard.title("Plugboard settings")
    win_plugboard.geometry('300x150')
    win_plugboard.rowconfigure(0, minsize=100, weight=1)
    win_plugboard.columnconfigure(1, minsize=100, weight=1)

    # creating input field
    txt_edit = tk.Text(win_plugboard)
    txt_edit.insert(tk.END, get_plugs('plugboard.enigma'))

    # creating save and exit buttons
    fr_buttons = tk.Frame(win_plugboard, relief=tk.RAISED, bd=2)
    btn_save = tk.Button(fr_buttons, text="Save", command=save_plugboard)
    btn_cancel = tk.Button(fr_buttons, text="Cancel", command=cancel_plugboard)

    # placing widgets
    btn_save.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_cancel.grid(row=1, column=0, sticky="ew", padx=5)
    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")

    win_plugboard.mainloop()


# main GUI
def gui():
    # encrypting function
    def encrypt(msg):
        # getting relevant variables from GUI
        msg = ''.join(filter(str.isalpha, msg.upper()))
        chosen_rotor_names = [str_var_rotor1_choice.get(), str_var_rotor2_choice.get(), str_var_rotor3_choice.get()]
        poss = [str_var_rotor1_pos.get(), str_var_rotor2_pos.get(), str_var_rotor3_pos.get()]
        rings = [str_var_rotor1_setting.get(), str_var_rotor2_setting.get(), str_var_rotor3_setting.get()]
        chosen_reflector_name = str_var_reflector_choice.get()

        # getting rotors from files
        temp = get_rotors('rotors.txt')
        frotor_names = temp[0]
        frotors_data = temp[1]

        # getting reflectors from file
        temp = get_reflectors('reflectors.txt')
        raw_reflector_names = temp[0]
        raw_reflectors = temp[1]

        # preparing data for enigma machine
        rotors = [frotors_data[frotor_names.index(chosen_rotor_names[i])] for i in range(3)]
        reflector = raw_reflectors[raw_reflector_names.index(chosen_reflector_name)]

        # plugboard
        plugboard = get_plug_data('plugboard.enigma')

        return enigma(msg, rotors, poss, rings, reflector, plugboard)

    # function called when text in input box is changed to encrypt it in output box
    def on_modification(event=None):
        txt_output.configure(state='normal')
        txt_output.delete("1.0", "end")
        txt_output.insert(tk.END, encrypt(txt_input.get(1.0, tk.END)))
        txt_output.configure(state='disabled')

    # making the window and configuring sizes
    win_main = tk.Tk()
    win_main.geometry("750x250")
    win_main.title('Enigma')
    win_main.rowconfigure(0, minsize=230, weight=1)
    win_main.columnconfigure(0, minsize=250, weight=1)
    win_main.columnconfigure(2, minsize=250, weight=1)

    # text bits
    txt_input = CustomText(win_main)
    txt_input.bind("<<TextModified>>", on_modification)
    fr_options = tk.Frame(win_main, relief=tk.RAISED, bd=2)
    txt_output = tk.Text(win_main)

    # temporary variables
    rotor_names = get_rotors('rotors.txt')[0]
    reflector_names = get_reflectors('reflectors.txt')[0]

    # rotors

    # # choosing rotors

    # # # creating all of the widgets
    lbl_rotor_choice = tk.Label(fr_options, text='Rotors')
    str_var_rotor1_choice = tk.StringVar(fr_options)
    str_var_rotor2_choice = tk.StringVar(fr_options)
    str_var_rotor3_choice = tk.StringVar(fr_options)
    str_var_rotor1_choice.set(rotor_names[0])
    str_var_rotor2_choice.set(rotor_names[1])
    str_var_rotor3_choice.set(rotor_names[2])

    om_r1choice = tk.OptionMenu(fr_options, str_var_rotor1_choice, *rotor_names)
    om_r2choice = tk.OptionMenu(fr_options, str_var_rotor2_choice, *rotor_names)
    om_r3choice = tk.OptionMenu(fr_options, str_var_rotor3_choice, *rotor_names)

    # # # placing all of the widgets
    lbl_rotor_choice.grid(row=0, column=0)
    om_r1choice.grid(row=1, column=0)
    om_r2choice.grid(row=2, column=0)
    om_r3choice.grid(row=3, column=0)

    # # rotor starting positions

    # # # creating all of the widgets
    alpha = list(ascii_uppercase)
    lbl_rotor_pos = tk.Label(fr_options, text='Rotor start positions')
    str_var_rotor1_pos = tk.StringVar(fr_options)
    str_var_rotor2_pos = tk.StringVar(fr_options)
    str_var_rotor3_pos = tk.StringVar(fr_options)
    str_var_rotor1_pos.set(alpha[0])
    str_var_rotor2_pos.set(alpha[0])
    str_var_rotor3_pos.set(alpha[0])

    om_r1pos = tk.OptionMenu(fr_options, str_var_rotor1_pos, *alpha)
    om_r2pos = tk.OptionMenu(fr_options, str_var_rotor2_pos, *alpha)
    om_r3pos = tk.OptionMenu(fr_options, str_var_rotor3_pos, *alpha)

    # # # placing all of the widgets
    lbl_rotor_pos.grid(row=0, column=1)
    om_r1pos.grid(column=1, row=1)
    om_r2pos.grid(column=1, row=2)
    om_r3pos.grid(column=1, row=3)

    # # rotor ring settings

    # # # making the widgets
    lbl_rotor_ring = tk.Label(fr_options, text='Rotor ring settings')
    str_var_rotor1_setting = tk.StringVar(fr_options)
    str_var_rotor2_setting = tk.StringVar(fr_options)
    str_var_rotor3_setting = tk.StringVar(fr_options)
    str_var_rotor1_setting.set(alpha[0])
    str_var_rotor2_setting.set(alpha[0])
    str_var_rotor3_setting.set(alpha[0])

    om_r1setting = tk.OptionMenu(fr_options, str_var_rotor1_setting, *alpha)
    om_r2setting = tk.OptionMenu(fr_options, str_var_rotor2_setting, *alpha)
    om_r3setting = tk.OptionMenu(fr_options, str_var_rotor3_setting, *alpha)

    # # # placing the widgets
    lbl_rotor_ring.grid(row=0, column=2)
    om_r1setting.grid(row=1, column=2)
    om_r2setting.grid(row=2, column=2)
    om_r3setting.grid(row=3, column=2)

    # reflector

    # # # making the reflector widgets
    lbl_reflector_choice = tk.Label(fr_options, text='Reflector')
    str_var_reflector_choice = tk.StringVar(fr_options)
    str_var_reflector_choice.set(reflector_names[0])
    om_rfchoice = tk.OptionMenu(fr_options, str_var_reflector_choice, *reflector_names)

    # # placing the reflector widgets
    lbl_reflector_choice.grid(row=4, column=1)
    om_rfchoice.grid(row=5, column=1)

    # plugboard

    # # creating widgets
    lbl_plug = tk.Label(fr_options, text='Plugboard')
    btn_plug = tk.Button(fr_options, text='Edit Plugboard', command=plugboard_editor)

    # # placing widgets
    lbl_plug.grid(row=6, column=1)
    btn_plug.grid(row=7, column=1)

    # Apply changes
    btn_apply = tk.Button(fr_options, text='Apply changes', command=on_modification)
    btn_apply.grid(row=8,column=1)

    # final placements
    txt_input.grid(row=0, column=0, sticky='nsew')
    fr_options.grid(row=0, column=1, sticky='ns')
    txt_output.grid(row=0, column=2, sticky='nsew')

    win_main.mainloop()
