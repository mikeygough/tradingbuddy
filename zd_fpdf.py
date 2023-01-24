from fpdf import FPDF
import numpy as np

class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='L')
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

    def draw_hilo(self, high, low, close,
              xpos_start, ypos_start,
              xpos_end, ypos_end):
        '''
        draws a high-low-close line with circle at the current price
        high: underlying high price
        low: underlying low price
        xpos_start: abscissa of first point
        ypos_start: ordinate of first point
        xpos_end: abscissa of second point
        ypos_end: ordinate of second point
        '''
        # draw line
        self.set_line_width(1)
        self.set_draw_color(r=230, g=30, b=180)
        self.line(x1=xpos_start, y1=ypos_start,
                 x2=xpos_end, y2=ypos_end)

        # calculate line length
        length = np.sqrt((xpos_end - xpos_start) ** 2 + (ypos_end - ypos_start) ** 2)
        # calculate position percent
        close_pct = close / high
        # calculate additional line pos
        additional_pos = close_pct * length
        # calculate circle position
        circle_x_position = additional_pos + xpos_start

        # draw circle at position
        self.draw_circle(xpos=circle_x_position, ypos=ypos_start-1.5, rad=3)

        # add annotations
        self.set_font('Helvetica', 'B', 12)
        
        # draw low text
        self.set_xy(xpos_start - self.get_string_width('{}'.format(low)) - 2,
                   ypos_start-8)
        self.cell(h=10, txt='{}'.format(low), align='L')
        self.set_xy(xpos_start - self.get_string_width('Low') - 2, ypos_start-2)
        self.cell(h=10, txt='Low', align='L')

        # draw high text
        self.set_xy(xpos_end, ypos_end-8)
        self.cell(h=10, txt='{}'.format(high), align='L')
        self.set_xy(xpos_end, ypos_end-2)
        self.cell(h=10, txt='High', align='L')
        
        # draw close text
        self.set_font('Helvetica', 'B', 14)

        self.set_xy(circle_x_position - (self.get_string_width('{}'.format(close)) / 2),       ypos_end-12)
        self.cell(h=10, txt='{}'.format(close), align='C')
        # pdf.set_xy(circle_x_position - (pdf.get_string_width('Close') / 2), ypos_end-2)
        # pdf.cell(h=10, txt='Close', align='C')

    def draw_sd(self, xpos, ypos):
        '''
        draws a normal distribution with 1, 2 & 3 sd movement values
        '''
        # standard deviation
        # std lines
        self.set_line_width(0.5)
        self.set_draw_color(37, 37, 37)
        
        #155 is the middle
        middle = xpos + 50
        
        # ~1 sd
        self.line(x1=xpos+43, y1=ypos+16,
                 x2=xpos+43, y2=ypos+28)
        self.line(x1=xpos+59, y1=ypos+15,
                 x2=xpos+59, y2=ypos+28)
        # ~2 sd
        self.set_draw_color(82, 82, 82)
        self.line(x1=xpos+35, y1=ypos+24,
                 x2=xpos+35, y2=ypos+28)
        self.line(x1=xpos+67, y1=ypos+23.5,
                 x2=xpos+67, y2=ypos+28)
        # ~3 sd
        self.set_draw_color(115, 115, 115)
        self.line(x1=xpos+25, y1=ypos+27,
                 x2=xpos+25, y2=ypos+28)
        self.line(x1=xpos+77, y1=ypos+27.5,
                 x2=xpos+77, y2=ypos+28)

        # base line
        self.set_line_width(0.5)
        self.set_draw_color(0, 0, 0)
        self.line(x1=xpos+20, y1=ypos+28,
                 x2=xpos+81, y2=ypos+28)

        # standard curve
        self.image('static/normal_distribution.png', x=xpos, y=ypos,
                  h=30, w=100)

        # add annotations
        self.set_font('Helvetica', 'B', 14)
        
        # draw low text
        # low 1
        self.set_xy(xpos+43 - (self.get_string_width('25') / 3),
                   ypos+28)
        self.cell(h=10, txt='25', align='L')

        # low 2
        self.set_xy(xpos+35 - (self.get_string_width('35') / 3),
                   ypos+28)
        self.cell(h=10, txt='35', align='L')

        # low 3
        self.set_xy(xpos+25 - (self.get_string_width('40') / 3),
                   ypos+28)
        self.cell(h=10, txt='40', align='L')


