from PIL import ImageFont
F='/home/user/render/node_modules/@expo-google-fonts/arimo/400Regular/Arimo_400Regular.ttf'
font=ImageFont.truetype(F,19)
def wrap(t,w):
    out=[];cur=''
    for word in t.split():
        c=(cur+' '+word).strip()
        if font.getlength(c)<=w: cur=c
        else: out.append(cur);cur=word
    out.append(cur);return out
R='#D95C86';N='#2C5F8A';B='#5AA9E0';G='#7F93A8'
def ray(pts,col=R,w=2.5,arrow=True):
    # pts: list of (x,y); arrow at midpoint of first segment
    s=[]
    for i in range(len(pts)-1):
        (x1,y1),(x2,y2)=pts[i],pts[i+1]
        if i==0 and arrow:
            mx,my=x1+(x2-x1)*0.6,y1+(y2-y1)*0.6
            s.append(('L',x1,y1,mx,my,True)); s.append(('L',mx,my,x2,y2,False))
        else: s.append(('L',x1,y1,x2,y2,False))
    return s
def lens(cx,cy,ry,bulge=10):
    return ('P',f'M{{x{cx}}} {{y{cy-ry}}} Q{{x{cx+bulge}}} {{y{cy}}} {{x{cx}}} {{y{cy+ry}}} Q{{x{cx-bulge}}} {{y{cy}}} {{x{cx}}} {{y{cy-ry}}} Z')
