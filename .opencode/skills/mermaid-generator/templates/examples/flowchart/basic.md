# Perusvirta (Flowchart) - Kirjautuminen

## Kuvaus
Yksinkertainen käyttäjän kirjautumisprosessi demonstroimaan perus Flowchart-elementtejä: aloitus/lopetus, syöte/tulo, besluutus, prosessi ja silmukat.

## Lähdekoodi
```mermaid
flowchart TD
    Start([Aloitus]) --> Input[/Syöte: tunnukset/]
    Input --> Validate{Tunnukset\nkelvolliset?}
    Validate -->|Kyllä| Success[/Kirjautuminen\nonnistui/]
    Validate -->|Ei| Error[/Virhe: väärät\ntunnukset/]
    Error --> Input
    Success --> End([Lopetus])
    
    classDef startEnd fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef process fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef decision fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef io fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    
    class Start,End startEnd;
    class Success,Error process;
    class Validate decision;
    class Input io;
```

## Renderöity
```mermaid
flowchart TD
    Start([Aloitus]) --> Input[/Syöte: tunnukset/]
    Input --> Validate{Tunnukset\nkelvolliset?}
    Validate -->|Kyllä| Success[/Kirjautuminen\nonnistui/]
    Validate -->|Ei| Error[/Virhe: väärät\ntunnukset/]
    Error --> Input
    Success --> End([Lopetus])
    
    classDef startEnd fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef process fill:#f3e5f5,stroke:#4a148c,stroke-width:2px;
    classDef decision fill:#fff3e0,stroke:#e65100,stroke-width:2px;
    classDef io fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
    
    class Start,End startEnd;
    class Success,Error process;
    class Validate decision;
    class Input io;
```

## Selitys

| Rivit | Elementti | Syntaksi | Kuvaus |
|-------|-----------|----------|--------|
| 1 | Diagrammi | `flowchart TD` | Top-Down suunta |
| 2 | Solmut + nuoli | `Start([Aloitus]) --> Input[/.../]` | Ympyrä `()`, parallelogrammi `[/ /]` |
| 3 | Besluutus | `Validate{...}` | Rombi `{}` |
| 4 | Haara Kyllä | `Validate -->|Kyllä| Success[/.../]` | Merkintä nuolen päällä `|teksti|` |
| 5 | Haara Ei | `Validate -->|Ei| Error[/.../]` | Toinen haarautuminen |
| 6 | Silmukka | `Error --> Input` | Takaisin syöttöön |
| 7 | Lopetus | `Success --> End([Lopetus])` | Ympyrä-solmu |
| 9-12 | Tyylit | `classDef nimi fill:,stroke:,stroke-width:` | CSS-tyylit luokille |
| 14-17 | Luokitus | `class SolmuID luokka` | Solmujen tyylien määrittely |

## Solmumuotojen yhtälöt

| Muoto | Syntaksi | Esimerkki | Käyttö |
|-------|----------|-----------|--------|
| Suorakulmio | `id[teksti]` | `A[Prosessi]` | Yleinen prosessi |
| Pyöristetty | `id(teksti)` | `A(Aloitus)` | Aloitus/lopetus |
| Rombi | `id{teksti}` | `A{Ehto?}` | Besluutus |
| Ympyrä | `id((teksti))` | `A((Käynnistys))` | Aloitus/lopetus (vaihtoehto) |
| Parallelogrammi | `id[/teksti/]` | `A[/Syöte/]` | Syöte/tulo |
| Toinen parall. | `id[\teksti\]` | `A[\Tulos\]` | Tulo/syöte (toinen suunta) |
| Asymmetrinen | `id>teksti]` | `A>Viesti]` | Viesti/data |
| Alikäsittely | `id[["teksti"]]` | `A[["Aliohjelma"]]` | Aliohjelmakutsu |
| Synkronointi | `id[("teksti")]` | `A[("Synkki")]` | Synkronointipiste |
| Data | `id[/"teksti"/]` | `A[/"Data"/]` | Data-objekti |

## Yleiset virheet & korjaukset

| Virhe | Oire | Korjaus |
|-------|------|---------|
| Puuttuva `flowchart` | Ei renderöi | Lisää `flowchart TD` ensimmäisenä rivinä |
| Epätasapainoiset sulut | Virheilmoitus parserissa | Tarkista `()`, `{}`, `[]`, `[/ /]` |
| Duplicate ID | Vain ensimmäinen näkyy | Käytä yksilöllisiä ID:tä (`Start`, `Start2`) |
| Viittaus olemattomaan | Nuoli ei näy / virhe | Varmista että kohdesolmu on määritelty |
| Erikoismerkit ID:ssä | Parsing-virhe | Käytä vain `a-z`, `A-Z`, `0-9`, `_` |
| Rivinvaihto merkinnässä | Rikki merkintä | Käytä `\n` merkinnässä: `\|Kyllä\nJatka\|` |

## Variatiot

### 1. Vaakasuunntainen (LR)
```mermaid
flowchart LR
    Start([Aloitus]) --> Input[/Syöte/]
    Input --> Validate{Ehto?}
    Validate -->|Kyllä| Success[/Onnistui/]
    Validate -->|Ei| Error[/Virhe/]
    Error --> Input
    Success --> End([Lopetus])
```

### 2. Ilman tyylejä (minimaalinen)
```mermaid
flowchart TD
    A([Aloitus]) --> B[/Syöte/]
    B --> C{Ehto?}
    C -->|Kyllä| D[/Onnistui/]
    C -->|Ei| E[/Virhe/]
    E --> B
    D --> F([Lopetus])
```

### 3. Alikatsaus (subgraph)
```mermaid
flowchart TD
    subgraph Auth["Kirjautumismoduuli"]
        Input[/Syöte/] --> Validate{Ehto?}
        Validate -->|Kyllä| Success[/Onnistui/]
        Validate -->|Ei| Error[/Virhe/]
        Error --> Input
    end
    Start([Aloitus]) --> Auth
    Success --> End([Lopetus])
```

## Tags
`#flowchart` `#beginner` `#authentication` `#decision` `#loop`

## Viittaukset
- [[02-syntaksi/flowchart|Flowchart syntaksi im detail]]
- [[01-diagrammit/flowchart|Flowchart syväsukellus]]
- [[03-esimerkit/flowchart/styling|Tyylit & luokat (seuraava)]]