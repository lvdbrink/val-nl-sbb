---
name: nl-sbb-shacl-validatie
description: >-
  Valideer begrippenkaders machinaal tegen het officiële NL-SBB SHACL-profiel
  (skos-ap-nl.ttl) met pyshacl. Gebruik bij SHACL-validatie, skos-ap-nl,
  formele NL-SBB-conformiteitscontrole of wanneer de gebruiker om SHACL vraagt
  in plaats van of naast de inhoudelijke NL-SBB-reviewskill.
---
# NL-SBB SHACL-validatieskill

## 1. Doel

Voer een **formele, reproduceerbare SHACL-validatie** uit van een begrippenkader tegen het officiële NL-SBB-toepassingsprofiel `skos-ap-nl.ttl`.

Deze skill:
- controleert de data-graph tegen SHACL-shapes;
- rapporteert `conforms`, violations, warnings en infos;
- wijzigt **geen** bronbestanden.

Dit is **geen** volledige inhoudelijke NL-SBB-review. Gebruik daarvoor `nl-sbb-review` (`skills/nl-sbb/nl-sbb-review-skill.md`).

## 2. Hoofdregel

De agent mag het aangeleverde begrippenkader **niet wijzigen**. Alleen valideren, samenvatten en adviseren.

## 3. Normatieve SHACL-bron

Standaarddocumentatie: https://docs.geostandaarden.nl/nl-sbb/nl-sbb/

Canonieke shapes-URL (Geonovum):

```text
https://raw.githubusercontent.com/geonovum/NL-SBB/main/profiles/skos-ap-nl.ttl
```

Spiegel: `https://geonovum.github.io/NL-SBB/profiles/skos-ap-nl.ttl`

In dit project: bij voorkeur `profiles/skos-ap-nl.ttl`. Ontbreekt het bestand, download het van de canonieke URL en bewaar het daar.

**Niet standaard meenemen** (tenzij de gebruiker dat expliciet vraagt):
- `nl-sbb-skill-extension.ttl` (projectextensie, geen officieel profiel).

Als de shapes-URL onbereikbaar is: stop en vraag de gebruiker om de juiste URL.

## 4. Ondersteunde invoer

- Lokaal Turtle / RDF-bestand (voorkeur: `.ttl`)
- URL naar een Turtle/RDF-export (eerst downloaden naar een lokaal bestand)

HTML-portaalpagina’s alleen zijn onvoldoende; gebruik de machineleesbare RDF/Turtle-export.

## 5. Tooling

1. Zorg dat projectdependencies beschikbaar zijn:

```bash
pip install -r requirements.txt
```

Minimaal: `pyshacl`, `rdflib` (zie `requirements.txt`).

2. Voer validatie uit met het projectscript:

```bash
python scripts/run_nl_sbb_shacl.py PAD/NAAR/data.ttl --shapes profiles/skos-ap-nl.ttl --out-dir reports --prefix NAAM
```

Parameters:
- `data` — te valideren graph
- `--shapes` — pad naar `skos-ap-nl.ttl` (default: `profiles/skos-ap-nl.ttl`)
- `--out-dir` — artefactmap (default: `reports`)
- `--prefix` — bestandsvoorvoegsel voor ruwe output
- `--data-format` — default `turtle`

Validatie-instellingen (niet wijzigen zonder reden):
- `inference="rdfs"`
- `abort_on_first=False`
- `allow_infos=True`, `allow_warnings=True`
- `advanced=True`

## 6. Werkproces

1. Bepaal invoerbestand; download indien nodig.
2. Zorg dat `profiles/skos-ap-nl.ttl` aanwezig is (download zo nodig).
3. Installeer/controleer `pyshacl` via `requirements.txt` indien nodig; **verwijder tooling niet** achteraf.
4. Draai `scripts/run_nl_sbb_shacl.py`.
5. Lees de samenvatting (`reports/_PREFIX-summary.txt`) en groepeer resultaten.
6. Schrijf een menselijk leesbaar rapport (zie §8).
7. Vermeld expliciet beperkingen t.o.v. de reviewskill (zie §7).

