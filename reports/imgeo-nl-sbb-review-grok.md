# NL-SBB-reviewrapport

## 1. Samenvatting
Bron: [https://definities.geostandaarden.nl/imgeo](https://definities.geostandaarden.nl/imgeo) (Turtle via `https://definities.geostandaarden.nl/rest/v1/imgeo/data`)
Type invoer: URL / Turtle (Skosmos)
Beoordeling: **Voldoet gedeeltelijk aan NL-SBB**
Aantal fouten: **3** (met meerdere instanties)
Aantal waarschuwingen: **7**
Aantal aanbevelingen: **5**
Aantal informatieve bevindingen: **8**
Korte conclusie: De basisstructuur (ConceptScheme, Concept, Collection, prefLabel, definition, inScheme) is grotendeels op orde, maar er zijn harde fouten rond ISO-hiërarchie naar niet-bestaande begrippen, topbegrippen met bovenliggende relaties, en minstens één placeholderdefinitie.

## 2. Totaaloordeel
Het kader is technisch herkenbaar als SKOS/NL-SBB-achtig begrippenkader: **464** begrippen, **1** conceptscheme, **57** collecties. Alle begrippen hebben een Nederlandse `skos:prefLabel`, een `skos:definition` en `skos:inScheme` naar `http://definities.geostandaarden.nl/imgeo`.

Het voldoet **niet volledig**, omdat:
- `isothes:broaderGeneric` in **39** gevallen verwijst naar **14** URI’s binnen de IMGeo-namespace die **geen** `skos:Concept` zijn (CityGML-achtige klassen zoals `Cityfurniture`, `Landuse`, `_cityobject`);
- **39** begrippen tegelijk `skos:topConceptOf` / `skos:hasTopConcept` én een bovenliggende ISO-relatie hebben;
- `LandschappelijkGebied` geen inhoudelijke definitie heeft (placeholdertekst).

Daarmee is publicatie als NL-SBB-conform nu niet verantwoord zonder herstel van deze relatie-, topconcept- en definitieproblemen.

## 3. Fouten
| Nr. | Begrip/onderdeel | Bevinding | Waarom dit niet voldoet aan NL-SBB | Advies |
|---|---|---|---|---|
| F1 | 14 doelen van `isothes:broaderGeneric` (o.a. `Cityfurniture`, `Landuse`, `Waterbody`, `_cityobject`, `_site`, `Plantcover`, `Trafficarea`, `Buildingpart`) — 39 relaties | Semantische/ISO-relaties wijzen naar URI’s in `.../imgeo/id/begrip/...` die niet als `skos:Concept` voorkomen | Semantische relatie mag niet naar iets verwijzen dat geen begrip is | Ontbrekende begrippen opnemen, of stabiele externe URI’s (CityGML/INSPIRE) gebruiken met passende mapping/ISO-relatie |
| F2 | 39 begrippen met `skos:topConceptOf` én `isothes:broaderGeneric` (o.a. `Buurt`, `Kunstwerkdeel`, `Bak`, `Registratiefgebied`, `Pand`, `Wegdeel`) | Topbegrip heeft een bovenliggend begrip | Topbegrip mag geen bovenliggend begrip hebben | `skos:topConceptOf` / `skos:hasTopConcept` verwijderen bij niet-topbegrippen; alleen echte wortels als top markeren |
| F3 | `LandschappelijkGebied` | Definitie is `"Definitie ontbreekt in de BAG."@nl` | Begrip heeft geen echte betekenisomschrijving | Inhoudelijke definitie toevoegen of begrip niet publiceren tot de definitie beschikbaar is |

### Detail F1 — ontbrekende doelen
`Auxiliarytrafficarea`, `Bridgeconstructionelement`, `Buildinginstallation`, `Buildingpart`, `Cityfurniture`, `Landuse`, `Plantcover`, `Railway`, `Solitaryvegetationobject`, `Trafficarea`, `Tunnelpart`, `Waterbody`, `_cityobject`, `_site`

### Detail F2 — topbegrippen met bovenliggende relatie
`Bak`, `Begroeidterreindeel`, `Bord`, `Buurt`, `Functioneelgebied`, `Gebouwinstallatie`, `Imgeo-object`, `Inrichtingselement`, `Installatie`, `Kast`, `Kunstwerkdeel`, `Mast`, `Onbegroeidterreindeel`, `Ondersteunendwaterdeel`, `Ondersteunendwegdeel`, `Ongeclassificeerdobject`, `Openbareruimte`, `Openbareruimtelabel`, `Overbruggingsdeel`, `Overigbouwwerk`, `Overigeconstructie`, `Overigescheiding`, `Paal`, `Pand`, `Put`, `Registratiefgebied`, `Scheiding`, `Sensor`, `Spoor`, `Stadsdeel`, `Straatmeubilair`, `Tunneldeel`, `Vegetatieobject`, `Waterdeel`, `Waterinrichtingselement`, `Waterschap`, `Wegdeel`, `Weginrichtingselement`, `Wijk`

## 4. Waarschuwingen
| Nr. | Begrip/onderdeel | Bevinding | Waarom dit aandacht vraagt volgens NL-SBB | Advies |
|---|---|---|---|---|
| W1 | 32 groepen dubbele `skos:prefLabel@nl` (o.a. `plus-type`×19, `niet-bgt`×18, `transitie`×13, `zand`×4, `bgt-type`×4) | Zelfde voorkeursterm voor verschillende begrippen in één kader | Dubbele voorkeurstermen bemoeilijken eenduidig gebruik en zoeken | Unieke, contextuele voorkeurstermen; context desnoods via `altLabel`/`scopeNote` of collectienaam |
| W2 | o.a. 18× `niet-bgt` (“Het object is geen BGT object.”), 12× `transitie` (“De waarde is tijdens transitie niet bekend.”) | Identieke, niet-onderscheidende definities voor verschillende begrippen | Definitie moet het begrip afbakenen | Definitie specificeren per objecttype/attribuutcontext |
| W3 | Alle 464 begrippen | Geen `dct:source` | Bronherleidbaarheid ontbreekt structureel | Bronnen koppelen (gegevenscatalogus IMGeo/BGT, normdocumenten) |
| W4 | ConceptScheme `.../imgeo` | Label/titel is `"Model"@nl`; geen `skos:prefLabel` / `dct:title` | Begrippenkader mist een duidelijke publieke titel | Titel/label `IMGeo` (of volledige naam) als voorkeurstitel zetten |
| W5 | Alle 464 begrippen | Ieder begrip is via `skos:hasTopConcept` als top gemarkeerd; hiërarchie vooral via ISO-relaties + 57 collecties; 0× `skos:broader`/`narrower`/`related` | Topconcept-gebruik en hiërarchie zijn inhoudelijk inconsistent | Tops beperken tot wortels; interne specialisaties als hiërarchie modelleren; collecties voor waardelijsten |
| W6 | o.a. `Pand`→`BuildingPart`, `Wegdeel`→`TrafficArea`, `Begroeidterreindeel`→`PlantCover`, `Inrichtingselement`→`CityFurniture`, `Imgeo-object`→`_CityObject` | Engelse CityGML-klassenamen als Nederlandse `prefLabel`, terwijl URI/definitie Nederlands zijn | Voorkeursterm moet de publieke term zijn; taal/label moeten aansluiten bij de definitie | Nederlandse voorkeursterm als `prefLabel`; CityGML-naam als `altLabel` of via externe mapping |
| W7 | 9 geldige `isothes:broaderGeneric`-relaties (o.a. `Buurt`→`Registratiefgebied`, `Kunstwerkdeel`→`Overigeconstructie`) naast 39 dangling | Interne specialisatie en externe CityGML-koppeling zijn hetzelfde relatietype | Onderscheid interne hiërarchie vs. externe alliantie wordt onduidelijk | Interne hiërarchie via `skos:broader` of ISO-generic naar bestaande IMGeo-begrippen; CityGML via mapping/`exactMatch`/`closeMatch` |

## 5. Aanbevelingen
| Nr. | Onderdeel | Aanbeveling | Reden | Prioriteit |
|---|---|---|---|---|
| A1 | Labels | `skos:altLabel` toevoegen voor synoniemen/afkortingen/CityGML-namen (nu 0) | Betere vindbaarheid zonder voorkeursterm te vervuilen | Midden |
| A2 | Codes | `skos:notation` overwegen voor waardelijstcodes | Beheer en uitwisseling van domeinwaarden | Midden |
| A3 | Schrijfwijze | Kapitalisatie van voorkeurstermen harmoniseren (nu ~51 met hoofdletter/CamelCase, ~413 zonder) | Consistentie in publicatie | Laag |
| A4 | Notities | `skos:scopeNote` bij begrippen die in meerdere waardelijsten voorkomen (`plus-type`, `niet-bgt`, `transitie`) | Context/afbakening zonder definitie te herhalen | Midden |
| A5 | Externe allianties | CityGML/INSPIRE-koppelingen via stabiele externe URI’s + eventueel `skos:*Match` | Duidelijker onderscheid interne hiërarchie vs. externe harmonisatie | Hoog |

## 6. Informatieve bevindingen
- **464** `skos:Concept`, **1** `skos:ConceptScheme`, **57** `skos:Collection`, **6102** triples
- Alle begrippen: `prefLabel@nl`, `definition@nl`, `inScheme` → `http://definities.geostandaarden.nl/imgeo`
- **0** `altLabel` / `hiddenLabel` / `notation` / `scopeNote` / `example` / mappingrelaties (`exactMatch` e.d.)
- **48** `isothes:broaderGeneric`, **9** `isothes:narrowerGeneric`; **0** standaard `skos:broader`/`narrower`/`related`
- **362** begrippen zitten in collecties; **102** niet (vooral objecttypen/metadata)
- Collecties zijn gelabeld en hebben leden (waardelijsten zoals `TypeWater`, `FysiekVoorkomen...`)
- Geen dubbele `skos:notation` (niet gebruikt); geen harmonisatierelaties binnen hetzelfde kader
- Bron kon volledig worden gelezen via de Turtle-dump (~547 KB)

## 7. Gecontroleerde NL-SBB-aspecten
| Aspect | Gecontroleerd |
|---|---|
| Concept / ConceptScheme / Collection | Ja |
| prefLabel, definition, inScheme | Ja |
| Taal-tags `@nl` | Ja |
| Dubbele voorkeurstermen | Ja |
| Bronnen (`dct:source`) | Ja (afwezig) |
| Semantische + ISO 25964-relaties | Ja |
| Harmonisatierelaties | Ja (niet gebruikt) |
| Topbegrippen / verweesde begrippen | Ja |
| Codes/`notation` | Ja (niet gebruikt) |
| Inhoudelijke steekproef definities | Ja (niet alle 464 diep inhoudelijk beoordeeld) |
| SHACL-machinevalidatie tegen officieel NL-SBB-shapesbestand | Nee (geen SHACL-run in deze review) |

## 8. Publicatieadvies
- Geschikt voor publicatie: **onder voorwaarden**
- Belangrijkste blokkade: dangling `broaderGeneric`-doelen en topbegrippen met bovenliggende relatie
- Belangrijkste verbeterpunt: hiërarchie/topconcepts rechtzetten en ontbrekende/externe begrippen correct modelleren
- Aanbevolen vervolgstap: F1–F3 herstellen, daarna dubbele voorkeurstermen, Engelse prefLabels en bronnen aanpakken, opnieuw valideren

---

**Geanalyseerde bron:**
- Type invoer: URL + Turtle-export
- Naam/URL: IMGEO — [definities.geostandaarden.nl/imgeo](https://definities.geostandaarden.nl/imgeo)
- Kon de inhoud volledig worden gelezen: **ja** (via REST Turtle)
- Beperkingen: geen formele SHACL-run; inhoudelijke beoordeling van definities steekproefsgewijs; HTML-portaalpagina niet volledig opgehaald (timeout), RDF-export wel
- Reviewdatum: 2026-07-20
