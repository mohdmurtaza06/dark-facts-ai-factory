# Cinematic rebuild: visual benchmark

## Why this branch exists
The Remotion/Three.js pilot exported successfully, but the geometric detective did not meet the agreed visual benchmark. This branch is a deliberate visual reset. It does not replace the working cloud-render branch or merge into main.

## Target look
Use the user's supplied reference as the quality target: expressive stylized 3D human character, sculpted hair and face, believable clothing, cinematic alley, warm practical lamp, cool atmospheric fill, depth of field and polished film lighting. Create original characters and environments. Do not copy the reference image's exact character or composition.

## First benchmark
renderer/blender/pilot_scene.py creates an original 3D character and a cinematic alley in Blender. It is a still-frame benchmark only, not yet an animation or production pipeline. The manual workflow cinematic-style-frame.yml renders one 540x960 PNG on a GitHub-hosted CPU runner and stores it as an artifact.

## Acceptance gates
1. Inspect the still at full size for face, silhouette, hands, clothing, lighting and environment.
2. Iterate character proportions and materials until the still is accepted.
3. Add a rig with facial controls and body motion.
4. Build a multi-shot scene plan and render short motion tests.
5. Add narration, sound design, captions only if editorially appropriate, and final 1080x1920 export.
6. Benchmark actual cloud time and storage before promising five videos/day.

## Cost and quality honesty
This workflow uses free GitHub Actions capacity when available and Blender CPU rendering. Free runner availability and quotas are not guaranteed. A successful still render is not proof of an affordable 55-70 second animation. No paid provider, publishing, or live YouTube upload is enabled.
