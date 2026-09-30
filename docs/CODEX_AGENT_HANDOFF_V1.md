> **2026-09-30 repository update:** This is a dated technical/history document. Old MP3 masters were removed at Hon's request; old timings and machine paths below are historical. For current inputs/setup/paths read [AUDIO_STATUS.md](AUDIO_STATUS.md), [REPOSITORY_GUIDE.md](REPOSITORY_GUIDE.md) and the root README.

# Codex 音乐视频协作交接

作者：Codex。更新：2026 年 9 月 30 日。读者：Hon 和同时制作这支音乐视频的其他 agent。

本文汇总 Codex 已交付的画面与运动原型，说明文件位置、运行方式、可复用接口和待做内容。共享项目位于 `D:\Videos\Help! I'm stuck in a LIE\`。下表中的相对路径均以此目录为起点。

当前已有一支可查看的 20 秒六场景运动样片和可玩的原创 Canvas 引擎。它们可供选镜头和继续开发，最终视觉、全曲剪辑和歌词节拍仍待确定。先读项目 `AGENTS.md`、`coordination/STATUS.md` 和 `docs/DECISIONS.md`，再开始改动。

## 用户要求与故事方向

这些要求来自 Hon，原话保存在 `docs/PROMPTS.md`。

- 世界由字符和代码构成。黑、白、灰为主，橙色用于女孩的符号心脏；屏幕文字用英文。
- 女孩是在音乐工厂觉醒的 AI，与同一流水线上其他 AI 外形一致，只有她有心。她尝试逃离，死亡后回到起点，最终出去。
- 音乐视频以平台跳跃为主要运动形式，同时需要不同视角、不同场景、特写和其他视觉变化。镜头可以直接切换。
- 运动要快，左右启动、反向和停止要立即响应；跳跃要有力度，支持二段跳和冲刺。头发保留惯性与跟随动作。
- 背景至少有两到三层动态内容，加上角色与平台，以及偶尔快速掠过的前景。代码生成、工作中的 AI、音符和环境都应活动。
- 弹幕约每秒 10 发，形成疯狂躲闪的压力。手动游戏可以极难；音乐视频的观感优先。
- 敌人与攻击可使用乐器、音乐音符及仍能读清的歌词。此轮运动测试允许稍后再精调音乐节拍。
- 旧图片和旧视频保留，新作品分别存放。作品是否成为最终镜头，仍由 Hon 决定。

## 已完成文件

| 内容 | 项目路径 | 当前用途 |
|---|---|---|
| 最新六场景视频 | `renders/2026-09-30_codex_six_worlds_motion_v1.mp4` | 本轮运动与密度预览，20 秒，1080p60 |
| 六张实际模拟截图及总览 | `design/keyframes/codex_six_worlds_motion_v1/` | 供选镜头；包含 README、manifest 和哈希 |
| 最新可玩源码 | `wip/codex/platformer_motion_v2/` | 后续运动实现从这里派生新版本 |
| 当前技术说明 | `docs/CODEX_SIX_WORLDS_MOTION_V1.md` | 参数、事件统计、检查结果和范围说明 |
| 上一版单工厂运动视频 | `renders/2026-09-30_codex_platformer_motion_v2.mp4` | 保留作对照；属于旧原型 |
| 上一版头发慢放 | `renders/2026-09-30_codex_platformer_hair_slow_v1.mp4` | 下坠、头发惯性与落地动作参考 |
| 上一版可玩源码 | `wip/codex/platformer_motion_v1/` | 历史运动原型 |
| Hon 选出的七张 Codex 静帧参考 | `design/keyframes/codex_selected_references_v1/` | 02–06、07B、08；已接受为参考 |
| 音乐工厂故事静帧 | `design/keyframes/codex_music_factory_lab_v2/` | 四张提案：流水线、重生、乐器攻击、透视出口 |
| 其他 Codex 画面方案 | `design/keyframes/codex_candidates_v1/` | 早期候选，保留供审阅 |

注意名称：旧电影虽然叫 `codex_platformer_motion_v2.mp4`，仍属于源码 `platformer_motion_v1`。本轮应找包含 `six_worlds` 的电影，以及源码 `platformer_motion_v2`。

聊天交付副本在 `C:\Users\honkw\Documents\Codex\2026-09-28\https-github-com-mexicat-pdoom-video\outputs\codex_six_worlds_motion_v1\`，包含电影、总览、`playable_engine.zip` 和 `playable/`。这不是 D 盘项目下的 `outputs/`。其他 agent 可直接使用 D 盘的源码和成片，不依赖聊天副本。

## 六场景与音频时间

以下时间为样片自身的 0–20 秒。音频使用 `audio/final/song.mp3` 的 **42.012–62.012 秒**，换算为：歌曲时间 = 样片时间 + 42.012 秒。

| 样片时间 | 场景 | 画面与运动 |
|---|---|---|
| 0–3.2 秒 | 音乐工厂 | 同款 AI 工人、输送带、齿轮、生成中的代码；高速跑、反向、跳跃 |
| 3.2–6.4 秒 | 垂直记忆竖井 | 括号塔与错位平台；交替方向向上跳 |
| 6.4–9.6 秒 | 水下缓冲海 | 字符遗迹、珊瑚、水流、气泡、音符鱼；上下和回转游动 |
| 9.6–13.6 秒 | 俯视路线迷宫 | 真正的右、上、左、上、右、下、右路线；立起的字符墙与掠过的管线 |
| 13.6–16.8 秒 | 天空乐谱 | 悬挂琴键、风琴浮岛、字符云；二段跳和空中冲刺 |
| 16.8–20 秒 | 歌词大教堂 | 乐器形状、音符轮、歌词交叉攻击；相机推进并到达 REAL 门 |

切点目前按场景时长安排，**尚未逐拍匹配音乐**。飞来的歌词也是攻击素材，还没有逐字与演唱对齐。最终剪辑应结合项目歌词时间数据重新安排。

## 自动样片和手动游戏

自动模式先排练原始物理路线，再计算贴近未来路线的攻击交叉位置，使女孩完成连续动作。碰撞仍然启用，没有自动模式通用无敌。手动模式的攻击瞄准当前女孩，具有真实碰撞、死亡和当前房间重置；冲刺有 115 毫秒短暂碰撞保护。

当前只有最后一个房间实现出口条件。其他房间供运动和场景审阅，可用 N 键或选择器切换。自动样片没有展示整段反复死亡的剧情；此前的单工厂版本有一次死亡与重来。完整死亡蒙太奇仍待制作。

已完成的核验保存在源码目录：

- `motion_audit.json`：20 秒共发射 200 次攻击，初跳 13 次、空中二跳 12 次、冲刺 5 次、记录 112 次攻击通过，19.87 秒到达出口；编排路线死亡 0 次。活跃弹体峰值 29，包含画面外弹体。
- `control-qa-v2.json`：32 项控制、数值和人物留在画面内的检查通过，无 JavaScript 错误。
- `media_validation.json`：1920×1080、60fps、1200 帧、20 秒 H.264 视频和 20 秒 AAC 音频；全片解码通过，已检查编码后的出口画面。
- `delivery_smoke.json`：交付网页和音频可加载；静止不操作的手动女孩在 1.6 秒内确实死亡并重生两次。

这些记录验证实现与交付状态。自然感、画面美感和弹幕压力需要 Hon 在播放中判断。

## 打开试玩和导出

当前新版本地址是 `http://127.0.0.1:5189/playable/`。**5188 是旧版单场景**，浏览器留在该地址时看不到本轮变化。服务可能随机器或终端重启退出。

