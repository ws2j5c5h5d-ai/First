import re,pyphen
d=pyphen.Pyphen(lang='de_DE')
def hy(t):
    return re.sub(r'[A-Za-zÄÖÜäöüß]{7,}',lambda m:d.inserted(m.group(0),hyphen='­'),t)
s=open('index.src.html',encoding='utf8').read()
s=re.sub(r'(<p(?:\s[^>]*)?>)(.*?)(</p>)',lambda m:m.group(1)+hy(m.group(2))+m.group(3),s,flags=re.S)
open('index.html','w',encoding='utf8').write(s)
