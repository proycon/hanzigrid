#!/usr/bin/env python3

import sys
import os
import svgwrite
import pinyin_dec
import unicodedata
import json
import argparse


path = os.path.dirname(os.path.abspath(__file__))

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def loadhsk(**kwargs):
    hskdata = {}
    hskwords = {}
    if kwargs.get("traditional"):
        index = 1
        altindex = 0
    else:
        index = 0
        altindex = 1
    for level in range(1,7):
        with open(os.path.join(path, "data", "HSK Official With Definitions 2012 L" + str(level) + " freqorder.txt"),'r',encoding='utf-8') as f:
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
                    tones = len(fields[index]) * [5]
                hskwords[fields[index]] = {
                    "hanzi": fields[index],
                    "pinyin": fields[3],
                    "level": level,
                    "description": fields[4],
                }
                for hanzi, alt, tone,singlepinyin in zip(fields[index], fields[altindex], tones, pinyin):
                    singlepinyin = singlepinyin.lower().strip("' ")
                    if hanzi not in hskdata:
                        hskdata[hanzi] = {
                            "tone": tone,
                            "level": level,
                            "pinyin": singlepinyin.strip(),
                            "words": [fields[index]],
                            "alt": alt if alt != hanzi else ""
                        }
                    else:
                        if hskdata[hanzi]['tone'] == 5:
                            hskdata[hanzi]['tone'] = tone
                            hskdata[hanzi]['pinyin'] = singlepinyin
                        elif tone != 5 and (hskdata[hanzi]['tone'] != tone or singlepinyin not in hskdata[hanzi]['pinyin'].split('/')):
                            hskdata[hanzi]['tone'] = 0
                            if singlepinyin not in hskdata[hanzi]['pinyin'].split('/'):
                                hskdata[hanzi]['pinyin'] += "/" + singlepinyin
                        hskdata[hanzi]['words'].append(fields[index])
    return hskdata, hskwords


