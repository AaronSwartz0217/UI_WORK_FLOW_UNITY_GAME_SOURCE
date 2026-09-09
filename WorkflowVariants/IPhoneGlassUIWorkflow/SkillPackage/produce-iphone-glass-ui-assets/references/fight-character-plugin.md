# UNITY Fight Character Flow Plugin integration

This rule applies only when a UI project controls, documents, or ships with the external Unity character plugin repository.

## 1. Source ownership

The only plugin source of truth is:

```text
https://github.com/AaronSwartz0217/UNITY_FIGHTCHRACTER_FLOW_PLUGIN
```

The workflow repository stores only compatibility metadata, invocation rules, and QA evidence. Never copy the plugin `Packages/` tree, package inventory, DLLs, models, or generated character assets into this workflow repository.

The verified compatibility lock is:

```text
../../../external-plugins/fight-character-plugin.lock.json
```

Current verified source:

- branch: `main`
- commit: `095dc3c9a0920c221b681f9ecf10508873451a97`
- `com.codex.split-rig-retargeter`: `1.4.0`
- `com.codex.mixamo-attachment-toolkit`: `0.3.0`

If the external repository commit or either package version changes, stop and re-run compatibility review. Do not silently accept the new inventory.

## 2. Mode contract

| Requested mode | Plugin package | What counts as completed | What does not count as completed |
|---|---|---|---|
| Animation retargeting | `com.codex.split-rig-retargeter` | A new clip is baked, assigned to a compatible Animator state, played on the target character, and passes motion QA | A `.anim`/FBX file merely exists |
| Animation repair | `com.codex.split-rig-retargeter` | The repaired clip plays on the original rig and passes first-frame, direction, continuity, root-motion, and loop checks | Using repair to convert between different skeleton structures |
| Rigid equipment / attachment | `com.codex.mixamo-attachment-toolkit` | Socket is created on the resolved bone; the equipment has `AttachmentItem`; runtime `Equip`/`Attach` visibly reparents it; `Unequip` and state offsets are tested | A character or equipment Prefab merely exists |
| Skinned clothing swap | Not provided | Route to a separate wardrobe/skinned-mesh system and record `Pending` until that system is present | Treating a rigid Socket attachment as skinned clothing replacement |
| Automatic skinned-mesh bone binding | Not provided | Route to a separate bone-remap/bind stage and verify every `SkinnedMeshRenderer.bones` entry | Saving a Prefab and assuming bones were bound |
| Apply action/animation | Partial: retarget output only | Wire the verified output clip into the intended Animator Controller/state, enter the state at runtime, and observe motion | Assuming the retargeter automatically edits Animator Controllers |

## 3. Required execution gates

### 3.1 Before Unity work

1. Obtain the plugin from its original repository.
2. Check out the commit recorded by the compatibility lock.
3. Run `scripts/check_fight_character_plugin.py --plugin-repo <LocalPluginRepository>`.
4. Stop if the repository is dirty, the origin is different, the commit differs, a package version differs, or a required API/file is missing.

### 3.2 Animation retargeting

1. Import source and target separately; do not merge their hierarchies.
2. Verify the target Avatar/rig configuration before baking.
3. Run the package mapping check and stop when a required body bone is missing.
4. Bake to a new output; do not overwrite the last accepted clip.
5. Add the output to the actual Animator Controller or test controller.
6. Enter and exit the state in Play Mode and check start pose, direction, limbs, root motion, loop, and end-frame rebound.

The package produces animation output. Animator state wiring remains an integration responsibility.

### 3.3 Rigid equipment attachment

1. Create a scene working copy of the character.
2. Resolve Humanoid bones first, then use the Mixamo-name fallback when needed.
3. Create or repair the required Socket.
4. Add or verify `AttachmentItem` on the equipment Prefab.
5. Preview the attachment and save its base/state offset Profile when required.
6. Save a new attachment-ready character Prefab; never overwrite the source FBX.
7. In Play Mode call `AttachmentController.Equip` or `Attach`, verify the hierarchy and pose change, then test `Unequip` and at least one relevant `SetState` transition.

### 3.4 Prefab and bone-binding gate

Saving a Prefab is not evidence of successful binding. Record separately:

- resolved character bone or Socket;
- equipment parent after runtime attach;
- presence of `AttachmentController`, `AttachmentSocket`, and `AttachmentItem` where applicable;
- whether the asset is rigid or skinned;
- for skinned assets, the separate binder used and the missing-bone count.

The current external plugin creates attachment Sockets. It does not rewrite `SkinnedMeshRenderer.bones` for clothing.

## 4. QA record

When the plugin is used, store a report outside formal PNG output, for example:

```text
<ProjectId>/QA/FIGHT_CHARACTER_PLUGIN_COMPATIBILITY.json
```

The report must include repository URL, actual commit, package IDs and versions, dirty-state result, selected mode, runtime verification result, and unresolved limitations. `Components/out/<ProjectId>/` remains PNG-only.

## 5. Update procedure

When the original plugin repository changes:

1. inspect the new external commit and package changelogs;
2. compare package IDs, versions, required files, public runtime calls, menus, and limitations;
3. update the lock only after the compatibility checker and relevant Unity tests pass;
4. update this mode table if capabilities changed;
5. never copy the external plugin inventory into this repository.
