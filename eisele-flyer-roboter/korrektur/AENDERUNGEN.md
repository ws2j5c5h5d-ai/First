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
