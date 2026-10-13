"""Silbentrennung: liest <dir>/index.src.html, schreibt <dir>/index.html mit weichen Trennstellen."""
import re, sys, pyphen
d = pyphen.Pyphen(lang='de_DE')
def hy(t):
    # nur Text außerhalb von Tags trennen
    return re.sub(r'(<[^>]+>)|([A-Za-zÄÖÜäöüß]{7,})',
                  lambda m: m.group(1) or d.inserted(m.group(2), hyphen='­'), t)
for folder in sys.argv[1:]:
    s = open(f'{folder}/index.src.html', encoding='utf8').read()
    s = re.sub(r'(<p(?:\s[^>]*)?>)(.*?)(</p>)', lambda m: m.group(1)+hy(m.group(2))+m.group(3), s, flags=re.S)
    open(f'{folder}/index.html', 'w', encoding='utf8').write(s)