cards=[
("Spectacles and Corrective Lenses","Convex lenses correct long-sightedness and concave lenses correct short-sightedness by bringing the image exactly on to the retina. Contact lenses work on the same principle of refraction.","Convex lens focuses rays","spec"),
("Microscopes","A compound microscope uses an objective and an eyepiece to give a highly magnified image of tiny objects such as cells and bacteria. Its resolving power is limited by diffraction.","Compound microscope","micro"),
("Telescopes","The objective collects light from distant objects and the eyepiece magnifies the image formed. Large reflecting telescopes use concave mirrors to study planets, stars and galaxies.","Refracting telescope","tele"),
("Cameras","A convex lens forms a real, inverted image on a film or electronic sensor. The aperture controls the amount of light and the shutter controls the exposure time.","Real, inverted image","cam"),
("Optical Fibres","Light travels along a thin glass core by repeated total internal reflection. Fibres carry telephone, television and internet signals over long distances with very little loss.","Total internal reflection","fibre"),
("Laser Technology","A laser gives an intense, monochromatic and coherent beam. It is used in eye surgery, cutting and welding, barcode scanners, printers, optical discs and holography.","Laser cavity and beam","laser"),
("Medical Imaging","An endoscope uses bundles of optical fibres to carry light into the body and bring the image back, letting doctors examine internal organs without major surgery.","Flexible endoscope","endo"),
("Scientific Instruments","Spectrometers, interferometers and polarimeters use dispersion, interference and polarisation to measure wavelengths, tiny distances and the concentration of solutions.","Prism spectrometer","spectro"),
]
fills=[('#EAF5FD','#B9DCF5',N),('#FDEEF3','#F6BFD0','#B8456F'),('#F3EFFC','#D3C8EE','#6E5BB0')]
def art(kind,ox,oy,cid):
    X=lambda v:round(ox+v,1); Y=lambda v:round(oy+v+8,1)
    o=[]
    def L(x1,y1,x2,y2,col=R,w=2.5,m=None,dash=None):
        a=f'      <line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" stroke="{col}" stroke-width="{w}"'
        if dash: a+=f' stroke-dasharray="{dash}"'
        if m: a+=f' marker-end="url(#{m})"'
        o.append(a+'/>')
    def RAY(pts,col=R,w=2.5):
        (x1,y1),(x2,y2)=pts[0],pts[1]
        mx,my=x1+(x2-x1)*0.6,y1+(y2-y1)*0.6
        L(x1,y1,mx,my,col,w,'arRose'); L(mx,my,x2,y2,col,w)
        for i in range(1,len(pts)-1): L(*pts[i],*pts[i+1],col,w)
    def LENS(cx,cy,ry,b=12):
        o.append(f'      <path d="M{X(cx)} {Y(cy-ry)} Q{X(cx+b)} {Y(cy)} {X(cx)} {Y(cy+ry)} Q{X(cx-b)} {Y(cy)} {X(cx)} {Y(cy-ry)} Z" fill="#DCEFFB" stroke="{B}" stroke-width="2"/>')
    def T(x,y,s,anchor='middle',size=14,col='#4A5D72',bold=False):
        fw=' font-weight="bold"' if bold else ''
        o.append(f'      <text x="{X(x)}" y="{Y(y)}" text-anchor="{anchor}" font-size="{size}"{fw} fill="{col}">{s}</text>')
    def AXIS(y=100):
        L(6,y,184,y,G,1.2,None,'5 4')
    if kind=='spec':
        AXIS(); LENS(70,100,62,14)
        for y in (60,140): RAY([(10,y),(70,y),(160,100)])
        RAY([(10,100),(70,100),(160,100)])
        o.append(f'      <circle cx="{X(160)}" cy="{Y(100)}" r="4.5" fill="{N}"/>')
        T(70,186,'Convex lens'); T(162,124,'F',bold=True,col=N,size=16)
    elif kind=='micro':
        AXIS(); LENS(48,100,30,8); LENS(138,100,50,12)
        L(16,100,16,80,N,3); L(100,100,100,132,N,3,None,'4 3')
        L(16,80,48,80,R,2); L(48,80,100,132,R,2); L(16,80,48,100,R,2); L(48,100,100,132,R,2)
        L(100,132,138,120,R,2); L(100,132,138,140,R,2)
        L(138,120,176,88,R,2,'arRose'); L(138,140,176,108,R,2,'arRose')
        T(48,150,'Objective'); T(138,172,'Eyepiece'); T(6,68,'Object',anchor='start')
    elif kind=='tele':
        AXIS(); LENS(40,100,62,14); LENS(150,100,32,8)
        RAY([(6,60),(40,60),(150,115),(184,115)]); RAY([(6,140),(40,140),(150,85),(184,85)])
        o.append(f'      <circle cx="{X(120)}" cy="{Y(100)}" r="4" fill="{N}"/>')
        T(44,186,'Objective'); T(146,156,'Eyepiece'); T(120,124,'F',bold=True,col=N,size=16)
    elif kind=='cam':
        o.append(f'      <rect x="{X(70)}" y="{Y(46)}" width="108" height="108" rx="8" fill="#F4FAFE" stroke="{G}" stroke-width="2"/>')
        o.append(f'      <rect x="{X(54)}" y="{Y(76)}" width="16" height="48" fill="#F4FAFE" stroke="{G}" stroke-width="2"/>')
        LENS(62,100,22,6)
        L(170,54,170,146,N,4)
        L(14,100,14,80,N,3); L(8,100,22,100,G,1.5)
        RAY([(14,80),(62,80),(166,143)]); RAY([(14,80),(62,100),(166,143)])
        L(166,100,166,143,R,3)
        T(62,146,'Lens',anchor='end'); T(132,172,'Sensor'); T(4,68,'Object',anchor='start')
    elif kind=='fibre':
        o.append(f'      <rect x="{X(10)}" y="{Y(68)}" width="170" height="64" rx="8" fill="#DCEFFB" stroke="#7DBDEA" stroke-width="2"/>')
        o.append(f'      <rect x="{X(10)}" y="{Y(84)}" width="170" height="32" fill="#FFFFFF" stroke="{B}" stroke-width="1.5"/>')
        pts=[(12,100),(30,84),(62,116),(94,84),(126,116),(158,84),(176,100)]
        for i in range(len(pts)-1):
            L(*pts[i],*pts[i+1],R,2.5,'arRose' if i==len(pts)-2 else None)
        T(95,56,'Cladding (lower n)'); T(95,154,'Core (higher n)')
    elif kind=='laser':
        o.append(f'      <rect x="{X(30)}" y="{Y(82)}" width="100" height="36" rx="6" fill="#FDEEF3" stroke="#D9739A" stroke-width="2"/>')
        L(24,72,24,128,N,5); L(136,72,136,128,B,3)
        L(38,100,122,100,R,2,None,'6 4')
        L(136,100,184,100,R,4,'arRose')
        for x in (55,80,105): L(x,50,x,78,G,2,'arGrey')
        T(80,40,'Energy input'); T(6,150,'Mirror',anchor='start'); T(184,150,'Partial mirror',anchor='end'); T(184,88,'Beam',anchor='end',col='#B8456F',bold=True)
    elif kind=='endo':
        d=f'M{X(26)} {Y(44)} C{X(26)} {Y(130)} {X(84)} {Y(60)} {X(100)} {Y(120)} S{X(166)} {Y(176)} {X(166)} {Y(110)}'
        o.append(f'      <path d="{d}" fill="none" stroke="#A7D3F2" stroke-width="16" stroke-linecap="round"/>')
        o.append(f'      <path d="{d}" fill="none" stroke="{R}" stroke-width="2.5" stroke-dasharray="6 4"/>')
        o.append(f'      <rect x="{X(12)}" y="{Y(18)}" width="28" height="26" rx="5" fill="#F3EFFC" stroke="#A593D6" stroke-width="2"/>')
        o.append(f'      <circle cx="{X(166)}" cy="{Y(98)}" r="9" fill="#EBCB4A" stroke="#F2A65A" stroke-width="2"/>')
        T(48,36,'Eyepiece',anchor='start'); T(184,78,'Light at tip',anchor='end'); T(10,170,'Fibre bundle',anchor='start')
    elif kind=='spectro':
        o.append(f'      <path d="M{X(66)} {Y(134)} L{X(100)} {Y(76)} L{X(134)} {Y(134)} Z" fill="#EAF5FD" stroke="#7DBDEA" stroke-width="2.5"/>')
        L(8,124,56,112,G,3,'arGrey'); L(56,112,86,104,G,3)
        for y,c in ((104,'#E57373'),(122,'#7CCF8A'),(140,'#B085E0')):
            o.append(f'      <path d="M{X(86)} {Y(104)} L{X(114)} {Y(100+ (y-104)*0.12)} L{X(176)} {Y(y)}" fill="none" stroke="{c}" stroke-width="2.5"/>')
        L(180,92,180,150,N,4)
        T(6,146,'Source',anchor='start'); T(100,156,'Prism'); T(184,82,'Detector',anchor='end')
    return '\n'.join(o)
