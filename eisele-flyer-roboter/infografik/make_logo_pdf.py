"""Erzeugt eine Logo-only-PDF aus Seite 1 des Flyers: alles außerhalb der Logobox wird
per Redaction entfernt (Text, Bilder, Grafik), damit im Poster keine versteckten Texte landen."""
import sys
import pymupdf
src, out = sys.argv[1:3]
LX0, LY0, LX1, LY1 = 405, 30, 560, 86
doc = pymupdf.open(src)
for i in range(len(doc) - 1, 0, -1):
    doc.delete_page(i)
p = doc[0]
W, H = p.rect.width, p.rect.height
for r in (pymupdf.Rect(0, 0, W, LY0), pymupdf.Rect(0, LY1, W, H), pymupdf.Rect(0, LY0, LX0, LY1), pymupdf.Rect(LX1, LY0, W, LY1)):
    p.add_redact_annot(r, fill=False)
p.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_REMOVE, graphics=pymupdf.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED,
                   text=pymupdf.PDF_REDACT_TEXT_REMOVE)
doc.save(out, garbage=4, deflate=True)
print('ok', repr(p.get_text()[:80]))