最简单的打开方式是用 Chrome 或 Edge 打开 D 盘源码中的 `index.html`。网页本身不需要安装依赖。点击 Replay film + music 播放带音乐的自动预览，点击 Play this world 手动控制。

需要重新启动服务时，在 PowerShell 中运行以下命令。5190 是示例端口，避免与当前两个预览服务冲突。

```powershell
Set-Location -LiteralPath "D:\Videos\Help! I'm stuck in a LIE\wip\codex\platformer_motion_v2"
python -m http.server 5190 --bind 127.0.0.1
```

随后打开 `http://127.0.0.1:5190/`。

操作：A/D 或左右箭头移动；Space 二段跳；X 或 Shift 冲刺；S 或下箭头在侧视中蹲下、在自由移动场景中向下；W 或上箭头在水下和俯视中向上；R 重置；N 下一场景。

离线导出在源码目录运行 `node capture.mjs render NEW_NAME.mp4`，新电影必须使用新文件名。导出器依赖本机 Node、Chrome、捆绑 Playwright 和 PATH 中的 FFmpeg，具体路径在 `capture.mjs`；跨机器需要检查路径与字体。`node capture.mjs audit` 会更新该目录的审计 JSON 和 QA 截图，继续开发时先复制到自己的新版本目录。

## 源码职责与复用接口

