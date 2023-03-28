from manage import ViewCard
import os

path = os.path.abspath(os.path.dirname(__file__))
form_data = ViewCard.layers

class Header:
    head_string = """
    <!DOCTYPE html>
        <html>
            <head>
                <title>Corro Variedades</title>
                <style>
                    * {
                        font-family: Cambria, Cochin, Georgia, Times, 'Times New Roman', serif;
                        font-size: 1rem;
                        font-weight: lighter;}
                    h3{
                        margin:0;
                        padding-left:4px; 
                        padding:8px;
                        justify-self:right;}
                    .intern-desc {
                        width:190px;
                        height:40;
                        border-left: 1px solid black;
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;}
                    .intern-val {
                        width:160px;
                        height:40;
                        border-left: 1px solid black;
                        border-right: 1px solid black;
                        border-bottom: 1px solid black;}
                    .card-base {
                        display: flex; 
                        flex-direction: row;}
                    .itens-r {
                        display: flex;
                        padding: 8px;
                        margin: 2px;}
                    .master {
                        display: flex;
                        flex-direction: column;}
                    .card-row{
                        display: flex;
                        flex-direction: row;}
                    .desc {
                        border: 1px solid black;
                        color: darkgray;
                        text-align: center;
                        justify-content: center;}
                </style>
            </head>
            <body>
                <div class="master">"""

    for count, card in enumerate(form_data):
        head_string+=f'''
                    <div class="card-row row-{count}">'''
        for item in form_data[card]:
            head_string+=f'''
                        <div class="card">
                            <h3 class=desc>{item.upper()}</h3>'''
            for label in form_data[card][item]:
                head_string+=f'''
                            <div class="card-base">
                                <div class="intern-desc">
                                    <h3>{label.upper().replace('_', ' ')}:</h3>
                                </div>
                                <div class="intern-val">
                                    <h3 id="{label.replace(' ', '_')}">{label}</h3>
                                </div>
                            </div>'''
            head_string+=f'''
                        </div>'''
        head_string+=f'''
                    </div>'''
    head_string +="""
                </div>
            </body>
            <script>
                (function(){
                    window.print();
                })();
            </script>
        </html>"""
    def create_template(self):
        with open(file=f'{path}/index.html', mode='w') as page:
            for char in self.head_string:
                page.writelines(char)
        
if __name__ == "__main__":
    header = Header()
    header.create_template()
         