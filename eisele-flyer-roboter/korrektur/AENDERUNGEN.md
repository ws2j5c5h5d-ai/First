# Korrekturen Flyer „Programm Humanoide Roboter“ (Poster + Seiten 1–6)

Ausgabe: `../final/Eisele_Flyer_Humanoide_Roboter_de_korrigiert.pdf` (7 Seiten).
Quellen: Seiten 1–6 nur als PDF vorhanden → Korrektur per `korrigiere_flyer.py` (Redaction + Neusatz in TeX Gyre Heros);
Poster aus `../infografik/make_a4_final.py` neu erzeugt.

| Seite | Alt | Neu |
|---|---|---|
| Poster | EXTREM KLEINBAUEND. KOMPLETTER DURCHFLUSS. | EXTREM KLEINBAUEND. AB M3 UND AD3. |
| Poster | Logo-Overlay enthielt unsichtbar den Volltext von Seite 1 (u. a. „bleifrei“) | Logo aus bereinigter Logo-PDF, kein versteckter Text |
| 1 | Badge „ALUMINIUM BLEIFREI“ | entfernt |
| 1 | Aluminium, bleifrei | Werkstoffe: Messing, Edelstahl und Aluminium |
| 1 | Extrem kleinbauend für kompletten Durchfluss | Extrem kleinbauend: ab Gewinde M3, ab ca. 2 g (863-4218) |
| 1 | KOMPLETTER DURCHFLUSS. | AB M3 UND AD3. |
| 1 | Verschraubungen: Schlauch ab AD3 | P12 ab AD3 · P5500 ab AD4 |
| 1 | Drehanschlüsse (Übersicht) | + „Ergänzend: Prüfstand und Fertigung“ |
| 1 | Bauweisen: VT5528-0202 · 628D / 686D | VT5528-0202 / (686D entfernt) |
| 1 | Modulare Schwenkkupplung | Schwenkkupplung |
| 1 | (keine Seitenzahl) | 1 / 6 (Poster ausdrücklich ohne Zählung) |
| 2 | Modulare Schwenkkupplung | Schwenkkupplung |
| 2 | Vier nummerierte Kanäle (1–4) und mittige Bohrung | Mittige Bohrung |
| 2 | Sechs Innensechskantschrauben, vier nummerierte Kanäle (1–4) | (entfernt) |
| 2 | Flanschseite mit sechs Innensechskantschrauben | (entfernt, folgende Zeile nachgerückt) |
| 2 | Block SCHWENKKUPPLUNG „Vier nummerierte Kanäle (1–4) in einem Bauteil“ | unverändert (einzige Nennung) |
| 3 | 686D-0409 Gewicht 101 | 105 |
| 3 | I (mm) | i (mm) |
| 3 | Fußnoten | + „i = Länge Einschraubgewinde laut Maßblatt.“ + „Vor Inbetriebnahme Dokument „Hinweis für Artikelgruppe 628D / 686D / 688D“ beachten (www.eisele.eu).“ |
| 3 | Werkstoff: Messing vernickelt, blank, POM | Werkstoff: Ms vernickelt / Ms blank / POM, Kugellager Edelstahl / Keramik |
| 3 | EIGENSCHAFTEN | + „Auch mit Einschraubgewinde G3/8 erhältlich (628D-06xx, 686D-06xx).“ (Block 8,6 → 7,6 pt) |
| 4 | Maßzeichnungs-Beschriftungen ca. 3,5–4 pt | 7 pt neu gesetzt; „6-kt.“ → „SW“; „für Schlauch mit Außen-Ø3/Ø4“ → „Schlauch AD3/AD4“; Toleranzen und Bezug „A“ entfernt |
| 5 | Titel PROGRAMM 15 | P15 (wie Übersicht und Seite 4 „P12 & P5500“); Langform „Programm 15“ bleibt in Fußnote/Block |
| 6 | EDELSTAHL & ALUMINIUM | EDELSTAHL |

## Umbau auf 6 Seiten (Poster = Übersicht)

Ausgabe: `final/Eisele_Flyer_Humanoide_Roboter_de_6S.pdf`, Skript `korrektur/baue_seite1.py`.

