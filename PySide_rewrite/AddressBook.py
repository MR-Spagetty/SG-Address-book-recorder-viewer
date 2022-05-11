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
     QMenu, QToolButton, QTabWidget, QPushButton,
     QDialog, QGridLayout, QInputDialog, QLineEdit,
     QCheckBox
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
    NONE_GLYPH_PATH = os.path.join(path, 'Glyphs', 'none.png')
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
    glyphs['none'] = QPixmap(NONE_GLYPH_PATH).scaled(
        large_size_px, large_size_px, Qt.KeepAspectRatio
        )
    smol_glyphs['none'] = QPixmap(NONE_GLYPH_PATH).scaled(
        smol_size_px, smol_size_px, Qt.KeepAspectRatio
        )
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
        self.inform_debug = QLabel("")

        self.glyph_dialogues = {
            'MW': GlyphEditDialog(self, 'MW'),
            'PEG': GlyphEditDialog(self, 'PEG'),
            'UNI': GlyphEditDialog(self, 'UNI')
        }

        self.address_displays = {}

        toolbar = self.menuBar()

        file_menu = toolbar.addMenu("&File")

        self.save_book = QAction("Save Book", self)
        self.save_book.setStatusTip("Saves an address book")
        self.save_book.triggered.connect(self.onSaveBookClick)
        # self.save_book.setDisabled(True)
        file_menu.addAction(self.save_book)

        self.save_book_as = QAction("Save Book As", self)
        self.save_book_as.setStatusTip(
            "Saves an address book to a specified file")
        self.save_book_as.triggered.connect(self.onSaveBookAsClick)
        # self.save_book_as.setDisabled(True)
        file_menu.addAction(self.save_book_as)

        load_book = QAction("Load Book", self)
        load_book.setStatusTip("Loads an address book")
        load_book.triggered.connect(self.onLoadBookClick)
        file_menu.addAction(load_book)

        file_menu.addSeparator()

        new_book = QAction("New Book", self)
        new_book.setStatusTip("Creates a new address book in the program")
        new_book.triggered.connect(self.onNewBookClick)
        file_menu.addAction(new_book)

        self.new_address = QAction("New Address", self)
        self.new_address.setStatusTip(
            "Creates a new address in the current book")
        self.new_address.triggered.connect(self.onNewAddressClick)
        # self.new_address.setDisabled(True)
        file_menu.addAction(self.new_address)

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
        return self.save_book_to_file(book_path)

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
        information_layout.addRow("Selected Book: ",
                                  self.inform_selected_book)
        information_layout.addRow("Selected Address: ",
                                  self.inform_selected_address)
        # information_layout.addRow("Debug: ",
        #                           self.inform_debug)

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
                action = QAction()
                self.address_displays[add_type][i].clicked.connect(
                    lambda s=False, glyph_pos=i, add_type=add_type:
                        self.onGlyphDisplayClick(glyph_pos, add_type))

        general_layout.addWidget(address_tabs)

        IDC_widget = QWidget()
        IDC_layout = QFormLayout()
        IDC_widget.setLayout(IDC_layout)
        general_layout.addWidget(IDC_widget)

        self.IDC_entry = QLineEdit()
        self.IDC_entry.textChanged.connect(self.onIDCEdit)
        IDC_layout.addRow('IDC:', self.IDC_entry)

        self.IDC_oc_broadcastable = QCheckBox()
        self.IDC_oc_broadcastable.clicked.connect(self.onIDCBroadcastableClick)
        IDC_layout.addRow('OC Broadcastable:', self.IDC_oc_broadcastable)

        self.IDC_oc_port = QLineEdit()
        self.IDC_oc_port.textChanged.connect(self.onIDCOCPortEdit)
        IDC_layout.addRow('OC Port:', self.IDC_oc_port)

        self.IDC_oc_address = QLineEdit()
        self.IDC_oc_address.textChanged.connect(self.onIDCOCCompAddress)
        IDC_layout.addRow('OC Address:', self.IDC_oc_address)

    def onIDCEdit(self, *args):
        if self.selected_address:
            self.loaded_books[self.selected_book][
                self.selected_address]["IDC"][
                    "code"] = self.IDC_entry.text()

    def onIDCBroadcastableClick(self, checked):
        if self.selected_address:
            self.loaded_books[self.selected_book][
                self.selected_address]["IDC"][
                    "OC broadcastable"] = checked

    def onIDCOCPortEdit(self, *args):
        if self.selected_address:
            self.loaded_books[self.selected_book][
                self.selected_address]["IDC"][
                    "OC port"] = self.IDC_oc_port.text()

    def onIDCOCCompAddress(self, *args):
        if self.selected_address:
            self.loaded_books[self.selected_book][
                self.selected_address]["IDC"][
                    "component address"] = self.IDC_oc_address.text()

    def onGlyphDisplayClick(self, glyph_pos, glyph_type):
        self.inform_debug.setText(f"{glyph_pos, glyph_type}")
        self.glyph_dialogues[glyph_type].setWindowTitle(
            f"{glyph_type}: {glyph_pos}")
        self.glyph_dialogues[glyph_type].exec()

    def onLoadBookClick(self, s):
        book_path = QFileDialog.getOpenFileName(
            self, "Open Book File", application_path, "JSON files (*.json)"
            )[0]
        book_name = os.path.split(book_path)[-1]
        if os.path.isfile(book_path):
            with open(book_path, 'r') as book_file:
                book = json.load(book_file)
            if '_BOOK_NAME' in book:
                book_name = book['_BOOK_NAME']
                # del book['_BOOK_NAME']
            book_items = {}
            for name, entry in book.items():
                try:
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
                    if type(book_items[name]['IDC']) is str:
                        book_items[name]['IDC'] = {
                            'code': book_items[name]["IDC"],
                            "OC broadcastable": False,
                            'OC port': '',
                            'component address': ''
                        }
                except AttributeError:
                    if type(entry) is str:
                        book_items[name] = entry
            self.books_path_list[book_name] = book_path
            self.loaded_books[book_name] = book_items
            self.update_book_list()
            # print("succesfull")
        elif book_path:
            print('failed - file not exist')

    def update_book_list(self):
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

    def onNewBookClick(self, s):
        text = QInputDialog.getText(self, "New Book", "Book Name:",
                                    QLineEdit.Normal)
        if text[0] and text[1]:
            self.loaded_books[text[0]] = {
                '_BOOK_NAME': text[0],
            }
            self.update_book_list()

    def update_address_list(self, book_name):
        if self.selected_book != "":
            self.auto_save("switch book")
        self.selected_book = book_name
        self.inform_selected_book.setText(book_name)
        self.inform_selected_address.setText("None")
        self.selected_address = ""
        for add_type in ['MW', 'PEG', 'UNI']:
            for i in range(8):
                self.address_displays[add_type][i].setIcon(QIcon())
        self.address_menu.clear()
        actions = {}
        for address_name in self.loaded_books[book_name]:
            if address_name != '_BOOK_NAME':
                actions[address_name] = QAction(address_name, self)
                self.address_menu.addAction(actions[address_name])
                s = False  # wierd Qt thing
                actions[address_name].triggered.connect(
                    lambda s=s, address_name=address_name:
                        self.onAddressClick(address_name)
                    )

    def onNewAddressClick(self, s):
        if self.selected_book:
            text = QInputDialog.getText(self, "New Address", "Address Name:",
                                        QLineEdit.Normal)
            if text[0] and text[1]:
                TEMPLATE = {
                    "mw": {},
                    "peg": {},
                    "uni": {},
                    'IDC': {
                        'code': '',
                        "OC broadcastable": False,
                        'OC port': '',
                        'component address': ''
                    }
                }
                self.loaded_books[self.selected_book][text[0]] = dict(TEMPLATE)
                self.update_address_list(self.selected_book)

    def onAddressClick(self, address_name):
        self.selected_address = address_name
        self.inform_selected_address.setText(address_name)
        for add_type in ['MW', 'PEG', 'UNI']:
            for i in range(8):
                self.address_displays[add_type][i].setIcon(
                    self.loaded_glyphs['norm'][add_type][
                        self.loaded_books[self.selected_book][address_name][
                            add_type.lower()][f'glyph{i+1}']])
        self.IDC_entry.setText(self.loaded_books[self.selected_book][
            self.selected_address]["IDC"]["code"])
        self.IDC_oc_broadcastable.setChecked(
            self.loaded_books[self.selected_book][self.selected_address][
                "IDC"]["OC broadcastable"])
        self.IDC_oc_port.setText(self.loaded_books[self.selected_book][
            self.selected_address]["IDC"]["OC port"])
        self.IDC_oc_address.setText(self.loaded_books[self.selected_book][
            self.selected_address]["IDC"]["component address"])

    def onSaveBookClick(self, s):
        if self.selected_book:
            self.save(self.selected_book)

    def onSaveBookAsClick(self, s):
        book_path = ''
        if self.selected_book:
            book_path = QFileDialog.getSaveFileName(
                self, "Save Book File", application_path, "JSON files (*.json)"
                )[0]
        if book_path:
            return self.save_book_to_file(book_path)

    def save_book_to_file(self, book_path):
        if '_BOOK_NAME' not in self.loaded_books[self.selected_book]:
            book_name = self.selected_book[
                :-5] if self.selected_book.endswith(
                    '.json') else self.selected_book

            self.loaded_books[self.selected_book]['_BOOK_NAME'] = book_name
        else:
            book_name = self.selected_book
        entries = self.loaded_books[self.selected_book]
        data_to_write = self.sort_book({
            entry_name: entry if type(entry) is str else entry.copy()
            for entry_name, entry in entries.items()
            })

        if self.selected_book.endswith('.json'):
            self.loaded_books[book_name] = self.sort_book(entries)
            del self.loaded_books[self.selected_book]
            self.selected_book = book_name
            self.inform_selected_book.setText(book_name)
            self.update_book_list()
            selected_address = self.selected_address
            self.update_address_list(book_name)
            if selected_address:
                self.onAddressClick(selected_address)
        if not book_path.endswith('.json'):
            book_path = f'{book_path}.json'
        with open(book_path, 'w') as book_file:
            json.dump(data_to_write, book_file, indent=4)
        self.books_path_list[self.selected_book] = book_path
        return 'succesfull', book_path

    def sort_book(self, book: dict) -> dict:
        order = reversed(sorted(book))
        return {piece: book[piece] if type(book[piece]) is str or int
                else book[piece].copy() for piece in order}


