# Mermaid Ultimate Generator - Obsidian Vault

## 🎯 Tavoite
Kehittää **ultimaattinen Mermaid-generaattori** joka:
- Ymmärtää kaikki Mermaid-diagrammityypit syvällisesti
- Generoi optimaalista, validia syntaksia
- Tukee kaikkia Mermaid-ominaisuuksia (teemat, tyylit, konfiguraatiot)
- Integroituu helposti erilaisiin työkaluihin

## 📁 Rakenne

| Kansio | Kuvaus |
|--------|--------|
| `00-meta` | Projektin yleisluonne, roadmap, muistiinpanot |
| `01-diagrammit` | Kunkin diagrammityypin syväoppiminen |
| `02-syntaksi` | Syntaksisääntöjen, grammariikan, validoinnin dokumentaatio |
| `03-esimerkit` | Kuratoidut, testatut esimerkit per tyyppi |
| `04-generaattori` | Generaattorin arkkitehtuuri, koodi, algoritmit |
| `05-testaus` | Testitapausten, validointien, regression-testien hallinta |
| `99-arkisto` | Vanhentuneet, referenssimateriaalit |

## 📊 Vault Statistics (Dataview)

```dataviewjs
const pages = dv.pages('""');
const mmdFiles = pages.where(p => p.file.ext === "mmd" || p.file.content?.includes("```mermaid"));
const mdFiles = pages.where(p => p.file.ext === "md");
const totalDiagrams = mmdFiles.length;
const byType = {};
for (const page of mmdFiles) {
    const match = page.file.content?.match(/```mermaid\s*(\w+)/);
    const type = match ? match[1] : "unknown";
    byType[type] = (byType[type] || 0) + 1;
}
dv.table(["Metric", "Value"], [
    ["Total .md files", mdFiles.length],
    ["Total Mermaid diagrams", totalDiagrams],
    ["Diagram Types", Object.keys(byType).length],
]);
dv.table(["Type", "Count"], Object.entries(byType).sort((a,b) => b[1]-a[1]));
```

## 🚀 Roadmap

### Phase 1: Tietokanta (viikko 1-2)
- [ ] Kaikki 14+ diagrammityyppi dokumenteittu
- [ ] Syntaksigrammariikka formuloitu
- [ ] 100+ validia esimerkkiä kerätty

### Phase 2: Generaattori core (viikko 3-4)
- [ ] AST-parser Mermaidille
- [ ] Template-engine diagrammityypeille
- [ ] Validaattori (syntaksi + semanttiikka)

### Phase 3: Älykkyys (viikko 5-6)
- [ ] Luonnollisesta kieleen diagrammiksi
- [ ] Koodista diagrammiksi (reverse engineering)
- [ ] Optimoija (layout, teemat, koko)

### Phase 4: Integraatiot (viikko 7-8)
- [ ] CLI-työkalu
- [ ] VS Code / Obsidian plugin
- [ ] API / MCP-palvelin

## 📚 Keskeiset resurssit

- [Mermaid Live Editor](https://mermaid.live)
- [Mermaid GitHub](https://github.com/mermaid-js/mermaid)
- [Mermaid Documentation](https://mermaid.js.org)

## 🔗 Linkit
- [[01-diagrammit/index|Diagrammityypit]]
- [[02-syntaksi/index|Syntaksi & Grammariikka]]
- [[03-esimerkit/index|Esimerkkikokoelma]]
- [[04-generaattori/arkkitehtuuri|Generaattori-arkkitehtuuri]]