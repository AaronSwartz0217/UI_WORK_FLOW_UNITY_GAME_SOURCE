# Project Contract

## Portable paths

Use relative paths in all stored Markdown and JSON. Import external wireframes and references into the workflow before production.

## Required project tree

```text
ProjectId/
├─ in/
├─ into/
│  ├─ Candidates/
│  ├─ Rejected/
│  └─ ReassemblyPreview/
├─ Components/out/ProjectId/
├─ Templates/
├─ FullUI/
├─ QA/
├─ project.json
└─ README.md
```

## Identity

```text
ProjectDisplayName: user-facing name
ProjectId: stable ASCII PascalCase identifier ending in UI
ComponentPrefix: stable ASCII PascalCase filename prefix
```

## Formal filename

```text
ComponentPrefix_ComponentName_State_WidthxHeight.png
```

Allowed common states: `Normal`, `Hover`, `Pressed`, `Disabled`, `Default`, `Empty`, `Selected`.

## Formal output

`Components/out/ProjectId/` contains only current, validated, directly importable PNG files. Keep every component from the project in this one directory.

## Hierarchy

```text
MainPanelBase
└─ LargeChildPanel
   └─ SmallPanel / Slot / Button / Icon / Track / Thumb
```

Parent layers must not bake in children. Reassembly previews are QA artifacts, not formal assets.

## User gates

- Generate one full UI at a time.
- Obtain full-UI approval before splitting.
- Obtain final-component approval before moving to the next UI.
