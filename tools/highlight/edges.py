import json,sys,numpy as np
from extract import load, ends
def free_ends(segs):
    out=[]
    for i,s in enumerate(segs):
        for k,(x,y) in enumerate(ends(s)):
            if s['free'][k]:
                # 끝이 향하는 방향 (선 바깥쪽)
                if s['a']=='v': d=(0,-1) if k==0 else (0,1)
                else: d=(-1,0) if k==0 else (1,0)
                out.append(dict(i=i,c=s['c'],x=x,y=y,d=d,a=s['a']))
    return out
def pairs(B,fe):
    """기호 하나를 사이에 두고 마주 보는 두 끝 → 기호(edge)"""
    E=[];usedp=set()
    cand=[]
    for p in range(len(fe)):
        for q in range(len(fe)):
            a,b=fe[p],fe[q]
            if p==q or a['c']==b['c']: continue
            if a['a']=='v' and b['a']=='v' and a['d']==(0,1) and b['d']==(0,-1) and abs(a['x']-b['x'])<=12 and 0<b['y']-a['y']<420:
                cand.append((b['y']-a['y'],p,q,'v'))
            if a['a']=='h' and b['a']=='h' and a['d']==(1,0) and b['d']==(-1,0) and abs(a['y']-b['y'])<=12 and 0<b['x']-a['x']<420:
                cand.append((b['x']-a['x'],p,q,'h'))
    cand.sort()
    for g,p,q,ax in cand:
        if p in usedp or q in usedp: continue
        usedp.add(p);usedp.add(q)
        a,b=fe[p],fe[q]
        # 기호 종류: 축 왼쪽(가로면 위쪽) 55~95px에 잉크가 있으면 원·상자(부하)
        if ax=='v':
            x=int(a['x']);y0=int(a['y']+g*.3);y1=int(b['y']-g*.3)
            side=B[y0:y1,x-95:x-55].any()
        else:
            y=int(a['y']);x0=int(a['x']+g*.3);x1=int(b['x']-g*.3)
            side=B[y-95:y-55,x0:x1].any()
        E.append(dict(p=p,q=q,ca=a['c'],cb=b['c'],gap=g,ax=ax,load=bool(side),x=(a['x']+b['x'])/2,y=(a['y']+b['y'])/2))
    return E,usedp
if __name__=='__main__':
    n=int(sys.argv[1]);B=load(n);segs=json.load(open(f'segs{n:02d}.json'))
    fe=free_ends(segs);E,used=pairs(B,fe)
    print(len(fe),'free ends',len(E),'edges')
    for e in E: print(f"{e['ax']} c{e['ca']}-c{e['cb']} gap{e['gap']:.0f} {'LOAD' if e['load'] else 'cont'} @({e['x']:.0f},{e['y']:.0f})")
    print('unpaired:',[(f['c'],int(f['x']),int(f['y'])) for k,f in enumerate(fe) if k not in used])
