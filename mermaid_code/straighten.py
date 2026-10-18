import sys,re,math
import xml.etree.ElementTree as ET
ET.register_namespace('',"http://www.w3.org/2000/svg")
ET.register_namespace('xlink',"http://www.w3.org/1999/xlink")
NS="{http://www.w3.org/2000/svg}"
src,dst=sys.argv[1],sys.argv[2]
tree=ET.parse(src); root=tree.getroot()
def cls(e): return (e.get('class') or '').split()
paths=[e for e in root.iter(NS+'path') if 'flowchart-link' in cls(e)]
labels=[]
for g in root.iter(NS+'g'):
    if 'edgeLabels' in cls(g):
        labels=[x for x in g if 'edgeLabel' in cls(x)]
pts=[]
for p in paths:
    nums=re.findall(r'(-?\d+\.?\d*(?:e-?\d+)?),(-?\d+\.?\d*(?:e-?\d+)?)',p.get('d'))
    a=tuple(map(float,nums[0])); b=tuple(map(float,nums[-1]))
    pts.append([a,b])
ids=[p.get('id') or '' for p in paths]
# offset opposite-direction pairs so they do not overlap
def ends(i):
    m=re.match(r'L[_-](.+)[_-](.+)[_-]\d+$',ids[i]); return m.groups() if m else None
for i in range(len(paths)):
    for j in range(i+1,len(paths)):
        ei,ej=ends(i),ends(j)
        if ei and ej and ei[0]==ej[1] and ei[1]==ej[0]:
            for k,s in ((i,-1),(j,1)):
                (x1,y1),(x2,y2)=pts[k]
                dx,dy=x2-x1,y2-y1; L=math.hypot(dx,dy) or 1
                ox,oy=-dy/L*22*s,dx/L*22*s
                pts[k]=[(x1+ox,y1+oy),(x2+ox,y2+oy)]
for p,(a,b) in zip(paths,pts):
    p.set('d',f"M{a[0]:.2f},{a[1]:.2f}L{b[0]:.2f},{b[1]:.2f}")
    if 'data-points' in p.attrib: del p.attrib['data-points']
for lab,(a,b) in zip(labels,pts):
    mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
    lab.set('transform',f"translate({mx:.2f}, {my:.2f})")
vb=[float(v) for v in root.get('viewBox').split()]
root.set('width',str(vb[2])); root.set('height',str(vb[3]))
st=root.get('style') or ''
root.set('style',re.sub(r'max-width:[^;]*;?','',st)+'background:white;')
tree.write(dst,xml_declaration=True,encoding='utf-8')
print(dst,len(paths),'edges',len(labels),'labels')
