# 东方巨构图生视频协议

仅在用户要求图生视频、首尾帧或视频提示词时读取。静态图必须先按 `SKILL.md` 选定唯一视角并通过硬约束。

## 核心原则

- 把源图作为固定首帧与构图合同，不重新设计场景。
- 一段视频只使用一种镜头运动；总运镜幅度默认控制在画幅的3–5%。
- 锁定核心巨构的轮廓、比例、位置、透视、材质与结构，不允许呼吸、弯曲、融化、增殖或尺度漂移。
- 锁定人物数量、大小和位置；只允许衣袂、发丝、呼吸或一个极慢步伐。
- 云海缓慢分层流动；云瀑始终跨越边缘并受重力向下流淌。
- 保持同一右侧低位主光、左冷右暖和近暖远冷，不闪烁、不变色、不跳曝光。
- 配景运动从属于巨构；不要自动增加鸟群、粒子、人物或新的浮岛。

## 视角—运镜路由

| 静态视角 | 唯一推荐运镜 | 禁止 |
|---|---|---|
| 殿内望天·巨型门洞框景 | 极慢前推3–5%，朝洞外靠近 | 穿门、环绕、门框变形 |
| 云门内观·巨柱开境 | 极慢前推或完全锁镜 | 横移导致双柱比例漂移 |
| 柱林仰穹·极低机位 | 固定机位极慢向上仰摇 | 前冲、绕柱、柱体弯曲 |
| 阙下侧望·门中重门 | 轻微单向侧移，产生台基与巨门视差 | 正面冲门、门洞放大 |
| 殿沿云瀑·悬挑侧景 | 缓慢横移，云瀑持续向下 | 沿瀑布俯冲、多向运镜 |
| 弧廊巡天·单点消失 | 沿唯一弧线缓慢跟随前进 | 偏离弧线、第二消失点 |
| 云阙峡谷·上下夹景 | 近乎锁镜，轻微下沉或前推 | 大幅升降、峡谷结构开合 |
| 月洞借景·巨月山水 | 锁镜；只让薄云和松枝微动 | 月亮移动、推近月面、圆框旋转 |
| 松崖候宫·隔云对望 | 锁镜或极轻侧移 | 推近远宫、让远宫持续变大 |
| 檐下仰观·悬殿外立面 | 轻微向上仰摇 | 大幅推进、露台膨胀 |

## 通用视频提示词骨架

```text
Use the source image as the fixed first-frame reference and composition contract.

Selected static viewpoint: <静态图唯一命名视角>
Selected camera motion: <从运镜路由中选择且只写一种>

Camera: one continuous, extremely slow, stabilized movement; total movement only 3–5%. Preserve the original framing, horizon, perspective and spatial hierarchy. No cuts, sudden reframing, handheld shake or aggressive zoom.

Megastructure lock: keep the colossal architecture completely stable and monumental. Preserve its silhouette, proportions, rooflines, columns, walls and position. No morphing, bending, breathing, reconstruction, duplication or scale drift. The distant structure remains geographically remote yet visually enormous.

Human lock: preserve the original number, tiny scale and location of all figures. Allow only subtle robe, hair, breathing or one very slow step. No face reveal, portrait reframing or character enlargement.

Atmosphere: move the cloud sea slowly in layered currents. Let every cloud waterfall flow continuously downward with clear gravity. Use restrained depth parallax in thin mist; no boiling fog, explosions or time-lapse speed.

Light: preserve one coherent low sun from the right. Keep restrained golden light on right-facing architecture, cloud crests and pine branches; keep left and distant regions cool blue-gray. No flicker, color shift or sudden exposure change.

Avoid: camera shake, cuts, orbit, fast dolly, aggressive zoom, warped architecture, duplicated columns, moving walls, melting roofs, scale change, growing figures, oversized furniture, new characters, random birds, turbulent clouds, upward cloudfall, text, watermark or interface.
```

## 提供方适配

- 工具支持运动强度时选择低档或最接近3–5%的幅度。
- 工具支持镜头控制时只启用路由表指定的一项，关闭自动运镜、智能重构和多镜头剪辑。
- 工具支持首尾帧时，尾帧只改变雾、云瀑、衣袂和轻微相机位置；建筑和人物比例保持一致。
- 工具不支持负面提示时，将最重要的锁定词和禁止项写入主提示词。
- 指定视频工具不可用时输出提示词，不假装生成视频。

## 视频硬失败

出现任一情况即判失败并重试：建筑几何漂移；人物变大或增殖；前景被重新扩张；远宫主动靠近；月亮或圆框移动；云瀑向上或横向倒流；主光闪烁；镜头出现第二种运动；画面发生切镜。
