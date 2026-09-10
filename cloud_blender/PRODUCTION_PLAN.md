# Shirase Koharu — Automated 3D Production Plan

## Non-negotiables
- No paid GPU/API without explicit approval.
- No claim of completion based on concept art or an unvalidated mesh.
- Each gate blocks the next phase when it fails.
- Preserve source character identity: silver short bob, cyan eyes, star pin, white/teal/black/gold outfit, translucent star cape, companion drone.

## Gates
### G0 Reference/spec lock
PASS: koharu_spec.json exists and is versioned.

### G1 Turnaround consistency
PASS only after front/side/back share the same proportions, hair silhouette, cape attachment, boots, utility pouch, and color placement. A generated board is reference, not geometry proof.

### G2 Static 3D silhouette
PASS only after actual Blender renders from front/side/back are recognizable as Koharu. Reject mannequin-like or generic results.

### G3 Face identity
PASS only after actual 3D front and 45-degree face renders retain cyan eyes, soft anime facial proportions, bob silhouette and star pin. Face mismatch blocks rigging.

### G4 Rig/deformation
PASS only after arm raise, elbow 90, hip flexion, knee 90, crouch and torso twist renders show no catastrophic deformation. Automatic weights may be used but are not accepted without these tests.

### G5 Export/reopen
PASS only when .blend and .glb exist, GLB can be reimported into a fresh Blender scene, materials/armature remain present, and scale is near 1.67 m.

### G6 Final QA
PASS only after turntable, validation JSON, final renders, triangle/material budgets, rig tests and deliverable package all pass.

## Failure controls
1. Never infer completion from AI concept images.
2. Keep cape and drone separable from body.
3. Prefer simple stable geometry before details.
4. Do not add physics until static + rigged model passes.
5. Do not add facial expressions until topology/face shape is accepted.
6. Use versioned outputs; never overwrite last known-good deliverable.
7. Automatic generation candidates must be rendered from multiple angles before acceptance.
8. Any automated 2D-to-3D candidate with fused limbs/cape/hair is rejected, not repaired by hiding the defect.
9. Validate normals, scale, missing materials, object count, armature presence, and export success automatically.
10. Treat free-cloud limitations as production constraints: CPU Blender for deterministic build/QA; free 2D-to-3D only when a callable non-paid service is available.

## Current status
- G0 PASS.
- Cloud Blender 5.2.1 LTS PASS.
- Automated blockout generated/exported/rendered.
- G1/G2/G3/G4/G6 NOT PASS yet; blockout is deliberately not accepted as final.
- G5 prototype export exists; final-model G5 remains pending.
