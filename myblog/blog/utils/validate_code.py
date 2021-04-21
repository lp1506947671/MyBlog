#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont


def gen_random_color():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


def gen_random_chr():
    random_num = str(random.randint(0, 9))
    random_low = chr(random.randint(95, 122))
    random_upper = chr(random.randint(65, 90))
    return random.choice([random_num, random_low, random_upper])


def gen_valid_code(request):
    """
            构造验证码数据
            1.设置长宽
            2.Image.new:构造图像,设置格式RGB,大小,颜色
            3.ImageDraw.Draw:创建Draw对象
            4.ImageFont.truetype创建Font对象,设置字体类型,字体大小
            5.Draw.text循环生成5个字符并将它写在背景上,设置颜色,字体和位置
            6.构建噪点
                1.构建噪点线:Draw.line(())
                2.构建噪点:Draw.point([])
                          Draw.arc()
            7.把字节存在内存中BytesIo
    """

    width = 270
    height = 40
    img = Image.new("RGB", (width, height), gen_random_color())
    draw = ImageDraw.Draw(img)
    my_font = ImageFont.truetype(font="static/font/kumo.ttf", size=32)
    valid_code_str = ''
    for i in range(5):
        random_chr = gen_random_chr()
        draw.text(xy=(i * 50 + 20, 0), text=random_chr, fill=gen_random_color(), font=my_font)
        valid_code_str += random_chr
    request.session["valid_code_str"] = valid_code_str
    print(valid_code_str)
    for j in range(10):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=gen_random_color())
    for x in range(100):
        x3 = random.randint(0, width)
        x4 = random.randint(0, width)
        y3 = random.randint(0, height)
        y4 = random.randint(0, height)
        draw.point([x3, y3], fill=gen_random_color())
        draw.arc((x4, y4, x4 + 4, y4 + 4), 0, 90, fill=gen_random_color())
    f = BytesIO()
    img.save(f, "png")
    data = f.getvalue()
    return data
