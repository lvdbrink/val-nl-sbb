# Vergelijking NL-SBB-reviewrapporten IMGEO

Vergelijking van de reviewuitkomsten in `reports/` en de relatie met de gedocumenteerde methoden, inclusief latere officiële SHACL-validatie.

## Betrokken bestanden

| Rapport | Methodebeschrijving | Kernmethode |
|---|---|---|
| `imgeo-nl-sbb-review-auto.md` | (geen aparte methode-file) | Eerdere/basisreview; Turtle via REST + portaalobservaties |
| `imgeo-nl-sbb-review-grok.md` | `grok-methode.md` | Python + **rdflib**; skillregels; geen SHACL |
| `imgeo-nl-sbb-review-composer.md` | `composer-methode.md` | Python + **regex/tekst**; grep; geen RDF-parser; geen SHACL |
| `imgeo-nl-sbb-review-GPT56terramedium.md` | `gpt-methode.md` | Python + **rdflib**; skillregels; geen SHACL |
| `imgeo-nl-sbb-shaclvalidatie-grok.md` | (beschreven in dat rapport) | **pyshacl** + officieel `skos-ap-nl.ttl`; data `tmp-imgeo.ttl` |

De eerste vier reviews gebruiken dezelfde skill (`skills/nl-sbb/nl-sbb-review-skill.md`) als regelbron. De SHACL-run gebruikt het officiële NL-SBB-profiel:

https://raw.githubusercontent.com/geonovum/NL-SBB/main/profiles/skos-ap-nl.ttl  
(lokaal: `profiles/skos-ap-nl.ttl`; tooling: `requirements.txt`, `scripts/run_imgeo_shacl.py`).

---

## Overeenkomsten tussen skill-reviews (kern)

Alle vier skill-rapporten komen tot hetzelfde totaaloordeel:

- **Beoordeling:** Voldoet gedeeltelijk aan NL-SBB  
- **Publicatie:** onder voorwaarden  
- **Fouten (zelfde drie harde bevindingen):**
  1. `isothes:broaderGeneric` naar URI’s die geen `skos:Concept` zijn (**14** doelen; in Grok/Composer/Auto ook **39** relaties genoemd)
  2. **39** topbegrippen met tegelijk een bovenliggende ISO-relatie
  3. `LandschappelijkGebied` met placeholderdefinitie (“Definitie ontbreekt in de BAG.”)

Gedeelde structuurcijfers:

- **464** Concept, **1** ConceptScheme, **57** Collection  
- alle begrippen hebben `prefLabel@nl`, `definition@nl`, `inScheme`  
- **48** `broaderGeneric`, **9** `narrowerGeneric`, **0** `skos:broader`/`narrower`/`related`  
- geen `dct:source`, geen mappingrelaties, geen `notation`

De methodische verschillen (rdflib vs. regex) hebben deze harde structurele fouten **niet** van elkaar doen afwijken.

---

## Verschillen tussen skill-reviews

### Aantallen

| Metric | auto | grok | composer | GPT |
|---|---:|---:|---:|---:|
| Fouten | 3 | 3 | 3 | 3 |
| Waarschuwingen | **6** | **7** | **7** | **6** |
| Aanbevelingen | 5 | 5 | 5 | 5 |
| Dubbele prefLabel-groepen (W1) | 31 | **32** | 31 | 31 |

### Inhoud waarschuwingen

| Thema | auto | grok | composer | GPT |
|---|---|---|---|---|
| Dubbele prefLabels | W1 (31) | W1 (32) | W1 (31) | W1 (31) |
| Identieke/vage definities | W2 | W2 | W2 | W2 |
| Geen `dct:source` | W3 | W3 | W3 | W3 |
| Scheme-label “Model” | W4 | W4 | W4 | W4 |
| Portaal-URI ≠ ConceptScheme-URI | **W5** | — | — | — |
| Alle begrippen als top / hiërarchie inconsistent | W6 | **W5** | **W5** | **W5** |
| Engelse CityGML-namen als NL-`prefLabel` | — | **W6** | **W6** | — |
| Interne vs. externe `broaderGeneric` door elkaar | — | **W7** | **W7** | — |
| Ontbrekende altLabel/scopeNote/example als waarschuwing | — | — | — | **W6** |

Kort:

