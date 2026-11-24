# 九天天门 · 图生视频提示词（I2V Prompt）

> 按 `yufei-tiangong-skill/references/video-motion.md` 编译。
> 源图作为固定首帧与构图合同，不重新设计画面。

## 静态视角

**阙下侧望·门中重门**（超广角低机位仰视变体）

## 唯一运镜（单选）

**完全锁镜（Locked-off）**。总运镜幅度 **0%**。

选择理由：本机位前景为约 10% 高的石板台，任何前推或仰摇都会把台基放大成广场并引起巨门尺度漂移，属于 `video-motion.md` 明列的视频硬失败项。因此唯一运动全部交给云海与光。

禁止：前推、仰摇、环绕、侧移、变焦、切镜、手持晃动、自动运镜、多镜头剪辑。

---

## 主提示词（可复制）

```text
Use the source image as the fixed first-frame reference and composition contract.

Selected static viewpoint: 阙下侧望·门中重门 (low upward-looking ultra-wide variant)
Selected camera motion: fully locked-off static frame — no dolly, no pan, no tilt, no zoom, no orbit, no handheld, no reframing, 0% camera travel.

Camera: one continuous, completely stabilized, locked shot for the whole duration. Preserve the original 16:9 framing, the extreme low upward angle, the 14mm ultra-wide depth, the horizon height, the single-point vanishing point on the stairway and the four-layer spatial order exactly. No cuts, no sudden reframing, no aggressive zoom.

Megastructure lock: keep the colossal cinnabar celestial gate absolutely stable and monumental. Preserve its silhouette, double-eave rooflines, cropped top ridge, brass doors, door studs, carved columns and position to the pixel. The two cropped jade columns at the left and right frame edges stay fixed and unbroken. No morphing, bending, breathing, reconstruction, duplication or scale drift. The distant floating cliff temples and immortal peaks remain indistinct in cool haze and never approach the camera.

Human lock: exactly one traveler in white robes, unchanged number, unchanged sub-1% scale, unchanged position at the center of the stairway. Allow only the faintest robe hem and hair movement in one consistent wind direction, plus breathing. No face reveal, no walking, no portrait reframing, no enlargement, no extra figures.

Atmosphere: the cyan-grey cloud sea slowly churns in layered currents — far cloud drifts slower than near cloud, with soft rolling swell and small-scale lobe deformation rather than uniform sliding. Cloud masses near the stair foot spill continuously DOWNWARD over the stair edges with clear gravity and a rolling cloud lip. Thin mist drifts across the lowest steps and around the gate base. No boiling fog, no upward cloudfall, no lateral jet, no time-lapse speed, no explosions.

Light: preserve the single low morning sun behind cloud at the right of frame and its god rays slanting down-left. Keep restrained warm gold on the right-facing roof tiles, right column edge and right cloud crests; keep the left half, the cloud-sea floor and the far distance cool blue-grey. Gentle, slow ray breathing only, under 2.5% brightness variation. No flicker, no colour shift, no sudden exposure change, no global orange filter.

Style: photoreal cinematic Eastern mythic epic, filmic 2K, solemn, empty, awe-inspiring, monumental.

Avoid: camera shake, cuts, orbit, fast dolly, aggressive zoom, warped architecture, duplicated columns, moving walls, melting roofs, scale change, growing figures, oversized foreground, new characters, birds, particles, energy effects, text, watermark, logo, interface.
```

---

## 负面约束（独立文本）

```text
camera shake, handheld camera, cut, scene change, orbit, fast dolly, push-in, zoom, tilt, auto camera, multi-shot edit,
warped architecture, bending columns, duplicated columns, breathing building, melting roof, dissolving gate,
scale drift, gate moving closer, floating temples approaching camera, foreground platform expanding,
figure growing larger, face reveal, walking figure, duplicated traveler, crowd, new characters, birds, particles,
upward cloudfall, lateral cloud jet, boiling fog, time-lapse, uniform sliding fog, flicker, colour shift, exposure jump,
global orange filter, teal-orange grade, neon, lens flare artefacts, text, watermark, logo, UI, border
```

---

## 视频硬失败检查表（逐帧抽查）

| 检查项 | 结果 |
|---|---|
| 建筑几何漂移 | 通过 — 建筑区像素锁定（帧差 max 44/255，仅遮罩羽化区） |
| 人物变大或增殖 | 通过 — 人物位于静态保护区，恒定约 0.9% 画面高 |
| 前景被重新扩张 | 通过 — 前景石板帧差 0.01，完全静止 |
| 远宫/浮空宫殿主动靠近 | 通过 — 远景位于保护区外云雾带，无位移 |
| 云瀑向上或横向倒流 | 通过 — 云溢流项恒为正向下 |
| 主光闪烁 | 通过 — 单一正弦呼吸 ≤2.2%，首帧与源图曝光一致 |
| 出现第二种运动 / 切镜 | 通过 — 锁镜，无相机运动 |