class GlyphEditDialog(QDialog):
    def __init__(self, parent: MainWindow, glyph_type: str):
        super(GlyphEditDialog, self).__init__(parent)
        self.glyph_type = glyph_type
        self.glyph_buttons = {}
        self.setLayout(QGridLayout())
        glyphs_list = list(parent.loaded_glyphs['smol'][glyph_type].keys())
        for glyph in glyphs_list:
            self.glyph_buttons[glyph] = QPushButton()
            self.glyph_buttons[glyph].clicked.connect(
                lambda s=False, glyph=glyph:
                    self.onGlyphClick(glyph)
            )
            self.glyph_buttons[glyph].setFixedSize(parent.smol_glyphs_size)
            self.glyph_buttons[glyph].setIcon(
                parent.loaded_glyphs['smol'][glyph_type][glyph])
            self.glyph_buttons[glyph].setIconSize(parent.smol_glyphs_size)
            pos = divmod(glyphs_list.index(glyph), 6)
            self.layout().addWidget(
                self.glyph_buttons[glyph], *pos
            )

        self.glyph_name_entry = QLineEdit()
        self.glyph_name_entry.textChanged.connect(self.onGlyphNameEntryEdit)
        self.glyph_name_entry.setFixedWidth(parent.smol_glyphs_size.width())
        self.glyph_name_button = QPushButton()
        self.glyph_name_button.clicked.connect(self.onGlyphNameClick)
        self.glyph_name_button.setFixedSize(parent.smol_glyphs_size)
        self.glyph_name_button.setIconSize(parent.smol_glyphs_size)
        self.last_correct_glyph = ""

        self.layout().addWidget(QLabel("Glyph name: "), pos[0]+1, 0)

        self.layout().addWidget(self.glyph_name_entry, pos[0]+1, 1)
        self.layout().addWidget(self.glyph_name_button, pos[0]+2, 1)

    def onGlyphClick(self, glyph):
        pos = int(self.windowTitle().split()[-1])
        current_address = self.parent().selected_address
        current_book = self.parent().selected_book
        if current_address:
            self.parent().loaded_books[current_book][current_address][
                self.glyph_type.lower()][f'glyph{pos+1}'] = glyph
            self.parent().onAddressClick(current_address)
        self.hide()

    def onGlyphNameEntryEdit(self, *args):
        glyph_name = self.fix_glyph_name(self.glyph_name_entry.text())
        if glyph_name in self.parent().loaded_glyphs['smol'][
                self.glyph_type]:
            self.glyph_name_button.setIcon(self.parent().loaded_glyphs['smol'][
                self.glyph_type][glyph_name])
            self.last_correct_glyph = glyph_name

    def onGlyphNameClick(self, *args):
        if self.last_correct_glyph:
            self.onGlyphClick(self.last_correct_glyph)
            self.last_correct_glyph = ''
            self.glyph_name_button.setIcon(QIcon())
            self.glyph_name_entry.setText('')

    def fix_glyph_name(self, name: str) -> str:
        return name.title() if self.glyph_type != 'uni' else name.lower()


app = QApplication(sys.argv)
app.setStyle("Fusion")
w = MainWindow()
w.show()
sys.exit(w.exit_handler(app.exec()))
