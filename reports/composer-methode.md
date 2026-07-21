# Technische validatie — werkwijze (Composer)

## Bron van de regels

De technische validatie baseerde ik op de **NL-SBB Review Skill** in [`skills/nl-sbb/nl-sbb-review-skill.md`](../skills/nl-sbb/nl-sbb-review-skill.md). Daarin staan:

- **Stap 3** — wat technisch gecontroleerd moet worden (eigenschappen, termen, definities, bronnen, relaties, topbegrippen, verweesde begrippen, codes)
- **§9–§14** — concrete regels per onderwerp (begrippen, begrippenkader, collecties, labels, definities, bronnen, relaties, topbegrippen/codes)
- **§7** — ernstniveaus (fout / waarschuwing / aanbeveling)

De skill verwijst normatief naar het NL-SBB SKOS-profiel, het **NL-SBB SHACL-profiel**, SKOS en ISO 25964. In de repo staat ook [`nl-sbb-skill-extension.ttl`](../nl-sbb-skill-extension.ttl) met aanvullende SHACL-shapes (o.a. topbegrip met `broader`, harmonisatie binnen hetzelfde kader, dubbele `notation`).

**Die SHACL-bestanden heb ik niet uitgevoerd.** Er is geen formele SHACL-run gedaan tegen `skos-ap-nl.ttl` of `nl-sbb-skill-extension.ttl`. Dat staat ook expliciet in het rapport onder “Gecontroleerde NL-SBB-aspecten”.

---

## Gebruikte tooling

Er is **geen bestaande validatietool in de repo** gebruikt. Ik heb tijdelijk **eigen Python-scripts** geschreven (`tmp-imgeo-review-run.py` en `tmp-imgeo-review-run2.py`), daarna weer verwijderd. Daarnaast:

- **grep/ripgrep** — patroontellingen in `tmp-imgeo.ttl`
- **Handmatig lezen** — steekproeven uit het TTL-bestand (o.a. ConceptScheme-blok, enkele definities)

Er is **geen RDF-parser** gebruikt (geen `rdflib`, geen `pyshacl`, geen SPARQL-engine, geen Skosmos/TopBraid). De Turtle is als **tekst** ingelezen en met **regex** geanalyseerd: subject-blokken splitsen op `<http...>`, patronen zoeken op `skos:prefLabel`, `skos:definition`, `isothes:broaderGeneric`, enz.

---

## Wat de scripts concreet controleerden

| Controle | Methode |
|---|---|
| Aantal `skos:Concept`, `ConceptScheme`, `Collection` | Regex op `a skos:Concept` e.d. |
| Ontbrekende `prefLabel`, `definition`, `inScheme` | Per concept-blok: property aanwezig? |
| Dubbele `prefLabel@nl` | Groeperen op label+taal |
| Topbegrip + bovenliggende relatie (F2) | Concept met `topConceptOf` én `isothes:broaderGeneric`/`skos:broader` |
| Relatie naar geen begrip (F1) | `isothes:broaderGeneric`-doel-URI niet in conceptenlijst |
| Placeholderdefinitie (F3) | `definition` met “definitie ontbreekt” |
| Aanwezigheid `dct:source`, `altLabel`, `notation`, mappingrelaties | Tellen per concept-blok |
| Verweesde begrippen | Geen top + geen enkele semantische/ISO-relatie |
| Collecties | Label en `skos:member` aanwezig; leden tellen |
| Dubbele definities | Zelfde `definition`-tekst bij meerdere begrippen |
| Engels/CamelCase `prefLabel` | Heuristiek op hoofdletters in labels |

---

## Wat níet geautomatiseerd is gecontroleerd

- **SHACL-conformiteit** — niet uitgevoerd
- **Volledige RDF-graf** — geen triple-store, geen inferentie, geen externe URI-oplossing
- **Alle 464 definities inhoudelijk** — steekproef + tellen van identieke/placeholder-teksten
- **Circulaire definities, genus-differentia-typering** — handmatig beoordeeld waar zichtbaar (§11), niet systematisch over alles
- **Turtle-syntaxvalidatie** — geen aparte parser; alleen impliciet via succesvolle regex-parsing

---

## Interpretatie en rapportage

De bevindingen zijn geclassificeerd volgens de **ernstniveaus uit de skill** (§7): bijv. ontbrekende definitie = fout, dubbele voorkeursterm = waarschuwing, `altLabel` toevoegen = aanbeveling.

De conclusie “voldoet gedeeltelijk” is dus gebaseerd op een **rule-based, tekstgebaseerde analyse** volgens de skill-regels — **niet** op een officiële SHACL-validatie of een bestaande validator in deze repo.

---

## Samengevat

| Aspect | Werkwijze |
|---|---|
| Regels | NL-SBB Review Skill (§9–§14); SHACL-bestanden in repo niet uitgevoerd |
| Tooling | Tijdelijke Python-regex-scripts + grep + handmatige steekproef |
| RDF/SHACL | Niet gebruikt |
| Betrouwbaarheid | Goed voor structurele patronen (aantallen, ontbrekende properties, dangling URIs); beperkt voor volledige NL-SBB-conformiteit zonder SHACL-run |
