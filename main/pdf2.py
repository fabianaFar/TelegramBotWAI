from fpdf import FPDF
import json

title = "UniBot di Farias Fabiana"
with open('config.json') as font_file:
    config = json.load(font_file)

quicksand = config['FONT']


class PDF(FPDF):
    def header(self):
        self.image('BOT.png', 10, 8, 25)
        self.add_font('Quicksand', '', 
                   quicksand, uni=True)
        self.set_font('Quicksand', '', 20)
        self.cell(0, 10, title, ln=1, align='C')
        self.ln(20)

    def footer(self):
        self.set_y(-15)
        self.set_font('Quicksand', '', 8)
        self.set_text_color(169,169,169)
        self.cell(0, 10, f"Page {self.page_no()}", align='C')

    def add_content(self, content):
        self.set_font('Quicksand', '', 10)
        self.multi_cell(0, 10, content)  # Permette di aggiungere più righe di testo.
        self.ln()

    def generate_pdf(self, content, file_name):
        self.alias_nb_pages()
        self.set_auto_page_break(auto=True, margin=15)
        self.add_page()
        self.add_content(content)
        self.output(file_name)
