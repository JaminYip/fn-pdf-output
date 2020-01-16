# -*- coding:utf-8 -*-

from PIL import Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# fonts
P_MEDIUM = "./fonts/GenShinGothic-P-Medium.ttf"
pdfmetrics.registerFont(TTFont('P_MEDIUM', P_MEDIUM))

# page size
PAGE_WIDTH = 21.0
PAGE_HEIGHT = 29.7


# pdfを作成する
def create_pdf(pdf_filename):
    # configuration
    c = canvas.Canvas('./' + pdf_filename, pagesize=A4)  # キャンバスの初期化
    c.setTitle(pdf_filename)
    c.setAuthor('')
    c.setSubject('')
    c.setCreator('')
    c.setProducer('')

    # 文字
    c.setFont('P_MEDIUM', 18)
    c.drawString((PAGE_WIDTH / 5) * cm, (PAGE_HEIGHT - 3) * cm, 'pdfサンプル', charSpace=1.0)  # Canvas.drawString(x, y, text)

    # 線
    p = c.beginPath()
    p_length = 7.0  # 線長さ
    p.moveTo((PAGE_WIDTH / 2 - p_length) * cm, (PAGE_HEIGHT - 3.5) * cm)  # path_object.moveTo(x,y)
    p.lineTo((PAGE_WIDTH / 2 + p_length) * cm, (PAGE_HEIGHT - 3.5) * cm)  # path_object.lineTo(x,y)
    c.setStrokeColorRGB(255 / 256, 140 / 256, 0 / 256)
    c.drawPath(p)

    # 画像
    image = Image.open('./images/teo.jpg')
    c.drawInlineImage(image, (PAGE_WIDTH / 2 - 6.0) * cm, 7.0 * cm, width=345.6, height=460.8)

    # pdfを保存する
    c.save()