print('''  <g id="lead-applications" data-pptx-bounds="80 205 1080 90">
    <text x="80" y="240" fill="#2F3B4A">The laws of reflection, refraction and wave optics are put to use in many instruments<tspan x="80" dy="34">and technologies. Eight important applications are described below.</tspan></text>
  </g>
''')
for i,(title,body,cap,kind) in enumerate(cards):
    x=80+552*(i%2); y=310+328*(i//2)
    f,s,tc=fills[i%3]
    lines=wrap(body,272)
    assert len(lines)<=8,(title,len(lines))
    tx=x+226
    tsp=lines[0]+''.join(f'<tspan x="{tx}" dy="26">{l}</tspan>' for l in lines[1:])
    print(f'''  <g id="card-{kind}" data-pptx-bounds="{x} {y} 528 310">
    <rect x="{x}" y="{y}" width="528" height="310" rx="16" fill="{f}" stroke="{s}" stroke-width="1.5"/>
    <text x="{x+20}" y="{y+40}" font-family="Georgia" font-size="22" font-weight="bold" fill="{tc}">{title}</text>
    <rect x="{x+16}" y="{y+58}" width="190" height="236" rx="12" fill="#FFFFFF" stroke="{s}" stroke-width="1.5"/>
    <g id="art-{kind}">
{art(kind,x+16,y+58,i)}
    </g>
    <text x="{x+111}" y="{y+280}" text-anchor="middle" font-size="15" font-style="italic" fill="#6C8198">{cap}</text>
    <text x="{tx}" y="{y+84}" font-size="19" fill="#2F3B4A">{tsp}</text>
  </g>
''')
