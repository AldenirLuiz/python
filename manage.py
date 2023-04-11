import json
from SysWay import MyWayApp as Way


class ViewCard:
    json_file: str = Way(file="cellNames.json").walk_sys_file().replace('library.zip', 'cellNames.json')
    print(f"json path: {json_file}")
    with open(json_file, "r", encoding="utf8", errors="ignore") as cell_names:
        layers = json.load(cell_names)

    def ret_card(self, card: str, celula: str = None):
        if celula:
            return self.layers[card][celula]
        return self.layers[card]

    @property
    def layers_(self):
        return self.layers

if __name__ == "__main__":
    print(ViewCard().layers)