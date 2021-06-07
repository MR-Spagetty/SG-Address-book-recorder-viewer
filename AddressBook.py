##
# AddressBook.py

import os
import tkinter as gui
import tkinter.filedialog as filedialog


def load_glyphs(path, folder='MW', glyph_names=[
    'Crater', 'Virgo', 'Bootes', 'Centaurus', 'Libra', 'Serpens Caput',
    'Norma', 'Scorpius', 'Corona Australis', 'Scutum', 'Sagittarius',
    'Aquila', 'Microscopium', 'Capricornus', 'Piscis Austrinus', 'Equuleus',
    'Aquarius', 'Pegasus', 'Sculptor', 'Pisces', 'Andromeda', 'Triangulum',
    'Aries', 'Perseus', 'Cetus', 'Taurus', 'Auriga', 'Eridanus', 'Orion',
    'Canis Minor', 'Monoceros', 'Gemini', 'Hydra', 'Lynx', 'Cancer',
    'Sextans', 'Leo Minor', 'Leo'
]):
    glyphs = {}
    failed_to_load = []

    for glyph_name in glyph_names:
        glyph_path = f'{path}Glyphs\\{folder}\\{glyph_names.index(glyph_name)+1} {glyph_name}.ico'
        if os.path.isfile(glyph_path):
            glyphs[glyph_name] = glyph_path
        else:
            failed_to_load.append(glyph_name)
    return glyphs, failed_to_load


def setup():
    global file_location
    file_location = __file__.replace('AddressBook.py', '')
    file_location.replace(chr(47), '/')  # chr(47) = /
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

    success, failed = load_glyphs(file_location)
    print(f"""{len(success)} glyphs were succesfully loaded
{len(failed)} glyphs failed to load
glyphs that failed to load:\n{failed}""")

    global loaded_books
    loaded_books = {}

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
                    address_name = line.strip('name=').strip()
                    book_items[address_name] = {}
                elif line == 'mw\n':
                    glyph_type = 'mw'
                    book_items[address_name][glyph_type] = {}
                elif line == 'pg\n':
                    glyph_type = 'pg'
                    book_items[address_name][glyph_type] = {}
                elif line == 'un\n':
                    glyph_type = 'un'
                    book_items[address_name][glyph_type] = {}
                elif 'glyph' in line:
                    glyph_num, glyph_name = line.strip().split('=')
                    book_items[address_name][glyph_type][glyph_num] = glyph_name
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

    selected_address = gui.StringVar()
    addresses_menu_button = gui.Menubutton(root, text='Addresses', bd=1)
    addresses_menu = gui.Menu(addresses_menu_button, tearoff=0)
    addresses_menu_button['menu'] = addresses_menu
    addresses_menu_button.pack()
    selected_address_Label = gui.Label(root, textvariable=selected_address)
    selected_address_Label.pack()


setup()
root.mainloop()
