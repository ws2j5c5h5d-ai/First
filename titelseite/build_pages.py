#!/usr/bin/env python3
"""Erzeugt seiten.html: Layout-Neubau der Seiten 2-6 (Ueberschriften, Raster, Fotos).
Fliesstexte sind bewusst als graue Textzeilen angedeutet."""
import html

DATE = "Montag, 13. August 1979"


def esc(t):
    return html.escape(t, quote=False).replace("\n", "<br>")


class Page:
    def __init__(self, rubric, bbox, blocks, tag=""):
        self.rubric, self.bbox, self.blocks, self.tag = rubric, bbox, blocks, tag

    def render(self):
        x0, y0, x1, y1 = self.bbox
        s = 1120 / (x1 - x0)
        out = [f'<section class="page" id="{self.tag}">',
               f'<div class="phead"><span class="rub">{esc(self.rubric)}</span><span class="dat">{DATE}</span></div>',
               f'<div class="canvas" style="height:{(y1 - y0) * s:.0f}px">']
        for b in self.blocks:
            x, y, w, h, items = b[:5]
            frame = b[5] if len(b) > 5 else ""
            st = (f"left:{(x - x0) * s:.0f}px;top:{(y - y0) * s:.0f}px;"
                  f"width:{w * s:.0f}px;height:{h * s:.0f}px")
            out.append(f'<div class="blk {frame}" style="{st}">')
            ncol = max(1, round(w / 96))
            for it in items:
                k = it[0]
                if k == "kick":
                    out.append(f'<div class="kick">{esc(it[1])}</div>')
                elif k == "h":
                    px = it[2]
                    al = it[3] if len(it) > 3 else "left"
                    out.append(f'<h2 style="font-size:{px}px;text-align:{al}">{esc(it[1])}</h2>')
                elif k == "deck":
                    al = it[2] if len(it) > 2 else "left"
                    out.append(f'<div class="deck" style="text-align:{al}">{esc(it[1])}</div>')
                elif k == "dl":
                    out.append(f'<div class="dl">{esc(it[1])}</div>')
                elif k == "by":
                    out.append(f'<div class="by">{esc(it[1])}</div>')
                elif k == "bar":
                    out.append(f'<div class="bar">{esc(it[1])}</div>')
                elif k == "sub":
                    out.append(f'<h3>{esc(it[1])}</h3>')
                elif k == "photo":
                    cap = it[2] if len(it) > 2 else ""
                    out.append(f'<img src="img/{it[1]}.png" alt="">')
                    if cap:
                        out.append(f'<div class="cap">{esc(cap)}</div>')
                elif k == "fill":
                    n = it[1] if len(it) > 1 else ncol
                    out.append('<div class="fill">' + '<i></i>' * n + '</div>')
                elif k == "table":
                    n = it[1] if len(it) > 1 else 1
                    out.append('<div class="tbl">' + '<i></i>' * n + '</div>')
                elif k == "gap":
                    out.append(f'<div style="height:{it[1]}px"></div>')
            out.append('</div>')
        out.append('</div></section>')
        return "\n".join(out)


