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
    failed_to_load = []

    for glyph_name in glyph_names:
        glyph_id = glyph_names.index(glyph_name)
        # glyph_path = f'{path}Glyphs\{folder}\Glyph ({glyph_id}).png'
        glyph_path = f'{path}Glyphs\{folder}\{glyph_name}.png'
        if os.path.isfile(glyph_path):
            image = Image.open(glyph_path)
            image = image.resize((300, 300), Image.ANTIALIAS)
            # gui.PhotoImage(file=glyph_path)
            glyphs[glyph_name] = ImageTk.PhotoImage(image)
        else:
            failed_to_load.append(glyph_name)
    return glyphs, failed_to_load


def output_generator(book_to_output, books, out_path):
    book_items = []
    for item in books[book_to_output]:
        book_item = f"""
name={book_to_output}
mw
glyph1={item['mw']['glyph1']}
glyph2={item['mw']['glyph2']}
glyph3={item['mw']['glyph3']}
glyph4={item['mw']['glyph4']}
glyph5={item['mw']['glyph5']}
glyph6={item['mw']['glyph6']}
glyph7={item['mw']['glyph7']}
glyph8={item['mw']['glyph8']}
peg
glyph1={item['peg']['glyph1']}
glyph2={item['peg']['glyph2']}
glyph3={item['peg']['glyph3']}
glyph4={item['peg']['glyph4']}
glyph5={item['peg']['glyph5']}
glyph6={item['peg']['glyph6']}
glyph7={item['peg']['glyph7']}
glyph8={item['peg']['glyph8']}
uni
glyph1={item['uni']['glyph1']}
glyph2={item['uni']['glyph2']}
glyph3={item['uni']['glyph3']}
glyph4={item['uni']['glyph4']}
glyph5={item['uni']['glyph5']}
glyph6={item['uni']['glyph6']}
glyph7={item['uni']['glyph7']}
glyph8={item['uni']['glyph8']}"""
        book_items.append(book_item)


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
                       'Poco Re', 'Abrin', 'Earth']

    UNI_GLYPHS_LIST = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'g9',
                       'g10', 'g11', 'g12', 'g13', 'g14', 'g15', 'g16', 'g17',
                       'g18', 'g19', 'g20', 'g21', 'g22', 'g23', 'g24', 'g25',
                       'g26', 'g27', 'g28', 'g29', 'g30', 'g31', 'g32', 'g33',
                       'g34', 'g35', 'g36']

    GLYPH_TYPES = {'MW': MW_GLYPHS_LIST,
                   'PEG': PEG_GLYPHS_LIST,
                   'UNI': UNI_GLYPHS_LIST}

    global loaded_glyphs
    loaded_glyphs = {}

    for folder, glyph_type in GLYPH_TYPES.items():
        success, failed = load_glyphs(file_location, folder, glyph_type)
        print(f"""{len(success)} glyphs were succesfully loaded
{len(failed)} glyphs failed to load
glyphs that failed to load:\n{failed}""")
        loaded_glyphs[folder] = success

    global loaded_books
    loaded_books = {}

    global none_image
    image = Image.open(f'{file_location}Glyphs\\none.png')
    image = image.resize((300, 300), Image.ANTIALIAS)
    none_image = ImageTk.PhotoImage(image)
    current_displayed_glyphs = {'glyph1': 'none', 'glyph2': 'none',
                                'glyph3': 'none', 'glyph4': 'none',
                                'glyph5': 'none', 'glyph6': 'none',
                                'glyph7': 'none', 'glyph8': 'none'}

    def load_book():
        book_path = filedialog.askopenfilename(
            filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if os.path.isfile(book_path):
            book_file = open(book_path, 'r')
            book_content = book_file.readlines()
            # Book file interperter
            address_name = ''
            glyph_type = ''
            book_items = {}

            for line in book_content:
                if 'name=' in line:
                    address_name = line.split('=')[1].strip()
                    book_items[address_name] = {}
                elif 'mw' in line:
                    glyph_type = 'mw'
                    book_items[address_name][glyph_type] = {}
                elif line == 'peg\n':
                    glyph_type = 'peg'
                    book_items[address_name][glyph_type] = {}
                elif line == 'uni\n':
                    glyph_type = 'uni'
                    book_items[address_name][glyph_type] = {}
                elif 'glyph' in line:
                    glyph_num, glyph_name = line.strip().split('=')
                    book_items[
                        address_name][glyph_type][glyph_num] = glyph_name
            book_path_order = book_path.split('/')
            book_name = book_path_order[-1]
            book_name_textvar.set(f'Book Name: {book_name}')
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
    add_book_button.pack()

    book_name_textvar = gui.StringVar(root, 'Book Name: ')

    def book_menu_update():
        Book_menu = gui.Menu(Book_menu_button, tearoff=0)
        Book_menu_button['menu'] = Book_menu
        for book in loaded_books:
            Book_menu.add_radiobutton(label=book, variable=selected_book)

    selected_book = gui.StringVar()
    Book_menu_button = gui.Menubutton(root, text='Books', bd=1)
    Book_menu = gui.Menu(Book_menu_button, tearoff=0)
    Book_menu_button['menu'] = Book_menu
    Book_menu_button.pack()
    selected_book_label = gui.Label(root, textvariable=selected_book)
    selected_book_label.pack()

    def address_menu_update(x, y, z):
        addresses_menu = gui.Menu(addresses_menu_button, tearoff=0)
        addresses_menu_button['menu'] = addresses_menu
        for address in loaded_books[gui.StringVar.get(selected_book)]:
            addresses_menu.add_radiobutton(label=address,
                                           variable=selected_address)
    selected_book.trace_add('write', address_menu_update)

    def change_displayed(x, y, z):
        selected_type = gui.StringVar.get(address_type_selected).lower()
        new_glyphs = []
        book = gui.StringVar.get(selected_book)
        adderss_name = gui.StringVar.get(selected_address)

        new_glyphs = loaded_books[book][adderss_name][selected_type]
        current_displayed_glyphs = new_glyphs
        update_display(current_displayed_glyphs)

    selected_address = gui.StringVar()
    selected_address.trace_add('write', change_displayed)
    addresses_menu_button = gui.Menubutton(root, text='Addresses', bd=1)
    addresses_menu = gui.Menu(addresses_menu_button, tearoff=0)
    addresses_menu_button['menu'] = addresses_menu
    addresses_menu_button.pack()
    selected_address_Label = gui.Label(root, textvariable=selected_address)
    selected_address_Label.pack()

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

    global displays
    displays = {}
    global stringvars
    stringvars = {}
    for num in current_displayed_glyphs.keys():
        stringvars[num] = gui.StringVar(display_window, 'none')
        displays[num] = (gui.Button(display_window),
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
                displays[id][0].configure(image=loaded_glyphs[gui.StringVar.get(address_type_selected)][glyph])
            except:
                stringvars[id].set('none')
                displays[id][0].configure(image=none_image)

setup()
root.mainloop()
