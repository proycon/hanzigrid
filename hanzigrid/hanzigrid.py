#!/usr/bin/env python3

import sys
import os
import svgwrite
import pinyin_dec
import unicodedata
import json
import argparse
import re

path = os.path.dirname(os.path.abspath(__file__))

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def loadDict(**kwargs):
    dictdata = {}
    dictwords = {}
    if kwargs.get("traditional"):
        index = 1
        altindex = 0
    else:
        index = 0
        altindex = 1
    file_list = os.listdir(os.path.join(path, "data"))
    for fn in file_list:
        with open(os.path.join(path, "data", fn),'r',encoding='utf-8') as f:
            try:
                level = int(re.search("(?<=HSK Official With Definitions 2012 L)\d", fn).group())
            except:
                level = 0 # File is not an official HSK file so there is no hsk level

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
                dictwords[fields[index]] = {
                    "hanzi": fields[index],
                    "pinyin": fields[3],
                    "level": level,
                    "description": fields[4],
                }
                for hanzi, alt, tone,singlepinyin in zip(fields[index], fields[altindex], tones, pinyin):
                    singlepinyin = singlepinyin.lower().strip("' ")
                    if hanzi not in dictdata:
                        dictdata[hanzi] = {
                            "tone": tone,
                            "level": level,
                            "pinyin": singlepinyin.strip(),
                            "words": [fields[index]],
                            "alt": alt if alt != hanzi else ""
                        }
                    else:
                        if dictdata[hanzi]['tone'] == 5:
                            dictdata[hanzi]['tone'] = tone
                            dictdata[hanzi]['pinyin'] = singlepinyin
                        elif tone != 5 and (dictdata[hanzi]['tone'] != tone or singlepinyin not in dictdata[hanzi]['pinyin'].split('/')):
                            dictdata[hanzi]['tone'] = 0
                            if singlepinyin not in dictdata[hanzi]['pinyin'].split('/'):
                                dictdata[hanzi]['pinyin'] += "/" + singlepinyin
                        dictdata[hanzi]['words'].append(fields[index])
    return dictdata, dictwords


