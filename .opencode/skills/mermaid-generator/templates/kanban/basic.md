# Kanban Templates

## 1. Basic Team Board
```mermaid
kanban
    title Team Kanban Board
    column Backlog [5]
    column Ready [3]
    column In Progress [3]
    column Review [2]
    column Done [10]
    
    task[Backlog] User research interviews (3d)
    task[Backlog] Competitor analysis (2d)
    task[Backlog] Technical spike: GraphQL (1d)
    task[Ready] Design login flow (2d)
    task[Ready] API spec for payments (3d)
    task[Ready] Database migration plan (1d)
    task[In Progress] Implement authentication
    task[In Progress] Build dashboard UI
    task[In Progress] Write unit tests
    task[Review] Code review: Auth module
    task[Review] QA: Dashboard filters
    task[Done] Project setup
    task[Done] CI/CD pipeline
    task[Done] Design system v1
```

## 2. Service Design Process
```mermaid
kanban
    title Service Design Process
    column Discover [8]
    column Define [5]
    column Develop [6]
    column Deliver [4]
    
    task[Discover] Stakeholder interviews
    task[Discover] User shadowing sessions
    task[Discover] Analytics review
    task[Discover] Competitor audit
    task[Discover] Survey distribution
    task[Discover] Journey mapping workshop
    task[Discover] Persona creation
    task[Discover] Problem statement
    task[Define] HMW questions
    task[Define] Design principles
    task[Define] Success metrics
    task[Define] Scope definition
    task[Define] Prioritization matrix
    task[Develop] Concept generation
    task[Develop] Service blueprint v1
    task[Develop] Prototype touchpoints
    task[Develop] Usability testing
    task[Develop] Iterate blueprint
    task[Develop] Technical feasibility
    task[Deliver] Implementation plan
    task[Deliver] Pilot design
    task[Deliver] Launch checklist
    task[Deliver] Handoff documentation
```

## 3. Sprint Board with Swimlanes
```mermaid
kanban
    title Sprint 15 Board
    column Backlog []
    column Sprint Backlog [8]
    column In Progress [3]
    column Code Review [2]
    column Testing [2]
    column Done []
    
    task[Sprint Backlog] US-123: User login (5pts)
    task[Sprint Backlog] US-124: Password reset (3pts)
    task[Sprint Backlog] US-125: Profile page (5pts)
    task[Sprint Backlog] US-126: Email notifications (2pts)
    task[Sprint Backlog] US-127: Dark mode toggle (3pts)
    task[Sprint Backlog] US-128: Export to PDF (5pts)
    task[Sprint Backlog] US-129: Keyboard shortcuts (2pts)
    task[Sprint Backlog] US-130: Accessibility audit (5pts)
    task[In Progress] US-123: User login
    task[In Progress] US-124: Password reset
    task[In Progress] US-125: Profile page
    task[Code Review] US-123: User login
    task[Code Review] US-124: Password reset
    task[Testing] US-123: User login
    task[Testing] US-124: Password reset
```

## 4. Personal Productivity
```mermaid
kanban
    title Personal Kanban
    column Inbox []
    column Today [3]
    column This Week [5]
    column Waiting For []
    column Done []
    
    task[Inbox] Research new framework
    task[Inbox] Reply to emails
    task[Inbox] Schedule dentist
    task[Today] Finish project proposal
    task[Today] Team standup 9am
    task[Today] Code review PR #45
    task[This Week] Write blog post
    task[This Week] Update documentation
    task[This Week] Learn Rust basics
    task[This Week] Plan vacation
    task[This Week] Refactor auth module
    task[Waiting For] Client feedback on design
    task[Waiting For] API credentials from vendor
    task[Done] Weekly report submitted
    task[Done] Sprint planning completed
```

## 5. Portfolio Kanban
```mermaid
kanban
    title Portfolio Kanban
    column Ideas [10]
    column Discovery [5]
    column Delivery [3]
    column Live [5]
    column Done [8]
    
    task[Ideas] AI-powered search
    task[Ideas] Mobile app v2
    task[Ideas] Partner marketplace
    task[Ideas] White-label solution
    task[Discovery] Voice interface
    task[Discovery] Advanced analytics
    task[Discovery] Real-time collab
    task[Discovery] Offline mode
    task[Discovery] Plugin system
    task[Delivery] Redesign checkout
    task[Delivery] New onboarding
    task[Delivery] Performance optimization
    task[Live] Core platform
    task[Live] Billing system
    task[Live] User management
    task[Live] Reporting dashboard
    task[Live] API platform
    task[Done] Legacy migration
    task[Done] GDPR compliance
    task[Done] SSO integration
    task[Done] Dark mode
    task[Done] Multi-language
    task[Done] Webhook system
    task[Done] Audit logs
    task[Done] Backup automation
```