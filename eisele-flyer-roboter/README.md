# EISELE Flyer: Roboterfigur überarbeitet

Geändert wurde nur die Roboterfigur auf Seite 1. Hintergrund, Callouts, Logo, Titel, Legende,
Fußzeile und die Seiten 2 bis 6 sind unverändert (per Pixelvergleich geprüft).

## Dateien

| Datei | Zweck |
|---|---|
| `Eisele_Flyer_Humanoide_Roboter_de_Figur-neu.pdf` | Digital-PDF (RGB) |
| `Eisele_Flyer_Humanoide_Roboter_de_Druck_PDFX4_FOGRA39_Schnittmarken_Figur-neu.pdf` | Druck-PDF, Figur über das eingebettete FOGRA39-Profil nach CMYK konvertiert (relativ farbmetrisch, Tiefenkompensierung) |
| `Roboterfigur_neu_RGBA_300ppi.png` | Freigestellte Figur für InDesign, Web und LinkedIn |
| `Vorher_Nachher_Titel.png` | Vergleich für die Abstimmung |
| `scripts/` | Reproduzierbare Retusche (`retouch.py`) und PDF-Austausch (`replace.py`) |

## Was an der Figur geändert wurde

| Bereich | Vorher (gemessen) | Nachher |
|---|---|---|
| Leitungsfarbe Vorlauf | #699DC4, passt nicht zur Legende | #3F91F5, nah an der Legende #2F8CFF |
| Leitungsfarbe Rücklauf | #D4A87D | #FD8A4A, nah an der Legende #FF7A2E |
| Druckluft/Vakuum | weiß, teils verdeckt | #D5D9DF wie in der Legende |
| Hülle | konstant 31 % Deckkraft | Fresnel: ca. 15 % in der Fläche, bis ca. 55 % am Rand |
| Innenteile | hellgrau #868A8F, lauter als die Leitungen | satiniertes Dunkelgrau um #5A626E |
| Rauschen | körnige Glühwürmchen an Taille und Torso | entrauscht |
| Blaue Säume | Kompositing-Saum an Ellbogen und Hüfte | entfernt |
| Visier | Hochglanz-Helm mit Glanzfleck | mattes Rauchglas |
| Hände | Schwarz #3F4043 | dunkel eloxiert, um #363C46 |
| Licht | kein Kantenlicht | kühles Rim #7FA6D9 von rechts, schwacher Key von links oben |
| Beine | hart abgeschnitten | weich über ca. 8 mm ausgeblendet |

## Grenzen dieser Version

Es ist eine Retusche des bestehenden Renders, kein Neu-Render. Silhouette, Proportionen
(Kopfgröße, Kapselglieder), Leitungsverlauf und Paarabstände sind deshalb unverändert.
Dafür braucht es das 3D-Quellmodell.

Vor dem Druck: Proof oder die Ausgabevorschau in Acrobat prüfen. Die gesättigten Blau- und
Orangetöne liegen voraussichtlich am Rand des FOGRA39-Farbraums.
