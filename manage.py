import json
from SysWay import MyWayApp as Way


class ViewCard:
    json_file: str = Way(file="cellNames.json").walk_sys_file()
    print(f"json path: {json_file}")
    with open(json_file, "r") as cell_names:
        layers = json.load(cell_names)

    def ret_card(self, card: str, celula: str = None):
        if celula:
            return self.layers[card][celula]
        return self.layers[card]

    @property
    def layers_(self):
        return self.layers
