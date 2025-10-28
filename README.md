# Trivox Conductor

Record --> Render --> Ready.
A PySide6 desktop app that orchestrates **OBS capture**, **ReplayMod exports**, **audio sync + mux**, **Resolve color**, **Drive handoff**, and **notifier hooks**; with a **plugin-first** architecture so you can swap adapters without touching core UI.

>Focus: Minecraft technical reels today. Built to scale for VFX/game pipelines tomorrow.

---

## Key features (current & planned)

- **PySide6 shell**: Dashboard · Logs · Settings (dark, creator-friendly).
- **OBS control (obs-websocket)**: connect/auth, Start/Stop, scene/profile picker.
- **Replay export watch**: folder watcher, stable-file detection, session correlation.
- **Session IDs & filename**s: ``YYYYMMDD_HHMM_s{start}_e{end}_{slug}.mp4``.
- **Event bus**: ``CAPTURE_STARTED/STOPPED``, ``REPLAY_RENDER_DETECTED``, … (extensible).
- **Audio sync & mux (FFmpeg)**: offset math, desktop+mic mix, copy-mux to video.
- **Color pass (DaVinci Resolve – Free)**: import IGReady, apply LUT, render IGColor.
- **Uploader (rclone)**: Drive remote, retries, progress.
- **Notifier (Trivox-Notify)**: Slack/Discord pings with deep links.
- **AI Creative Brain (planned)**: hook/caption/hashtags + song candidates & beat markers.
- **Traveling manifest**: JSON sidecar that carries meta/story/publish intent across stages.

## Requirements

- **Windows 10/11** (primary dev target).
- **Python 3.9+**.
- **Poetry 2.0+**
- **OBS Studio + obs-websocket** plugin enabled.
- **FFmpeg available** in PATH.
- (Later) **DaVinci Resolve (Free)**, **rclone**, **Trivox-Notify** endpoint.

## Quick start (developer)

```python
# Install dependencies
poetry install
.venv/Scripts/activate # (Windows)

# run
python manage.py run
```

## Contributing

PRs welcome. Please:

1. Open an issue describing the change.
2. Follow the plugin contract and add unit tests for adapters.
3. Include before/after screenshots or short clips when UI changes.

## License

MIT (see [LICENSE](LICENSE)).

## FAQ

**Why a desktop app, not web?**
Low-latency device control (OBS/Resolve/FFmpeg), local file watching, and creators’ existing desktop pipelines make desktop the right first step.

**Why Resolve Free?**
You can import, apply a LUT, and render with audio OFF—exactly what we need. Studio is nice, not required.

**Why not render music in Resolve?**
IG Edits/CapCut manage trending audio & rights. We place a reference track and markers only; final audio is added on IG.