def hanzigrid(**kwargs):
    hskdata, hskwords = loadhsk(**kwargs)
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
    WIDTH = COLS * CELLWIDTH
    if ROWS:
        HEIGHT = ROWS * CELLHEIGHT
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
        if not os.path.exists(filename) and filename[0] != '/':
            print("File not found in current working directory, falling back to input directory...",file=sys.stderr)
            filename = os.path.join(path,"input", filename)
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


    html =  open(OUTPUTPREFIX+".html",'w',encoding='utf-8')
    html.write(f"""<!DOCTYPE HTML>
<html>
    <head>
        <title>Hanzi Grid</title>
        <meta name="generator" content="hanzigrid" />
        <meta charset="utf-8" />
        <style>
            object {{
                margin: 0px;
                padding: 0px;
                width: 100%;
                height: 100%;
            }}
            #info {{
                position: fixed;
                background: white;
                display: none;
                top: 25px;
                left: 25px;
                width: 90%;
                opacity: 0.9;
                border: 2px black solid;
                font-size: 2em;
            }}
            #hanzi {{
                width: 100%;
                text-align: center;
                background: black;
                color: white;
                font-weight: bold;
            }}
            #info .level {{
               font-size: 50%;
               font-weight: normal;
            }}
            #info .description {{
                font-style: italic;
            }}
            #info .hidden {{
                visibility: hidden;
            }}
            #words {{
                color: #666;
            }}
            #words .hanzi {{
                color: black;
            }}
        </style>
        <script src="{OUTPUTPREFIX}.js"></script>
        <script
          src="https://code.jquery.com/jquery-3.4.1.min.js"
          integrity="sha256-CSXorXvZcTkaix6Yvo6HppcZGetbYMGWSFlBw8HfCJo="
          crossorigin="anonymous"></script>
        <script>
function initpage(page) {{
    if (data == null) {{
        window.setTimeout(function(){{initpage(page)}}, 500);
        return;
    }}
    var i = 0;
    for (i = 0; i < data.length; i++) {{
        var page = $('#page' + data[i].page)[0];
        // Get the SVG document inside the Object tag
        var svgdoc = page.contentDocument;
        // Get the hanzi by ID
        var hanzi = svgdoc.getElementById("h" + i);
        if (hanzi !== null) {{
            hanzi.index = i;
            hanzi.addEventListener("click", showinfo, false);
        }}
    }}
}};

function showinfo(event) {{
        var i = event.currentTarget.index;
        $('#hanzi').html(data[i].hanzi + " <span class='level'>(HSK" + data[i].level + ")</span>");
        $('#pinyin').html(data[i].pinyin);
        $('#description').html(data[i].description);
        var words = "";
        for (j = 0; j < data[i].words.length; j++) {{
            worddata = hskwords[data[i].words[j]];
            words += "<span class='level'>(" + worddata.level + ")</span> <span class='hanzi' onclick='showextra(" + j + "); event.stopPropagation();'>" + worddata.hanzi + "</span>";
            var cls = "pinyin";
            if (!infopinyin) cls += " hidden";
            words += "<span class='" + cls + "' id='pinyin" + j + "'> - " + worddata.pinyin + "</span>";
            var cls = "description";
            if (!infotranslation) cls += " hidden";
            words += "<span class='" + cls + "' id='description" + j +"'> - " + worddata.description + "</span>";
            words += "<br/>";
        }}
        $('#words').html(words);
        $("#info").show();
}};

function showextra(i) {{
    $("#pinyin" + i).removeClass("hidden");
    $("#description" + i).removeClass("hidden");
}}

infopinyin=false;
infotranslation=false;

$(function() {{
    $('#infopinyin').click(function() {{
        if ($('#infopinyin').is(':checked')) {{
            infopinyin = true;
        }} else {{
            infopinyin = false;
        }}
        if ($('#infotranslation').is(':checked')) {{
            infotranslation = true;
        }} else {{
            infotranslation = false;
        }}
    }});
}});
    </script>
    </head>
    <body>
<div id="info" onclick="$('#info').hide();">
    <div id="hanzi">
    </div>
    <div id="pinyin">
    </div>
    <div id="description">
    </div>
    <div id="level">
    </div>
    <div id="description">
    </div>
    <div id="words">
    </div>
</div>
""")

    datafile =  open(OUTPUTPREFIX+".js",'w',encoding='utf-8')
    datafile.write("hskwords = " + json.dumps(hskwords, ensure_ascii=False) + "\n")
    datafile.write("data = [")

    eof = False
    if not ROWS:
        c = svgwrite.Drawing(filename=OUTPUTPREFIX+".svg", profile="tiny")
        html.write("<object type=\"image/svg+xml\" data=\"" + OUTPUTPREFIX + ".svg\" id=\"page1\" onload=\"initpage(1)\"></object>\n")
    else:
        c = svgwrite.Drawing(filename=OUTPUTPREFIX+"_1.svg", viewBox=("0 0 %d %d" % (WIDTH,HEIGHT)), profile="tiny")
        html.write("<object type=\"image/svg+xml\" data=\"" + OUTPUTPREFIX + "_1.svg\" id=\"page1\" onload=\"initpage(1)\"></object>\n")
    row = 0
    page = 1 if ROWS else 0
    while True:
        row += 1
        if ROWS and row > ROWS:
            row = 1
            page += 1
            print("PAGE " + str(page),file=sys.stderr)
            if c:
                c.save()
                c = None
            c = svgwrite.Drawing(filename=OUTPUTPREFIX+"_" + str(page) + ".svg", viewBox=("0 0 %d %d" % (WIDTH,HEIGHT)), profile="tiny")
            html.write("<object type=\"image/svg+xml\" data=\"" + OUTPUTPREFIX + "_" + str(page) + ".svg\" id=\"page" + str(page) + "\" onload=\"initpage(" + str(page) + ")\"></object>\n")
        begin = ((page-1)*ROWS*COLS) + (row-1) * COLS
        end = begin + COLS
        for col, index in enumerate(range(begin, end)):
            item = data[index]
            hanzi = item['hanzi']
            if hanzi in hskdata:
                if hskdata[hanzi]["words"]:
                    item['words'] = hskdata[hanzi]['words']
                if hskdata[hanzi]["alt"]:
                    item['alt'] = hskdata[hanzi]['alt']
            item['seqnr'] = index
            item['row'] = row
            item['page'] = page
            print(json.dumps(item,ensure_ascii=False) + ",",file=datafile)
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
            c.add(c.text(hanzi, insert=(x,y), font_family=FONT,font_size=fontsize, fill=color, stroke=color,stroke_width=1,id="h"+ str(index)))
            subfontsize = fontsize / 2.8
            if PINYIN and hanzi in hskdata and hskdata[hanzi]["pinyin"]:
                c.add(c.text(hskdata[hanzi]["pinyin"], insert=(x,y+(subfontsize*0.25)+subfontsize), font_family=FONT,font_size=subfontsize, fill=color, stroke=color,stroke_width=0,font_weight="normal"))
                voffset = subfontsize
                wordlimit = 1
            else:
                voffset = 0
                wordlimit = 2

            if WORDS and hanzi in hskdata and hskdata[hanzi]["words"]:
                words = [ w for w in hskdata[hanzi]["words"] if len(w) > 1 and len(w) <= (2 if not ALT else 2) ]
                if kwargs['maxlevel'] > 0:
                    words = [ w for w in words if hskwords[w]['level'] <= kwargs['maxlevel'] ]
                for i, word in enumerate(words):
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
    datafile.write("];\n")
    html.write("""
<div class="buttons">
Info: pinyin? <input type="checkbox" id="infopinyin" name="infopinyin" /> | translations? <input type="checkbox" id="infotranslation" name="infotranslation" />
</div>
""")
    html.write("</body>")
    html.write("</html>")

