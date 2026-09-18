# material_logistics_sequence

```mermaid
sequenceDiagram
    autonumber
    actor Planner as Suunnittelija
    actor SiteManager as Työmaapäällikkö
    actor Worker as Työntekijä
    participant Mobile as Mobiilisovellus
    participant ERP as ERP-järjestelmä
    participant Supplier as Toimittaja
    participant Logistics as Logistiikkapalvelu
    
    Note over Planner,Logistics: 1. TEHTÄVÄN SUUNNITTELU JA TARVELUETTELO
    
    Planner->>ERP: Luo työpaketti ja tehtävät
    activate ERP
    ERP-->>Planner: Työpaketti luotu (ID: WP-001)
    deactivate ERP
    
    Planner->>ERP: Määritä materiaalitarpeet per tehtävä
    activate ERP
    ERP->>ERP: Hae materiaaliluettelo (BOM)
    ERP-->>Planner: Tarveluettelo valmis (15 kpl)
    deactivate ERP
    
    Note over Planner,Logistics: 2. VARASTON TARKISTUS JA TILAUS
    
    Planner->>ERP: Tarkista varastotilanne (Worksite: WS-001)
    activate ERP
    ERP->>ERP: Lasketaan saatavilla = on_hand - reserved
    alt Varasto riittää
        ERP-->>Planner: Materiaalit varattu (Reserved qty updated)
    else Varasto ei riitä
        ERP-->>Planner: Puutteet havaittu (7 kpl)
        Planner->>ERP: Luo materiaalipyyntö (MR-042)
        activate ERP
        ERP->>ERP: Valitse toimittaja (lead time, hinta)
        ERP->>Supplier: Lähetä tilaus (PO-1234)
        activate Supplier
        Supplier-->>ERP: Vahvista tilaus (toim. 3 pv)
        deactivate Supplier
        ERP-->>Planner: Pyntö luotu, tilaus lähetetty
        deactivate ERP
    end
    
    Note over Planner,Logistics: 3. TOIMITUS JA VASTAANOTTO
    
    Supplier->>Logistics: Toimitusvalmistelu (pakkaus, asiakirjat)
    activate Logistics
    Logistics->>Logistics: Reittisuunnittelu, ajankohta
    Logistics-->>Supplier: Noutoajan varaus
    deactivate Logistics
    
    Supplier->>SiteManager: Toimitus saapuu työmaalle (DLV-089)
    activate SiteManager
    SiteManager->>Mobile: Skannaa toimitus (QR/viivakoodi)
    activate Mobile
    Mobile->>ERP: Vastaanota toimitus (DLV-089)
    activate ERP
    ERP->>ERP: Tarkista: tilaus vs. toimitus (3-tason tarkistus)
    alt Toimitus OK
        ERP->>ERP: Päivitä varasto (on_hand += qty)
        ERP->>ERP: Vapauta varaukset (reserved -= qty)
        ERP-->>Mobile: Vastaanotto hyväksytty
        Mobile-->>SiteManager: ✅ Materiaalit vastaanotettu
    else Virhe toimituksessa
        ERP-->>Mobile: ⚠️ Ero havaittu (qty/laatu/asiakirjat)
        Mobile-->>SiteManager: Merkitse poikkeama
        SiteManager->>Supplier: Ota yhteyttä (palautus/korvaus)
        activate Supplier
        Supplier-->>SiteManager: Korvaava toimitus / hyvitys
        deactivate Supplier
    end
    deactivate ERP
    deactivate Mobile
    deactivate SiteManager
    
    Note over Planner,Logistics: 4. TEHTÄVÄN ALOITUS (materiaalit valmiina)
    
    Worker->>Mobile: Avaa tehtävä (TASK-007)
    activate Mobile
    Mobile->>ERP: Hae tehtävän materiaalit
    activate ERP
    ERP-->>Mobile: Lista: 3 kpl (kaikki available)
    deactivate ERP
    Mobile-->>Worker: ✅ Materiaalit valmiina
    deactivate Mobile
    
    Worker->>Mobile: Aloita tehtävä
    activate Mobile
    Mobile->>ERP: Päivitä tila: InProgress, start_time=now
    activate ERP
    ERP-->>Mobile: Tehtävä aloitettu
    deactivate ERP
    deactivate Mobile
    
    Note over Planner,Logistics: 5. EDISTYMYSPÄIVITYS JA LOPETUS
    
    Worker->>Mobile: Päivitä edistyminen (50%, 2h)
    activate Mobile
    Mobile->>ERP: ProgressUpdated(task, 50%, 2h)
    activate ERP
    ERP-->>Mobile: OK
    deactivate ERP
    deactivate Mobile
    
    Worker->>Mobile: Merkitse valmiiksi
    activate Mobile
    Mobile->>ERP: TaskCompleted(task, quality_check=true)
    activate ERP
    ERP->>ERP: Vapauta jäljellä olevat varaukset
    ERP-->>Mobile: Tehtävä valmis, tunnit: 4.5h
    deactivate ERP
    deactivate Mobile
```