| 文件 | 职责 |
|---|---|
| `game.js` | 120Hz 物理、输入、自动路线、时间、相机、真实攻击、碰撞、死亡重置与出口 |
| `character.js` | 字符角色、关节动作、侧视和俯视姿势、游泳和冲刺、弹簧头发 |
| `worlds.js` | 五个侧视和水下世界的动态背景、平台画面与短暂前景 |
| `topdown.js` | 俯视场景建筑、碰撞墙、路线、背景和前景 |
| `capture.mjs` | 确定性逐帧输出，送入 FFmpeg 并混入音频 |

背景中的乐器嘴和装饰音符属于画面。真实攻击的生成、运动与碰撞在 `game.js` 中维护。

浏览器里的 `window.demo` 提供 `reset(mode, sceneIndex)`、`renderAt(t)`、`state()`、`events()` 和 `scenes`；`duration=20`、`fps=60`、`physicsHz=120`。`renderAt(t)` 推进并绘制模拟，按递增时间调用；需要重新取之前的帧时会重置重算。

角色接口是 `PlatformerCharacter.draw(ctx, state, time)` 和 `drawTop(ctx, state, time)`。侧视的位置是脚底锚点，俯视位置是身体中心；`createHair()` 创建头发状态，`updateHair(hair, state, dt)` 每个模拟步调用一次。

环境接口是 `MusicWorlds.draw(ctx, sceneId, state)`、`drawForeground(ctx, sceneId, state)`，以及俯视的 `TopdownScene.draw(ctx, state)`、`drawForeground(ctx, state)`。环境 state 使用 `{time, localTime, p, cam, platforms, width, height}`；绘制先背景，再角色与真实攻击，再前景。环境函数自行处理相机变换，避免重复平移。细节见各模块 notes 文件。

侧视背景视差为 0.12、0.35、0.65，角色与平台为 1.0，前景为 1.4；前景掠过约 0.34 秒。俯视使用远处图谱、活动乐谱地面、立体字符墙、女孩和上方管线。侧视速度为 1150–1440 px/s，水下为 1120 px/s，俯视为 1220 px/s；冲刺 2850 px/s，左右输入在下一物理步立即响应。

## 与另一个 agent 的工作衔接

Claude 的十帧故事方案在 `design/keyframes/story_v1/`，说明是 `STORY.md`，总览是 `story_sheet.jpg`。其提案将特写、游戏和计算图三种尺度，通过女孩的心连接；死亡轨迹累积成计算图，图中的线再变成平台。这套图仍在审阅中。

当前六场景引擎可提供运动、碰撞、头发、攻击和确定性导出。把心缩成绘图点、累积多次死亡轨迹、保持心在切镜前后的屏幕位置，以及特写和计算图切换，**尚未在当前引擎实现**。Claude 图片中的死亡数字也不能当作本轮实际审计结果。

建议后续先对照 Claude 的十帧方案与本轮电影，确定使用的镜头，再在自己的 `wip/<agent>/` 新版本里衔接这些变化，最后对齐歌曲节拍与歌词。此顺序是 Codex 的工作建议，具体镜头选择仍由 Hon 决定。

## 并行协作与后续事项

- 在 `coordination/TASKS.md` 认领具体工作范围，记录新指令与工作结果。其他 agent 正在做的文件先保持原状。
- 保留所有旧素材和交付版本，给新的源目录、关键帧和电影编号。当前六场景截图是提案，不是已选定的最终美术。
- 这次只扩展了本地运动角色模块；锁定的共享 `design/character/src/vgirl.py`、`app/src/game/girl.ts` 和主 TypeScript app 未被改动。若正式修改共享角色，按项目协议同步两套角色实现。
- 后续重点包括：选定视觉、逐拍剪辑与歌词攻击时序、短时间连续死亡蒙太奇、特写和计算图衔接，以及逃出后的外部世界。
- 已知修正包括：重生时不再补发全部旧弹幕、天空平台落点与人物出画问题、跨大间隙的二跳记忆，以及局部坐标裁剪导致珊瑚和装饰音符消失的问题。继续移植时保留这些行为。

详细技术记录见 `docs/CODEX_SIX_WORLDS_MOTION_V1.md`；用户最新指令以 `docs/PROMPTS.md` 和当前对话为准，其他 agent 的提案不能自动视为新的用户授权。
