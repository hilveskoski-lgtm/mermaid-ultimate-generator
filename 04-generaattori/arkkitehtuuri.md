# Generaattori-arkkitehtuuri

## 📊 Architecture Components (Dataview)

```dataviewjs
const pages = dv.pages('"04-generaattori"');
const components = [
    { layer: "Input", items: ["Natural Language", "Code (AST)", "Structured Data (JSON)"] },
    { layer: "Core", items: ["Intent Parser", "Template Engine", "Validator Pipeline", "Optimizer"] },
    { layer: "Output", items: ["Mermaid Source", "SVG/PNG Export", "Interactive HTML"] }
];
for (const c of components) {
    dv.header(3, c.layer);
    dv.list(c.items);
}
```

## Yleiskatsavo

```
┌─────────────────────────────────────────────────────────────┐
│                    MERMAID ULTIMATE GENERATOR               │
├─────────────────────────────────────────────────────────────┤
│  INPUT LAYER                                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Natural     │ │ Code        │ │ Structured  │           │
│  │ Language    │ │ (AST)       │ │ Data (JSON) │           │
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘           │
│         │               │               │                   │
│         └───────────────┼───────────────┘                   │
│                         ▼                                   │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            INTENT PARSER / NORMALIZER               │   │
│  │  - Entiteettien tunnistaminen                       │   │
│  │  - Suhteiden purkaminen                             │   │
│  │  - Diagrammityypin ehdotus                          │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           ▼                                   │
│  CORE ENGINE                                              │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  TEMPLATE ENGINE                                    │   │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐   │   │
│  │  │Flowchart│ │Sequence │ │  Class  │ │  State  │...│   │
│  │  │Template │ │Template │ │Template │ │Template │   │   │
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘   │   │
│  └───────┼───────────┼───────────┼───────────┼────────┘   │
│          │           │           │           │             │
│          ▼           ▼           ▼           ▼             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              VALIDATOR PIPELINE                     │   │
│  │  1. Syntaksivalidaattori (Grammariikka)             │   │
│  │  2. Semanttinen validaattori (Logiikka)             │   │
│  │  3. Render-testaus (Mermaid CLI / Playwright)       │   │
│  │  4. Optimoija (Layout, teema, koko)                 │   │
│  └────────────────────────┬────────────────────────────┘   │
│                           ▼                                   │
│  OUTPUT LAYER                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Mermaid     │ │ SVG/PNG     │ │ Interactive │           │
│  │ Source      │ │ Export      │ │ HTML        │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└─────────────────────────────────────────────────────────────┘
```

## Moduulit

### 1. Intent Parser (`src/parser/intent.ts`)
```typescript
interface ParsedIntent {
  diagramType: DiagramType;
  entities: Entity[];
  relationships: Relationship[];
  metadata: {
    suggestedTheme?: Theme;
    suggestedDirection?: Direction;
    complexity: 'simple' | 'medium' | 'complex';
  };
}
```

### 2. Template Engine (`src/templates/`)
Jokainen diagrammityyppi = oma template-tiedosto Handlebars/Jinja2 -tyyliin

```typescript
interface Template {
  type: DiagramType;
  render(data: TemplateData): string;
  validate(data: TemplateData): ValidationResult;
  getDefaults(): Partial<TemplateData>;
}
```

### 3. Validator Pipeline (`src/validator/`)
```typescript
interface Validator {
  validate(source: string): ValidationResult;
  fix(source: string): string; // auto-fix yleiset virheet
}

const pipeline = [
  new SyntaxValidator(grammar),      // PEG.js / Chevrotain parser
  new SemanticValidator(rules),      // domain-spesifit säännöt
  new RenderValidator(renderer),     // testaillaan renderointi
  new Optimizer(layoutEngine)        // dagre / elkjs layout
];
```

### 4. Layout Engine (`src/layout/`)
- **Dagre** - suuntaa flowcharteille
- **ELKJS** - parempi hierarkkinen layout
- **Mermaid-internal** - sequence, state, class käyttävät omia

## Teknologiavalinnat

| Kerros | Teknologia | Peruste |
|--------|------------|---------|
| Parser | Chevrotain / PEG.js | Virheenkäsittely, CST/AST |
| Templates | Handlebars / Eta | Logiikka templateissa, partialit |
| Validaattori | Zod + custom | Schema-validaatio + custom rules |
| Layout | ELKJS + Dagre | Tehdasasetukset, optimaaliset sijainnit |
| Render-testaus | @mermaid-js/mermaid-cli | Headless render, virheiden palautus |
| CLI | Commander.js / CAC | Moderni, tyyppituki |
| Testit | Vitest | Nopea, ESM-valmis |

## Datastruktuurit

### Entity
```typescript
interface Entity {
  id: string;
  label: string;
  type: 'node' | 'actor' | 'class' | 'state' | 'entity';
  properties: Record<string, any>; // kentät, metodit, attribuutit
  style?: StyleConfig;
  metadata?: Record<string, any>;
}
```

### Relationship
```typescript
interface Relationship {
  from: string;
  to: string;
  type: EdgeType;
  label?: string;
  properties?: Record<string, any>;
  style?: StyleConfig;
}
```

## Konfiguraatio (generaattori.config.json)
```json
{
  "defaults": {
    "theme": "default",
    "direction": "TD",
    "fontSize": 14,
    "fontFamily": "Arial"
  },
  "templates": {
    "customPath": "./templates"
  },
  "validator": {
    "strictMode": true,
    "autoFix": true,
    "renderTest": true
  },
  "optimizer": {
    "enabled": true,
    "layoutEngine": "elkjs",
    "maxIterations": 100
  }
}
```

## CLI-rajapinta
```bash
# Luonnollisesta kieleen
mermaid-gen "luo sekvenssikaavio käyttäjän kirjautumisesta" -o login.mmd

# Koodista (TypeScript)
mermaid-gen --from-code src/auth.ts --type classDiagram -o auth-class.mmd

# JSON-datasta
mermaid-gen --from-json data.json --type flowchart -o flow.mmd

# Interaktiivinen
mermaid-gen --interactive

# Validoi olemassa oleva
mermaid-gen --validate diagram.mmd --fix
```

## Seuraavat vaiheet
- [ ] PEG.js-grammaari Mermaid-syntaksille
- [ ] Template-engine perusrakenne
- [ ] Ensimmäinen template: flowchart
- [ ] Syntaksivalidaattori
- [ ] CLI-scaffolding