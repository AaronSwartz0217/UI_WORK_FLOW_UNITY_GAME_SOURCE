# Style Reference Index

## Required priority

| Priority | Reference set | Location | Files | Role |
|---:|---|---|---:|---|
| 1 | Cook — primary standard | `Standards/Primary_Cook/` | 25 PNG | Governs the overall UI identity: black-steel material, silver edge hierarchy, restrained amber highlights, red danger state, surface wear, cards, buttons, quantity controls, slider and state transitions. |
| 2 | Equipment Identification — secondary standard | `Standards/Secondary_EquipmentIdentification/` | 15 PNG | Supplements component classes not fully covered by Cook: help button, equipment/material slots, portrait clean-template treatment and compact identification-button structure. |
| 3 | Legacy full-screen style reference | `StyleReference_01.jpg` | 1 JPG | Context-only fallback for atmosphere and broad material language. It must not override the two standards above. |

Component-level legacy references remain indexed at `../SharedComponents/SHARED_COMPONENT_INDEX.md`.

## Conflict resolution

1. The current wireframe always controls layout, ratio, panel count, position and hierarchy.
2. Cook controls the default visual language for every future UI.
3. Equipment Identification may fill a missing component class only when Cook does not define it.
4. If the two sets disagree, Cook wins.
5. Never copy business layout, localized text, dynamic numbers or project-specific content from either reference set.
6. The baked `鉴定` label in the secondary IdentifyButton is reference content only. New localizable action buttons must use a clean solid plate plus engine text unless the user explicitly requires baked text.
7. Reference PNGs are immutable inputs: do not erase or repaint text inside the standard-reference folders. Text removal applies only to newly generated project UI and exported project assets.

## Required use in future projects

- Before generating a new UI, inspect every file in both standard folders.
- Copy the actually used primary and secondary reference files into the new project's `in/` folder.
- In generation prompts, label the new wireframe as layout-only, Cook as primary style, and Equipment Identification as secondary style.
- Project README and QA must record which files were used and confirm that Cook remained primary.
- New full-UI review drafts should already omit ordinary/localized text and dynamic numbers. Preserve only functional symbols such as `X`, `?`, `+`, `-`, and arrows, and reconstruct complete solid surfaces beneath removed text.

Review contact sheets:

- `../ReferenceNotes/ContactSheets/Cook_Primary_ContactSheet.jpg`
- `../ReferenceNotes/ContactSheets/EquipmentIdentification_Secondary_ContactSheet.jpg`
## Canonical reusable controls

Validated functional-button families may be copied verbatim into new projects to keep critical controls stable. Cook remains the primary source. For example, Cook_CloseButton_{State}_52x50.png is the canonical Close/X family. All four states must travel together, with only the project prefix renamed.
