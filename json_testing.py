import json

eg_entry = {
    "name": "earth",
    "addresses": [{
        "type": "mw",
        "glyph1": "Eridanus",
        "glyph2": "Taurus",
        "glyph3": "Libra",
        "glyph4": "Sextans",
        "glyph5": "Aquila",
        "glyph6": "Orion",
        "glyph7": "none",
        "glyph8": "none"
    }, {
        "type": "peg"
    }]
}

# with open('SG-Address-book-recorder-viewer\\books\\testbook.json', 'w') as file:
#     json.dump(eg_entry, file, indent=4)

with open('SG-Address-book-recorder-viewer\\books\\testbook.json', 'r') as file:
    print(json.load(file))