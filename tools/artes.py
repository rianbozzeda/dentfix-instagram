from PIL import Image, ImageDraw, ImageFont, ImageChops
import os, random, math
REPO=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT=os.path.join(REPO,'posts','2026-12')
os.makedirs(OUT,exist_ok=True)
DARK=(58,59,62); GREEN=(121,163,97); BLUE=(43,116,156); GRAY=(145,149,154); BG=(248,249,247); LINE=(225,227,224); CARD=(238,242,235)
W,H=1080,1350; M=80
F='/usr/share/fonts/opentype/inter/'
def font(n,s): return ImageFont.truetype(F+'Inter-'+n+'.otf',s)

def logo():
    src=Image.open(os.path.join(REPO,'assets','logo-dentfix.png')).convert('RGB').crop((325,340,1190,598))
    lw=500; lh=int(src.height*lw/src.width); src=src.resize((lw,lh),Image.LANCZOS)
    out=Image.new('RGB',src.size,BG); px=out.load(); sp=src.load()
    for y in range(src.height):
        for x in range(src.width):
            r,g,b=sp[x,y]
            if r>235 and g>235 and b>235: continue
            if x>src.width-40 and y>src.height-28: continue   # stray dots
            px[x,y]=(min(255,int(r*255/248)),min(255,int(g*255/248)),min(255,int(b*255/248)))
    return out
LOGO=logo()

def wrap(d,text,f,maxw):
    words=text.split(); lines=[]; cur=''
    for w in words:
        t=(cur+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur)
    return lines

def base(kicker,headline):
    img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,18],fill=GREEN); d.rectangle([W-260,0,W,18],fill=BLUE)
    y=130
    d.text((M,y),kicker.upper(),font=font('SemiBold',34),fill=GREEN); y+=70
    for line in headline:
        d.text((M,y),line,font=font('Bold',78),fill=DARK); y+=100
    return img,d,y

def footer(img,d):
    d.rectangle([M,1130,W-M,1134],fill=LINE)
    img.paste(LOGO,(M,1165))
    t="Centro • Bertioga/SP"; tf=font('Medium',30)
    d.text((W-M-d.textlength(t,font=tf),1225),t,font=tf,fill=GRAY)

def tips(name,kicker,headline,items,note=None):
    img,d,y=base(kicker,headline); y+=60
    for i,(a,b) in enumerate(items,1):
        d.ellipse([M,y,M+96,y+96],fill=GREEN)
        nf=font('Bold',52); n=str(i); tw=d.textlength(n,font=nf)
        d.text((M+48-tw/2,y+14),n,font=nf,fill='white')
        d.text((220,y+4),a,font=font('SemiBold',42),fill=DARK)
        d.text((220,y+54),b,font=font('Regular',38),fill=GRAY)
        y+=185
    if note:
        d.rounded_rectangle([M,1010,W-M,1090],radius=14,fill=CARD)
        nf=font('SemiBold',36); tw=d.textlength(note,font=nf)
        d.text(((W-tw)/2,1032),note,font=nf,fill=DARK)
    footer(img,d); img.save(os.path.join(OUT,name))

def info(name,kicker,headline,rows,note=None):
    img,d,y=base(kicker,headline); y+=50
    for label,value in rows:
        d.rounded_rectangle([M,y,W-M,y+150],radius=18,fill=CARD)
        d.rectangle([M,y+10,M+12,y+140],fill=GREEN)
        d.text((M+44,y+24),label.upper(),font=font('SemiBold',28),fill=GREEN)
        d.text((M+44,y+68),value,font=font('Bold',54),fill=DARK)
        y+=180
    if note:
        for ln in wrap(d,note,font('Regular',38),W-2*M):
            d.text((M,y+10),ln,font=font('Regular',38),fill=GRAY); y+=52
    footer(img,d); img.save(os.path.join(OUT,name))

def msg(name,kicker,headline,text,sub=None):
    img=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,18],fill=GREEN); d.rectangle([W-260,0,W,18],fill=BLUE)
    hf=font('Bold',86); tf=font('Regular',50); sf=font('SemiBold',46)
    hl=wrap(d,' '.join(headline),hf,W-2*M-60)
    tl=wrap(d,text,tf,W-2*M-48); sl=wrap(d,sub,sf,W-2*M-48) if sub else []
    total=50+len(hl)*120+50+len(tl)*74+((40+len(sl)*66) if sl else 0)
    y=int(150+(1090-150-total)/2)
    d.rectangle([M,y-6,M+12,y+total+6],fill=GREEN)
    x=M+48
    d.text((x,y),kicker.upper(),font=font('SemiBold',34),fill=GREEN); y+=70
    for l in hl: d.text((x,y),l,font=hf,fill=DARK); y+=120
    y+=30
    for l in tl: d.text((x,y),l,font=tf,fill=DARK); y+=74
    if sl:
        y+=30
        for l in sl: d.text((x,y),l,font=sf,fill=GREEN); y+=66
    footer(img,d); img.save(os.path.join(OUT,name))


