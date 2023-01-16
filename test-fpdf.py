from fpdf import FPDF
import numpy as np

# create pdf
pdf = FPDF(orientation='L')
pdf.set_margin(0)
print("page layout", pdf.page_layout)
print("default page dimensions", pdf.default_page_dimensions)
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

def draw_sd():
    '''
    draws a normal distribution with 1, 2 & 3 sd movement values
    '''
    pass

# symbol circle
draw_circle(xpos=10, ypos=10, symbol='/ES')

# high low close
draw_hilo(high=100, low=10, close=79, 
          xpos_start=55, ypos_start=22,
          xpos_end=100, ypos_end=22)

# standard deviation
# std lines
pdf.set_line_width(0.5)
pdf.set_draw_color(37, 37, 37)
#155 is the middle
# ~1 sd
pdf.line(x1=148, y1=23,
         x2=148, y2=35)
pdf.line(x1=164, y1=22,
         x2=164, y2=35)
# ~2 sd
pdf.set_draw_color(82, 82, 82)
pdf.line(x1=140, y1=31,
         x2=140, y2=35)
pdf.line(x1=172, y1=30.5,
         x2=172, y2=35)
# ~3 sd
pdf.set_draw_color(115, 115, 115)
pdf.line(x1=130, y1=34,
         x2=130, y2=35)
pdf.line(x1=182, y1=34.5,
         x2=182, y2=35)

# base line
pdf.set_line_width(0.5)
pdf.set_draw_color(0, 0, 0)
pdf.line(x1=125, y1=35,
         x2=186, y2=35)

# standard curve
pdf.image('static/normal_distribution.png', x=105, y=7,
    h=30, w=100)



# output file
pdf.output('test-fpdf.pdf')