# ---------------------------------------------------------------- Seite 2: Politik
politik = Page("Politik", (130, 128, 882, 1300), [
    (148, 150, 292, 224, [("photo", "karikatur",
                           "„Ich habe damit überhaupt nichts zu tun ...“   Aus: Kölner Stadt-Anzeiger")]),
    (148, 378, 292, 370, [("bar", "Bonn verstärkt Hilfe für Vietnam-Flüchtlinge"),
                          ("deck", "Botschafterkonferenz soll Aufnahme beschleunigen", "center"),
                          ("dl", "BONN (dpa)"), ("fill",)]),
    (148, 760, 292, 185, [("h", "Neue Festnahmen in Teheran", 17), ("dl", "TEHERAN (dpa)"), ("fill",)]),
    (148, 955, 292, 345, [("bar", "Gisela Küstler: Der Ruf des Pfauen"), ("fill",)]),
    (448, 150, 193, 430, [("h", "Bahr wirft der DDR neuen Mauerbau vor", 30, "center"),
                          ("deck", "Ost-Berlin nennt 13. August einen „Grund zum Feiern“", "center"),
                          ("dl", "HAMBURG (dpa)"), ("fill",)]),
    (448, 590, 193, 245, [("h", "Sowjetische Presse würdigt Moskauer Vertrag mit Bonn", 22, "center"),
                          ("deck", "Krupp-Chef Beitz erwartet Ausbau des Handels", "center"),
                          ("dl", "MOSKAU (dpa)"), ("fill",)]),
    (448, 845, 193, 215, [("kick", "Deutsch-israelische Beziehungen"),
                          ("h", "Schütz: Keine Verstimmung", 22, "center"),
                          ("dl", "BONN (dpa)"), ("fill",)]),
    (448, 1070, 193, 230, [("bar", "Das Turmzimmer"), ("fill",)]),
    (650, 150, 95, 158, [("h", "Kritik Rumäniens an Aufrüstung", 16), ("dl", "BUKAREST (dpa)"), ("fill",)]),
    (650, 316, 95, 176, [("h", "„Vorwürfe der SPD unhaltbar“", 16), ("dl", "STUTTGART (dpa)"), ("fill",)]),
    (650, 500, 95, 175, [("h", "Beauftragter für Kinder gefordert", 16), ("dl", "STOLBERG (dpa)"), ("fill",)]),
    (650, 684, 95, 190, [("h", "Verwirrung unter Persiens Wählern", 15), ("fill",)]),
    (650, 884, 95, 416, [("fill",)]),
    (754, 150, 128, 160, [("h", "Selbstkritik in Prag", 17), ("dl", "PRAG (dpa)"), ("fill",)]),
    (754, 318, 128, 130, [("h", "Zustimmung für Rhodesien-Plan", 16), ("dl", "SALISBURY/KAIRO (dpa)"), ("fill",)]),
    (754, 456, 128, 118, [("h", "Brandanschlag noch ungeklärt", 16), ("dl", "BERLIN (dpa)"), ("fill",)]),
    (754, 582, 128, 160, [("h", "Ärzteverband sieht Mißbrauch", 16), ("dl", "BONN (dpa)"), ("fill",)]),
    (754, 750, 128, 150, [("h", "Afghanische Rebellen planen neue Offensive", 15), ("dl", "PESCHAWAR (dpa)"), ("fill",)]),
    (754, 910, 128, 390, [("bar", "Wie wird das Wetter?"), ("sub", "Wärmer"), ("fill",),
                          ("kick", "Wetterkarte, Vorhersage für 13. August 1979"), ("table", 1)], "box"),
], "politik")

