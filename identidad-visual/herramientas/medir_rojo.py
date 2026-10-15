import sys, numpy as np, glob, os
from PIL import Image
def pct(f, broad=False):
    a=np.asarray(Image.open(f).convert('RGB')).astype(int); r,g,b=a[...,0],a[...,1],a[...,2]
    if broad: m=(r>90)&(r>1.9*g)&(r>1.7*b)&(g<130)
    else: m=(r>150)&(r>2.4*g)&(r>2*b)&(g<120)&(b<110)
    return round(m.mean()*100,1)
if __name__=='__main__':
    a,b=sys.argv[1],sys.argv[2]
    for f in sorted(glob.glob(a+'/*.jpg')):
        n=os.path.basename(f); g=os.path.join(b,n)
        print(n.ljust(34),'v4',pct(f),pct(f,1),'| v5',pct(g),pct(g,1))
