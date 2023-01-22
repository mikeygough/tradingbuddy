from fpdf import FPDF
import numpy as np


pdf = FPDF(orientation='L')
pdf.add_page()
pdf.set_font('Arial', 'B', 16)

# create pdf
# pdf.set_margin(0)


print("page layout", pdf.page_layout)

# unit mm
print("default page dimensions", pdf.default_page_dimensions)
# (841.89, 595.28)mm
pdf.set_line_width(0)

# add page
pdf.add_page()

def draw_circle(xpos, ypos, rad=25, symbol=''):
    '''
    draws a filled in circle of radius rad as xpos, ypos
    xpos: abscissa of upper-left bounding box
    ypos: ordinate of upper-left bounding box
    rad: radius of circle, default 25
    '''
    pdf.set_line_width(1)
    pdf.set_draw_color(240)
    pdf.set_fill_color(r=230, g=30, b=180)
    pdf.circle(x=xpos, y=ypos, r=rad, style='F')

    # add text annotation
    pdf.set_font('Helvetica', 'B', 16)
    pdf.set_xy(xpos, ypos)
    pdf.cell(w=rad, h=rad-2, txt='{}'.format(symbol), align='C')


def draw_hilo(high, low, close,
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
    pdf.set_line_width(1)
    pdf.set_draw_color(r=230, g=30, b=180)
    pdf.line(x1=xpos_start, y1=ypos_start,
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
    draw_circle(xpos=circle_x_position, ypos=ypos_start-1.5, rad=3)

    # add annotations
    pdf.set_font('Helvetica', 'B', 12)
    
    # draw low text
    pdf.set_xy(xpos_start - pdf.get_string_width('{}'.format(low)) - 2,
               ypos_start-8)
    pdf.cell(h=10, txt='{}'.format(low), align='L')
    pdf.set_xy(xpos_start - pdf.get_string_width('Low') - 2, ypos_start-2)
    pdf.cell(h=10, txt='Low', align='L')

    # draw high text
    pdf.set_xy(xpos_end, ypos_end-8)
    pdf.cell(h=10, txt='{}'.format(high), align='L')
    pdf.set_xy(xpos_end, ypos_end-2)
    pdf.cell(h=10, txt='High', align='L')
    
    # draw close text
    pdf.set_font('Helvetica', 'B', 14)

    pdf.set_xy(circle_x_position - (pdf.get_string_width('{}'.format(close)) / 2),       ypos_end-12)
    pdf.cell(h=10, txt='{}'.format(close), align='C')
    # pdf.set_xy(circle_x_position - (pdf.get_string_width('Close') / 2), ypos_end-2)
    # pdf.cell(h=10, txt='Close', align='C')

def draw_sd(xpos, ypos):
    '''
    draws a normal distribution with 1, 2 & 3 sd movement values
    '''
    # standard deviation
    # std lines
    pdf.set_line_width(0.5)
    pdf.set_draw_color(37, 37, 37)
    
    #155 is the middle
    middle = xpos + 50
    
    # ~1 sd
    pdf.line(x1=xpos+43, y1=ypos+16,
             x2=xpos+43, y2=ypos+28)
    pdf.line(x1=xpos+59, y1=ypos+15,
             x2=xpos+59, y2=ypos+28)
    # ~2 sd
    pdf.set_draw_color(82, 82, 82)
    pdf.line(x1=xpos+35, y1=ypos+24,
             x2=xpos+35, y2=ypos+28)
    pdf.line(x1=xpos+67, y1=ypos+23.5,
             x2=xpos+67, y2=ypos+28)
    # ~3 sd
    pdf.set_draw_color(115, 115, 115)
    pdf.line(x1=xpos+25, y1=ypos+27,
             x2=xpos+25, y2=ypos+28)
    pdf.line(x1=xpos+77, y1=ypos+27.5,
             x2=xpos+77, y2=ypos+28)

    # base line
    pdf.set_line_width(0.5)
    pdf.set_draw_color(0, 0, 0)
    pdf.line(x1=xpos+20, y1=ypos+28,
             x2=xpos+81, y2=ypos+28)

    # standard curve
    pdf.image('static/normal_distribution.png', x=xpos, y=ypos,
    h=30, w=100)

# draw sd
draw_sd(xpos=105, ypos=7)

# symbol circle
draw_circle(xpos=10, ypos=10, symbol='/ES')

# high low close
draw_hilo(high=100, low=10, close=79, 
          xpos_start=55, ypos_start=22,
          xpos_end=100, ypos_end=22)


# sample chart
pdf.image('static/chart.png', x=190, y=8,
    h=30, w=100)

# output file
pdf.output('static/test-fpdf.pdf')

























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

