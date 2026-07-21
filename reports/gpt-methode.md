# Methode voor de technische validatie

De technische validatie was een eigen RDF/SKOS-controle, geen formele NL-SBB-SHACL-validatie.

De regels kwamen uit `skills/nl-sbb/nl-sbb-review-skill.md`. Daarin staan de te controleren NL-SBB-verwachtingen, onder meer:

- elk `skos:Concept` heeft `skos:prefLabel`, `skos:definition` en `skos:inScheme`;
- concepten, begrippenkader en collecties hebben de juiste SKOS-typen;
- maximaal één voorkeursterm per taal en signalering van dubbele voorkeurstermen;
- unieke `skos:notation` binnen een begrippenkader;
- semantische en ISO 25964-relaties mogen alleen naar begrippen wijzen;
- topconcepten mogen geen bovenliggend begrip hebben;
- harmonisatierelaties horen niet binnen hetzelfde begrippenkader;
- controle op bronnen, taal-tags, collectielabels en leden.

Ik heb `tmp-imgeo.ttl` met Python en RDFLib 7.6.0 als Turtle ingelezen. Een tijdelijk Python-script heeft de triples doorlopen en onder andere geteld en gecontroleerd:

- aantallen triples, concepten, conceptschemes en collecties;
- ontbrekende verplichte concept-eigenschappen;
- dubbele `skos:prefLabel`-waarden per taal;
- relatiedoelen die niet als `skos:Concept` voorkomen;
- topconcepten met `skos:broader` of ISO `broader*`;
- verweesde concepten;
- dubbele notaties;
- interne mappingrelaties;
- ontbrekende bronnen;
- gebruikte talen en relevante predicate-aantallen.

Het tijdelijke controlescript is na afloop verwijderd. Het bronbestand is niet aangepast.

## Beperking

Ik heb niet het officiële NL-SBB-SHACL-shapesbestand opgehaald of uitgevoerd. Daardoor is het resultaat een controle tegen de in de review-skill beschreven regels plus inhoudelijke steekproeven, en geen formeel SHACL-conformiteitsresultaat.
