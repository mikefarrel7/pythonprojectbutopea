from flask import Flask, render_template
from xml.etree import ElementTree as ET
import sqlite3
import html

conn = sqlite3.connect("data.sqlite")

cursor = conn.execute("SELECT distinct a.product_id, a.model, b.description, a.image as image_link, a.status, a.price, d.name as brand FROM product as a, product_description as b,product_image as c, manufacturer as d WHERE a.product_id = b.product_id and a.product_id = c.product_id and a.manufacturer_id = d.manufacturer_id and a.status='1'")

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

top = ET.Element('channel')

title = ET.SubElement(top,"title")
title.text = "Butopea.com Feed"

link = ET.SubElement(top,"link")
link.text = "http://www.butopea.com"

description = ET.SubElement(top,"description")
description.text = "Butopea Product"

for row in cursor:
    item = ET.SubElement(top,"item")
    id = ET.SubElement(item,"id")
    id.text = row[0]
    title = ET.SubElement(item,"title")
    title.text = row[1]
    description = ET.SubElement(item,"description")
    description.text = html.escape(row[2])
    link = ET.SubElement(item,"link")
    link.text = "https://butopea.com/p/"+row[0]
    imagelink = ET.SubElement(item,"image_link")
    imagelink.text = "https://butopea.com/"+row[3]
    condition = ET.SubElement(item,"condition")
    condition.text = "New"
    availability = ET.SubElement(item,"availability")
    availability.text = "updated stock"
    price = ET.SubElement(item,"price")
    price.text = row[5] + "  Ft"


xml_file = ET.ElementTree(top)
xml_file.write("./static/feed.xml",xml_declaration=True,encoding='utf-8',method="xml")


if __name__ == "__main__":
    app.run(debug=True)