| Seite | alt | neu |
|---|---|---|
| 1 | Poster ohne Übersicht, ohne Seitenzahl | Poster oben (Roboter, Callouts, Legende, KI-Hinweis), darunter PROGRAMMÜBERSICHT (5 Spalten, → SEITE 2 bis 6), VORTEILE, BAUWEISEN, Fußzeile mit „1 / 6“; Wortlaut 1:1 aus der gelöschten Übersichtsseite |
| 1 | Headline doppelt (Poster + Übersichtsseite) | einmal: „EXTREM KLEINBAUEND. AB M3 UND AD3.“ |
| 1 | Leiste „IM UMFELD / Prüfstand und Fertigung“ mit Fotos 628D, 686D, V0129 | entfernt; Kennzeichnung nur noch einmal: „Ergänzend: Prüfstand und Fertigung“ in der Spalte Drehanschlüsse |
| 1 | Roboterbild bis zum Seitenfuß | verkleinert (0,31 pt/px), endet an der Oberkante des Übersichtsbands |
| 1 | Logofeld weiß, EISELE navy, „Member of“ grau, HENN-Schriftzug #ED1C24 | Feld #0B335E, EISELE und „Member of“ weiß, „HENN Connector Group“ #FF0000; weiterhin Vektor, Proportionen unverändert |
| 2 (alt) | Seite PROGRAMMÜBERSICHT | gelöscht |
| 2–6 | Seiten 3–7 der 7-seitigen Fassung | unverändert, Seitenzahlen „2 / 6“ bis „6 / 6“ |

Farbwerte:
- Navy #0B335E (RGB 11/51/94): aus der Flyer-Quelldatei `Eisele_Flyer_Humanoide_Roboter_de_7.pdf`, Füllfarbe des Footer-Balkens S. 6 (0, 748,5, 595,5, 842,2) und des VORTEILE-Blocks.
- Rot #FF0000: aus `quellen/HENN_connector_group_logo_aus_Praesentation1.svg` (= `ppt/media/image1.svg` in `Präsentation1.pptx`), `fill="#FF0000"`. Keine CMYK-Angabe in der Datei. Abweichung: das Logo in der Flyer-Quelldatei verwendete #ED1C24.