- **auto** is de enige met een waarschuwing over **portaalmetadata vs. RDF-URI**.  
- **grok** en **composer** voegen twee extra waarschuwingen toe: Engelse prefLabels (W6) en vermenging interne/externe hiërarchie (W7).  
- **GPT** houdt 6 waarschuwingen; zet ontbrekende alt/scope/example op waarschuwingsniveau i.p.v. (alleen) aanbeveling, en noemt Engelse prefLabels / interne-vs-externe mixed use niet als aparte W.

### Aanbevelingen

| auto / grok / composer (vergelijkbaar) | GPT |
|---|---|
| A1 altLabel | A1 topconcepten herstellen (overlap met F2) |
| A2 notation | A2 ISO-relatiedoelen herstellen (overlap met F1) |
| A3 kapitalisatie labels | A3 dubbele voorkeurstermen |
| A4 scopeNote | A4 bronnen |
| A5 externe CityGML/INSPIRE-mappings | A5 altLabel/scopeNote |

GPT herformuleert deels de **foutcorrecties** als aanbevelingen met hoge prioriteit. De andere rapporten houden aanbevelingen meer op **kwaliteitsverbeteringen** ná herstel van F1–F3.

Kleine detailverschillen:

- kapitalisatie: grok ~51 hoofdletter/CamelCase; composer “ca. 55 Engels/CamelCase”  
- informatief: grok/auto noemen **6102** triples; GPT “6.102”; composer telt **1043 RDF-subjecten** i.p.v. triples (past bij tekst/regex-aanpak)

---

## Herleiding skill-verschillen naar methoden

### 1. Zelfde regelbron, geen SHACL → zelfde kernfouten

Alle skill-methoden lezen de skillregels (§9–§14) en voeren **custom checks** uit. Omdat F1–F3 eenvoudig telbaar zijn in de Turtle (dangling URI’s, top+broader, placeholdertekst), convergeren alle skill-rapporten daarop — ongeacht rdflib of regex.

### 2. rdflib (grok, GPT) vs. regex (composer)

| Aspect | Effect op uitkomst |
|---|---|
| Structurele tellingen (464/57/48/39/14) | **Gelijk** — regex was hier voldoende betrouwbaar |
| Triple-telling | grok/auto/GPT: 6102 triples; composer: subjecten i.p.v. triples |
| Dubbele prefLabels 31 vs 32 | Waarschijnlijk **groeperingsverschil** (bijv. case-normalisatie) — methodisch, niet inhoudelijk anders |
| Engelse prefLabels (W6) | Niet inherent aan rdflib: **composer** én **grok** vonden dit; **GPT** (ook rdflib) niet als W |

Parserkeuze verklaart **niet** de grote inhoudelijke verschillen tussen skill-rapporten; die zitten vooral in **welke bevindingen als waarschuwing worden opgevoerd**.

### 3. Broninvoer: URL/portaal vs. lokaal bestand

- **auto** keek (ook) naar portaalgedrag → unieke W5 over portaal-URI.  
- **composer** en **GPT** startten van lokaal `tmp-imgeo.ttl` → geen portaalwaarschuwing.  
- **grok** downloadde REST-Turtle; HTML-portaal timeout → geen portaal-W, wel RDF-only analyse.

### 4. Classificatie en diepte van inhoudelijke review

Verschillen in W6/W7 en aanbevelingen komen vooral door **agentinterpretatie**, niet door toolingkeuze.

---

## SHACL-methode vs. skill-methoden

### Methodeverschil

| | Skill-reviews (auto/grok/composer/GPT) | SHACL-validatie (Grok) |
|---|---|---|
| Regelbron | Review-skill §9–§14 (+ interpretatie) | Officieel `skos-ap-nl.ttl` |
| Tooling | Custom Python (rdflib of regex) | **pyshacl 0.40.0** |
| Ernstniveaus | Fout / waarschuwing / aanbeveling (skill) | Violation / Warning / Info (SHACL) |
| Inhoudelijke kwaliteit | Steekproef (definities, Engelse labels, …) | Alleen wat shapes afdwingen |
| Reproduceerbaarheid | Afhankelijk van agentscript/-keuzes | Deterministisch t.o.v. shapes + data |

### Uitkomstverschil (hoofdzaak)

| Aspect | Skill-reviews | Officiële SHACL |
|---|---|---|
| Totaaloordeel | **Voldoet gedeeltelijk** | Machine: **`conforms = true`** |
| Harde fouten / violations | **3** (F1–F3) | **0** |
| Waarschuwingen | 6–7 thematische W’s | **351** machine-warnings |
| Publicatieadvies skill | Onder voorwaarden | Formeel “conform”, maar met veel warnings |

