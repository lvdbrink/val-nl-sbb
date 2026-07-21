# NL-SBB-reviewrapport

## 1. Samenvatting

- Bron: `tmp-imgeo.ttl`
- Type invoer: Turtle / RDF
- Kon de inhoud volledig worden gelezen: ja
- Beoordeling: **Voldoet gedeeltelijk aan NL-SBB**
- Aantal fouten: **3**
- Aantal waarschuwingen: **6**
- Aantal aanbevelingen: **5**

Korte conclusie: de basisstructuur is op orde. Alle 464 `skos:Concept`-instanties hebben een Nederlandse voorkeursterm, definitie en `skos:inScheme`. Publicatie als NL-SBB-conform is echter niet verantwoord totdat de hiërarchie en topconcepten zijn gecorrigeerd.

## 2. Totaaloordeel

Het begrippenkader is technisch herkenbaar als een SKOS-begrippenkader, met een `skos:ConceptScheme`, concepten en collecties. De harde problemen zitten in ISO-hiërarchieën naar niet-begrippen, topconcepten die tegelijk een bovenliggend begrip hebben, en een placeholder in een definitie.

Daarom voldoet het kader gedeeltelijk aan NL-SBB: herstel is nodig voordat een conformiteitsoordeel of onvoorwaardelijke publicatie verantwoord is.

## 3. Fouten

| Nr. | Begrip/onderdeel | Bevinding | Waarom dit niet voldoet aan NL-SBB | Advies |
|---|---|---|---|---|
| F1 | 14 doelen van `isothes:broaderGeneric` | De ISO-hiërarchie verwijst naar URI's die niet als `skos:Concept` zijn getypeerd, waaronder `Cityfurniture`, `Landuse`, `Waterbody`, `_cityobject` en `_site`. | Een semantische relatie moet naar een begrip verwijzen. | Neem de ontbrekende begrippen op of gebruik stabiele externe URI's met een passende mapping. |
| F2 | 39 topconcepten, waaronder `Buurt`, `Kunstwerkdeel` en `Registratiefgebied` | Begrippen zijn zowel topconcept als ondergeschikt via `isothes:broaderGeneric`. | Een topbegrip mag geen bovenliggend begrip hebben. | Markeer alleen daadwerkelijke wortelbegrippen als topconcept. |
| F3 | `LandschappelijkGebied` | De definitie is: “Definitie ontbreekt in de BAG.” | Dit is geen inhoudelijke betekenisomschrijving van het begrip. | Voeg een inhoudelijke definitie toe of publiceer het begrip niet totdat die beschikbaar is. |

## 4. Waarschuwingen

| Nr. | Begrip/onderdeel | Bevinding | Waarom dit aandacht vraagt volgens NL-SBB | Advies |
|---|---|---|---|---|
| W1 | 31 groepen voorkeurstermen | Dubbele Nederlandse voorkeurstermen, bijvoorbeeld `plus-type` (19), `niet-bgt` (18) en `transitie` (13). | Dit belemmert eenduidig gebruik en zoeken. | Maak termen contextueel onderscheidend. |
| W2 | Onder meer `niet-bgt` en `transitie` | Verschillende begrippen hebben identieke, onvoldoende onderscheidende definities. | Een definitie moet het begrip afbakenen. | Specificeer de definitie per objecttype of attribuutcontext. |
| W3 | Alle 464 begrippen | Er is geen `dct:source`. | Bronherleidbaarheid ontbreekt structureel. | Koppel herleidbare bronnen aan begrippen of beheerdomeinen. |
| W4 | Begrippenkader `.../imgeo` | Het kader heeft alleen `rdfs:label` “Model” en geen `skos:prefLabel`. | De publieke naam is onvoldoende duidelijk. | Geef het kader een duidelijke voorkeurstitel, bijvoorbeeld IMGEO. |
| W5 | Hiërarchie en topconcepten | Alle concepten zijn als topconcept gemarkeerd, terwijl ISO-hiërarchieën aanwezig zijn. | De navigatiestructuur is inhoudelijk inconsistent. | Beperk topconcepten tot de wortels van de hiërarchie. |
| W6 | Labels en notities | `skos:altLabel`, `hiddenLabel`, `scopeNote` en voorbeelden ontbreken. | Context en vindbaarheid zijn beperkt. | Gebruik deze eigenschappen waar synoniemen, gebruikscontext of voorbeelden nodig zijn. |

## 5. Aanbevelingen

| Nr. | Onderdeel | Aanbeveling | Reden | Prioriteit |
|---|---|---|---|---|
| A1 | Topconcepten | Modelleer alleen daadwerkelijke wortelbegrippen als topconcept. | Consistente hiërarchische navigatie. | Hoog |
| A2 | ISO-relaties | Typeer relatiedoelen als concepten of gebruik externe URI's met een passende mapping. | Geldige en interpreteerbare semantische relaties. | Hoog |
| A3 | Labels | Voeg context toe aan dubbele voorkeurstermen. | Eenduidiger gebruik en betere vindbaarheid. | Midden |
| A4 | Bronnen | Voeg per begrip of beheerdomein een herleidbare bron toe. | Beheerbaarheid en verantwoording. | Midden |
| A5 | Notities en alternatieve termen | Gebruik `altLabel` en `scopeNote` waar relevant. | Betere zoekbaarheid en begripsafbakening. | Midden |

## 6. Informatieve bevindingen

- 6.102 triples, 464 concepten, 1 `skos:ConceptScheme` en 57 collecties.
- Alle concepten hebben `skos:prefLabel@nl`, `skos:definition@nl` en `skos:inScheme`.
- Er zijn 48 `isothes:broaderGeneric`- en 9 `isothes:narrowerGeneric`-relaties.
- Er zijn geen standaard `skos:broader`, `skos:narrower` of `skos:related`-relaties.
- Er zijn geen mappingrelaties, notaties of bronverwijzingen.
- De collecties zijn gelabeld met `rdfs:label` en hebben leden.

## 7. Gecontroleerde NL-SBB-aspecten

Gecontroleerd:

- SKOS-typen voor concepten, begrippenkader en collecties;
- voorkeurstermen, definities en `inScheme`;
- taal-tags;
- dubbele voorkeurstermen;
- bronnen;
- collecties;
- semantische en ISO 25964-relaties;
- harmonisatierelaties;
- topconcepten, verweesde begrippen en notaties.

Niet uitgevoerd:

- formele SHACL-validatie met het officiële NL-SBB-shapesbestand;
- volledige diepgaande inhoudelijke beoordeling van alle 464 definities.

## 8. Publicatieadvies

- Geschikt voor publicatie: **onder voorwaarden**
- Belangrijkste blokkade: ISO-relaties naar niet-begrippen en topconcepten met een bovenliggende relatie.
- Belangrijkste verbeterpunt: herstel de hiërarchie en markeer uitsluitend werkelijke wortelbegrippen als topconcept.
- Aanbevolen vervolgstap: herstel F1 tot en met F3 en valideer daarna opnieuw met de officiële NL-SBB-SHACL-shapes.