| Seite | alt | neu |
|---|---|---|
| 1 | Poster-Hintergrund aus Bildrand (dunkler als #0B335E), Logofeld als sichtbarer Kasten | Poster-Grund #0B335E; dunkle Bildpixel des Roboterbilds tonwertgleich auf #0B335E verschoben (helle Roboterteile unverändert); Logofeld fügt sich nahtlos ein |

## Feinschliff (6 Seiten)

Ausgabe: `final/Eisele_Flyer_Humanoide_Roboter_de_6S_v2.pdf`, Skript `korrektur/feinschliff.py` (Eingabe: `final/Eisele_Flyer_Humanoide_Roboter_de_6S.pdf`).

| Seite | alt | neu |
|---|---|---|
| 1 | Badge „NEU“ neben „NEUHEIT“ | (entfernt) |
| 1 | Spaltenkopf „V0129-/1850-040601“ zweizeilig, 15,5 pt | „V0129-1850-040601“ einzeilig, 9.9 pt; „Schwenkkupplung“ auf Höhe der Nachbarspalten |
| 1 | BAUWEISEN: Gruppen GERADE/WINKEL links gedrängt, rechts Leerfläche | Gruppen auf 1/4 und 3/4 der Blockbreite verteilt (Inhalt unverändert) |
| 2 | Abbildung „Flanschseite“ oben rechts mit Bildunterschrift | (entfernt; Ansicht bleibt unter ANSICHTEN & DETAILS) |
| 2 | Produktfoto 164 × 149 pt, Bildunterschrift links darunter | Produktfoto 213 × 194 pt (×1.30), Bildunterschrift rechtsbündig unten |
| 2 | „Mittige Bohrung“ unter Abbildung „Stirnseite“ | (entfernt; steht im Block SCHWENKKUPPLUNG) |
| 2 | Block MUSTER & DATEN ANFRAGEN: ab y 594, Titel 10,5 pt, Text 8 pt, QR 47 pt | weiße Karte mit Navy-Kante ab y 571, Titel 12,5 pt, Text 8,6 pt, QR 62 pt |
| 3 | Steckanschluss mit Lösehülse, Schlauch AD8 bis AD12 | Schlauch AD8 bis AD12 |
| 3 | „… Kugellager Edelstahl“ / „/ Keramik“ (Wortrest allein) | „… POM,“ / „Kugellager Edelstahl/Keramik“ |
| 3 | „… erhältlich (628D-06xx,“ / „686D-06xx).“ | „… erhältlich“ / „(628D-06xx, 686D-06xx).“ |
| 4 | (keine) | Fußnote „Nennmaße, Toleranzen siehe Maßblatt.“ |
| 4 | VT5528-0202: „ca. 11,6“ auf Kontur/Hilfslinie, Maßlinien 1,4 pt unter dem Bauteil | Maßlinien auf y 501,5 / 515 / 528,5 gezogen, Hilfslinien verlängert; Maßzahlen unverändert |
| 5 | Maßzeichnungen 863-4218 / 887-4218: Beschriftung ca. 3,5–4 pt (Kurven), Toleranzen ±0,07 / ±0,1 | neu gesetzt in 7 pt, Toleranzen entfernt; „für Schlauch mit Außen-Ø 3“ bzw. „für Schlauch mit AD“ + „3“ → „Schlauch AD3“ (wie S. 4) |
| 6 | Maßzeichnungen SA2113-1 / SA2113-2: Beschriftung ca. 3,5 pt (Kurven), Bezugstexte senkrecht | neu gesetzt in 7 pt; „für Stecknippel SA2113-2“ / „für Kupplung SA2113-1“ waagerecht zweizeilig am Ende der Bezugslinie |
| 5 | PROGRAMM 15 | PROGRAMM P15 |
| 5 | * Programm 15 mit metrischem und zölligem Gewinde. … | * P15 mit metrischem und zölligem Gewinde. … |
| 5 | (keine) | Fußnote „Nennmaße, Toleranzen siehe Maßblatt.“ |
| 6 | (keine) | Fußnote „Nennmaße, Toleranzen siehe Maßblatt.“ unter der Tabelle (Tabelle 6 pt höher, graues Band 3,4 pt länger) |
| 6 | Footer-Logo: „HENN Connector Group“ weiß | „HENN Connector Group“ #FF0000 (EISELE und „Member of“ weiß, Vektor, Geometrie unverändert) |

Hinweise: Seite 3 EIGENSCHAFTEN steht laut PDF in 7,6 pt (nicht 8,6 pt) und bleibt in 7,6 pt; 8,6 pt passt nicht über den Haftungshinweis. Fußnote S. 5: zweiter Satz „Länge = Gesamtlänge laut Maßblatt.“ beibehalten (wie S. 4). Rot im Footer-Logo S. 6: #FF0000 aus `quellen/HENN_connector_group_logo_aus_Praesentation1.svg`.

## Letzte Runde

| Seite | alt | neu |
|---|---|---|
| 2 | Titel „NEUHEIT / SCHWENKKUPPLUNG“ | Titel zweizeilig „SCHWENKKUPPLUNG / V0129-1850-040601“ (25 pt, wie Seiten 3–6) |

Web-PDF: `final/Eisele_Flyer_Humanoide_Roboter_de_Web.pdf`. Druck-PDF: laut Auftraggeber nicht benötigt.

## Produktfotos aus dem Webshop

| Seite | alt | neu |
|---|---|---|
| 1 | Kacheln 863-4218, 887-4218, VT5528-0202 (2x): Renderings | Fotos aus dem EISELE-Webshop, freigestellt (`infografik/freistellen.py`) |
| 4 | Produktfoto VT5528-0202: Rendering | Webshop-Foto |
| 5 | Produktfotos 863-4218, 887-4218: Renderings | Webshop-Fotos |

Quelle: Screenshots der Shop-Seiten www.eisele-connectors.com/produkte/<Artikel> (Firecrawl), da pim.eisele.eu in dieser Umgebung gesperrt ist; Ausschnitte ca. 660 x 480 px in `quellen/produktbilder_shop/`.
