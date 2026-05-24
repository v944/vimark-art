# Work Log

## Website Changes

### Pricing Update (index.html, ru/index.html)
Updated the Pricing block in the About section:

| Service | Price |
|---------|-------|
| Illustration | from $500 |
| Book cover | from $700 |
| Character design | from $700 |
| Environment concept | from $800 |

Files modified:
- `index.html`
- `ru/index.html`

---

## Desert Giants WebGL Scene (WIP)

**Status:** Work in progress. Not yet linked from the main portfolio.
**Location:** `scenes/desert-giants/`

### Assets
- **Replaced GLB:** `assets/desert_scene.glb` — user-edited version with original desert mesh removed
- **Added normal map:** `assets/Normal_4K_Rippled_Sand.PNG` — 4K rippled sand normal map
- **Removed billboards:** `assets/giant_billboard_01.png`, `assets/giant_billboard_02.png`
- **HDR environment:** `assets/desert_sunset_2k.hdr` (unchanged)

### Scene Implementation
- **Infinite desert plane:** `PlaneGeometry(1000, 1000)` with `MeshStandardMaterial`
  - Color: dark brown `0x5a3d20`
  - Roughness: 0.9
  - Normal map tiling: 120
  - Normal scale: 1.0
  - Shadows enabled
- **Ground fog:** 5 shader-based `PlaneGeometry(120, 120)` layers
  - Opacity: 0.15
  - Spread along Z: -45 to +40
  - Drift speed: 0.05
  - Color: warm brown `vec3(0.55, 0.45, 0.30)`
- **Sand particles:** 1200 `Points` drifting along +X with reset loop
- **Camera:**
  - FOV: 75°
  - Position: `(-55, 1.2, 12)`
  - Target: `(-32, 3, 0)`
  - Low angle, behind the shepherds, framing all giants
- **Lighting:**
  - Sun: `DirectionalLight(0xffaa66, 1.5)` at `(50, 80, 30)`
  - Fill: `DirectionalLight(0x6688ff, 0.3)` at `(-30, 40, -20)`
  - Ambient: `AmbientLight(0x404040, 0.4)`
- **Controls:** OrbitControls with damping, min/max distance, max polar angle

### Dev Tools
- **test.js** — Playwright script for automated screenshot capture
  - Serves local server on `127.0.0.1:9090`
  - Waits 10 seconds for scene load
  - Saves `test-result.png` and `test-logs.json`
- **open-browser.js** — Helper to open browser for local testing

### Documentation
- `__UE_web/desert_giants_webgl_brief.md` — Updated to reflect current asset list (no billboards)

---

*Last updated: 2026-05-24*
