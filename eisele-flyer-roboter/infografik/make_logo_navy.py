"""Logo für Navy-Grund: Vektor bleibt erhalten, nur Farboperatoren werden getauscht.
weiß (Hintergrund) -> Navy #0B335E (Flyer-Quelldatei), Navy (EISELE) -> weiß,
Grau (Member of) -> weiß, Rot -> #FF0000 (HENN-Logo-SVG aus Präsentation1.pptx)."""
import sys
import pikepdf
src, out = sys.argv[1:3]
NAVY = (0.0431, 0.2, 0.3686)
MAP = {
    (1.0, 1.0, 1.0): NAVY,
    (0.0431, 0.2, 0.3686): (1.0, 1.0, 1.0),
    (0.4745, 0.5059, 0.5137): (1.0, 1.0, 1.0),
    (0.9294, 0.1098, 0.1412): (1.0, 0.0, 0.0),
}
pdf = pikepdf.open(src)
pg = pdf.pages[0]
ops = pikepdf.parse_content_stream(pg)
new, n = [], 0
for operands, op in ops:
    if str(op) in ('rg', 'RG') and len(operands) == 3:
        key = tuple(round(float(v), 4) for v in operands)
        if key in MAP:
            operands = [pikepdf.objects.Object.parse(f'{v:.4f}'.encode()) if False else v for v in MAP[key]]
            n += 1
    new.append((operands, op))
pg.Contents = pdf.make_stream(pikepdf.unparse_content_stream(new))
# Formulare/XObjects im Logo prüfen
pdf.save(out)
print('ok', n, 'Farbangaben getauscht')