# ---------- artes festivas (datas importantes) ----------
def gradient(top,bottom,h):
    g=Image.new('RGB',(W,h)); gd=ImageDraw.Draw(g)
    for y in range(h):
        t=y/(h-1); gd.line([(0,y),(W,y)],fill=tuple(int(top[i]+(bottom[i]-top[i])*t) for i in range(3)))
    return g

def star5(d,cx,cy,r,fill):
    pts=[]
    for i in range(10):
        a=-math.pi/2+i*math.pi/5; rr=r if i%2==0 else r*0.45
        pts.append((cx+rr*math.cos(a),cy+rr*math.sin(a)))
    d.polygon(pts,fill=fill)

def festive_base(top,bottom):
    PH=1100
    img=Image.new('RGB',(W,H),BG); img.paste(gradient(top,bottom,PH),(0,0))
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    return img,ov,od,PH

def white_text(d,x,y,lines,f,fill,lh):
    for l in lines: d.text((x,y),l,font=f,fill=fill); y+=lh
    return y

def festive_natal(name,kicker,headline,text,sub):
    random.seed(7)
    img,ov,od,PH=festive_base((121,163,97),(88,132,72))
    for _ in range(110):
        r=random.choice([4,5,6,8,11]); x=random.randint(20,W-20); y=random.randint(40,PH-30)
        if 110<y<690 and 40<x<W-40: continue
        od.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255,random.randint(70,150)))
    # tree
    cx=540; dark=(52,92,52)
    for apex,base_y,hw in [(730,860,130),(800,950,190),(870,1042,250)]:
        od.polygon([(cx,apex),(cx-hw,base_y),(cx+hw,base_y)],fill=dark+(255,))
    od.rectangle([cx-32,1042,cx+32,1088],fill=DARK+(255,))
    for (x,y,c) in [(cx-70,830,'w'),(cx+60,805,'b'),(cx-120,925,'b'),(cx+30,910,'w'),(cx+135,935,'w'),(cx-40,1010,'w'),(cx+105,1015,'b'),(cx-175,1018,'b'),(cx+190,1025,'w')]:
        col=(255,255,255,255) if c=='w' else BLUE+(255,)
        od.ellipse([x-17,y-17,x+17,y+17],fill=col)
    star5(od,cx,712,40,(255,255,255,255))
    img=Image.alpha_composite(img.convert('RGBA'),ov).convert('RGB'); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,18],fill=BG); d.rectangle([0,0,W-260,18],fill=BLUE); d.rectangle([W-260,0,W,18],fill=DARK)
    y=140
    d.text((M,y),kicker.upper(),font=font('SemiBold',34),fill=(255,255,255)); y+=76
    y=white_text(d,M,y,wrap(d,headline,font('Bold',124),W-2*M),font('Bold',124),(255,255,255),150)
    y+=20
    y=white_text(d,M,y,wrap(d,text,font('Regular',50),W-2*M),font('Regular',50),(255,255,255),72)
    y+=18
    white_text(d,M,y,[sub],font('SemiBold',44),(235,245,228),60)
    footer(img,d); img.save(os.path.join(OUT,name))

