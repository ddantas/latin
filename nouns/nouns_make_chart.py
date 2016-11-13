import re
import yaml
import common as c
import shoebot
import sys

inputfile  = sys.argv[1] 
outputfile = sys.argv[2]

print "Input file = {}".format(inputfile)
print "Output file = {}".format(outputfile)

with open(inputfile, "r") as f:
    data = yaml.load(f.read())

# 8.5x11"
bot = shoebot.create_bot(outputfile=outputfile)
bot.size(data['page']['width'], data['page']['height'])

default_color = '#a74ed5'
colors = {
    'blue': '#156eb4',
    'red': '#d61d67',
    'purple': '#a74ed5',
}

bot.font("Minion", fontsize=11)
bot.background(1)

# Swap out [ending] for <ending>ending</ending>
def style_line(l):
    text_line = re.sub(r"\{(.*?)\}", r"<stem>\1</stem>", l)
    text_line = re.sub(r"\[(.*?)\]", r"<ending>\1</ending>", text_line)
    return "<w>%s</w>" % text_line
    
    
# Draw the group header ("1st Person", etc.)    
def draw_group_header(x, y, title, width):
    bot.push()
    bot.translate(x, y)
    
    # Top rule
    bot.nofill()
    bot.strokewidth(0.25)
    bot.stroke(0.5)
    bot.line(0, -12, width, -12)

    # Group title
    bot.font("Museo Sans", fontsize=data['group_header_size'])
    bot.fill(0.1)
    bot.text(group['title'].upper(), 0, 0)
    #font(tracking=0)
    
    bot.pop()


# Draw the side headings    
def draw_side_headings(x, y, headings):
    bot.push()
    
    bot.translate(x, y + data['side_heading_initial_offset'])
    
    bot.font("Times", fontsize=data['side_heading_size'] * .8)
    bot.fill(0.65)
    
    for heading in headings:
        bot.text(heading.upper(), data['side_heading_indent'], 0)
        
        # Line spacing
        bot.translate(0, data['side_heading_spacing'])

    bot.fill(0)
    #font(sc=False)    
    
    bot.pop()


# Draw an individual column
def draw_column(x, y, column):
    bot.push()
    bot.translate(x, y)
    
    if 'sample_word' in column and column['sample_word'] != '':
        bot.font("Times", fontsize=data['sample_size'])
        #TODO: add support to xml formatting as in NodeBox
        txt = column['sample_word']
        txt = re.sub(r"<.*?>", "", txt)
        bot.fill(0.45)
        bot.text(txt, 0, 0, 200)

    bot.translate(0, data['sample_word_spacing'])        
    
    bot.fill(0.65)
    if 'color' in column and column['color'] != '':
        fill_color = colors[column['color']]
    else:
        fill_color = default_color
    
    # Draw the title
    if 'title' in column and column['title'] != '':
        bot.font("Times", fontsize=data['heading_size'] * .8)
        bot.text(column['title'].upper(), 0, 0, 1)
        
    bot.translate(0, data['title_spacing'])
    
    bot.fill(0)
    
    # Draw the words
    bot.font("Times", fontsize=data['word_size'])
    for case in data['headings']:
        item = column[case]
        c.draw_word(bot, item, 0, fill_color)
        bot.translate(0, data['line_spacing'])
    
    bot.pop()
    
    
# Draw a side

def draw_side(base_x, base_y, group):
    # Width of group
    if 'width' in group:
        width = data['half_width']
    else:
        width = data['width']
        
    # Draw the group header
    draw_group_header(base_x, base_y, group['title'], width)
    
    # Draw the side headings
    side_top = base_y + 20
    if 'side_top' in group:
        side_top += group['side_top']
    draw_side_headings(base_x, side_top, data['headings'])
    
    # Draw the individual columns
    col_x = base_x + data['side_heading_offset']
    for index, column in enumerate(group['data']):
        if 'sample_word' in column and column['sample_word'] != '':
            # Space it out (sample word = new group)
            col_x += data['subgroup_spacing']
            
        draw_column(col_x, base_y + 18, column)
        col_x += data['column_spacing']



# Heading
bot.font("Museo Sans", fontsize=14)
bot.text("Latin {}".format(data['label']).upper(), data['margin'], data['margin'] + 10)

# Heading metadata
bot.align(bot.RIGHT)
bot.font("Museo Sans", fontsize=8)
bot.stroke(0)
bot.fill(0.5)

bot.translate(0, -data['side_heading_spacing'])
msg = "github.com/ddantas, design by bencrowder.net"
w = bot.textwidth(msg)
bot.text(msg, data['page']['width'] - data['margin'] - w, data['margin'] + 10)

bot.translate(0, data['side_heading_spacing'])
msg = data['updated']
w = bot.textwidth(msg)
bot.text(msg, data['page']['width'] - data['margin'] - w, data['margin'] + 10)
#font(italic=False)

bot.align(bot.LEFT)
bot.strokewidth(0.5)


# Draw left side

base_y = data['margin'] + 50
for index, row in enumerate(data['left_rows']):
    base_x = data['margin']
    for group in row['groups']:
        draw_side(base_x, base_y, group)
        
        base_x += data['group_spacing_x']
        
    base_y += data['group_spacing_y']
    
# Draw right side

base_y = data['margin'] + 50
for index, row in enumerate(data['right_rows']):
    base_x = 420
    for group in row['groups']:
        draw_side(base_x, base_y, group)
        
        base_x += data['group_spacing_x']
        
    base_y += data['group_spacing_y']



bot.finish()
#bot.snapshot('output.png')
#bot.snapshot('output.pdf')
#drawing = svg2rlg("file.svg")
#renderPDF.drawToFile(drawing, "file.pdf")

#print(sys.argv)
