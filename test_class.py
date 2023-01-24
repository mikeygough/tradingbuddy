from fpdf import FPDF


class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L')
        self.col = 0  # Current column
        self.y0 = 0  # Ordinate of column start
        self.add_page()
        self.set_margin(0)


    def draw_circle(self, xpos, ypos, rad=25, symbol=''):
        '''
        draws a filled in circle of radius rad as xpos, ypos
        xpos: abscissa of upper-left bounding box
        ypos: ordinate of upper-left bounding box
        rad: radius of circle, default 25
        '''
        self.set_line_width(1)
        self.set_draw_color(240)
        self.set_fill_color(r=230, g=30, b=180)
        self.circle(x=xpos, y=ypos, r=rad, style='F')

        # add text annotation
        self.set_font('Helvetica', 'B', 16)
        self.set_xy(xpos, ypos)
        self.cell(w=rad, h=rad-2, txt='{}'.format(symbol), align='C')

new_pdf = PDF()
new_pdf.draw_circle(xpos=10, ypos=10, symbol='/ES')
# output file
new_pdf.output('static/test-class.pdf')

print(new_pdf.__dict__)