# ---------------------------------------------------------------- Seite 3: Blick in die Welt
blick = Page("Blick in die Welt", (58, 130, 775, 1298), [
    (58, 132, 350, 330, [("kick", "20 000 Hektar Wald wurden zu Asche"),
                         ("h", "Camper flüchten vor Feuer\nAuslaufsperre für Segler", 40),
                         ("deck", "Die Brandkatastrophe in Südfrankreich und Spanien"),
                         ("dl", "PARIS/MADRID (dpa)"), ("fill",)]),
    (415, 150, 355, 260, [("photo", "waldbrand", "Feuerwalze in Südfrankreich: Zum Glück ließ gestern der Mistral nach.   Funkbild: dpa/UPI")]),
    (58, 468, 78, 190, [("bar", "Leute im Blick"), ("photo", "leute", ""), ("fill", 1)], "box"),
    (142, 468, 165, 200, [("h", "Radlerkarawane setzte sich im Morgengrauen in Marsch", 21),
                          ("deck", "DDR-Grenzer fertigten 70köpfige Gruppe zügig ab"),
                          ("dl", "BERLIN (dpa)"), ("fill",)]),
    (142, 680, 165, 175, [("bar", "Zur Tarnung Politikermasken"), ("dl", "(ddp)"), ("fill",)]),
    (58, 665, 78, 190, [("h", "Grubenunglück in der Ukraine", 16), ("dl", "MOSKAU (dpa)"), ("fill", 1)]),
    (410, 420, 248, 190, [("h", "Der FC Nantes hat seinen Meisterpokal wieder", 20),
                          ("deck", "Aktion von Stahlarbeitern gegen Entlassungen"),
                          ("dl", "NANTES (dpa)"), ("fill",)]),
    (662, 420, 108, 195, [("h", "Camper zog es in Schönwetterländer", 16), ("dl", "MÜNCHEN (dpa)"), ("fill", 1)]),
    (312, 615, 348, 230, [("h", "Nach der Ölpest die große Dürre?", 26),
                          ("deck", "Experte: Ölfilm behindert die Verdunstung des Wassers"),
                          ("dl", "URBANA, Bundesstaat Illinois (dpa)"), ("fill",)]),
    (662, 625, 108, 215, [("h", "13 000 Liter Heizöl ausgelaufen", 16), ("dl", "DONAUWÖRTH/Schw. (dpa)"), ("fill", 1)]),
    (312, 850, 348, 140, [("kick", "„Proletarische Justiz“ droht Exekution an"),
                          ("h", "Skandalbankier wurde entführt", 22), ("dl", "NEW YORK (dpa)"), ("fill",)]),
    (58, 880, 250, 410, [("kick", "FEUILLETON"), ("h", "Die einen im Smoking – die anderen in Jeans", 24),
                         ("deck", "Nach sieben Jahren wieder Filmfestspiele in Venedig"), ("fill",)]),
    (312, 1000, 348, 290, [("h", "Ein „frecher Führer“", 22), ("by", "Kultur – notiert und kommentiert"), ("fill",)]),
    (662, 850, 108, 440, [("fill", 1)]),
], "blick")

# ---------------------------------------------------------------- Seite 4: Sport vom Wochenende
sport1 = Page("Sport", (125, 85, 893, 1300), [
    (285, 88, 600, 40, [("h", "Sport vom Wochenende", 34)], "banner"),
    (165, 148, 108, 215, [("photo", "maier", "Staunend sah Sepp Maier zum Bundesliga-Auftakt auf der Tribüne des Olympiastadions.   Funkbild: dpa")]),
    (165, 372, 108, 262, [("sub", "„Komme wieder“"), ("fill", 1)]),
    (165, 640, 108, 175, [("bar", "Bundesliga"), ("table", 1)], "box"),
    (165, 822, 108, 90, [("sub", "Die nächsten Spiele"), ("fill", 1)]),
    (278, 128, 250, 330, [("kick", "Flaue Premiere der Fußball-Bundesliga 1979/80"),
                          ("h", "Nur 20 Tore hielten die Begeisterung in Grenzen", 24),
                          ("deck", "Nur Kaiserslautern und HSV setzten Glanzlichter"),
                          ("by", "Von unseren Mitarbeitern und Agenturen"), ("fill",)]),
    (278, 468, 250, 215, [("sub", "Da staunte selbst Zebec"), ("fill",)]),
    (278, 690, 250, 35, [("sub", "Gelbe Karten unter Schnitt")]),
    (278, 740, 252, 25, [("bar", "+ Bundesliga-Stenogramm +")]),
    (278, 770, 252, 150, [("fill", 3)]),
    (530, 140, 360, 255, [("photo", "tor", "Das erste Bundesliga-Tor der Saison: Bernd Dürnberger bezwingt Leverkusens Torwart Bockhof.")]),
    (530, 420, 360, 380, [("kick", "Duisburgs Talentschuppen trotzte dem VfB ein 1:1 ab"),
                          ("h", "Mit diesem Punkt waren beide zufrieden", 23),
                          ("deck", "Volkert und Kelsch trafen nur das Holz – Dietz in neuer Rolle als überragender Libero"),
                          ("by", "Von unserem Mitarbeiter Friedrich Kaufhold"), ("fill",)]),
    (548, 810, 92, 220, [("bar", "Trainer-Weisheiten"), ("fill", 1)], "box"),
    (548, 1020, 92, 270, [("bar", "Bundesliga-Splitter"), ("fill", 1)], "box"),
    (645, 810, 245, 20, [("kick", "Bei jedem Ballkontakt Pfiffe für Müller, aber:")]),
    (645, 832, 245, 160, [("h", "Hansis Nerven hielten", 24, "center"), ("fill",)], "box"),
    (645, 1000, 108, 290, [("kick", "Nach dem 4:0-Sieg des 1. FCK"), ("h", "„Atze“ bleibt doch", 16), ("fill", 1)], "box"),
    (758, 1000, 132, 290, [("kick", "Die Sache mit den Brocks"), ("h", "Mit beiden zufrieden", 16), ("fill", 1)]),
    (125, 925, 415, 28, [("kick", "Der Auftritt des Heinz Flohe in seiner alten Heimat")]),
    (125, 955, 415, 40, [("h", "Vom Liebling zum Buhmann", 24)]),
    (125, 1000, 240, 285, [("fill", 2)]),
    (372, 1000, 105, 190, [("photo", "flohe", "Bild: Weres")]),
    (372, 1195, 168, 90, [("fill", 2)]),
], "sport1")

