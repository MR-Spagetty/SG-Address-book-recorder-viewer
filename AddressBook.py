##
# AddressBook.py

import os
import sys
if sys.version_info < (3, 10):
    raise Exception('to run this programe you are required to use python 3.10\
or greater')
try:
    import tkinter as gui
    import tkinter.filedialog as filedialog
except ImportError:
    raise ImportError('to run this program you need the tkinter module')

try:
    from PIL import ImageTk, Image
except ImportError:
    raise ImportError('to run this program you need the PIL module')

try:
    import json
except ImportError:
    raise ImportError('to run this program you need the json module')

try:
    import re
except ImportError:
    raise ImportError('to run this program you need the re module')


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

file_location = os.path.dirname(os.path.abspath(__file__))
print(file_location)


def load_config():
    default_configs = """{
# when edited you must releanch hte program if it is running
"images": {
    # the width and height of the glyphs
    # used in the edit window
    "small glyph size px": 100,

    # the width and height of the glyphs
    # used in the display window
    "large glyph size px": 300
    }
}"""
    global application_path
    if not os.path.isfile(os.path.join(application_path, 'AddresssBook.cfg')):
        with open(os.path.join(application_path,
                               'AddresssBook.cfg'), 'w') as config_file:
            config_file.write(default_configs)
    with open(os.path.join(application_path,
                           'AddresssBook.cfg'), 'r') as config_file:
        global configs
        config = config_file.read()
        config = ''.join(re.sub("#.*", "", config, flags=re.MULTILINE).split())
        configs = json.loads(config)


def load_glyphs(path, folder, glyph_names):
    """Loads a seris of glyphs and returns a
    <large glyph sizedefined in config>px^2 and a
    <small glyph sizedefined in config>px^2
    version aswell as a list of those that failed to load

    Args:
        path (str): path to use
        folder (str): folder images are contained in
        glyph_names (list): a list of glyph names to load

    Returns:
        dict: dictionary of image objects using glyph names as keys
        dict: smol version of previous
        list: list of glyph names that failed to load
    """
    global configs
    glyphs = {}
    smol_glyphs = {}
    failed_to_load = []
    smol_size_px = configs['images']['smallglyphsizepx']
    large_size_px = configs['images']['largeglyphsizepx']

    for glyph_name in glyph_names:
        glyph_path = os.path.join(path, 'Glyphs', folder, f'{glyph_name}.png')
        if os.path.isfile(glyph_path):
            image = Image.open(glyph_path)
            image = image.resize((large_size_px, large_size_px),
                                 Image.ANTIALIAS)
            smol_image = image.resize((smol_size_px, smol_size_px),
                                      Image.ANTIALIAS)
            glyphs[glyph_name] = ImageTk.PhotoImage(image)
            smol_glyphs[glyph_name] = ImageTk.PhotoImage(smol_image)
        else:
            failed_to_load.append(glyph_name)
    return glyphs, smol_glyphs, failed_to_load


