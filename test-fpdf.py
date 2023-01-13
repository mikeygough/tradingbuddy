from fpdf import FPDF

# create pdf
pdf = FPDF(orientation='L')

# add page
pdf.add_page()

# set font
pdf.set_font('Arial', 'B', 16)

# add some text
pdf.cell(40, 10, 'Hello World!')

# add a circle!
pdf.set_line_width(2)
pdf.set_draw_color(240)
pdf.set_fill_color(r=230, g=30, b=180)
pdf.circle(x=50, y=50, r=50, style="FD")

# output file
pdf.output('test-fpdf.pdf', 'F')