# ---------------------------------------------------------------- Seite 5: Sport
sport2 = Page("Sport", (103, 80, 893, 1300), [
    (105, 88, 105, 240, [("bar", "2. Liga Süd"), ("table", 1)]),
    (105, 336, 105, 245, [("bar", "2. Liga Nord"), ("table", 1)]),
    (105, 588, 105, 190, [("bar", "Landesliga, Staffel 2"), ("table", 1)]),
    (105, 786, 105, 285, [("bar", "Landesliga, Staffel 3"), ("table", 1)]),
    (105, 1078, 105, 215, [("bar", "Landesliga, Staffel 4"), ("table", 1)]),
    (215, 112, 380, 250, [("kick", "2. Fußball-Liga Süd: KSC patzte beim ESV Ingolstadt"),
                          ("h", "Hessen-Trio hat saubere Weste", 29),
                          ("deck", "Offenbach weiter auf Torjagd – Darmstadts erfolgreicher Einstand in Würzburg"),
                          ("dl", "(sid/dpa)"), ("fill",)]),
    (215, 365, 245, 290, [("photo", "freiburg", "Freiburgs Torwart Armbrust hielt auch gegen Saarbrücken wieder überragend.")]),
    (465, 365, 130, 285, [("fill", 1)]),
    (215, 660, 380, 0, []),
    (598, 112, 292, 25, [("kick", "Ulm und Kickers schlen trotz Regen die Sonne")]),
    (598, 138, 145, 440, [("h", "Ein Tor und seine Folgen", 20), ("fill", 1)], "box"),
    (746, 138, 144, 440, [("h", "Nun wird’s „normal“", 20), ("fill", 1)], "box"),
    (490, 590, 400, 215, [("kick", "Auftakt Fußball-Oberliga: Neuling Eppingen mit Traumstart"),
                          ("h", "Debakel für disziplinlose Mannheimer", 26),
                          ("deck", "Drei Aufsteiger holten auswärts Teilerfolge – 4200 Besucher beim Derby in Kuppenheim"),
                          ("by", "Von unseren Mitarbeitern und Agenturen"), ("fill",)]),
    (490, 810, 400, 230, [("fill",)]),
    (215, 665, 130, 25, [("bar", "Auf einen Blick")]),
    (215, 690, 130, 335, [("sub", "AUSLANDSFUSSBALL"), ("fill", 1)]),
    (350, 665, 125, 25, [("bar", "Verbandsliga")]),
    (350, 690, 125, 330, [("table", 1)]),
    (215, 1030, 260, 255, [("sub", "WASSERBALL"), ("kick", "Starker Liverpooler Start"),
                           ("h", "„Klasse unterstrichen“", 17), ("fill",)]),
    (350, 1030, 125, 0, []),
    (490, 1050, 290, 25, [("bar", "Im Telegrammstil")]),
    (490, 1080, 290, 215, [("fill", 3)]),
    (790, 1050, 100, 245, [("table", 1)]),
], "sport2")