def setup():
    """sets up the GUI for the program
    """
    global configs

    def disable_event():
        pass

    global file_location

    global root
    root = gui.Tk()
    root.title('Address book')

    MW_GLYPHS_LIST = ['Crater', 'Virgo', 'Bootes', 'Centaurus', 'Libra',
                      'Serpens Caput', 'Norma', 'Scorpius',
                      'Corona Australis', 'Scutum', 'Sagittarius', 'Aquila',
                      'Microscopium', 'Capricornus', 'Piscis Austrinus',
                      'Equuleus', 'Aquarius', 'Pegasus', 'Sculptor', 'Pisces',
                      'Andromeda', 'Triangulum', 'Aries', 'Perseus', 'Cetus',
                      'Taurus', 'Auriga', 'Eridanus', 'Orion', 'Canis Minor',
                      'Monoceros', 'Gemini', 'Hydra', 'Lynx', 'Cancer',
                      'Sextans', 'Leo Minor', 'Leo']

    PEG_GLYPHS_LIST = ['Acjesis', 'Lenchan', 'Alura',
                       'Ca Po', 'Laylox', 'Ecrumig', 'Avoniv', 'Bydo',
                       'Aaxel', 'Aldeni', 'Setas', 'Arami', 'Danami',
                       'Robandus', 'Recktic', 'Zamilloz', 'Subido', 'Dawnre',
                       'Salma', 'Hamlinto', 'Elenami', 'Tahnan', 'Zeo',
                       'Roehi', 'Once El', 'Sandovi', 'Illume', 'Amiwill',
                       'Sibbron', 'Gilltin', 'Ramnon', 'Olavii', 'Hacemill',
                       'Poco Re', 'Abrin', 'Baselai']

    UNI_GLYPHS_LIST = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9',
                       'g10', 'g11', 'g12', 'g13', 'g14', 'g15', 'g16', 'g17',
                       'g18', 'g19', 'g20', 'g21', 'g22', 'g23', 'g24', 'g25',
                       'g26', 'g27', 'g28', 'g29', 'g30', 'g31', 'g32', 'g33',
                       'g34', 'g35', 'g36']

    global GLYPH_TYPES
    GLYPH_TYPES = {'MW': MW_GLYPHS_LIST,
                   'PEG': PEG_GLYPHS_LIST,
                   'UNI': UNI_GLYPHS_LIST}

    global loaded_glyphs
    loaded_glyphs = {}
    global smol_loaded_glyphs
    smol_loaded_glyphs = {}

    for folder, glyph_type in GLYPH_TYPES.items():
        normal, smol, failed = load_glyphs(file_location, folder, glyph_type)
        if not getattr(sys, 'frozen', False):
            print(f"""{len(normal)} glyphs were succesfully loaded
{len(failed)} glyphs failed to load
glyphs that failed to load:\n{failed}""")
        loaded_glyphs[folder] = normal
        smol_loaded_glyphs[folder] = smol

    global loaded_books
    loaded_books = {}

    global none_image
    global smol_none_image
    image = Image.open(os.path.join(file_location, 'Glyphs', 'none.png'))
    image = image.resize((configs['images']['largeglyphsizepx'],
                          configs['images']['largeglyphsizepx']),
                         Image.ANTIALIAS)
    none_image = ImageTk.PhotoImage(image)
    smol_image = image.resize((configs['images']['smallglyphsizepx'],
                               configs['images']['smallglyphsizepx']),
                              Image.ANTIALIAS)
    smol_none_image = ImageTk.PhotoImage(smol_image)

    global current_displayed_glyphs
    current_displayed_glyphs = {'glyph1': 'none', 'glyph2': 'none',
                                'glyph3': 'none', 'glyph4': 'none',
                                'glyph5': 'none', 'glyph6': 'none',
                                'glyph7': 'none', 'glyph8': 'none'}

    def load_book():
        book_path = filedialog.askopenfilename(
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        book_name = os.path.split(book_path)[-1]
        if os.path.isfile(book_path):
            with open(book_path, 'r') as book_file:
                book = json.load(book_file)
            book_items = {}
            for name, entry in book.items():
                book_items[name] = {}
                for address_type, address in entry.items():
                    book_items[name][address_type] = {}
                    if type(address) is dict:
                        for item, value in address.items():
                            book_items[name][address_type][item] = value
                    else:
                        book_items[name][address_type] = address
                if 'IDC' not in entry:
                    book_items[name]['IDC'] = ''
            return 'successfull', book_items, book_name
        else:
            book_name_textvar.set('Book Name: ')
            return 'failed - file not exist', [], None

    def add_book():
        status, items, name = load_book()
        global loaded_books
        if status == 'successfull':
            loaded_books[name] = items
        book_menu_update()
    add_book_button = gui.Button(
        root, command=add_book, background='white', text='Load',
        font=('Sans Serif', 12), fg='black')
    add_book_button.grid(row=0, column=0)

    book_name_textvar = gui.StringVar(root, 'Book Name: ')

    def book_menu_update():
        Book_menu = gui.Menu(Book_menu_button, tearoff=0)
        Book_menu_button['menu'] = Book_menu
        for book in loaded_books:
            Book_menu.add_radiobutton(label=book, variable=selected_book)

    new_item_window = gui.Toplevel(root)
    new_item_window.withdraw()
    new_item_window.protocol("WM_DELETE_WINDOW", disable_event)

    def new_book():

        new_item_window.title('New book')

        book_name = gui.StringVar(new_item_window)
        book_name_entry = gui.Entry(new_item_window, textvariable=book_name)
        book_name_entry.grid(row=0, column=0)

        def finish():
            global loaded_books
            new_item_window.withdraw()
            loaded_books[gui.StringVar.get(book_name)] = {}
            book_menu_update()
            for child in new_item_window.winfo_children():
                child.destroy()

        done_button = gui.Button(new_item_window, text='Done', command=finish)
        done_button.grid(row=0, column=1)

        new_item_window.deiconify()

    selected_book = gui.StringVar()
    Book_menu_button = gui.Menubutton(root, text='Books', bd=1)
    Book_menu = gui.Menu(Book_menu_button, tearoff=0)
    Book_menu_button['menu'] = Book_menu
    Book_menu_button.grid(row=1, column=0)
    selected_book_label = gui.Label(root, textvariable=selected_book)
    selected_book_label.grid(row=1, column=1)
    new_book_button = gui.Button(root, text='New book', command=new_book)
    new_book_button.grid(row=1, column=2)

    def save_book():
        book_path = filedialog.asksaveasfilename(
            filetypes=(('JSON files', '*.json'), ('All files', '*.*'))
        )
        entries = loaded_books[gui.StringVar.get(selected_book)]
        data_to_write = {
            entry_name: dict(entry) for entry_name, entry in entries.items()
        }

        if not book_path.endswith('.json'):
            book_path = f'{book_path}.json'
        with open(book_path, 'w') as book_file:
            json.dump(data_to_write, book_file, indent=4)
        return 'succesfull', book_path

    save_button = gui.Button(root, text='Save', command=save_book)
    save_button.grid(row=0, column=1)

    def import_address():
        address_path = filedialog.askopenfilename(
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        address_name = os.path.split(address_path)[-1][:-5]
        if os.path.isfile(address_path):
            with open(address_path, 'r') as address_file:
                address = json.load(address_file)
            if 'IDC' not in address:
                address['IDC'] = ''
            global loaded_books
            loaded_books[selected_book.get()][address_name] = address
            address_menu_update(1, 2, 3)

    def export_address():
        address_path = filedialog.asksaveasfilename(
            filetypes=(('JSON files', '*.json'), ('All files', '*.*'))
        )

        data_to_write = loaded_books[selected_book.get()][
            selected_address.get()]

        if not address_path.endswith('.json'):
            book_path = f'{address_path}.json'
        with open(book_path, 'w') as book_file:
            json.dump(data_to_write, book_file, indent=4)
        return 'succesfull', book_path

    address_export_button = gui.Button(root, text="Export address",
                                       command=export_address, state='disabled'
                                       )
    address_import_button = gui.Button(root, text="Import address",
                                       command=import_address, state='disabled'
                                       )
    address_import_button.grid(row=3, column=0)
    address_export_button.grid(row=3, column=2)

    def address_menu_update(x, y, z):
        if selected_book.get():
            address_import_button.configure(state='normal')
        else:
            address_import_button.configure(state='disabled')
        addresses_menu = gui.Menu(addresses_menu_button, tearoff=0)
        addresses_menu_button['menu'] = addresses_menu
        for address in loaded_books[gui.StringVar.get(selected_book)]:
            addresses_menu.add_radiobutton(label=address,
                                           variable=selected_address)
        selected_address.set('')
        change_displayed(1, 2, 3)
    selected_book.trace_add('write', address_menu_update)

    def change_displayed(x, y, z):
        if selected_address.get():
            address_export_button.configure(state='normal')
        else:
            address_export_button.configure(state='disabled')
        global current_displayed_glyphs
        selected_type = gui.StringVar.get(address_type_selected).lower()
        new_glyphs = []
        book = gui.StringVar.get(selected_book)
        address_name = gui.StringVar.get(selected_address)
        try:
            new_glyphs = loaded_books[book][address_name][selected_type]
            current_displayed_glyphs = new_glyphs
            idc.set(loaded_books[book][address_name]['IDC'])
            update_display(current_displayed_glyphs)
        except KeyError:
            pass

    def new_address():
        TEMPLATE = {
            "mw": {
                "glyph1": "none",
                "glyph2": "none",
                "glyph3": "none",
                "glyph4": "none",
                "glyph5": "none",
                "glyph6": "none",
                "glyph7": "none",
                "glyph8": "none"
            },
            "peg": {
                "glyph1": "none",
                "glyph2": "none",
                "glyph3": "none",
                "glyph4": "none",
                "glyph5": "none",
                "glyph6": "none",
                "glyph7": "none",
                "glyph8": "none"
            },
            "uni": {
                "glyph1": "none",
                "glyph2": "none",
                "glyph3": "none",
                "glyph4": "none",
                "glyph5": "none",
                "glyph6": "none",
                "glyph7": "none",
                "glyph8": "none"
            },
            'IDC': ''
        }
        new_item_window.title('New address')

        address_name = gui.StringVar(new_item_window)
        address_name_entry = gui.Entry(new_item_window,
                                       textvariable=address_name)
        address_name_entry.grid(row=0, column=0)

        def finish():
            global loaded_books
            new_item_window.withdraw()
            loaded_books[
                gui.StringVar.get(selected_book)
                ][
                    gui.StringVar.get(address_name)] = dict(TEMPLATE)
            address_menu_update('a', 'b', 'c')
            for child in new_item_window.winfo_children():
                child.destroy()

        done_button = gui.Button(new_item_window, text='Done', command=finish)
        done_button.grid(row=0, column=1)

        new_item_window.deiconify()

    selected_address = gui.StringVar()
    selected_address.trace_add('write', change_displayed)
    addresses_menu_button = gui.Menubutton(root, text='Addresses', bd=1)
    addresses_menu = gui.Menu(addresses_menu_button, tearoff=0)
    addresses_menu_button['menu'] = addresses_menu
    addresses_menu_button.grid(row=2, column=0)
    selected_address_Label = gui.Label(root, textvariable=selected_address)
    selected_address_Label.grid(row=2, column=1)
    new_address_button = gui.Button(root, text='New address',
                                    command=new_address)
    new_address_button.grid(row=2, column=2)

    display_window = gui.Toplevel(root)
    display_window.title('address display')
    display_window.protocol("WM_DELETE_WINDOW", disable_event)

    address_type_selected = gui.StringVar(display_window)
    address_type_spin = gui.Spinbox(display_window,
                                    values=list(GLYPH_TYPES.keys()),
                                    textvariable=address_type_selected)
    address_type_spin.grid(column=0, row=0, columnspan=3)
    address_type_selected.trace_add('write', change_displayed)

    display_locations = {'glyph1': (0, 1), 'glyph2': (1, 1),
                         'glyph3': (2, 1), 'glyph4': (0, 3),
                         'glyph5': (1, 3), 'glyph6': (2, 3),
                         'glyph7': (0, 5), 'glyph8': (2, 5)}

    edit_window = gui.Toplevel(display_window)
    edit_window.withdraw()

    def change_glyph_logic(id, glyph_name='none'):
        global current_displayed_glyphs
        current_displayed_glyphs[id] = glyph_name
        update_display(current_displayed_glyphs)
        finish_edit()

    def change_glyph(id):
        edit_window.title(f'editing {id}')
        global GLYPH_TYPES
        edit_window.deiconify()
        global current_displayed_glyphs
        test_button = gui.Button(edit_window, command=finish_edit)
        test_button.grid()
        selected_type = gui.StringVar.get(address_type_selected)
        buttons = {
            glyph: gui.Button(
                edit_window,
                image=smol_loaded_glyphs[selected_type][glyph],
                command=lambda glyph_name=glyph: change_glyph_logic(
                    id, glyph_name
                ),
                background='magenta2',
            )
            for glyph in GLYPH_TYPES[selected_type]
        }

        for glyph_name, button in buttons.items():
            row, column = divmod(
                GLYPH_TYPES[selected_type].index(glyph_name), 6)
            button.grid(row=row, column=column)
        global smol_none_image
        none_button = gui.Button(edit_window, image=smol_none_image,
                                 background='magenta2',
                                 command=lambda: change_glyph_logic(id))
        if column == 5:
            row += 1
            column = 0
        else:
            column += 1
        none_button.grid(row=row, column=column)

        glyph_to_select = gui.StringVar(edit_window)
        glyph_name_entry = gui.Entry(
            edit_window, textvariable=glyph_to_select, bg="magenta2",
            width=2 * int(divmod(configs['images']['smallglyphsizepx'], 7)[0]))
        glyph_name_entry.grid(row=(row + 1), column=0, columnspan=2)

        glyph_name_entry_submit = gui.Button(
            edit_window, text="→",
            command=lambda: change_glyph_logic(
                id, gui.StringVar.get(glyph_to_select).title()),
            background="red", state="disabled")

        global glyph_valid
        glyph_valid = False

        def submit_via_enter(_):
            global glyph_valid
            if glyph_valid:
                change_glyph_logic(id,
                                   gui.StringVar.get(glyph_to_select).title())

        glyph_name_entry.bind("<Return>", submit_via_enter)

        def update_submit_button(glyph_name, button):
            global glyph_valid
            if glyph_name.title() in GLYPH_TYPES[selected_type]:
                glyph_valid = True
                button.configure(background="green2", state="normal")
            else:
                glyph_valid = False
                button.configure(background="red", state="disabled")

        glyph_to_select.trace_add(
            'write', lambda x, y, z: update_submit_button(
                gui.StringVar.get(glyph_to_select), glyph_name_entry_submit))

        glyph_name_entry_submit.grid(row=(row + 1), column=2)

    def finish_edit():
        for child in edit_window.winfo_children():
            child.destroy()
        edit_window.withdraw()

    edit_window.protocol("WM_DELETE_WINDOW", finish_edit)

    global displays
    displays = {}
    global stringvars
    stringvars = {}
    for num in current_displayed_glyphs.keys():
        stringvars[num] = gui.StringVar(display_window, 'none')
        displays[num] = (gui.Button(display_window, background="royal blue2",
                                    command=lambda id=num: change_glyph(id)),
                         gui.Label(display_window,
                                   textvariable=stringvars[num]))
    for id, display in displays.items():
        colume, row = display_locations[id]
        display[0].grid(column=colume, row=row)
        display[1].grid(column=colume, row=row + 1)

    def update_display(glyphs):
        global stringvars
        global displays
        global loaded_glyphs
        global none_image
        for id, glyph in glyphs.items():
            try:
                stringvars[id].set(glyph)
                displays[id][0].configure(
                    image=loaded_glyphs[gui.StringVar.get(
                        address_type_selected)][glyph])
            except KeyError:
                stringvars[id].set('none')
                displays[id][0].configure(image=none_image)
    update_display(current_displayed_glyphs)

    IDC_window = gui.Toplevel(display_window)
    IDC_window.title('IDC')
    IDC_window.protocol("WM_DELETE_WINDOW", disable_event)

    def edit_entry_idc():
        global loaded_books
        book = selected_book.get()
        address_name = selected_address.get()
        try:
            loaded_books[book][address_name]['IDC'] = idc.get()
        except KeyError:
            pass

    global idc
    idc = gui.StringVar(IDC_window)
    IDC_entry = gui.Entry(IDC_window, textvariable=idc,
                          width=3 * int(divmod(configs['images'][
                              'smallglyphsizepx'], 7)[0]),
                          state='readonly')
    IDC_entry.grid(row=0, column=0, columnspan=3)
    idc.trace_add('write', lambda x, y, z: edit_entry_idc())

    def IDC_button_logic(button_id):
        if type(button_id) is int:
            if len(idc.get()) < 9:
                idc.set(f'{idc.get()}{button_id}')
        else:
            match button_id:
                case '<':
                    if len(idc.get()) > 1:
                        idc.set(idc.get()[0:-1])
                    else:
                        idc.set('')
                case 'c':
                    idc.set('')

    button_order = {7: (0, 1), 8: (1, 1), 9: (2, 1),
                    4: (0, 2), 5: (1, 2), 6: (2, 2),
                    1: (0, 3), 2: (1, 3), 3: (2, 3),
                    '<': (0, 4), 0: (1, 4), 'c': (2, 4)}
    IDC_buttons = {}
    for button_id, coordinates in button_order.items():
        IDC_buttons[button_id] = gui.Button(
            IDC_window, text=button_id,
            command=lambda id=button_id: IDC_button_logic(id),
            font=('Ariel', int(4 * int(divmod(configs['images'][
                'smallglyphsizepx'], 7)[0])))
        ).grid(column=coordinates[0], row=coordinates[1])


if __name__ == '__main__':
    load_config()
    setup()
    root.mainloop()
