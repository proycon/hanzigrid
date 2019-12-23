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







hskdata = {}
for level in range(1,7):
    with open("HSK Official With Definitions 2012 L" + str(level) + " freqorder.txt",'r',encoding='utf-8') as f:
        for line in f:
            fields = line.split("\t")
            tones = [ int(c) for c in fields[2] if c.isnumeric() ]
            if len(tones) != len(fields[0]):
                tones = len(fields[0]) * [0]
            for hanzi, tone in zip(fields[0],tones):
                if hanzi not in hskdata or hskdata[hanzi]['tone'] in (0,5):
                    hskdata[hanzi] =  {"tone": tone, "level": level, "words": [fields[0]] }
                else:
                    hskdata[hanzi]['words'].append(fields[0])





def hanzigrid(**kwargs):
    COLS = kwargs['columns']
    WORDS = kwargs['words']
    CELLWIDTH = kwargs['cellwidth']
    if WORDS:
        CELLHEIGHT = CELLWIDTH + CELLWIDTH / 2
    else:
        CELLHEIGHT = CELLWIDTH
    TONECOLOR = {
        0: "#000", #used for unknown/ambiguous tones (multiple readings)
        1: "#800",
        2: "#880",
        3: "#080",
        4: "#008",
        5: "#000",
    }
    FONT = kwargs['font']


    data = []
    seen = set()
    for filename in kwargs['inputfiles']:
        with open(filename,'r',encoding='utf-8') as f:
            for line in f:
                for hanzi in line.strip().split("\t"):
                    if hanzi.strip():
                        hanzi = hanzi.strip()
                        if hanzi in seen:
                            #duplicate
                            continue
                        if hanzi in hskdata:
                            data.append( {"hanzi": hanzi,  "tone": hskdata[hanzi]["tone"], "level": hskdata[hanzi]["level"] } )
                        else:
                            data.append( {"hanzi": hanzi,  "tone": 0, "level": 0 } )
                        seen.add(hanzi)

    for hanzi, item in hskdata.items():
        if hanzi not in seen:
            print("NOTICE: hanzi in HSK " + str(item["level"]) + " but not in confusibles (this is no problem): ", hanzi,file=sys.stderr)

    eof = False
    c = svgwrite.Drawing(filename="hanzi.svg", profile="tiny")
    row = 0
    while True:
        row += 1
        #c.add(c.line(start=(0,row * CELLHEIGHT),end=(COLS*CELLWIDTH, row * CELLHEIGHT), stroke=GRIDCOLOR))
        begin = (row-1) * COLS
        end = begin + COLS
        print(begin, end,file=sys.stderr)
        for col, index in enumerate(range(begin, end)):
            item = data[index]
            print(item,file=sys.stderr)


            fontsize = (CELLWIDTH * 0.8)
            x = col * CELLWIDTH + (0.25*fontsize)
            y = row * CELLHEIGHT -  (CELLHEIGHT-CELLWIDTH) - (0.25*fontsize)

            color = TONECOLOR[item["tone"]]
            if item["level"] == 0:
                c.add(c.rect(insert=(x,(row-1)*CELLHEIGHT), size=(CELLWIDTH,CELLHEIGHT), fill="#aaa"))
            if item["level"] == 6:
                c.add(c.rect(insert=(x,(row-1)*CELLHEIGHT), size=(CELLWIDTH,CELLHEIGHT), fill="#fbb"))
            if item["level"] == 5:
                c.add(c.rect(insert=(x,(row-1)*CELLHEIGHT), size=(CELLWIDTH,CELLHEIGHT), fill="#ffb"))
            if item["level"] == 4:
                c.add(c.rect(insert=(x,(row-1)*CELLHEIGHT), size=(CELLWIDTH,CELLHEIGHT), fill="#ddd"))
            hanzi = item["hanzi"]
            c.add(c.text(hanzi, insert=(x,y), font_family=FONT,font_size=fontsize, fill=color, stroke=color,stroke_width=1))
            if WORDS and hanzi in hskdata and hskdata[hanzi]["words"]:
                subfontsize = fontsize / 2.8
                for i, word in enumerate([ w for w in hskdata[hanzi]["words"] if len(w) > 1 and len(w) <= 3 ]):
                    print(word,file=sys.stderr)
                    c.add(c.text(word, insert=(x,y+subfontsize*0.25+(subfontsize*(i+1))), font_family=FONT,font_size=subfontsize, fill="#333", stroke="#000",stroke_width=0,font_weight="normal"))
                    if i == 1: break


            if index == len(data)-1:
                eof = True
                break
        if eof:
            break

    c.save()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Create a hanzi learning grid", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--font', type=str,help="The font", action='store',default="sans")
    parser.add_argument('--cellwidth',type=int,help="The width of a cell in pixels (determines resolution)", action='store',default=128)
    parser.add_argument('--columns',type=int,help="Number of columns", action='store',default=15)
    parser.add_argument('-w','--words',help="Add example words from HSK", action='store_true',default=True)
    parser.add_argument('inputfiles', nargs='+', help='A file with hanzi')
    args = parser.parse_args()
    #args.storeconst, args.dataset, args.num, args.bar
    hanzigrid(**args.__dict__)