# ---------------------------------------------------------------- Seite 6: Südwestumschau
sw = Page("Südwestumschau", (105, 75, 885, 1300), [
    (108, 85, 100, 215, [("h", "SPD kritisiert die Monopolstellung des TÜV", 15), ("dl", "STUTTGART (lsw)"), ("fill", 1)]),
    (108, 305, 100, 115, [("h", "Pakistani-Schlägerei: Acht Schwerverletzte", 14), ("dl", "VILLINGEN-SCHWENNINGEN"), ("fill", 1)]),
    (108, 425, 100, 250, [("h", "Eifersuchtsdrama am Urlaubsort: Zwei Tote", 14), ("dl", "ÖSTERREICH/Allgäu"), ("fill", 1)]),
    (108, 680, 100, 225, [("h", "Sozialausschüsse wollen Heizkostenzuschlag", 14), ("dl", "STUTTGART (lsw)"), ("fill", 1)]),
    (108, 910, 100, 205, [("h", "Mehr Lehrer für ausländische Schüler", 14), ("dl", "STUTTGART (lsw)"), ("fill", 1)]),
    (108, 1120, 100, 180, [("h", "Namen von Weinberglagen sind geschützt", 14), ("dl", "KARLSRUHE (lsw)"), ("fill", 1)]),
    (215, 105, 390, 285, [("photo", "kutsche", "Statt angespannt im Wagen auf der Autobahn, angespannt durch die Natur.   Foto: Gröhe")]),
    (215, 398, 390, 335, [("h", "Tripsdriller Geschmacklosigkeiten – oder: Schade um die alte Mühle", 24, "center"),
                          ("by", "Von unserem Redaktionsmitglied"), ("fill",)], "box"),
    (215, 745, 132, 400, [("photo", "fels", "Urlaub zu Hause: Klettertour am Hausener Felsen im Geißental bei Geislingen.   Foto: Lindel")]),
    (352, 748, 253, 190, [("h", "Architekten drängen nicht mehr in öffentlichen Dienst", 22),
                          ("deck", "In der freien Wirtschaft wieder bessere Aussichten"),
                          ("dl", "STUTTGART (lsw)"), ("fill",)]),
    (352, 945, 125, 175, [("h", "Landesbürgschaft für die Flitz-Gruppe", 15), ("dl", "MÜHLACKER (VWD)"), ("fill", 1)]),
    (482, 945, 123, 175, [("h", "Junghandwerker mit Beruf sehr zufrieden", 15), ("dl", "STUTTGART (lsw)"), ("fill", 1)]),
    (352, 1130, 125, 170, [("h", "Gegen Streckenstilllegung", 15), ("dl", "STUTTGART (lsw)"), ("fill", 1)]),
    (482, 1130, 123, 170, [("h", "„Zündhütle“ wird renoviert", 15), ("dl", "KARLSRUHE (lsw)"), ("fill", 1)]),
    (615, 105, 270, 240, [("h", "Nach verregnetem Wochenende zum Trost ein „Baby-Hoch“?", 24),
                          ("deck", "Am Sonntag war es auf den Straßen im Land ruhig"),
                          ("dl", "STUTTGART (lsw)"), ("fill",)]),
    (615, 350, 130, 235, [("sub", "Vom Traktor überrollt"), ("dl", "EPPINGEN"), ("fill", 1)]),
    (750, 350, 135, 235, [("sub", "Bei Zusammenstoß getötet"), ("dl", "LEONBERG"), ("fill", 1)]),
    (615, 590, 270, 125, [("h", "Auch für ausländische Opfer von Verbrechen bald Geld?", 22),
                          ("deck", "Antrag Hopmeiers zielt auf Initiative im Bundesrat"),
                          ("by", "Von unserer Stuttgarter Redaktion  STUTTGART (lsw)"), ("fill",)]),
    (615, 722, 270, 575, [("bar", "Telegramm"), ("sub", "1. Programm ARD"), ("fill", 1)], "box"),
    (750, 755, 100, 100, [("photo", "tv", "")]),
], "sw")