def festive_ano(name,kicker,text):
    random.seed(11)
    img,ov,od,PH=festive_base((43,116,156),(28,84,124))
    cx,cy=540,560
    for i in range(48):
        a=i*math.pi*2/48; r1=250; r2=560 if i%2==0 else 430
        od.line([(cx+r1*math.cos(a),cy+r1*math.sin(a)),(cx+r2*math.cos(a),cy+r2*math.sin(a))],fill=(255,255,255,45),width=7)
    cols=[(255,255,255),(121,163,97),(150,200,230),(255,255,255)]
    for _ in range(46):
        x=random.randint(20,W-20); y=random.randint(40,PH-30)
        if 120<y<1010: continue
        w,h=random.choice([(12,26),(10,22),(16,16)]); c=random.choice(cols)
        p=Image.new('RGBA',(40,40),(0,0,0,0)); pd=ImageDraw.Draw(p)
        pd.rectangle([20-w//2,20-h//2,20+w//2,20+h//2],fill=c+(220,))
        p=p.rotate(random.randint(0,180),resample=Image.BICUBIC)
        ov.alpha_composite(p,(x-20,y-20))
    for (x,y,r) in [(900,190,28),(985,110,18),(110,1045,22),(980,1040,28)]:
        star5(od,x,y,r,(255,255,255,235))
    img=Image.alpha_composite(img.convert('RGBA'),ov).convert('RGB'); d=ImageDraw.Draw(img)
    d.rectangle([0,0,W,18],fill=GREEN); d.rectangle([W-260,0,W,18],fill=BG)
    d.text((M,140),kicker.upper(),font=font('SemiBold',34),fill=(255,255,255))
    d.text((M,200),"Feliz",font=font('Bold',120),fill=(255,255,255))
    nf=font('Black',330); tw=d.textlength("2027",font=nf)
    d.text(((W-tw)/2,300),"2027",font=nf,fill=(255,255,255))
    white_text(d,M,760,wrap(d,text,font('Regular',50),W-2*M),font('Regular',50),(255,255,255),72)
    footer(img,d); img.save(os.path.join(OUT,name))


# ---------- Stories (1080x1920) com a arte do feed ----------
def story_from_feed(feed_png, out_png, pill="NOVO NO FEED", bottom="Toque no perfil e veja o post completo"):
    SW,SH=1080,1920
    img=gradient((121,163,97),(43,116,156),SH) if False else Image.new('RGB',(SW,SH))
    g=ImageDraw.Draw(img)
    top=(121,163,97); bot=(43,116,156)
    for y in range(SH):
        t=y/(SH-1); g.line([(0,y),(SW,y)],fill=tuple(int(top[i]+(bot[i]-top[i])*t) for i in range(3)))
    # feed image, scaled, rounded, with soft shadow (safe zone: y 250..1670)
    fw=800; fh=1000
    art=Image.open(feed_png).convert('RGB').resize((fw,fh),Image.LANCZOS)
    x0=(SW-fw)//2; y0=470
    sh=Image.new('RGBA',(SW,SH),(0,0,0,0)); sd=ImageDraw.Draw(sh)
    sd.rounded_rectangle([x0+8,y0+16,x0+fw+8,y0+fh+16],radius=36,fill=(0,0,0,70))
    img=Image.alpha_composite(img.convert('RGBA'),sh).convert('RGB')
    mask=Image.new('L',(fw,fh),0); ImageDraw.Draw(mask).rounded_rectangle([0,0,fw,fh],radius=32,fill=255)
    img.paste(art,(x0,y0),mask)
    g=ImageDraw.Draw(img)
    pf=font('Bold',44); tw=g.textlength(pill,font=pf)
    pw=int(tw+90); px=(SW-pw)//2
    g.rounded_rectangle([px,300,px+pw,390],radius=45,fill=(255,255,255))
    g.text((px+45,318),pill,font=pf,fill=GREEN)
    bf=font('SemiBold',42)
    for i,l in enumerate(wrap(g,bottom,bf,SW-160)):
        lw=g.textlength(l,font=bf); g.text(((SW-lw)/2,1520+i*58),l,font=bf,fill=(255,255,255))
    img.save(out_png)

def stories():
    d=os.path.join(OUT,'stories'); os.makedirs(d,exist_ok=True)
    for f in sorted(os.listdir(OUT)):
        if f.endswith('.png'):
            story_from_feed(os.path.join(OUT,f),os.path.join(d,f.replace('.png','-story.png')))

def dezembro():
    tips('2026-12-01-consultas-fim-de-ano.png','Antes do recesso',['Agende suas consultas','de fim de ano'],
         [('Consulta de rotina e limpeza','um bom começo para o seu sorriso'),
          ('Tratamentos em andamento','não deixe a continuidade para 2027'),
          ('Manutenção do aparelho','mantenha o tratamento em dia')],
         note='Atendemos até 22/12')
    info('2026-12-08-recesso.png','Aviso importante',['Recesso de','fim de ano'],
         [('Último dia de atendimento','22/12 (terça-feira)'),('Recesso','23/12 a 10/01'),('Voltamos a atender','11/01 (segunda-feira)')],
         note='Agende antes pelo nosso WhatsApp.')
    tips('2026-12-10-ferias-criancas.png','Férias escolares',['Férias: hora do','check-up das crianças'],
         [('Sem a correria da escola','fica mais fácil encontrar um horário'),
          ('Consulta de rotina','acompanha a saúde bucal dos pequenos'),
          ('Cuidado com os doces','escovar bem depois das festas')],
         note='Atendemos até 22/12')
    tips('2026-12-15-dica-festas.png','Época de festas',['Sorriso em dia','nas festas e no verão'],
         [('Escove os dentes depois','das refeições, mesmo na correria'),
          ('Use fio dental:','a ceia adora ficar entre os dentes'),
          ('Beba bastante água','ao longo do dia')])
    msg('2026-12-22-ultimo-dia.png','Último dia de 2026',['Hoje é nosso último','dia de atendimento'],
        'Agradecemos a confiança de cada paciente durante este ano.','Voltamos em 11/01. Boas festas!')
    festive_natal('2026-12-24-natal-festivo.png','Equipe DentFix','Feliz Natal!','Que o seu Natal seja leve, com muita saúde, união e muitos sorrisos.','Com carinho, equipe DentFix.')
    msg('2026-12-29-checkup-janeiro.png','Em 2027',['Comece o ano com','o sorriso em dia'],
        'Voltamos a atender em 11/01. Agende seu check-up de janeiro pelo nosso WhatsApp.')
    festive_ano('2026-12-31-feliz-2027-festivo.png','Equipe DentFix','Obrigada por confiar na DentFix em 2026. Que o novo ano venha com muita saúde e muitos sorrisos.')

if __name__=='__main__':
    dezembro()
    stories()
