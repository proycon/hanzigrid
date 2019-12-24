#!/usr/bin/env python3

import sys
import svgwrite
import pinyin_dec
import unicodedata

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def loadhsk(**kwargs):
    hskdata = {}
    if kwargs.get("traditional"):
        index = 1
        altindex = 0
    else:
        index = 0
        altindex = 1
    for level in range(1,7):
        with open("HSK Official With Definitions 2012 L" + str(level) + " freqorder.txt",'r',encoding='utf-8') as f:
            for line in f:
                fields = line.split("\t")
                pinyin = []
                tones = []
                begin = 0
                for i, c in enumerate(fields[2]):
                    if c.isnumeric():
                        tones.append(int(c))
                        pinyin.append( pinyin_dec.fix_pinyin_word(fields[2][begin:i+1]))
                        begin = i+1
                if len(tones) != len(fields[index]):
                    tones = len(fields[index]) * [0]
                for hanzi, alt, tone,pinyin in zip(fields[index], fields[altindex], tones, pinyin):
                    if hanzi not in hskdata:
                        hskdata[hanzi] = {
                            "tone": tone,
                            "level": level,
                            "pinyin": pinyin.strip(),
                            "words": [fields[index]],
                            "alt": alt if alt != hanzi else ""
                        }
                    else:
                        if hskdata[hanzi]['tone'] in (0,5):
                            hskdata[hanzi]['tone'] = tone
                            hskdata[hanzi]['pinyin'] = pinyin
                        hskdata[hanzi]['words'].append(fields[index])
    return hskdata


