# Service Design Examples

Curated service design diagrams for construction industry use cases.

## Diagrams

### 1. Daily Construction Site Process (Swimlane Flowchart)

**File:** `daily_process_swimlane.mmd` / `daily_process_swimlane_pure.mmd`

**Description:** Complete daily workflow for construction site management with swimlanes for Worker, Site Manager, Safety Officer, and Planner.

**Time Segments:**
- Morning (06:00-08:00): Arrival, briefing, safety check
- Before Break (08:00-10:00): Work execution, issue resolution
- Break (10:00-10:30): Progress check
- Before Lunch (10:30-12:00): Work continuation, handover prep
- Lunch (12:00-12:45): Logistics check
- Afternoon (12:45-15:30): Completion, quality check, acceptance
- Handover (15:30-16:00): Shift transition

**Swimlanes:**
- 👷 Työntekijä (Worker)
- 👨‍💼 Työmaapäällikkö (Site Manager)
- 🛡️ Turvallisuus (Safety)
- 📋 Suunnittelija (Planner)

**Key Decision Points:**
- Material availability check
- Issue resolution (material/resource/technical)
- Safety observation reporting
- Go/No-go for afternoon work
- Quality acceptance

### 2. Material Logistics - ER Diagram

**File:** `material_logistics_er.mmd` / `material_logistics_er_pure.mmd`

**Description:** Entity-relationship model for construction material logistics.

**Entities:**
- `WORKSITE` - Construction site
- `WORK_PACKAGE` - Work packages within site
- `TASK` - Individual tasks
- `MATERIAL_CATALOG` - Material master data
- `MATERIAL_REQUIREMENT` - Task-material requirements
- `SUPPLIER` - Supplier master data
- `SUPPLIER_CATALOG` - Supplier-specific materials
- `MATERIAL_REQUEST` - Purchase requests
- `MATERIAL_REQUEST_LINE` - Request line items
- `DELIVERY` - Goods receipt
- `DELIVERY_LINE` - Delivery line items
- `STOCK_LEVEL` - Site inventory levels

**Key Relationships:**
- Worksite → Work Package (1:N)
- Work Package → Task (1:N)
- Task → Material Requirement (1:N)
- Material Requirement → Material Catalog (N:1)
- Material Request → Supplier (N:1)
- Delivery → Material Request (1:1)
- Stock Level → Worksite + Material (unique)

### 3. Material Logistics - Sequence Diagram

**File:** `material_logistics_sequence.mmd` / `material_logistics_sequence_pure.mmd`

**Description:** End-to-end material flow from planning to task execution.

**Actors:**
- Planner (Suunnittelija)
- Site Manager (Työmaapäällikkö)
- Worker (Työntekijä)
- Mobile App (Mobiilisovellus)
- ERP System (ERP-järjestelmä)
- Supplier (Toimittaja)
- Logistics Service (Logistiikkapalvelu)

**Key Flows:**
1. **Planning & Requirement Definition** - Planner creates work packages, defines material needs
2. **Stock Check & Ordering** - ERP checks stock, creates purchase orders for shortages
3. **Delivery & Receiving** - Supplier delivers, Site Manager receives via Mobile, 3-way match
4. **Task Execution** - Worker checks material availability, executes task, reports progress
5. **Exception Handling** - Emergency orders for missing materials, quality rejection handling

**Exception Paths:**
- Emergency material order (express delivery)
- Quality rejection & RMA process

## Usage

```bash
# Validate all
python .opencode/skills/mermaid-syntax-validator/validate.py *.mmd

# Render to PNG
python .opencode/skills/mermaid-renderer/render.py daily_process_swimlane.mmd -o daily_process.png
python .opencode/skills/mermaid-renderer/render.py material_logistics_er.mmd -o material_er.png
python .opencode/skills/mermaid-renderer/render.py material_logistics_sequence.mmd -o material_seq.png

# Generate from generator
python .opencode/skills/mermaid-generator/generator.py flowchart daily_process_swimlane_pure.mmd -o output.mmd
```

## Tags

`#service-design` `#construction` `#logistics` `#process-modeling` `#swimlane` `#sequence-diagram` `#er-diagram`