def main():
    # create pdf
    pdf = PDF()
    
    # describe pdf
    print("page layout", pdf.page_layout)
    # unit mm
    print("default page dimensions", pdf.default_page_dimensions)
    # (841.89, 595.28)mm
    
    # draw sd
    pdf.draw_sd(xpos=105, ypos=7)

    # symbol circle
    pdf.draw_circle(xpos=10, ypos=10, symbol='/ES')

    # high low close
    pdf.draw_hilo(high=100, low=10, close=79, 
              xpos_start=55, ypos_start=22,
              xpos_end=100, ypos_end=22)

    # sample chart
    pdf.image('static/chart.png', x=190, y=8,
    h=30, w=100)

    # output file
    pdf.output('static/test-fpdf.pdf')


if __name__ == '__main__':
    main()






























## OOOOOLLLLLDD

# # -- initialize pdf
# pdf = FPDF(orientation='L')

# # the origin is at the upper-left corner and the current position is by default placed at 1 cm from the borders; the margins can be changed with set_margins.
# pdf.add_page()

# # set font
# pdf.set_font('Arial', 'B', 16)

# # a cell is a rectangular area, possibly framed, which contains some text. It is output at the current position. We specify its dimensions, its text (centered or aligned), if borders should be drawn, and where the current position moves after it (to the right, below or to the beginning of the next line)
# # TITLE
# pdf.cell(w=40, h=10, txt='/ES',
#          border=0, ln=0, align='',
#          fill=False, link='')
# # add line break
# # h = the height of the break.
# pdf.ln(h='')

# # STATISTICS
# # print('close', CLOSE)# close
# pdf.cell(w=40, h=10, txt='Close: {:.2f}'.format(CLOSE),
#          border=0, ln=1, align='',
#          fill=False, link='')

# # print('high', HIGH)
# pdf.cell(w=40, h=10, txt='Period High: {:.2f}'.format(HIGH),
#     ln=1)

# # print('low', LOW)
# pdf.cell(w=40, h=10, txt='Period Low: {:.2f}'.format(LOW),
#     ln=1)

# # print('return', RETURN)
# pdf.cell(w=40, h=10, txt='Period Return: {:.2%}'.format(RETURN),
#     ln=1)

# # print('one_sd', ONE_SD)
# pdf.cell(w=42, h=10, txt='One Sd.: +/-{}'.format(ONE_SD),
#     ln=0)

# print(pdf.get_x())

# # print('two_sd', TWO_SD)
# pdf.cell(w=40, h=10, txt='Two Sd.: +/-{}'.format(TWO_SD),
#     ln=0)

# print(pdf.get_x())

# # print('three_sd', THREE_SD)
# pdf.cell(w=40, h=10, txt='Three Sd.: +/-{}'.format(THREE_SD),
#     ln=1)

# # print('historical_vol', HISTORICAL_VOL)
# pdf.cell(w=40, h=10, txt='Historical Volatility: {:.2f}'.format(HISTORICAL_VOL),
#     ln=1)

# # print('one day upper range', UPPER_1)
# pdf.cell(w=40, h=10, txt='Upper 1: {:.2f}'.format(UPPER_1),
#     ln=1)

# # print('two day upper range', UPPER_2)
# pdf.cell(w=40, h=10, txt='Upper 2: {:.2f}'.format(UPPER_2),
#     ln=1)

# # print('three day upper range', UPPER_3)
# pdf.cell(w=40, h=10, txt='Upper 3: {:.2f}'.format(UPPER_3),
#     ln=1)

# # print('four day upper range', UPPER_4)
# pdf.cell(w=40, h=10, txt='Upper 4: {:.2f}'.format(UPPER_4),
#     ln=1)

# # print('five day upper range', UPPER_5)
# pdf.cell(w=40, h=10, txt='Upper 5: {:.2f}'.format(UPPER_5),
#     ln=1)

# # print('one day lower range', LOWER_1)
# pdf.cell(w=40, h=10, txt='Lower 1: {:.2f}'.format(LOWER_1),
#     ln=1)

# # print('two day lower range', LOWER_2)
# pdf.cell(w=40, h=10, txt='Lower 2: {:.2f}'.format(LOWER_2),
#     ln=1)

# # print('three day lower range', LOWER_3)
# pdf.cell(w=40, h=10, txt='Lower 3: {:.2f}'.format(LOWER_3),
#     ln=1)

# # print('four day lower range', LOWER_4)
# pdf.cell(w=40, h=10, txt='Lower 4: {:.2f}'.format(LOWER_4),
#     ln=1)

# # print('five day lower range', LOWER_5)
# pdf.cell(w=40, h=10, txt='Lower 5: {:.2f}'.format(LOWER_5),
#     ln=1)

# pdf.output('2-pandas-fpdf.pdf', 'F')

