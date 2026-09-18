# Diagrammityypit - Yleiskatsaus

Mermaid tukee **14+ diagrammityyppiä**. Jokaisella on oma syntaksinsa ja käyttötapauksensa.

## Luokittelu

### Rakenteelliset (Structural)
| Tyyppi | Avainsana | Kuvaus |
|--------|-----------|--------|
| Luokka | `classDiagram` | OO-suunnittelu, UML-luokkakaaviot |
| Objekti | `objectDiagram` | Olioiden instanssit ja suhteet |
| Komponentti | `componentDiagram` | Järjestelmän komponentit ja riippuvuudet |
| Paketti | `packageDiagram` | Pakettirakenne ja riippuvuudet |
| Käyttötapaus | `useCaseDiagram` | Toiminnallisuus käyttäjän näkökulmasta |

### Käyttäytymiset (Behavioral)
| Tyyppi | Avainsana | Kuvaus |
|--------|-----------|--------|
| Sekvenssi | `sequenceDiagram` | Viestinvaihto aikajärjestyksessä |
| Tila | `stateDiagram-v2` | Olion tilat ja siirtymät |
| Toiminta | `activityDiagram` | Työnkulut, haarautuminen, yhdistäminen |
| Aikajana | `timeline` | Tapahtumien kronologinen esitys |

### Erityistyypit
| Tyyppi | Avainsana | Kuvaus |
|--------|-----------|--------|
| Flowchart | `flowchart` / `graph` | Virtauskaaviot (TD, TB, BT, RL, LR) |
| Gantt | `gantt` | Projektin aikataulutus |
| Git | `gitGraph` | Haarojen ja commitin visualisointi |
| ER | `erDiagram` | Entiteetti-suhde-malli (tietokannat) |
| User Journey | `journey` | Käyttäjän kokemuspolku |
| Pie | `pie` | Tortakaavio |
| Quadrant | `quadrantChart` | Neljänneljäkävio |
| Requirement | `requirementDiagram` | Vaatiimuskaavio |
| C4 | `C4Context` / `C4Container` / `C4Component` / `C4Code` | C4-arkkitehtuurimalli |
| Mindmap | `mindmap` | Mielikartat |
| Kanban | `kanban` | Kanban-taulut |
| Architecture | `architecture-beta` | Arkkitehtuurikaaviot (beta) |

## Prioriteetti täyttämiseen

1. **Korkea**: flowchart, sequenceDiagram, classDiagram, stateDiagram-v2, erDiagram
2. **Keski**: gantt, gitGraph, journey, pie, mindmap, componentDiagram
3. **Matala**: requirementDiagram, quadrantChart, useCaseDiagram, objectDiagram, packageDiagram, kanban, architecture-beta, C4*, timeline

## Seuraavat vaiheet
- [[01-diagrammit/flowchart|Flowchart syväsukellus]]
- [[01-diagrammit/sequenceDiagram|Sequence Diagram syväsukellus]]
- [[01-diagrammit/classDiagram|Class Diagram syväsukellus]]