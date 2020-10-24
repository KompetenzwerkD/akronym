from PIL import Image, ImageFont, ImageDraw

def create_card(title):
    acronym = title.split(" - ")[0]
    acronym = acronym.replace("<span class='highlight'>", "").replace("</span>", "")

    title = title.split(" - ")[-1]
    print(title.split("</span>"))

    img = Image.new('RGB', (876, 438), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("Merriweather-Bold.ttf", size=45)

    (x,y) = (50, 50)
    
    color = 'rgb(0, 0, 0)'

    draw.text((x,y), acronym, fill=color, font=font)

    #img.save('test.png')
    img.show("test-image")



if __name__ == "__main__":

    create_card("<span class='highlight'>SCHWECHEL</span> - <span class='highlight'>S</span>ä<span class='highlight'>c</span><span class='highlight'>h</span>sische Akademie der <span class='highlight'>W</span>iss<span class='highlight'>e</span>ns<span class='highlight'>c</span><span class='highlight'>h</span>aft<span class='highlight'>e</span>n zu <span class='highlight'>L</span>eipzig")