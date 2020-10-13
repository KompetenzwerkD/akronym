from sanic import Sanic, response
from sanic_jinja2 import SanicJinja2
from acronym import WordList, Phrase

N_DATASET = "data/N_1M_clean.csv"
word_list = WordList(N_DATASET)

app = Sanic(name="Akronymisierungstool")
jinja = SanicJinja2(app, pkg_name="app")


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



@app.route("/")
async def index(request):

    results = []
    title = ""

    if "title" in request.args:
        title = request.args["title"][0]
        if len(title.split()) > 1:
            
            p = Phrase(title)
            p.find_acronyms(word_list)
            
            for i, acronym in enumerate(p.acronyms[:50]):
                results.append({
                    "rank": i+1,
                    "acronym": acronym.word.value.upper(),
                    "score": acronym.score,
                    "html": build_title_html(p, acronym)
                })

    return jinja.render("index.html", request, title=title, results=results)


if __name__ ==  "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)