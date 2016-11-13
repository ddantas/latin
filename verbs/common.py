

# Draw an individual word. Text between [] is colored.
def draw_word(bot, word, color_default = 0, color = 0):
    pos = 0
    bot.fill(color_default)
    strike = False
    for c in word:
      if (c == '-'):   # Minus sign (-) denotes defective form
        strike = True
        bot.fill(0.5)
      elif (c == '['):
        if (not strike):
          bot.fill(color)
      elif (c == ']'):
        if (not strike):
          bot.fill(color_default)
      else:        
        bot.text(c, pos, 0, 200)
        pos += bot.textwidth(c)
    if (strike):
      bot.strokewidth(0.1)
      bot.line(0, -2, pos, -2)
    bot.fill(color_default)


def draw_example(bot, example):
    arr_example = example.split(',')
    pos = 0
    bot.fill(0.5)
    for i in range(len(arr_example)):
        pos0 = pos
        strike = False
        word = arr_example[i]
        for c in word:
            if (c == '-'):   # Minus sign (-) denotes defective form
                strike = True
            else:        
                bot.text(c, pos, 0, 200)
                pos += bot.textwidth(c)
        if (strike):
            bot.strokewidth(0.1)
            bot.stroke(0.5)
            bot.line(pos0, -2, pos, -2)

        vg = ', '
        if i < len(arr_example) - 1:
            bot.text(vg, pos, 0, 200)
            pos += bot.textwidth(vg)



