##
# AddressBook.py

import os
import tkinter as gui
import tkinter.filedialog as filedialog
from PIL import ImageTk, Image
import json


class Book:
    pass


class Address:
    pass


def load_glyphs(path, folder, glyph_names):
    glyphs = {}
    smol_glyphs = {}
    failed_to_load = []

    for glyph_name in glyph_names:
        glyph_path = f'{path}Glyphs\{folder}\{glyph_name}.png'
        if os.path.isfile(glyph_path):
            image = Image.open(glyph_path)
            image = image.resize((300, 300), Image.ANTIALIAS)
            smol_image = image.resize((100, 100), Image.ANTIALIAS)
            glyphs[glyph_name] = ImageTk.PhotoImage(image)
            smol_glyphs[glyph_name] = ImageTk.PhotoImage(smol_image)
        else:
            failed_to_load.append(glyph_name)
    return glyphs, smol_glyphs, failed_to_load


def setup():
    global file_location
    file_location = __file__.replace('AddressBook.py', '')
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
        print(f"""{len(normal)} glyphs were succesfully loaded
{len(failed)} glyphs failed to load
glyphs that failed to load:\n{failed}""")
        loaded_glyphs[folder] = normal
        smol_loaded_glyphs[folder] = smol

    global loaded_books
    loaded_books = {}

    global none_image
    global smol_none_image
    image = Image.open(f'{file_location}Glyphs\\none.png')
    image = image.resize((300, 300), Image.ANTIALIAS)
    none_image = ImageTk.PhotoImage(image)
    smol_image = image.resize((100, 100), Image.ANTIALIAS)
    smol_none_image = ImageTk.PhotoImage(smol_image)

    global current_displayed_glyphs
    current_displayed_glyphs = {'glyph1': 'none', 'glyph2': 'none',
                                'glyph3': 'none', 'glyph4': 'none',
                                'glyph5': 'none', 'glyph6': 'none',
                                'glyph7': 'none', 'glyph8': 'none'}

    def load_book():
        book_path = filedialog.askopenfilename(
            filetypes=(("JSON files", "*.json"), ("All files", "*.*")))
        book_name = book_path.split('/')[-1]
        if os.path.isfile(book_path):
            with open(book_path, 'r') as book_file:
                book = json.load(book_file)
            book_items = {}
            for name, entry in book.items():
                book_items[name] = {}
                for address_type, address in entry.items():
                    book_items[name][address_type] = {}
                    for item, value in address.items():
                        book_items[name][address_type][item] = value
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
        root, command=add_book, background='white', text='+',
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
        data_to_write = {}
        for entry_name, entry in entries.items():
            data_to_write[entry_name] = dict(entry)
        if not book_path.endswith('.json'):
            book_path = f'{book_path}.json'
        with open(book_path, 'w') as book_file:
            json.dump(data_to_write, book_file, indent=4)
        if True:
            return 'succesfull', book_path

    save_button = gui.Button(root, text='Save', command=save_book)
    save_button.grid(row=0, column=1)

    def address_menu_update(x, y, z):
        addresses_menu = gui.Menu(addresses_menu_button, tearoff=0)
        addresses_menu_button['menu'] = addresses_menu
        for address in loaded_books[gui.StringVar.get(selected_book)]:
            addresses_menu.add_radiobutton(label=address,
                                           variable=selected_address)
    selected_book.trace_add('write', address_menu_update)

    def change_displayed(x, y, z):
        global current_displayed_glyphs
        selected_type = gui.StringVar.get(address_type_selected).lower()
        new_glyphs = []
        book = gui.StringVar.get(selected_book)
        adderss_name = gui.StringVar.get(selected_address)
        try:
            new_glyphs = loaded_books[book][adderss_name][selected_type]
            current_displayed_glyphs = new_glyphs
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
            }
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
        print(current_displayed_glyphs[id])
        test_button = gui.Button(edit_window, command=finish_edit)
        test_button.grid()
        buttons = {}
        selected_type = gui.StringVar.get(address_type_selected)
        for glyph in GLYPH_TYPES[selected_type]:
            buttons[glyph] = gui.Button(edit_window,
                                        image=smol_loaded_glyphs[
                                            selected_type][glyph],
                                        command=lambda glyph_name=glyph:
                                            change_glyph_logic(id, glyph_name),
                                            background='magenta2')
        for glyph_name, button in buttons.items():
            row, column = divmod(
                GLYPH_TYPES[selected_type].index(glyph_name), 6)
            button.grid(row=row, column=column)
        global smol_none_image
        none_button = gui.Button(edit_window, image=smol_none_image,
                                 background='magenta2',
                                 command=lambda: change_glyph_logic(id))
        if column + 1 == 6:
            row += 1
            column = 0
        else:
            column += 1
        none_button.grid(row=row, column=column)

    def finish_edit():
        for child in edit_window.winfo_children():
            child.destroy()
        edit_window.withdraw()

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
            except:
                stringvars[id].set('none')
                displays[id][0].configure(image=none_image)
    update_display(current_displayed_glyphs)

setup()
root.mainloop()
