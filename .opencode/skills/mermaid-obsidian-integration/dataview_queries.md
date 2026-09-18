# Dataview Queries for Mermaid Diagrams

Use these queries in Obsidian with the Dataview plugin to query and organize your diagrams.

## Basic Queries

### All diagrams by type
```dataview
TABLE file.folder as Folder, type, tags
FROM ""
WHERE contains(file.content, "```mermaid")
FLATTEN regexmatch(file.content, "```mermaid\\s*(\\w+)") as type
SORT type
```

### Flowcharts only
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE contains(file.content, "flowchart") OR contains(file.content, "graph TD") OR contains(file.content, "graph LR")
```

### Sequence diagrams
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE contains(file.content, "sequenceDiagram")
```

### Class diagrams
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE contains(file.content, "classDiagram")
```

### State diagrams
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE contains(file.content, "stateDiagram")
```

### ER diagrams
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE contains(file.content, "erDiagram")
```

## Advanced Queries

### Diagrams with specific tags
```dataview
TABLE file.folder as Folder, file.name as Name, tags
FROM ""
WHERE contains(file.content, "```mermaid")
AND contains(tags, "architecture")
SORT file.folder
```

### Count diagrams by type
```dataview
TABLE length(rows) as Count
FROM ""
WHERE contains(file.content, "```mermaid")
FLATTEN regexmatch(file.content, "```mermaid\\s*(\\w+)") as type
GROUP BY type
SORT length(rows) DESC
```

### Diagrams modified recently
```dataview
TABLE file.folder as Folder, file.name as Name, file.mtime as Modified
FROM ""
WHERE contains(file.content, "```mermaid")
SORT file.mtime DESC
LIMIT 20
```

### Diagrams by folder
```dataview
TABLE file.name as Name, regexmatch(file.content, "```mermaid\\s*(\\w+)") as Type
FROM "03-esimerkit"
WHERE contains(file.content, "```mermaid")
SORT file.folder, file.name
```

### Find diagrams with specific patterns
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE contains(file.content, "classDef")
AND contains(file.content, "```mermaid")
```

### Diagrams with click handlers
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE contains(file.content, "click ")
AND contains(file.content, "```mermaid")
```

### Diagrams with subgraphs
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE contains(file.content, "subgraph")
AND contains(file.content, "```mermaid")
```

### List all mermaid files
```dataview
LIST
FROM ""
WHERE file.ext = "mmd" OR file.ext = "mermaid"
SORT file.folder
```

## Dashboard Queries

### Diagram inventory dashboard
```dataviewjs
const pages = dv.pages('""').where(p => p.file.content && p.file.content.includes("```mermaid"));
const byType = {};
for (const page of pages) {
    const match = page.file.content.match(/```mermaid\s*(\w+)/);
    const type = match ? match[1] : "unknown";
    if (!byType[type]) byType[type] = [];
    byType[type].push(page.file.link);
}

for (const [type, files] of Object.entries(byType)) {
    dv.header(3, `${type} (${files.length})`);
    dv.list(files);
}
```

### Diagram health check
```dataviewjs
const pages = dv.pages('""').where(p => p.file.content && p.file.content.includes("```mermaid"));
let valid = 0, invalid = 0, warnings = 0;

for (const page of pages) {
    // Simple checks
    const content = page.file.content;
    const hasType = /```mermaid\s*\w+/.test(content);
    const hasNodes = /\[.*?\]|\(.*?\)|\{.*?\}|\(\(.*?\)\)/.test(content);
    const balancedBrackets = (content.match(/\[/g)||[]).length === (content.match(/\]/g)||[]).length &&
                             (content.match(/\(/g)||[]).length === (content.match(/\)/g)||[]).length &&
                             (content.match(/\{/g)||[]).length === (content.match(/\}/g)||[]).length;
    
    if (!hasType) invalid++;
    else if (!hasNodes) warnings++;
    else if (!balancedBrackets) invalid++;
    else valid++;
}

dv.table(["Status", "Count"], [
    ["✅ Valid", valid],
    ["⚠️ Warnings", warnings],
    ["❌ Invalid", invalid]
]);
```

### Render status
```dataview
TABLE file.folder as Folder, file.name as Name, 
       CASE WHEN contains(file.content, "```mermaid") THEN "Has Mermaid" ELSE "No Mermaid" END as Status
FROM ""
WHERE file.ext = "md"
SORT file.folder
```

## Template Queries for One-Pagers

### Strategy documents with diagrams
```dataview
TABLE file.folder as Folder, file.name as Name
FROM "03-strategia"
WHERE contains(file.content, "```mermaid")
```

### Requirements with diagrams
```dataview
TABLE file.folder as Folder, file.name as Name
FROM "02-vaatimukset"
WHERE contains(file.content, "```mermaid")
```

### Cases with diagrams
```dataview
TABLE file.folder as Folder, file.name as Name
FROM "01-tapaukset"
WHERE contains(file.content, "```mermaid")
```

## Maintenance Queries

### Find diagrams with syntax issues (no diagram type)
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE file.ext = "md"
AND contains(file.content, "```mermaid")
AND !regexmatch(file.content, "```mermaid\\s*\\w+")
```

### Diagrams without styling
```dataview
TABLE file.folder as Folder, file.name as Name
FROM ""
WHERE contains(file.content, "```mermaid")
AND !contains(file.content, "classDef")
AND !contains(file.content, "%%{init")
```

### Large diagrams (many lines)
```dataview
TABLE file.folder as Folder, file.name as Name, 
       length(regexmatches(file.content, "```mermaid[\\s\\S]*?```")) as DiagramCount
FROM ""
WHERE contains(file.content, "```mermaid")
SORT DiagramCount DESC
```

## Usage Notes

1. Install Dataview plugin in Obsidian
2. Copy query into a note with ````dataview` ` ` ` or use Dataview Query block
3. Adjust folder paths to match your vault structure
4. Combine with Templater for dynamic reports