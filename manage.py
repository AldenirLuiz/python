from ctypes import Union
import json


class ViewCard:
    json_file: str = "cellNames.json"
    with open(json_file, "r") as cell_names:
        layers = json.load(cell_names)

    def ret_card(self, card: str, celula: str = None):
        if celula:
            return self.layers[card][celula]
        return self.layers[card]

    @property
    def layers_(self):
        return self.layers
