from fpdf import FPDF

class Shirtificate(FPDF):
    def __init__(self, text = ''):
        super().__init__()
        self.add_page(orientation="portrait", format="A4")
        self.set_margin(0)
        self.set_auto_page_break(False)
        self.set_font('Helvetica', size=50)
        self.image('shirtificate.png', keep_aspect_ratio=False,y=70, x=5, dims=(560,560))
        self.cell(
            text='CS50 Shirtificate', 
            h=77, 
            align='c', 
            center=True, 
            new_x='LEFT', 
            new_y='NEXT')
        self.set_text_color(255,255,255)
        self.set_font_size(25)
        self.cell(text=text, h=120 ,align='c', center=True)
        self.output('shirtificate.pdf')


def main():
    text = input('Name: ') + ' took CS50'
    Shirtificate(text)

if __name__ == "__main__":
    main()