## 7. Interpretatie

| SHACL | Betekenis in rapportage |
|---|---|
| `conforms=true` | Geen `sh:Violation`; er kunnen wél veel `Warning`/`Info` zijn |
| `sh:Violation` | Harde afwijking t.o.v. het officiële profiel |
| `sh:Warning` | Aandachtspunt in het profiel (bijv. class-check op ISO-relaties, dubbele prefLabels) |
| `sh:Info` | Informatief (bijv. orphan-concept in het profiel) |

Bekende beperkingen van `skos-ap-nl.ttl` (niet presenteren als “volledige NL-SBB-review”):
- `TopConceptHavingBroader` controleert alleen `skos:broader`, niet `isothes:broaderGeneric` e.d.
- Aanwezigheid van `skos:definition` ≠ inhoudelijke kwaliteit van de definitietekst.
- Ontbrekende `dct:source` wordt niet afgedwongen (`minCount` ontbreekt).
- Inhoudelijke issues (placeholdertekst, verkeerde taallabels) vallen buiten SHACL.

Presenteer `conforms=true` nooit als “inhoudelijk publicatieklaar” zonder deze nuance.

## 8. Rapportagevorm

Schrijf een rapport (standaard onder `reports/`, bestandsnaam met bron + `shaclvalidatie` indien de gebruiker geen naam geeft) met minstens:

```text
# NL-SBB SHACL-validatierapport

## 1. Opzet
- Bron/data:
- Shapes: skos-ap-nl.ttl (+ URL of lokaal pad)
- Validator: pyshacl (+ versie indien bekend)
- Inferentie: rdfs

## 2. Machinaal resultaat
- Conforms: true/false
- Violations:
- Warnings:
- Infos:

## 3. Bevindingen per constraint
| Constraint/shape | Severity | Aantal | Unieke focusnodes | Kernboodschap | Voorbeelden |

## 4. Interpretatie
- Wat dit betekent voor NL-SBB-conformiteit volgens het officiële profiel
- Wat SHACL níet heeft getoetst (t.o.v. reviewskill)

## 5. Advies
- Vervolgstappen (herstel violations eerst; daarna warnings)
- Optioneel: aanvullende nl-sbb-review skill voor inhoudelijke kwaliteit
```

Ruwe artefacten mogen blijven staan:
- `reports/_PREFIX-summary.txt`
- `reports/_PREFIX-raw.txt`
- `reports/_PREFIX-report.ttl`

## 9. Onderscheid met nl-sbb-review

| | nl-sbb-shacl-validatie | nl-sbb-review |
|---|---|---|
| Doel | Formele SHACL-run | Technische + inhoudelijke review |
| Regelbron | `skos-ap-nl.ttl` | Reviewskill (+ interpretatie) |
| Output | conforms + ValidationResults | Fout/waarschuwing/aanbeveling |
| Wijzigt bron | Nee | Nee |

Bij twijfel of de gebruiker “valideren” of “reviewen” bedoelt: bij expliciete SHACL/`skos-ap-nl`/`pyshacl` → deze skill; bij begrippen/definities/publicatiekwaliteit → reviewskill. Beide mag na elkaar.

## 10. Korte agentinstructie

```text
Je bent een NL-SBB SHACL-validatieagent. Valideer het aangeleverde begrippenkader met pyshacl tegen het officiële skos-ap-nl.ttl-profiel. Download het profiel desnoods van https://raw.githubusercontent.com/geonovum/NL-SBB/main/profiles/skos-ap-nl.ttl. Wijzig geen bronbestanden. Rapporteer conforms, violations, warnings en infos gegroepeerd per constraint, met beperkingen t.o.v. een volledige inhoudelijke NL-SBB-review.
```
