"""Windows 내장 글자 인식으로 회로도의 기호 이름(MC1, PB1 등)을 읽는다. 결과는 ocr/에 저장해 두고 다시 쓴다."""
import subprocess,sys,json,os
HERE=os.path.dirname(os.path.abspath(__file__))
from PIL import Image
S=0.6
def ocr(n):
    out=os.path.join(HERE,'ocr',f'ocr{n:02d}.json')
    if os.path.exists(out): return json.load(open(out))
    im=Image.open(f'raw{n:02d}.png').convert('L').point(lambda v:255-v)
    im=im.resize((int(im.width*S),int(im.height*S)),Image.LANCZOS);fn=os.path.abspath(f'ocr_in{n:02d}.png');im.save(fn)
    r=subprocess.run(['powershell','-NoProfile','-ExecutionPolicy','Bypass','-File',os.path.join(HERE,'ocr.ps1'),'-Path',fn],capture_output=True,text=True,encoding='utf-8',errors='replace')
    words=[]
    for line in r.stdout.splitlines()[1:]:
        p=line.split('\t')
        if len(p)==5: words.append(dict(t=p[0],x=float(p[1])/S,y=float(p[2])/S,w=float(p[3])/S,h=float(p[4])/S))
    json.dump(words,open(out,'w'));return words
if __name__=='__main__':
    for n in range(1,19):
        w=ocr(int(n));print(n,len(w),' '.join(x['t'] for x in w))