### Mapping van skill-bevindingen naar SHACL

| Skill-bevinding | SHACL-resultaat | Verklaring |
|---|---|---|
| **F1** dangling `broaderGeneric` (14 doelen / 39 relaties) | **Warning** (39× `Concept-broaderGeneric`) | Shape heeft `sh:class skos:Concept` maar severity **Warning**, geen Violation |
| **F2** top + `isothes:broaderGeneric` (39) | **Niet gevonden** | `TopConceptHavingBroader` toetst alleen `skos:broader` |
| **F3** placeholderdefinitie | **Niet gevonden** | Alleen `definition` minCount ≥ 1; geen tekstinhoud |
| W1 dubbele prefLabels | **Warning** (254 resultaten / 127 focusnodes) | Zelfde issue; andere telling (paargewijs per focusnode) |
| W3 geen `dct:source` | **Niet gevonden** | `Concept-source` heeft geen `sh:minCount` |
| W4 scheme-titel zwak (“Model”) | **Warning**: mist `dct:title` | SHACL eist `dct:title`, niet `rdfs:label`/`skos:prefLabel` |
| Collecties OK via `rdfs:label` | **Warning** (57× mist `skos:prefLabel`) | **Nieuw** t.o.v. alle skill-reviews |
| Engelse prefLabels / mixed hierarchy / vage definities | Niet of deels | Buiten officiële shapes |

### Wat SHACL wél en níet toevoegt

**Wel:**

- Reproduceerbare machinecontrole tegen het officiële Geonovum-profiel.  
- Bevestigt F1-technisch (dangling doelen), maar milder geclassificeerd.  
- Bevestigt dubbele prefLabels en ontbrekende scheme-`dct:title`.  
- Signaleert collectie-`prefLabel`-probleem dat skill-reviews oversloegen.

**Niet:**

- Geen vervanging van skill-oordeel “gedeeltelijk voldoen”: formeel **conform** ondanks 351 warnings.  
- Mist F2 en F3 die skill-reviews als blokkerend zagen.  
- Geen inhoudelijke review (placeholdertekst, CityGML als NL-label, bronkwaliteit).  
- Projectextensie `nl-sbb-skill-extension.ttl` (strengere top+ISO-broader e.d.) is **niet** meegedraaid.

### Methodeles skill vs. SHACL

De spreiding tussen skill-agents (6 vs. 7 waarschuwingen, formulering van aanbevelingen) is **klein** vergeleken met het gat tussen **skill-cluster** en **officiële SHACL**:

- Skill-cluster: eensgezind over drie harde fouten → “gedeeltelijk”.  
- SHACL: 0 violations → “conforms”, terwijl twee van die drie fouten buiten de shapes vallen en de derde alleen Warning is.

Daarmee is de keuze **skill vs. officieel SHACL-profiel** bepalender voor het oordeel dan rdflib vs. regex of welk LLM de skill uitvoert.

---

## Samenvatting

| Vraag | Antwoord |
|---|---|
| Verschillen tussen skill-reviews? | Ja, vooral in **waarschuwingen** (6 vs. 7), **W1-telling** (31 vs. 32), **aanbevelingsformulering** (GPT), en **portaal-W** (auto). Kernfouten F1–F3 gelijk. |
| Te herleiden naar skill-methoden? | **Deels** (bronobservatie, groepering, interpretatiediepte); parserkeuze rdflib/regex niet beslissend. |
| Verschilt SHACL van skill-reviews? | **Ja, wezenlijk:** skill → gedeeltelijk + 3 fouten; SHACL → **conforms=true**, 0 violations, 351 warnings; F2/F3 gemist; collectie-`prefLabel` nieuw. |
| Te herleiden naar SHACL-methode? | **Ja.** Andere regelbron (`skos-ap-nl.ttl`), andere ernstmapping, geen inhoudelijke teksttoets, smallere topconcept-SPARQL. |
| Belangrijkste les | Zonder gedeelde classificatie blijven skill-waarschuwingen licht uiteenlopen. **Officiële SHACL alleen** geeft een **positiever formeel oordeel** dan de reviewskill; skill + (eventueel) skill-extensie dekken relationele/inhoudelijke gaten die `skos-ap-nl.ttl` nu niet sluit. |
