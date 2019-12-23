#!/usr/bin/env python3

import sys
import svgwrite

data = []

try:
    MAXLEVEL = int(sys.argv[2])
except:
    MAXLEVEL = 3

try:
    MINLEVEL = int(sys.argv[3])
except:
    MINLEVEL  = 1


WORDS = False

seen = set()
for level in range(MINLEVEL,MAXLEVEL+1):
    with open("HSK Official With Definitions 2012 L" + str(level) + " freqorder.txt",'r',encoding='utf-8') as f:
        for i, line in enumerate(f):
            fields = line.split("\t")
            tones = [ int(c) for c in fields[2] if c.isnumeric() ]
            if WORDS:
                data.append( {"hanzi": fields[0].strip(), "pinyin": fields[3], "tones": tones, "level": level } )
            else:
                if len(tones) != len(fields[0]):
                    tones = len(fields[0]) * [0]
                for hanzi, tone in zip(fields[0],tones):
                    if hanzi not in seen:
                        data.append( {"hanzi": hanzi, "tones": [tone], "level": level } )
                        seen.add(hanzi)


try:
    COLS = int(sys.argv[1])
except:
    COLS = 15

CELLWIDTH = 64
CELLHEIGHT = 64
GRIDCOLOR = "#aaa"
TONECOLOR = {
    0: "#000", #used for unknown/ambiguous tones (multiple readings)
    1: "#600",
    2: "#660",
    3: "#060",
    4: "#006",
    5: "#606",
}
FONT = "WenQuanYi Zen Hei"



seen = set()

eof = False
c = svgwrite.Drawing(filename="hanzi.svg", profile="tiny")
row = 0
prevlevel = 0
while True:
    row += 1
    #c.add(c.line(start=(0,row * CELLHEIGHT),end=(COLS*CELLWIDTH, row * CELLHEIGHT), stroke=GRIDCOLOR))
    begin = (row-1) * COLS
    end = begin + COLS
    print(begin, end,file=sys.stderr)
    for col, index in enumerate(range(begin, end)):
        item = data[index]
        print(item,file=sys.stderr)

        if len(item['hanzi']) != len(item['tones']):
            tones = [0] * len(item['hanzi']) #unknown
        else:
            tones = item['tones']

        length = len(tones)
        fontsize = (CELLWIDTH * 0.8) / length
        x = col * CELLWIDTH + (0.1*fontsize)
        y = row * CELLHEIGHT - (0.25*fontsize)

        for i, (hanzi, tone) in enumerate(zip(item['hanzi'], tones)):
            if length > 1 and hanzi in seen:
                color = "#000"
            else:
                color = TONECOLOR[tone]
            c.add(c.text(hanzi, insert=(x+(i*fontsize),y), font_family=FONT,font_size=fontsize, fill=color, stroke=color,stroke_width=1))
            seen.add(hanzi)
        if prevlevel and prevlevel < item['level']:
            c.add(c.line(start=(0,row * CELLHEIGHT),end=(COLS*CELLWIDTH, row * CELLHEIGHT), stroke="#ff0000", stroke_width=2))

        prevlevel = item['level']
        if index == len(data)-1:
            eof = True
            break
    if eof:
        break


for col in range(1,COLS+1):
    c.add(c.line(start=(col * CELLWIDTH,0),end=(col*CELLWIDTH, row*CELLHEIGHT), stroke=GRIDCOLOR))

c.save()