def hanzigrid(**kwargs):
    hskdata = loadhsk(**kwargs)
    COLS = kwargs['columns']
    ROWS = kwargs['rows']
    WORDS = not kwargs.get('nowords')
    ALT = kwargs.get('alternative')
    HSKONLY = kwargs.get('hskonly')
    PINYIN = kwargs.get('pinyin')
    PINYINORDER = kwargs.get('pinyinorder')
    MINLEVEL = kwargs['minlevel']
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
    OUTPUTPREFIX = kwargs['outputprefix']


    data = []
    seen = set()
    for filename in kwargs['inputfiles']:
        with open(filename,'r',encoding='utf-8') as f:
            for line in f:
                for hanzi in line.strip().split("\t"):
                    for hanzi in hanzi: #extra level needed if input consists of multiple connected hanzi
                        hanzi = hanzi.strip()
                        if hanzi:
                            if hanzi in seen:
                                #duplicate
                                continue
                            if hanzi in hskdata:
                                if hskdata[hanzi]["level"] >= MINLEVEL:
                                    data.append( {"hanzi": hanzi,  "tone": hskdata[hanzi]["tone"], "pinyin": hskdata[hanzi]["pinyin"], "level": hskdata[hanzi]["level"] } )
                            elif not HSKONLY:
                                data.append( {"hanzi": hanzi,  "tone": 0, "pinyin": "", "level": 0 } )
                            seen.add(hanzi)


    if PINYINORDER:
        data = [ x for x in sorted(data, key=lambda x: strip_accents(x['pinyin']).lower())]

    for hanzi, item in hskdata.items():
        if hanzi not in seen:
            print("NOTICE: hanzi in HSK " + str(item["level"]) + " but not in input (this is no problem): ", hanzi,file=sys.stderr)


    eof = False
    c = None
    if not ROWS:
        c = svgwrite.Drawing(filename=OUTPUTPREFIX+".svg", profile="tiny")
    row = 0
    page = 0
    while True:
        row += 1
        if ROWS and (row-1) % ROWS == 0:
            page += 1
            if c:
                c.save()
                c = None
            c = svgwrite.Drawing(filename=OUTPUTPREFIX+"_" + str(page) + ".svg", profile="tiny")
        begin = (row-1) * COLS
        end = begin + COLS
        print(begin, end,file=sys.stderr)
        for col, index in enumerate(range(begin, end)):
            item = data[index]
            if hanzi in hskdata:
                if hskdata[hanzi]["words"]:
                    item['words'] = hskdata[hanzi]['words']
                if hskdata[hanzi]["alt"]:
                    item['alt'] = hskdata[hanzi]['alt']
            print(item,file=sys.stderr)
            if hanzi in hskdata:
                if 'words' in item: del item['words']
                if 'alt' in item: del item['alt']


            fontsize = (CELLWIDTH * 0.8)
            x = col * CELLWIDTH + (0.25*fontsize)
            y = row * CELLHEIGHT -  (CELLHEIGHT-CELLWIDTH) - (0.25*fontsize)

            if not kwargs.get('notones'):
                color = TONECOLOR[item["tone"]]
            else:
                color = "black"
            if not kwargs.get('nolevels'):
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
            subfontsize = fontsize / 2.8
            if PINYIN and hanzi in hskdata and hskdata[hanzi]["pinyin"]:
                c.add(c.text(hskdata[hanzi]["pinyin"], insert=(x,y+(subfontsize*0.25)+subfontsize), font_family=FONT,font_size=subfontsize, fill=color, stroke=color,stroke_width=0,font_weight="normal"))
                voffset = subfontsize
                wordlimit = 1
            else:
                voffset = 0
                wordlimit = 2

            if WORDS and hanzi in hskdata and hskdata[hanzi]["words"]:
                for i, word in enumerate([ w for w in hskdata[hanzi]["words"] if len(w) > 1 and len(w) <= (2 if not ALT else 2) ]):
                    c.add(c.text(word, insert=(x,y+subfontsize*0.25+voffset+(subfontsize*(i+1))), font_family=FONT,font_size=subfontsize, fill="#333", stroke="#000",stroke_width=0,font_weight="normal"))
                    if i == wordlimit - 1: break

            if ALT and hanzi in hskdata and hskdata[hanzi]["alt"]:
                c.add(c.text(hskdata[hanzi]['alt'], insert=(x+(CELLWIDTH-subfontsize),y+(subfontsize*0.25)+(subfontsize*2)), font_family=FONT,font_size=subfontsize, fill=color, stroke=color,stroke_width=0,font_weight="normal"))


            if index == len(data)-1:
                eof = True
                break
        if eof:
            break

    if c:
        c.save()


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Create a hanzi learning grid", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--font', type=str,help="The font", action='store',default="sans")
    parser.add_argument('-o','--outputprefix', type=str,help="Output prefix", action='store',default="hanzigrid")
    parser.add_argument('--cellwidth',type=int,help="The width of a cell in pixels (determines resolution)", action='store',default=128)
    parser.add_argument('--columns',type=int,help="Number of columns", action='store',default=15)
    parser.add_argument('--rows',type=int,help="Number of rows per page/image, if the number is exceeded a new image/page will be started (defaults to 0 meaning unlimited)", action='store',default=0)
    parser.add_argument('--nowords',help="Don't add example words from HSK", action='store_true')
    parser.add_argument('--nolevels',help="Don't distinguish HSK levels", action='store_true')
    parser.add_argument('--notones',help="No tone colours", action='store_true')
    parser.add_argument('--pinyin',help="Add pinyin", action='store_true')
    parser.add_argument('--pinyinorder',help="Order by pinyin", action='store_true')
    parser.add_argument('--hskonly',help="Do not include hanzi hanzi not in HSK", action='store_true')
    parser.add_argument('-t','--traditional',help="Use traditional hanzi instead of simplified", action='store_true')
    parser.add_argument('-a','--alternative',help="Show alternative hanzi (traditional/simplified)", action='store_true')
    parser.add_argument('--minlevel',type=int,help="Minimum HSK level", action='store',default=0)
    parser.add_argument('inputfiles', nargs='+', help='A file with hanzi')
    args = parser.parse_args()
    #args.storeconst, args.dataset, args.num, args.bar
    hanzigrid(**args.__dict__)




