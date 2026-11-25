"""Build an original editable SVG and matching 512px PNG using only the standard library."""
from pathlib import Path
import math
import struct
import zlib

ROOT=Path(__file__).resolve().parents[1]
SIZE=512
SCALE=2
N=SIZE*SCALE
pixels=bytearray(N*N*3)

def color(value):return tuple(bytes.fromhex(value.lstrip('#')))
def put(x,y,c):
    if 0<=x<N and 0<=y<N:
        p=(y*N+x)*3;pixels[p:p+3]=bytes(c)
def circle(cx,cy,r,fill):
    cx*=SCALE;cy*=SCALE;r*=SCALE;c=color(fill)
    for y in range(max(0,int(cy-r)),min(N,int(cy+r)+1)):
        for x in range(max(0,int(cx-r)),min(N,int(cx+r)+1)):
            if (x+.5-cx)**2+(y+.5-cy)**2<=r*r:put(x,y,c)
def polygon(points,fill):
    pts=[(x*SCALE,y*SCALE) for x,y in points];c=color(fill)
    for y in range(max(0,int(min(p[1] for p in pts))),min(N,int(max(p[1] for p in pts))+1)):
        sy=y+.5;cross=[]
        for i,(x1,y1) in enumerate(pts):
            x2,y2=pts[(i+1)%len(pts)]
            if (y1<=sy<y2) or (y2<=sy<y1):cross.append(x1+(sy-y1)*(x2-x1)/(y2-y1))
        cross.sort()
        for a,b in zip(cross[::2],cross[1::2]):
            for x in range(max(0,math.ceil(a-.5)),min(N,math.ceil(b-.5))):put(x,y,c)
def line(points,width,fill):
    for (x1,y1),(x2,y2) in zip(points,points[1:]):
        length=math.hypot(x2-x1,y2-y1);dx=-(y2-y1)/length*width/2;dy=(x2-x1)/length*width/2
        polygon([(x1+dx,y1+dy),(x2+dx,y2+dy),(x2-dx,y2-dy),(x1-dx,y1-dy)],fill)
    for x,y in points:circle(x,y,width/2,fill)

for y in range(N):
    fraction=y/(N-1);c=tuple(round(a+(b-a)*fraction) for a,b in zip(color('10264f'),color('1547a0')))
    pixels[y*N*3:(y+1)*N*3]=bytes(c)*N
polygon([(128,80),(316,80),(384,148),(384,424),(128,424)],'f8fbff')
polygon([(316,80),(316,148),(384,148)],'b9d7ff')
line([(160,210),(324,210)],7,'dbe8fb')
line([(160,325),(264,325)],7,'dbe8fb')
line([(200,245),(178,267),(200,289)],10,'2459b8')
line([(286,245),(308,267),(286,289)],10,'2459b8')
line([(258,239),(232,296)],9,'2459b8')
circle(365,368,79,'10264f')
circle(365,362,74,'29d4d0')
line([(330,362),(354,386),(401,338)],13,'10264f')
font={'A':['01110','10001','10001','11111','10001','10001','10001'],
'G':['01111','10000','10000','10111','10001','10001','01110'],
'E':['11111','10000','10000','11110','10000','10000','11111'],
'N':['10001','11001','10101','10011','10001','10001','10001'],
'T':['11111','00100','00100','00100','00100','00100','00100'],
'S':['01111','10000','10000','01110','00001','00001','11110'],
'.':['00000','00000','00000','00000','00000','00110','00110'],
'M':['10001','11011','10101','10101','10001','10001','10001'],
'D':['11110','10001','10001','10001','10001','10001','11110']}
for index,ch in enumerate('AGENTS.MD'):
    for row,bits in enumerate(font[ch]):
        for col,bit in enumerate(bits):
            if bit=='1':
                x=153+index*21+col*3;y=169+row*3
                polygon([(x,y),(x+3,y),(x+3,y+3),(x,y+3)],'2459b8')
raw=bytearray()
for y in range(SIZE):
    raw.append(0)
    for x in range(SIZE):
        for channel in range(3):
            raw.append(round(sum(pixels[((y*SCALE+dy)*N+x*SCALE+dx)*3+channel] for dy in range(SCALE) for dx in range(SCALE))/(SCALE*SCALE)))
def chunk(kind,data):return struct.pack('!I',len(data))+kind+data+struct.pack('!I',zlib.crc32(kind+data)&0xffffffff)
png=b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('!IIBBBBB',512,512,8,2,0,0,0))+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')
folder=ROOT/'release';folder.mkdir(exist_ok=True)
(folder/'icon.png').write_bytes(png)
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">
<defs><linearGradient id="b" x2="0" y2="1"><stop stop-color="#10264f"/><stop offset="1" stop-color="#1547a0"/></linearGradient></defs>
<path fill="url(#b)" d="M0 0h512v512H0z"/><path fill="#f8fbff" d="M128 80h188l68 68v276H128z"/><path fill="#b9d7ff" d="M316 80v68h68z"/>
<text x="153" y="190" font-family="monospace" font-size="24" font-weight="700" fill="#2459b8">AGENTS.md</text>
<path d="M160 210h164M160 325h104" fill="none" stroke="#dbe8fb" stroke-width="7" stroke-linecap="round"/>
<path d="m200 245-22 22 22 22m86-44 22 22-22 22m-28-50-26 57" fill="none" stroke="#2459b8" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>
<circle cx="365" cy="368" r="79" fill="#10264f"/><circle cx="365" cy="362" r="74" fill="#29d4d0"/><path d="m330 362 24 24 47-48" fill="none" stroke="#10264f" stroke-width="13" stroke-linecap="round" stroke-linejoin="round"/>
</svg>'''
(folder/'icon.svg').write_text(svg+'\n',encoding='utf-8')
(folder/'icon-design.md').write_text('''# 图标设计与交付

独立原创的深蓝渐变背景、浅色 AGENTS.md 文档、代码括号与青色检查徽章。无第三方 Logo 或素材。SVG 可编辑，PNG 是同构代码绘制版，文字采用内置5×7点阵以避免外部字体依赖；两者文字栅格细节不同。

PNG：512×512、RGB、不透明背景、PNG真实编码，目标小于500KB。由 tools/create_icon.py 使用标准库确定性绘制，不使用生成式模型或第三方图像。颜色：#10264f、#1547a0、#f8fbff、#29d4d0。小尺寸保留文档、代码与校验轮廓。

使用前按实际 WorkBuddy 提交表单核实尺寸、比例、透明度与体积限制。本项目尺寸为任务书目标，不声称平台已确认。版权和授权遵循 Apache-2.0。
''',encoding='utf-8')
print('icon.png:',len(png),'bytes')
