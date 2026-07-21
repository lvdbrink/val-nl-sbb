# Grok-methode: technische validatie IMGEO

De technische validatie was **geen SHACL-machinevalidatie** tegen een officieel NL-SBB-shapesbestand, maar een **regelgestuurde analyse** op basis van de skill en een custom Python-script.

## Waar de regels vandaan kwamen

De te toetsen regels kwamen uit [`skills/nl-sbb/nl-sbb-review-skill.md`](skills/nl-sbb/nl-sbb-review-skill.md), met name:

- §9 Technische validatie (Concept, ConceptScheme, Collection)
- §10 Labels/termen
- §11 Definities
- §12 Bronnen
- §13 Relaties (SKOS, ISO 25964, harmonisatie)
- §14 Topbegrippen, verweesde begrippen, codes
- §7 Ernstniveaus (fout/waarschuwing/aanbeveling)

In dit project stonden **geen** NL-SBB SKOS/SHACL-profielbestanden (geen `.ttl`/`.shacl` met shapes). De skill noemt die wel als normatieve basis, maar die zijn niet lokaal geladen of uitgevoerd.

## Welke bron is gevalideerd

Niet de HTML-pagina, maar de Turtle-export:
`https://definities.geostandaarden.nl/rest/v1/imgeo/data`  
(gedownload met PowerShell `Invoke-WebRequest`, tijdelijk als `imgeo-review.ttl`).

## Welke tooling/scripts

1. **rdflib** (Python) — Turtle inlezen als RDF-graph
2. **Tijdelijke analyse-scripts** (`_analyze_imgeo.py`, `_analyze_imgeo2.py`) — zelf geschreven checks, o.a.:
   - tellen van Concept / ConceptScheme / Collection
   - ontbrekende `prefLabel`, `definition`, `inScheme`
   - dubbele `prefLabel` per scheme+taal
   - topbegrippen met `broaderGeneric`
   - ISO-relaties naar niet-bestaande begrippen
   - bronnen, notations, mappingrelaties, collecties, taal-tags
3. **Handmatige/steekproefsgewijze inspectie** van definities en enkele Turtle-fragmenten
4. **ripgrep** alleen voor snelle stringcontroles in het TTL-bestand

Er is **geen** `pyshacl`, Jena, TopBraid of andere SHACL-validator gebruikt. Na de analyse zijn de tijdelijke TTL en scripts weer verwijderd.
