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
        glyph_path = f'{path}Glyphs\\{folder}\\Glyph ({glyph_names.index(glyph_name)+1}).jpg'
        if os.path.isfile(glyph_path):
            glyphs[glyph_name] = glyph_path
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

    PEG_GLYPHS_LIST = ['Subdio', 'Earth', 'Acejesis', 'Lenchan', 'Alura',
                       'Ca Po', 'Laynox', 'Ecrumig', 'Avoniv', 'Bydo',
                       'Aaxel', 'Aldeni', 'Setas', 'Arami', 'Danami',
                       'Robandus', 'Recktic', 'Zamilloz', 'Dawnre', 'Salma',
                       'Hamlinto', 'Elenami', 'Tahnan', 'Zeo', 'Roehi',
                       'Once El', 'Sandovi', 'Illume', 'Amiwill', 'Sibbron',
                       'Gillitin', 'Ramnon', 'Olavii', 'Hacemill', 'Poco Re',
                       'Abrin']

    UNI_GLYPHS_LIST = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                       17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
                       31, 32, 33, 34, 35, 36]

    GLYPH_TYPES = {'MW': MW_GLYPHS_LIST, 'PEG': PEG_GLYPHS_LIST, 'UNI': UNI_GLYPHS_LIST}

    for folder, glyph_type in GLYPH_TYPES.items():
        success, failed = load_glyphs(file_location, folder, glyph_type)
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
