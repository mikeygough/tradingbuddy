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

# set font
pdf.set_font('Helvetica', 'B', 16)

# add some text
pdf.set_xy(10, 10)
print("xpos before text", pdf.get_x())
print("ypos before text", pdf.get_y())
pdf.cell(40, 10, 'Current prices relative to recent highs and lows')

# add a circle!
print("xpos after text, before circle", pdf.get_x())
print("ypos after text, before circle", pdf.get_y())
pdf.set_line_width(1)
pdf.set_draw_color(240)
pdf.set_fill_color(r=230, g=30, b=180)
pdf.circle(x=10, y=30, r=25, style='F')
print("xpos after circle, before /es", pdf.get_x())
print("ypos after circle, before /es", pdf.get_y())

# reset position
pdf.set_xy(10, 37)
pdf.cell(w=25, h=10, txt='/ES', align='C')
print("xpos after /es", pdf.get_x())
print("ypos after /es", pdf.get_y())

# test getting string width
print("string width", pdf.get_string_width('/ES'))

def draw_circle(xpos, ypos, rad=25):
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

def draw_hilo(high, low, close,
              xpos_start, ypos_start,
              xpos_end, ypos_end):
    '''
    draws a high-low line with circle at the current price
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


# draw_circle(xpos=40, ypos=50)

draw_hilo(high=100, low=0, close=50, 
          xpos_start=40, ypos_start=100,
          xpos_end=80, ypos_end=100)

# output file
pdf.output('test-fpdf.pdf')

