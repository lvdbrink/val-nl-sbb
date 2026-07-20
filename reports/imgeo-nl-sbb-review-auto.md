# NL-SBB-reviewrapport

## 1. Samenvatting
Bron: [http://definities.geostandaarden.nl/imgeo](http://definities.geostandaarden.nl/imgeo) (Turtle via `https://definities.geostandaarden.nl/rest/v1/imgeo/data`)  
Type invoer: URL / Turtle (Skosmos)  
Beoordeling: **Voldoet gedeeltelijk aan NL-SBB**  
Aantal fouten: **3** (met meerdere instanties)  
Aantal waarschuwingen: **6**  
Aantal aanbevelingen: **5**  
Aantal informatieve bevindingen: **8**  
Korte conclusie: Basisstructuur (ConceptScheme, Concept, Collection, prefLabel, definition, inScheme) is grotendeels op orde, maar er zijn harde fouten rond ISO-hiërarchie, topbegrippen en minstens één ontbrekende inhoudelijke definitie.

## 2. Totaaloordeel
Het kader is technisch herkenbaar als SKOS/NL-SBB-achtig begrippenkader: 464 begrippen, 1 conceptscheme, 57 collecties, allemaal met Nederlandse voorkeursterm, definitie en `skos:inScheme`.

Het voldoet **niet volledig**, omdat:
- `isothes:broaderGeneric` verwijst naar 14 URI’s binnen het IMGEO-namespace die **geen** `skos:Concept` zijn;
- 39 begrippen tegelijk `skos:topConceptOf` én een bovenliggende ISO-relatie hebben;
- `LandschappelijkGebied` geen inhoudelijke definitie heeft (placeholdertekst).

Daarmee is publicatie als NL-SBB-conform nu niet verantwoord zonder herstel van deze relatie- en topconcept-problemen.

## 3. Fouten
| Nr. | Begrip/onderdeel | Bevinding | Waarom dit niet voldoet aan NL-SBB | Advies |
|---|---|---|---|---|
| F1 | 14 doelen van `isothes:broaderGeneric` (o.a. `Cityfurniture`, `Landuse`, `Waterbody`, `_cityobject`, `_site`) | Semantische/ISO-relaties wijzen naar URI’s in `.../imgeo/id/begrip/...` die niet als `skos:Concept` voorkomen | Semantische relatie mag niet naar iets verwijzen dat geen begrip is | Ontbrekende begrippen opnemen, of externe canonieke URI’s gebruiken (bijv. INSPIRE/CityGML) met passende mapping/ISO-relatie |
| F2 | 39 begrippen met `skos:topConceptOf` én `isothes:broaderGeneric` (o.a. `Buurt`, `Kunstwerkdeel`, `Bak`, `Registratiefgebied`) | Topbegrip heeft een bovenliggend begrip | Topbegrip mag geen bovenliggend begrip hebben | `skos:topConceptOf` / `skos:hasTopConcept` verwijderen bij niet-topbegrippen; alleen echte wortels als top markeren |
| F3 | `LandschappelijkGebied` | Definitie is `"Definitie ontbreekt in de BAG."@nl` | Begrip heeft geen echte betekenisomschrijving | Inhoudelijke definitie toevoegen of begrip niet publiceren tot de definitie beschikbaar is |

## 4. Waarschuwingen
| Nr. | Begrip/onderdeel | Bevinding | Waarom dit aandacht vraagt volgens NL-SBB | Advies |
|---|---|---|---|---|
| W1 | 31 groepen dubbele `skos:prefLabel@nl` (o.a. `plus-type`×19, `niet-bgt`×18, `transitie`×13, `zand`×4) | Zelfde voorkeursterm voor verschillende begrippen in één kader | Dubbele voorkeurstermen bemoeilijken eenduidig gebruik en zoeken | Unieke, contextuele voorkeurstermen; context desnoods via `altLabel`/`scopeNote` of collectienaam |
| W2 | o.a. 18× `niet-bgt`, 12× `transitie` | Identieke, niet-onderscheidende definities voor verschillende begrippen | Definitie moet het begrip afbakenen | Definitie specificeren per objecttype/attribuutcontext |
| W3 | Alle 464 begrippen | Geen `dct:source` | Bronherleidbaarheid ontbreekt structureel | Bronnen koppelen (gegevenscatalogus IMGeo/BGT, normdocumenten) |
| W4 | ConceptScheme `.../imgeo` | Label/titel is `"Model"@nl`; geen `skos:prefLabel` | Begrippenkader mist een duidelijke publieke titel | Titel/label `IMGEO` (of volledige naam) als voorkeurstitel zetten |
| W5 | Portaalmetadata vs. RDF | Portaal toont URI `http://definities.geostandaarden.nl/`; RDF-scheme is `.../imgeo` | Identificatie is inconsistent voor gebruikers en machines | Portaal-URI gelijk trekken met ConceptScheme-URI |
| W6 | Hiërarchie vs. collecties | Bijna geen `skos:broader`/`narrower`; wel ISO-relaties + 57 collecties; alle begrippen als top gemarkeerd | Topconcept-gebruik en hiërarchie zijn inhoudelijk inconsistent | Interne specialisaties als hiërarchie modelleren; collecties voor waardelijsten; tops beperken tot wortels |

## 5. Aanbevelingen
| Nr. | Onderdeel | Aanbeveling | Reden | Prioriteit |
|---|---|---|---|---|
| A1 | Labels | `skos:altLabel` toevoegen voor synoniemen/afkortingen (nu 0) | Betere vindbaarheid zonder voorkeursterm te vervuilen | Midden |
| A2 | Codes | `skos:notation` overwegen voor waardelijstcodes | Beheer en uitwisseling van domeinwaarden | Midden |
| A3 | Schrijfwijze | Kapitalisatie van voorkeurstermen harmoniseren (nu ~51 met hoofdletter, ~413 zonder) | Consistentie in publicatie | Laag |
| A4 | Notities | `skos:scopeNote` bij begrippen die in meerdere waardelijsten voorkomen | Context/afbakening zonder definitie te herhalen | Midden |
| A5 | Externe allianties | CityGML/INSPIRE-koppelingen via stabiele externe URI’s + eventueel `skos:*Match` | Duidelijker onderscheid interne hiërarchie vs. externe harmonisatie | Hoog |

## 6. Informatieve bevindingen
- **464** `skos:Concept`, **1** `skos:ConceptScheme`, **57** `skos:Collection`
- Alle begrippen: `prefLabel@nl`, `definition@nl`, `inScheme` → `http://definities.geostandaarden.nl/imgeo`
- **0** `altLabel` / `hiddenLabel` / `notation` / `scopeNote` / `example` / mappingrelaties (`exactMatch` e.d.)
- **48** `isothes:broaderGeneric`, **9** `isothes:narrowerGeneric`; **0** standaard `skos:broader`/`narrower`/`related`
- **362** begrippen zitten in collecties; **102** niet (vooral objecttypen/metadata)
- Collecties zijn gelabeld en hebben leden (waardelijsten zoals `TypeWater`, `FysiekVoorkomen...`)
- HTML-download “TURTLE” op de portaalpagina gaf geen Turtle; de REST-export wel
- Bron kon volledig worden gelezen via de Turtle-dump (~547 KB, 6102 triples)

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
- Aanbevolen vervolgstap: F1–F3 herstellen, daarna dubbele voorkeurstermen en bronnen aanpakken, opnieuw valideren

---

**Geanalyseerde bron:**
- Type invoer: URL + Turtle-export
- Naam/URL: IMGEO — [definities.geostandaarden.nl/imgeo](http://definities.geostandaarden.nl/imgeo)
- Kon de inhoud volledig worden gelezen: **ja** (via REST Turtle; HTML-download niet bruikbaar)
- Beperkingen: geen formele SHACL-run; inhoudelijke beoordeling van definities steekproefsgewijs
- Reviewdatum: 2026-07-20