PAGES = [politik, blick, sport1, sport2, sw]

CSS = """
:root{--ink:#141414;--paper:#fdfcf8;--grey:#d9d8d3;--rule:#1b1b1b;--ph:#bdbab2}
*{box-sizing:border-box}
html{background:#e9e8e3}
body{margin:0;padding:24px 0;color:var(--ink);font-family:"Source Serif 4",Georgia,serif}
.page{width:1180px;margin:0 auto 32px;background:var(--paper);padding:22px 30px 30px;box-shadow:0 2px 18px rgba(0,0,0,.18);page-break-after:always}
.phead{display:grid;grid-template-columns:1fr auto 1fr;align-items:end;border-bottom:2.4px solid var(--ink);padding-bottom:5px;margin-bottom:14px;
  font-family:"Archivo",Arial,sans-serif;font-weight:700}
.phead .rub{grid-column:2;font-size:22px;font-stretch:80%;font-weight:800;letter-spacing:.02em}
.phead .dat{grid-column:3;justify-self:end;font-size:11.5px;font-weight:600}
.canvas{position:relative}
.blk{position:absolute;display:flex;flex-direction:column;overflow:hidden;padding:0 4px;border-left:1.2px solid var(--rule)}
.blk.box{border:1.6px solid var(--ink);padding:6px 7px}
.blk.banner{border:0;border-bottom:2px solid var(--ink);padding:0}
h2,h3,.kick,.deck,.bar{font-family:"Archivo","Helvetica Neue",Arial,sans-serif}
h2{margin:0 0 6px;font-stretch:78%;font-weight:700;line-height:1.04;letter-spacing:-.01em}
h3{margin:6px 0 5px;font-size:15px;font-stretch:84%;font-weight:800}
.kick{font-size:12.5px;font-stretch:88%;font-weight:800;margin:2px 0 4px;border-bottom:1.4px solid var(--ink);padding-bottom:3px}
.deck{font-size:12.6px;font-stretch:88%;font-weight:700;line-height:1.15;margin:0 0 7px}
.dl{font-size:11px;font-weight:700;margin:0 0 4px}
.by{font-family:"Archivo",Arial,sans-serif;font-size:10px;font-weight:500;margin:0 0 5px}
.bar{background:var(--grey);border:1.4px solid var(--ink);font-size:15px;font-stretch:80%;font-weight:800;padding:4px 7px;margin:0 0 6px;line-height:1.05;text-align:center}
.blk.banner h2{font-size:34px;margin:0;font-stretch:80%;font-weight:800}
img{display:block;width:100%;height:auto;filter:contrast(1.04)}
.cap{font-family:"Archivo",Arial,sans-serif;font-stretch:88%;font-size:9.6px;line-height:1.25;margin:4px 0 6px}
.fill{flex:1;display:flex;gap:10px;min-height:0}
.fill i{flex:1;background:repeating-linear-gradient(to bottom,var(--ph) 0 5px,transparent 5px 13.4px);border-left:0}
.fill i+i{box-shadow:-5px 0 0 -4.4px var(--rule)}
.tbl{flex:1;display:flex;gap:8px;min-height:0}
.tbl i{flex:1;background:repeating-linear-gradient(to bottom,#9d9a92 0 1px,transparent 1px 9px)}
@media print{html,body{background:#fff;padding:0}.page{box-shadow:none;margin:0}}
"""


def main():
    head = ('<!doctype html><html lang="de"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>NWZ Göppinger Kreisnachrichten, 13. August 1979, Seiten 2 bis 6</title>'
            '<link rel="preconnect" href="https://fonts.googleapis.com">'
            '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
            '<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,500..800&family=Source+Serif+4:opsz,wght@8..60,400..700&display=swap" rel="stylesheet">'
            f'<style>{CSS}</style></head><body>')
    body = "\n".join(p.render() for p in PAGES)
    open("seiten.html", "w", encoding="utf8").write(head + body + "</body></html>")


if __name__ == "__main__":
    main()
