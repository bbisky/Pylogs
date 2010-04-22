#coding=utf-8
from django.http import HttpResponse
import md5
import cStringIO
import Image, ImageDraw, ImageFont, random 
from datetime import datetime
from os import path
def get_validatecode_img(request):
    IMG_W = 100
    IMG_H = 35
    FONT_FILE = path.join(path.dirname(__file__),'actionj.ttf')
    #im = Image.open(image)
    im = Image.new('RGBA',(IMG_W ,IMG_H),'#efefef')
    
    
    mp = md5.new()   
    mp_src = mp.update(str(datetime.now()))   
    mp_src = mp.hexdigest()   
    rand_str = mp_src[0:4]
    
    img_text0 =  Image.new('RGBA',(IMG_W/4,IMG_H))   
    draw0 = ImageDraw.Draw(img_text0)
    draw0.text((0,0), rand_str[0], font=ImageFont.truetype(FONT_FILE, random.randrange(25,40)),fill=(0,255,0))   
    del draw0
    img_text0 = img_text0.rotate(random.randrange(-45,45))    
    
    img_text1 =  Image.new('RGBA',(IMG_W/4,IMG_H))    
    draw1 = ImageDraw.Draw(img_text1)
    draw1.text((0,0), rand_str[1], font=ImageFont.truetype(FONT_FILE, random.randrange(25,40)),fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))   
    del draw1
    img_text1 = img_text1.rotate(random.randrange(-45,45))    
    
    x = im.size[0]
    y = im.size[1]
    draw = ImageDraw.Draw(im)
    draw.line((random.randrange(0,x),random.randrange(0,y),random.randrange(0,x),random.randrange(0,y)), fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
    draw.line((random.randrange(0,x),random.randrange(0,y),random.randrange(0,x),random.randrange(0,y)), fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
   # draw.line((random.randrange(0,x),random.randrange(0,y),random.randrange(0,x),random.randrange(0,y)), fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
   # draw.line((random.randrange(0,x),random.randrange(0,y),random.randrange(0,x),random.randrange(0,y)), fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
    #draw.line((rx,ry+random.randrange(25,50),rx+random.randrange(25,50),ry), fill=(0,255,0))
   # draw.line((rx,ry,rx-ry,ry-rx), fill=(0,255,0))
   # draw.line((rx,ry,rx-ry,ry-rx), fill=(0,255,0))
    #draw.text((3,3), rand_str[0], font=ImageFont.truetype("ARIAL.TTF", random.randrange(15,50)),fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))   
    #draw.bitmap((0,0),img_text0)
    #draw.bitmap((IMG_W/4,0),img_text1)
    #draw.text((18,3), rand_str[1], font=ImageFont.truetype("ARIAL.TTF", random.randrange(15,50)),fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))   
    im.paste(img_text0,(0,0,img_text0.size[0],img_text0.size[1]),img_text0)
    im.paste(img_text1,(25,0,25+img_text1.size[0],img_text1.size[1]),img_text1)
    
    draw.text((45,3), rand_str[2], font=ImageFont.truetype(FONT_FILE, random.randrange(25,40)),fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))   
    draw.text((67,3), rand_str[3], font=ImageFont.truetype(FONT_FILE, random.randrange(25,40)),fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))   
    draw.line((random.randrange(0,x),random.randrange(0,y),random.randrange(0,x),random.randrange(0,y)), fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
    draw.line((random.randrange(0,x),random.randrange(0,y),random.randrange(0,x),random.randrange(0,y)), fill=(random.randrange(0,255),random.randrange(0,255),random.randrange(0,255)))
    del draw   
    #im.transform((100,35),Image.QUAD,(35,8,0,35,98,0,98,35))
    request.session['vcode'] = rand_str.lower()
    buf = cStringIO.StringIO()
    
    im.save(buf, 'png')   
    return HttpResponse(buf.getvalue(),'image/png')  
