import json, re, csv, urllib, os
import urllib.request
from sys import platform
from urllib.parse import quote, unquote
import pinyin_dec

if platform == "darwin":
    import certifi
import pinyin

def getCharacter(character): 
    fields = ["string", "kMandarin", "kDefinition", "kTraditionalVariant"]
    url_radicals = f"http://ccdb.hemiola.com/characters/string/{quote(character)}?fields={','.join(fields)}"
    if platform == "darwin":
        json_file = urllib.request.urlopen(url_radicals, cafile=certifi.where()).read()
    else:
        json_file = urllib.request.urlopen(url_radicals).read()

    data = json.loads(json_file)[0]
    if data['kTraditionalVariant']:
        tmp = data['kTraditionalVariant'][2:]
        data["kTraditionalVariant"] = chr(int(tmp, 16))
    else:
        data["kTraditionalVariant"] = data["string"]
    data["kMandarin"] = "/".join(data["kMandarin"].lower().split(" "))
    return data

if __name__ == "__main__":
    """Takes the character list from /input/non_hsk_characters.txt and gets
    simplified char., traditional char., pinyin and definition of this characters.
    Uses the API from ccdb.hemiola.com. Saves the data in data/other_vocabs.txt."""
    
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, "input", "non_hsk_characters.txt"), "r", encoding="UTF8") as csvfile:
        rows = csv.reader(csvfile, delimiter="\t")
        data = []
        for r in rows:
            data.append(getCharacter(r[0]))
    with open(os.path.join(path, "data", "other_vocabs.txt"), 'w', newline='', encoding="UTF8") as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for d in data:
            tmp = "/".join([pinyin_dec.fix_pinyin_word(x) for x in d["kMandarin"].lower().split("/")])

            writer.writerow([d["string"], d["string"], d["kMandarin"].lower(), tmp, d["kDefinition"]])
