import redis
import json
import logging
from PIL import Image, ImageDraw, ImageFont
from io import StringIO, BytesIO
from sanic import Sanic, response
from sanic_jinja2 import SanicJinja2
from acronym import WordList, Phrase

N_DATASET = "data/N_1M_clean.csv"
word_list = WordList(N_DATASET)

app = Sanic(name="Akronymisierungstool")
jinja = SanicJinja2(app, pkg_name="app")


r = redis.StrictRedis(
    host="localhost", 
    port=6379, 
    db=0,
    charset="utf-8", 
    decode_responses=True)


def build_title_html(phrase, acronym):
    html = ""

    if acronym.positions[0] == 0:
        html += "<span class='highlight'>"

    for i, c in enumerate(phrase.s):
        html += c
        if i in acronym.positions:
            html += "</span>"
        if i+1 in acronym.positions:
            html += "<span class='highlight'>"
    return "<span class='highlight'>{}</span> - {}".format(acronym.word.value.upper(), html)


def get_acronyms(title):
    results = []
    if len(title.split()) > 1:
        
        if not r.exists(title):

            p = Phrase(title)
            p.find_acronyms(word_list)
            
            for i, acronym in enumerate(p.acronyms[:100]):
                results.append({
                    "rank": i+1,
                    "acronym": acronym.word.value.upper(),
                    "score": acronym.score,
                    "html": build_title_html(p, acronym),
                    "positions": acronym.positions
                })
            r.set(title, json.dumps(results))
        
        else:
            logging.info("retrieve results from redis")
            results = json.loads(r.get(title))

    return results


@app.route("/<title>/<n>.png")
async def result_card(request, title, n):
    results = get_acronyms(title)
    n = int(n)
    if n > 0 and n <= len(results):

        data = results[n-1]

        acronym = data["acronym"]

        img = Image.new('RGB', (876, 438), (15, 30, 60))
        draw = ImageDraw.Draw(img)

        # print acronym
        font = ImageFont.truetype("Merriweather-Bold.ttf", size=45)
        (x,y) = (50, 80)
        color = 'rgb(255, 120, 120)'
        draw.text((x,y), acronym, fill=color, font=font)

        # print full title
        x_offset = 50
        y_offset = y + 90

        font = ImageFont.truetype("Merriweather-Bold.ttf", size=35)

        index = 0
        for word in title.split():
            
            # check if word is too long for current line
            word_width = draw.textsize(word, font=font)[0]
            if x_offset + word_width > 826:
                x_offset = 50
                y_offset += 55
            
            # print word character by character
            for char in word:
                char_width = draw.textsize(char, font=font)[0]

                if index in data["positions"]:
                    color = 'rgb(255, 120, 120)'
                else:
                    color = 'rgb(240, 240, 240)'

                draw.text((x_offset, y_offset), char, fill=color, font=font)
                x_offset += char_width
                index += 1

            # add blank on the end of the word
            draw.text((x_offset, y_offset), " ", fill=color, font=font)
            x_offset += draw.textsize(" ", font=font)[0]
            index += 1

        # serve image as bytestream
        img_io = BytesIO()
        img.save(img_io, 'PNG', quality=70)
        img_io.seek(0)
        return response.raw(img_io.getvalue(), content_type='image/png')

    else:
        return response.json({})

@app.route("/<title>")
async def index(request, title):        
    results = get_acronyms(title)

    return jinja.render("index.html", request, title=title, results=results)


if __name__ ==  "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)