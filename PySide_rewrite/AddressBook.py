##
# AddressBook.py

import os
import sys
if sys.version_info < (3, 10):
    raise EnvironmentError(
        'to run this programe you are required to use python 3.10 or greater')
try:
    from PySide6.QtWidgets import (
     QApplication, QMainWindow, QWidget,
     QHBoxLayout, QVBoxLayout, QFormLayout,
     QLabel, QToolBar, QStatusBar, QFileDialog,
     QMenu, QToolButton, QTabWidget, QPushButton
    )
    from PySide6.QtGui import QAction, QIcon, QImage, QPixmap
    from PySide6.QtCore import Qt, QSize
except ImportError as e:
    raise ImportError('to run this program you need the PySide6 module') from e

try:
    import json
except ImportError as err:
    raise ImportError('to run this program you need the json module') from err

try:
    import re
except ImportError as exception:
    raise ImportError(
        'to run this program you need the re module') from exception


if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

file_location = os.path.dirname(os.path.abspath(__file__))
print('file location:', file_location)


def load_config():
    global application_path
    if not os.path.isfile(os.path.join(application_path, 'AddresssBook.cfg')):
        default_configs = """{
# when edited you must relaunch the program if it is running
"app": {
    # Theme of the app one of: ["dark", "light", "custom"]
    "theme": "dark",
    # Custom theme colours
    "custom theme": {
        # for allowed colours see PySide6 Documentation
        "main window background colour": "Dark-Gray",
        "main window menu bar colour": "Gray",
        "displays background colour": "Gray",
        # Glyphs colour is an rgb value
        "glyphs colour": [0, 0, 0],
        "edit displays background colour": "Gray"
    },
    # weather or not to automatically save changes
    "auto save": true,
    # when to automatically save can be one of:
    # ["change-made", "switch-book", "on-close", "switch-or-close"]
    "auto save time": "switch-or-close",
    # Display arrangements (g is the location of a glyph)
    # 1:
    # G G G
    # G G G
    # G   G
    # 2:
    # G G G
    # G G G
    #  G G
    "display arrangement": 1
},
"images": {
    # the width and height of the glyphs
    # used in the edit window
    "small glyph size px": 75,

    # the width and height of the glyphs
    # used in the display window
    "large glyph size px": 200
    }
}"""
        with open(os.path.join(application_path,
                               'AddresssBook.cfg'), 'w') as config_file:
            config_file.write(default_configs)
    with open(os.path.join(application_path,
                           'AddresssBook.cfg'), 'r') as config_file:
        global configs
        config = config_file.read()
        config = ''.join(re.sub("#.*", "", config, flags=re.MULTILINE).split())
        config = re.sub("-", " ", config, flags=re.MULTILINE)
        configs = json.loads(config)
        configs['app']['customtheme']['glyphscolour'] = tuple(
            configs['app']['customtheme']['glyphscolour'])
        print('config:', configs)


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
            glyphs[glyph_name] = QPixmap(glyph_path).scaled(
                large_size_px, large_size_px, Qt.KeepAspectRatio
                )
            smol_glyphs[glyph_name] = QPixmap(glyph_path).scaled(
                smol_size_px, smol_size_px, Qt.KeepAspectRatio
                )
        else:
            failed_to_load.append(glyph_name)
    return glyphs, smol_glyphs, failed_to_load


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Address Book")
        load_config()

        self.loaded_glyphs = {'norm': {}, 'smol': {}}
        self.load_glyphs()
        self.large_glyphs_size = QSize(configs["images"]["largeglyphsizepx"],
                                       configs["images"]["largeglyphsizepx"])
        self.smol_glyphs_size = QSize(configs["images"]["smallglyphsizepx"],
                                      configs["images"]["smallglyphsizepx"])

        self.loaded_books = {}
        self.books_path_list = {}
        self.inform_selected_book = QLabel("None")
        self.selected_book = ""
        self.inform_selected_address = QLabel("None")
        self.selected_address = ""

        self.address_displays = {}

        toolbar = self.menuBar()

        load_book = QAction("Load Book", self)
        load_book.setStatusTip("Loads an address book")
        load_book.triggered.connect(self.onLoadBookClick)
        toolbar.addAction(load_book)

        save_book = QAction("Save Book", self)
        save_book.setStatusTip("Saves an address book")
        save_book.triggered.connect(self.onSaveBookClick)
        toolbar.addAction(save_book)

        self.books_menu = toolbar.addMenu("&Books")
        self.books_menu.addAction('There are no books Loaded')

        self.address_menu = toolbar.addMenu("&Address")
        self.address_menu.addAction('Please Select a book')

        self.generate_layout()

    def save(self, book_name):
        unknown_path = False
        try:
            book_path = self.books_path_list[book_name]
        except KeyError:
            unknown_path = True
        if unknown_path or not os.path.isfile(book_path):
            book_path = QFileDialog.getSaveFileName(
                self, "Save Book File", application_path, "JSON files (*.json)"
            )[0]
        entries = self.loaded_books[self.selected_book]
        data_to_write = {
            entry_name: dict(entry) for entry_name, entry in entries.items()
        }
        with open(book_path, 'w') as book_file:
            json.dump(data_to_write, book_file, indent=4)
        self.books_path_list[self.selected_book] = book_path

    def auto_save(self, source):
        if configs['app']['autosave']:
            if source == 'on close' and\
                    configs['app']['autosavetime'] == 'on close':
                for book_name in self.loaded_books:
                    self.save(book_name)
            elif source == configs['app']['autosavetime']:
                self.save(self.selected_book)
            elif configs['app']['autosavetime'] == "switch or close" and\
                    source in ["on close", 'switch book']:
                if source == 'on close':
                    for book_name in self.loaded_books:
                        self.save(book_name)
                else:
                    self.save(self.selected_book)

    def exit_handler(self, *args):
        self.auto_save("on close")
        return args[0]

    def load_glyphs(self):
        MW_GLYPHS_LIST = ['Crater', 'Virgo', 'Bootes', 'Centaurus', 'Libra',
                          'Serpens Caput', 'Norma', 'Scorpius',
                          'Corona Australis', 'Scutum', 'Sagittarius',
                          'Aquila', 'Microscopium', 'Capricornus',
                          'Piscis Austrinus', 'Equuleus', 'Aquarius',
                          'Pegasus', 'Sculptor', 'Pisces', 'Andromeda',
                          'Triangulum', 'Aries', 'Perseus', 'Cetus', 'Taurus',
                          'Auriga', 'Eridanus', 'Orion', 'Canis Minor',
                          'Monoceros', 'Gemini', 'Hydra', 'Lynx', 'Cancer',
                          'Sextans', 'Leo Minor', 'Leo']

        PEG_GLYPHS_LIST = ['Acjesis', 'Lenchan', 'Alura',
                           'Ca Po', 'Laylox', 'Ecrumig', 'Avoniv', 'Bydo',
                           'Aaxel', 'Aldeni', 'Setas', 'Arami', 'Danami',
                           'Robandus', 'Recktic', 'Zamilloz', 'Subido',
                           'Dawnre', 'Salma', 'Hamlinto', 'Elenami', 'Tahnan',
                           'Zeo', 'Roehi', 'Once El', 'Sandovi', 'Illume',
                           'Amiwill', 'Sibbron', 'Gilltin', 'Ramnon',
                           'Olavii', 'Hacemill', 'Poco Re', 'Abrin', 'Baselai']

        UNI_GLYPHS_LIST = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8',
                           'g9', 'g10', 'g11', 'g12', 'g13', 'g14', 'g15',
                           'g16', 'g17', 'g18', 'g19', 'g20', 'g21', 'g22',
                           'g23', 'g24', 'g25', 'g26', 'g27', 'g28', 'g29',
                           'g30', 'g31', 'g32', 'g33', 'g34', 'g35', 'g36']

        global GLYPH_TYPES
        GLYPH_TYPES = {'MW': MW_GLYPHS_LIST,
                       'PEG': PEG_GLYPHS_LIST,
                       'UNI': UNI_GLYPHS_LIST}

        for folder, glyph_type in GLYPH_TYPES.items():
            normal, smol, failed = load_glyphs(file_location, folder,
                                               glyph_type)
            if not getattr(sys, 'frozen', False):
                print(f"""{len(normal)} glyphs were succesfully loaded
{len(failed)} glyphs failed to load
glyphs that failed to load:\n{failed}""")
            self.loaded_glyphs['norm'][folder] = normal
            self.loaded_glyphs['smol'][folder] = smol

    def generate_layout(self):
        general_layout = QHBoxLayout()

        self.setCentralWidget(QWidget())
        self.centralWidget().setLayout(general_layout)

        information_layout = QFormLayout()
        information_widget = QWidget()
        information_widget.setLayout(information_layout)
        general_layout.addWidget(information_widget)
        information_layout.addRow("Selected Book: ", self.inform_selected_book)
        information_layout.addRow("Selected Address: ", self.inform_selected_address)

        address_tabs = QTabWidget()
        mw_address_tab = QWidget()

        self.address_displays['MW'] = [
            QPushButton(), QPushButton(), QPushButton(),
            QPushButton(), QPushButton(), QPushButton(),
            QPushButton(), QPushButton()
        ]

        mw_vbox = QVBoxLayout()
        mw_address_tab.setLayout(mw_vbox)
        mw_row_1 = QHBoxLayout()
        mw_row_1_widget = QWidget()
        mw_row_1_widget.setLayout(mw_row_1)
        mw_vbox.addWidget(mw_row_1_widget)
        mw_row_2 = QHBoxLayout()
        mw_row_2_widget = QWidget()
        mw_row_2_widget.setLayout(mw_row_2)
        mw_vbox.addWidget(mw_row_2_widget)
        mw_row_3 = QHBoxLayout()
        mw_row_3_widget = QWidget()
        mw_row_3_widget.setLayout(mw_row_3)
        mw_vbox.addWidget(mw_row_3_widget)

        mw_row_1.addWidget(self.address_displays['MW'][0])
        mw_row_1.addWidget(self.address_displays['MW'][1])
        mw_row_1.addWidget(self.address_displays['MW'][2])

        mw_row_2.addWidget(self.address_displays['MW'][3])
        mw_row_2.addWidget(self.address_displays['MW'][4])
        mw_row_2.addWidget(self.address_displays['MW'][5])

        mw_row_3.addWidget(self.address_displays['MW'][6])
        if configs['app']['displayarrangement'] == 1:
            mw_row_3.addWidget(QWidget())
        mw_row_3.addWidget(self.address_displays['MW'][7])

        peg_address_tab = QWidget()
        self.address_displays['PEG'] = [
            QPushButton(), QPushButton(), QPushButton(),
            QPushButton(), QPushButton(), QPushButton(),
            QPushButton(), QPushButton()
        ]

        peg_vbox = QVBoxLayout()
        peg_address_tab.setLayout(peg_vbox)
        peg_row_1 = QHBoxLayout()
        peg_row_1_widget = QWidget()
        peg_row_1_widget.setLayout(peg_row_1)
        peg_vbox.addWidget(peg_row_1_widget)
        peg_row_2 = QHBoxLayout()
        peg_row_2_widget = QWidget()
        peg_row_2_widget.setLayout(peg_row_2)
        peg_vbox.addWidget(peg_row_2_widget)
        peg_row_3 = QHBoxLayout()
        peg_row_3_widget = QWidget()
        peg_row_3_widget.setLayout(peg_row_3)
        peg_vbox.addWidget(peg_row_3_widget)
        peg_row_1.addWidget(self.address_displays['PEG'][0])
        peg_row_1.addWidget(self.address_displays['PEG'][1])
        peg_row_1.addWidget(self.address_displays['PEG'][2])
        peg_row_2.addWidget(self.address_displays['PEG'][3])
        peg_row_2.addWidget(self.address_displays['PEG'][4])
        peg_row_2.addWidget(self.address_displays['PEG'][5])
        peg_row_3.addWidget(self.address_displays['PEG'][6])
        if configs['app']['displayarrangement'] == 1:
            peg_row_3.addWidget(QWidget())
        peg_row_3.addWidget(self.address_displays['PEG'][7])

        uni_address_tab = QWidget()
        self.address_displays['UNI'] = [
            QPushButton(), QPushButton(), QPushButton(),
            QPushButton(), QPushButton(), QPushButton(),
            QPushButton(), QPushButton()
        ]

        uni_vbox = QVBoxLayout()
        uni_address_tab.setLayout(uni_vbox)
        uni_row_1 = QHBoxLayout()
        uni_row_1_widget = QWidget()
        uni_row_1_widget.setLayout(uni_row_1)
        uni_vbox.addWidget(uni_row_1_widget)
        uni_row_2 = QHBoxLayout()
        uni_row_2_widget = QWidget()
        uni_row_2_widget.setLayout(uni_row_2)
        uni_vbox.addWidget(uni_row_2_widget)
        uni_row_3 = QHBoxLayout()
        uni_row_3_widget = QWidget()
        uni_row_3_widget.setLayout(uni_row_3)
        uni_vbox.addWidget(uni_row_3_widget)

        uni_row_1.addWidget(self.address_displays['UNI'][0])
        uni_row_1.addWidget(self.address_displays['UNI'][1])
        uni_row_1.addWidget(self.address_displays['UNI'][2])
        uni_row_2.addWidget(self.address_displays['UNI'][3])
        uni_row_2.addWidget(self.address_displays['UNI'][4])
        uni_row_2.addWidget(self.address_displays['UNI'][5])
        uni_row_3.addWidget(self.address_displays['UNI'][6])
        if configs['app']['displayarrangement'] == 1:
            uni_row_3.addWidget(QWidget())
        uni_row_3.addWidget(self.address_displays['UNI'][7])

        address_tabs.addTab(mw_address_tab, 'MW')
        address_tabs.addTab(peg_address_tab, 'PEG')
        address_tabs.addTab(uni_address_tab, 'UNI')

        for add_type in ['MW', 'PEG', 'UNI']:
            for i in range(8):
                self.address_displays[add_type][i].setFixedSize(
                    self.large_glyphs_size)
                self.address_displays[add_type][i].setIconSize(
                    self.large_glyphs_size)

        general_layout.addWidget(address_tabs)

    def onLoadBookClick(self, s):
        book_path = QFileDialog.getOpenFileName(
            self, "Open Book File", application_path, "JSON files (*.json)"
            )[0]
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
            self.books_path_list[book_name] = book_path
            self.update_book_list('successfull', book_items, book_name)
        else:
            self.update_book_list('failed - file not exist', [], None)

    def update_book_list(self, status, book_items, book_name):
        if status != 'successfull':
            return False
        self.loaded_books[book_name] = book_items
        self.books_menu.clear()
        actions = {}
        for book_name in self.loaded_books:
            actions[book_name] = QAction(book_name, self)
            self.books_menu.addAction(actions[book_name])
            s = False  # wierd Qt thing
            actions[book_name].triggered.connect(
                lambda s=s, book_name=book_name:
                    self.update_address_list(book_name)
                )

    def update_address_list(self, book_name):
        if self.selected_book != "":
            self.auto_save("switch book")
        self.selected_book = book_name
        self.inform_selected_book.setText(book_name)
        self.selected_address = ""
        for add_type in ['MW', 'PEG', 'UNI']:
            for i in range(8):
                self.address_displays[add_type][i].setIcon(QIcon())
        self.address_menu.clear()
        actions = {}
        for address_name in self.loaded_books[book_name]:
            actions[address_name] = QAction(address_name, self)
            self.address_menu.addAction(actions[address_name])
            s = False  # wierd Qt thing
            actions[address_name].triggered.connect(
                lambda s=s, address_name=address_name:
                    self.onAddressClick(address_name)
                )

    def onAddressClick(self, address_name):
        self.selected_address = address_name
        self.inform_selected_address.setText(address_name)
        for add_type in ['MW', 'PEG', 'UNI']:
            for i in range(8):
                self.address_displays[add_type][i].setIcon(
                    self.loaded_glyphs['norm'][add_type][
                        self.loaded_books[self.selected_book][address_name][
                            add_type.lower()][f'glyph{i+1}']])

    def onSaveBookClick(self, s):
        book_path = QFileDialog.getSaveFileName(
            self, "Save Book File", application_path, "JSON files (*.json)"
            )[0]
        entries = self.loaded_books[self.selected_book]
        data_to_write = {
            entry_name: dict(entry) for entry_name, entry in entries.items()
        }

        if not book_path.endswith('.json'):
            book_path = f'{book_path}.json'
        with open(book_path, 'w') as book_file:
            json.dump(data_to_write, book_file, indent=4)
        self.books_path_list[self.selected_book] = book_path
        return 'succesfull', book_path


app = QApplication(sys.argv)
w = MainWindow()
w.show()
sys.exit(w.exit_handler(app.exec()))
