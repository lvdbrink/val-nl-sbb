# IMGEO — NL-SBB SHACL-validatie (Grok)

## 1. Opzet

| Item | Waarde |
|---|---|
| Data | `tmp-imgeo.ttl` |
| Officiële standaard | [NL-SBB](https://docs.geostandaarden.nl/nl-sbb/nl-sbb/) |
| SHACL-profiel | `profiles/skos-ap-nl.ttl` (v1.0.0) |
| Bron van het SHACL-bestand | Zie §2 |
| Validator | **pyshacl 0.40.0** (+ rdflib / owlrl) |
| Projecttooling | `requirements.txt`, `scripts/run_imgeo_shacl.py` (blijven staan) |
| Inferentie | RDFS |
| Datum | 2026-07-21 |

## 2. Waar de SHACL-regels vandaan komen

De documentatie op https://docs.geostandaarden.nl/nl-sbb/nl-sbb/ vermeldt:

- niet-normatieve formaten **SHACL** en **SKOS**;
- in §4.3 / specificatie: *“De specificatie is ook in SHACL beschreven en is hier beschikbaar.”*

De concrete download-URL staat niet als stabiel pad onder `docs.geostandaarden.nl/.../skos-ap-nl.ttl` (404). Wel bereikbaar via de Geonovum NL-SBB-repository die bij deze standaard hoort (bevestigd o.a. in [Geonovum/NL-SBB#97](https://github.com/geonovum/NL-SBB/issues/97)):

- https://raw.githubusercontent.com/geonovum/NL-SBB/main/profiles/skos-ap-nl.ttl  
- spiegel: https://geonovum.github.io/NL-SBB/profiles/skos-ap-nl.ttl  

Dit bestand is lokaal opgeslagen als `profiles/skos-ap-nl.ttl`.

**Niet meegenomen in deze run:** `nl-sbb-skill-extension.ttl` (projectextensie; geen officieel NL-SBB-profiel).

## 3. Uitvoering

```text
python scripts/run_imgeo_shacl.py
```

Ruwe artefacten:

- `reports/_shacl-summary-imgeo.txt` — samenvattingstelling
- `reports/_shacl-raw-imgeo.txt` — pyshacl-tekstrapport
- `reports/_shacl-report-imgeo.ttl` — ValidationReport in Turtle

## 4. SHACL-resultaat (machinaal)

| Metric | Waarde |
|---|---|
| **Conforms** | **True** |
| Violations | **0** |
| Warnings | **351** |
| Infos | **0** |

Omdat er geen `sh:Violation` is, rapporteert pyshacl het graph als **conform**, ondanks honderden waarschuwingen.

### 4.1 Waarschuwingen per constraint

| Constraint / shape | Aantal resultaten | Unieke focusnodes | Kernboodschap |
|---|---:|---:|---|
| `UniquePreflabelWithinConceptScheme` | 254 | 127 | Meerdere begrippen met dezelfde voorkeursterm binnen één kader |
| `Collection-label` | 57 | 57 | Collectie mist `skos:prefLabel` (minCount 1); wel vaak `rdfs:label` |
| `Concept-broaderGeneric` | 39 | 39 | Doelwaarde heeft geen class `skos:Concept` |
| `ConceptScheme-label` | 1 | 1 | Begrippenkader mist `dct:title` (minCount 1) |

### 4.2 Detail: dangling `broaderGeneric` (SHACL-Warning)

De 39 resultaten wijzen naar **14** unieke niet-concept-URI’s — dezelfde set als in de skill-reviews:

`Auxiliarytrafficarea`, `Bridgeconstructionelement`, `Buildinginstallation`, `Buildingpart`, `Cityfurniture`, `Landuse`, `Plantcover`, `Railway`, `Solitaryvegetationobject`, `Trafficarea`, `Tunnelpart`, `Waterbody`, `_cityobject`, `_site`

In het officiële profiel heeft `Concept-broaderGeneric` severity **`sh:Warning`** (niet Violation), ondanks `sh:class skos:Concept`.

### 4.3 Wat SHACL níet als Violation/Warning vond (relevant t.o.v. eerdere reviews)

| Skill-reviewbevinding | SHACL-uitkomst | Waarom |
|---|---|---|
| **F2** Topbegrip + `isothes:broaderGeneric` (39) | **Niet gesignaleerd** | `TopConceptHavingBroader` toetst alleen `skos:broader`, niet ISO-`broaderGeneric`/`broaderPartitive`/… |
| **F3** Placeholderdefinitie `LandschappelijkGebied` | **Niet gesignaleerd** | Alleen `skos:definition` minCount ≥ 1; geen inhoudelijke tekstcontrole |
| Ontbrekende `dct:source` op alle begrippen | **Niet gesignaleerd** | `Concept-source` heeft geen `sh:minCount` |
| Engelse CityGML-namen als NL-`prefLabel` | **Niet gesignaleerd** | Geen label-taal/inhoudsregel daarvoor |
| Alle 464 begrippen als top | **Niet als fout** | `hasTopConcept`/`topConceptOf` mag; geen “alleen wortels”-constraint |
| Verweesde begrippen | **0** | `OrphanConcept` is Info én elk begrip is top → filter sluit ze uit |

## 5. Vergelijking met eerdere skill-gebaseerde reviews (zonder SHACL)

Referentie: o.a. `reports/imgeo-nl-sbb-review-grok.md` (skill + custom rdflib; oordeel **voldoet gedeeltelijk**, 3 fouten / 7 waarschuwingen).

| Aspect | Skill-review (Grok e.a.) | Officiële SHACL-run |
|---|---|---|
| Totaaloordeel | Voldoet **gedeeltelijk** | Machine: **conforms = true** |
| Harde blokkades | 3 fouten (F1–F3) | **0 violations** |
| Dangling ISO-doelen | Fout (F1) | Warning (39×) |
| Top + bovenliggend | Fout (F2, via ISO) | **Gemist** (alleen `skos:broader` in shape) |
| Placeholderdefinitie | Fout (F3) | **Gemist** |
| Dubbele prefLabels | Waarschuwing (~31–32 groepen) | Warning (254 resultaten / 127 focusnodes) |
| Scheme-titel | Waarschuwing (“Model” / geen prefLabel) | Warning: geen `dct:title` |
| Collectielabels | OK geacht (`rdfs:label` aanwezig) | Warning: geen `skos:prefLabel` (57×) — **nieuw t.o.v. skill-reviews** |
| Bronnen ontbreken | Waarschuwing | Niet door SHACL |
| Engelse prefLabels / mixed hierarchy | Extra waarschuwingen in sommige reviews | Niet door SHACL |

### Conclusie over “zijn de uitkomsten anders?”

**Ja.** Met officiële SHACL-validatie:

1. Het kader **slaagt** formeel (`conforms=true`), terwijl skill-reviews tot **gedeeltelijk voldoen** met drie harde fouten kwamen.
2. De dangling CityGML-doelen blijven zichtbaar, maar alleen als **Warning**, niet als Violation.
3. Twee skill-fouten (top+ISO-broader, placeholderdefinitie) vallen **buiten** het officiële SHACL-profiel zoals nu geformuleerd.
4. SHACL voegt een **nieuwe** structurele waarschuwing toe: alle 57 collecties missen `skos:prefLabel`.
5. De skill/review-extensie en inhoudelijke kwaliteitstoetsen dekken meer dan `skos-ap-nl.ttl` alleen.

Daarmee is SHACL nuttig als **machinecontrole op het officiële profiel**, maar **geen volledige vervanging** van de NL-SBB-reviewskill (inhoud + strengere relatie-/topconceptregels in de skill/extensie).

## 6. Reproduceerbaarheid

```bash
pip install -r requirements.txt
python scripts/run_imgeo_shacl.py
```

Benodigde bestanden: `tmp-imgeo.ttl`, `profiles/skos-ap-nl.ttl`.
