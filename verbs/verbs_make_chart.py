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

page_width = 792
page_height = 612

heading_size = 7
group_heading_size = 7
word_size = 9
horizontal_spacing = 63
default_spacing = 13 # line spacing
group_header_size = 9
group_header_offset = 16
row_spacing = 130

bot = shoebot.create_bot(outputfile=outputfile)
bot.size(page_width, page_height)
bot.background(1)

bot.font("Times", fontsize=11)

#stylesheet("ending", weight="bold")
#stylesheet("stem", italic=True)
    
def style_line(l):
    text_line = re.sub(r"\{(.*?)\}", r"\1", l)    
    return text_line
    # swap out [ending] for <ending>ending</ending>
    text_line = re.sub(r"\{(.*?)\}", r"<stem>\1</stem>", l)
    text_line = re.sub(r"\[(.*?)\]", r"<ending>\1</ending>", text_line)
    return "<w>%s</w>" % text_line
    
def draw_chart(x, y, chart, fill_color="#cb202c", spacing=default_spacing):
    bot.push()
    bot.translate(x, y)
    
    bot.font("Times", fontsize=word_size)
    bot.fill(0)

    #stylesheet("ending", fill=fill_color, weight="bold")

    for l in chart:
        if l != '':
            #bot.text("C"+style_line(l), 0, 0, 200)
            c.draw_word(bot, style_line(l), 0, fill_color)
       
        # line spacing
        bot.translate(0, spacing)

    #font(tracking=0)
    
    bot.pop()

def draw_group(x, y, group, fill_color="#cb202c", spacing=default_spacing):
    bot.push()
    bot.translate(x, y)

    if group['chart']:
        bot.font("Museo Sans", fontsize=group_heading_size)
        bot.fill(0.5)
        if group['title']:
            bot.text(group['title'].upper(), 0, 0)
        #bot.font(tracking=0)
            
        draw_chart(0, group_header_offset, group['chart'], fill_color, spacing)
    
    bot.pop()
    
def draw_headings(x, y, headings, spacing=default_spacing):
    bot.push()
    bot.translate(x, y + group_header_offset - 0.75)
    bot.font("Times", fontsize=heading_size * .8)
    bot.fill(0.5)
    
    for line in headings:
        bot.text(line.upper(), 0, 0)
        
        # line spacing
        bot.translate(0, spacing)

    #bot.font(sc=False)    
    bot.pop()

def draw_group_header(x, y, label, width):
    bot.push()
    bot.fill(0)
    bot.stroke(0.5)
    bot.strokewidth(1)
    bot.translate(x, y)
    bot.font("Museo Sans", fontsize=group_header_size)
    bot.line(0, -11, width, -11)
    bot.text(label.upper(), 0, 0)
    #bot.font(tracking=0)
    bot.pop()

def parse_list(groups):
    response = []
    
    for line in groups:
        data = line.split('|')
        
        group = {
            'title': data[0].strip(),
            'chart': [x.strip() for x in data[1:]],
        }
        
        response.append(group)
    
    return response

headings = [
    '1st sg.',
    '2nd sg.',
    '3rd sg.',
    '1st pl.',
    '2nd pl.',
    '3rd pl.',
]

active_headings = [
    'active',
    'passive',
]

gerund_headings = [
    'gen.',
    'dat.',
    'acc.',
    'abl.',
]    

margin = 30

# Heading

bot.font("Museo Sans", fontsize=14)
bot.text(u"{} - {}".format(data['name'], data['label']).upper(), margin, margin + 10)

"""
bot.align(bot.RIGHT)
bot.font("Times", fontsize=9)
bot.stroke(0)
bot.fill(0.5)
bot.text("bencrowder.net - Last modified {}".format(data['updated']), page_width-margin, margin + 10, 200)
#bot.font(italic=False)
"""

# Heading metadata
bot.align(bot.RIGHT)
bot.font("Times", fontsize=7)
bot.stroke(0)
bot.fill(0.5)

#bot.translate(0, -35)
msg = "github.com/ddantas, design by bencrowder.net, {}".format(data['updated'])
w = bot.textwidth(msg)
bot.text(msg, page_width - margin - w, margin + 10)

side_heading_spacing = 16
#bot.translate(0, side_heading_spacing)
msg = data['updated']
w = bot.textwidth(msg)
bot.text(msg, page_width - margin - w, margin + 10)
#font(italic=False)


bot.font("Times", fontsize=8)

bot.align(bot.LEFT)
bot.translate(margin, 3.5*side_heading_spacing)
if 'example_word' in data:
    c.draw_example(bot, data['example_word'])
    #bot.text(style_line(data['example_word']), margin, margin + 25, 200)

bot.translate(-margin, -3.5*side_heading_spacing)

# Groups

# Left side    
base_y = margin + 50

for group in data['left']:
    draw_group_header(margin, base_y, group['title'], 430)
    draw_headings(30, base_y + 20, headings)
    
    for index, g in enumerate(parse_list(group['groups'])):
        draw_group(margin + 40 + (index * horizontal_spacing), base_y + 20, g, fill_color=group['fill'])
        
    base_y += row_spacing

# Right side    
right_x = 520
base_y = margin + 50
    
for group in data['right']:
    if 'type' in group and group['type'] == 'headerless':
        headings_list = gerund_headings
        base = base_y + 4
    else:
        headings_list = active_headings
        base = base_y + 20
    
    draw_group_header(right_x, base_y, group['title'], 242)
    draw_headings(right_x, base, headings_list)
    
    for index, g in enumerate(parse_list(group['groups'])):
        draw_group(right_x + 40 + (index * horizontal_spacing), base, g, fill_color=group['fill'])
        
    base_y += row_spacing

if 'note' in data:
    bot.font("Minion", fontsize=8)
    bot.text(data['note'], right_x, page_height - margin - 11, 200)
    

bot.finish()

#export(data['output'])