def hanzigrid(**kwargs):
    dictdata, dictwords = loadDict(**kwargs)
    COLS = kwargs['columns']
    ROWS = kwargs['rows']
    SUBROWS = kwargs['subrows']
    WORDS = not kwargs.get('nowords')
    ALT = kwargs.get('alternative')
    HSKONLY = kwargs.get('hskonly')
    PINYIN = kwargs.get('pinyin')
    PINYINORDER = kwargs.get('pinyinorder')
    MINLEVEL = kwargs['minlevel']
    CELLWIDTH = kwargs['cellwidth']
    FONTSIZE = (CELLWIDTH * 0.8)
    SUBFONTSIZE = FONTSIZE / 2.8
    PINYINFONTSIZE = FONTSIZE / 4

    if WORDS:
        CELLHEIGHT = CELLWIDTH + SUBFONTSIZE * SUBROWS
    else:
        CELLHEIGHT = CELLWIDTH
    WIDTH = COLS * CELLWIDTH
    if ROWS:
        HEIGHT = ROWS * CELLHEIGHT
    TONECOLOR = {
        "default": {
        0: "#000", #used for unknown/ambiguous tones (multiple readings)
        1: "#800",
        2: "#880",
        3: "#080",
        4: "#008",
        5: "#000"},
        "pleco": {
        0: "#000", #used for unknown/ambiguous tones (multiple readings)
        1: "#e30000",
        2: "#01b31c",
        3: "#150ff0",
        4: "#8800bf",
        5: "#777777",
        }}
    BGCOLORS = {
        'default':
        {
            0: None,
            1: None,
            2: None,
            3: None,
            4: '#ddd',
            5: '#ffb',
            6: '#f5caca',
        },
        'grey':
        {
            0: None,
            1: None,
            2: None,
            3: None,
            4: '#ddd',
            5: '#ccc',
            6: '#aaa',
        }
    }
    FONT = kwargs['font']
    SUBFONT = kwargs['subfont']
    OUTPUTPREFIX = kwargs['outputprefix']

    bgcolorscheme = kwargs.get('bgcolor')
    colorscheme = kwargs.get('tonecolor')

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
                            if hanzi in dictdata:
                                if dictdata[hanzi]["level"] >= MINLEVEL:
                                    data.append( {"hanzi": hanzi,  "tone": dictdata[hanzi]["tone"], "pinyin": dictdata[hanzi]["pinyin"], "level": dictdata[hanzi]["level"] } )
                            elif not HSKONLY:
                                data.append( {"hanzi": hanzi,  "tone": 0, "pinyin": "", "level": 0 } )
                            seen.add(hanzi)


    if PINYINORDER:
        data = [ x for x in sorted(data, key=lambda x: strip_accents(x['pinyin']).lower())]

    for hanzi, item in dictdata.items():
        if hanzi not in seen:
            # print("NOTICE: hanzi in HSK " + str(item["level"]) + " but not in input (this is no problem): ", hanzi,file=sys.stderr)
            pass


    OUTPUTPREFIX_STRIPPED = os.path.basename(OUTPUTPREFIX)
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
                font-family: "{FONT}", sans-serif;
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
                display: inline-block;
                min-width: 150px;
                color: black;
                font-size: 150%;
                font-family: "{SUBFONT}", sans-serif;
            }}
        </style>
        <script src="{OUTPUTPREFIX_STRIPPED}.js"></script>
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
            worddata = dictwords[data[i].words[j]];
            words += "<span class='level' onclick='showextra(" + j + "); event.stopPropagation();'>(" + worddata.level + ")</span> <span class='hanzi' onclick='showextra(" + j + "); event.stopPropagation();'>" + worddata.hanzi + "</span>";
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
    datafile.write("dictwords = " + json.dumps(dictwords, ensure_ascii=False) + "\n")
    datafile.write("data = [")

    eof = False
    if not ROWS:
        c = svgwrite.Drawing(filename=OUTPUTPREFIX+".svg", profile="tiny")
        html.write("<object type=\"image/svg+xml\" data=\"" + os.path.basename(OUTPUTPREFIX) + ".svg\" id=\"page1\" onload=\"initpage(1)\"></object>\n")
    else:
        c = svgwrite.Drawing(filename=OUTPUTPREFIX+"_1.svg", viewBox=("0 0 %d %d" % (WIDTH,HEIGHT)), profile="tiny")
        html.write("<object type=\"image/svg+xml\" data=\"" + os.path.basename(OUTPUTPREFIX) + "_1.svg\" id=\"page1\" onload=\"initpage(1)\"></object>\n")
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
            html.write("<object type=\"image/svg+xml\" data=\"" + os.path.basename(OUTPUTPREFIX) + "_" + str(page) + ".svg\" id=\"page" + str(page) + "\" onload=\"initpage(" + str(page) + ")\"></object>\n")
        begin = ((page-1)*ROWS*COLS) + (row-1) * COLS
        end = begin + COLS
        for col, index in enumerate(range(begin, end)):
            item = data[index]
            hanzi = item['hanzi']
            if hanzi in dictdata:
                if dictdata[hanzi]["words"]:
                    item['words'] = dictdata[hanzi]['words']
                if dictdata[hanzi]["alt"]:
                    item['alt'] = dictdata[hanzi]['alt']
            item['seqnr'] = index
            item['row'] = row
            item['page'] = page
            print(json.dumps(item,ensure_ascii=False) + ",",file=datafile)
            if hanzi in dictdata:
                if 'words' in item: del item['words']
                if 'alt' in item: del item['alt']


            x = col * CELLWIDTH
            y = row * CELLHEIGHT -  (CELLHEIGHT-CELLWIDTH) - (0.25*FONTSIZE)

            if not kwargs.get('notones'):
                color = TONECOLOR[colorscheme][item["tone"]]
            else:
                color = "black"
            if not kwargs.get('nolevels'):
                bgcolor = BGCOLORS[bgcolorscheme][item["level"]] 
                if bgcolor is not None:
                    c.add(c.rect(insert=(x,(row-1)*CELLHEIGHT), size=(CELLWIDTH,CELLHEIGHT), fill=bgcolor))
            c.add(c.text(hanzi, insert=(x,y), font_family=FONT,font_size=FONTSIZE, fill=color, stroke=color,stroke_width=1,id="h"+ str(index)))
            if PINYIN and hanzi in dictdata and dictdata[hanzi]["pinyin"]:
                c.add(c.text(dictdata[hanzi]["pinyin"], insert=(x,y+(PINYINFONTSIZE*0.25)+PINYINFONTSIZE), font_family=FONT,font_size=PINYINFONTSIZE, fill=color, stroke=color,stroke_width=0,font_weight="normal"))
                voffset = SUBFONTSIZE
                wordlimit = SUBROWS-1
            else:
                voffset = 0
                wordlimit = SUBROWS

            if WORDS and hanzi in dictdata and dictdata[hanzi]["words"]:
                words = [ w for w in dictdata[hanzi]["words"] if len(w) > 1 and len(w) <= (3 if not ALT else 2) ]
                if kwargs['maxlevel'] > 0:
                    words = [ w for w in words if dictwords[w]['level'] <= kwargs['maxlevel'] ]
                for i, word in enumerate(words):
                    if not kwargs.get('nolevels'):
                        if word in dictwords:
                            bgcolor = BGCOLORS[bgcolorscheme][dictwords[word]['level']] 
                            if bgcolor is not None:
                                bgwidthfactor= 0.6 if ALT else 1
                                c.add(c.rect(insert=(x,y+SUBFONTSIZE*0.4+voffset+(SUBFONTSIZE*i)), size=(CELLWIDTH*bgwidthfactor,SUBFONTSIZE), fill=bgcolor, stroke=bgcolor,stroke_width=1))

                    c.add(c.text(word, insert=(x,y+SUBFONTSIZE*0.25+voffset+(SUBFONTSIZE*(i+1))), font_family=SUBFONT,font_size=SUBFONTSIZE, fill="#333", stroke="#000",stroke_width=0,font_weight="normal"))
                    if i == wordlimit - 1: break

            if ALT and hanzi in dictdata and dictdata[hanzi]["alt"]:
                altfontsize=SUBFONTSIZE*1.5
                c.add(c.text(dictdata[hanzi]['alt'], insert=(x+(CELLWIDTH-altfontsize),y+(SUBFONTSIZE*0.25)+(SUBFONTSIZE*1.05)), font_family=FONT,font_size=altfontsize, fill="#d45500", stroke=color,stroke_width=0,font_weight="normal"))


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
    parser.add_argument('--subfont', type=str,help="The font", action='store',default="sans")
    parser.add_argument('-o','--outputprefix', type=str,help="Output prefix", action='store',default="hanzigrid")
    parser.add_argument('--tonecolor', type=str ,help="Choose tonecolor: ['default', 'pleco']", action='store', default='default')
    parser.add_argument('--bgcolor', type=str, help="Choose background: ['default', 'grey']", action='store', default='default')
    parser.add_argument('--cellwidth',type=int,help="The width of a cell in pixels (determines resolution)", action='store',default=128)
    parser.add_argument('--columns',type=int,help="Number of columns", action='store',default=15)
    parser.add_argument('--rows',type=int,help="Maximum number of rows per page/image, if the number is exceeded a new image/page will be started (defaults to 0 meaning unlimited)", action='store',default=0)
    parser.add_argument('--subrows',type=int,help="Number of rows for words", action='store',default=2)
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