def main():
    parser = argparse.ArgumentParser(description="Create a hanzi learning grid", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--font', type=str,help="The font", action='store',default="sans")
    parser.add_argument('-o','--outputprefix', type=str,help="Output prefix", action='store',default="hanzigrid")
    parser.add_argument('--cellwidth',type=int,help="The width of a cell in pixels (determines resolution)", action='store',default=128)
    parser.add_argument('--columns',type=int,help="Number of columns", action='store',default=15)
    parser.add_argument('--rows',type=int,help="Maximum number of rows per page/image, if the number is exceeded a new image/page will be started (defaults to 0 meaning unlimited)", action='store',default=0)
    parser.add_argument('--nowords',help="Don't add example words from HSK", action='store_true')
    parser.add_argument('--nolevels',help="Don't distinguish HSK levels", action='store_true')
    parser.add_argument('--notones',help="No tone colours", action='store_true')
    parser.add_argument('--pinyin',help="Add pinyin", action='store_true')
    parser.add_argument('--pinyinorder',help="Order by pinyin", action='store_true')
    parser.add_argument('--hskonly',help="Do not include hanzi hanzi not in HSK", action='store_true')
    parser.add_argument('-t','--traditional',help="Use traditional hanzi instead of simplified", action='store_true')
    parser.add_argument('-a','--alternative',help="Show alternative hanzi (traditional/simplified)", action='store_true')
    parser.add_argument('--minlevel',type=int,help="Minimum HSK level", action='store',default=0)
    parser.add_argument('--maxlevel',type=int,help="Maximum HSK level", action='store',default=0)
    parser.add_argument('inputfiles', nargs='+', help='A file with hanzi')
    args = parser.parse_args()
    hanzigrid(**args.__dict__)

if __name__ == '__main__':
    main()

