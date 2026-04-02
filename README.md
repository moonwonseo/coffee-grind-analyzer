# TrueGrind — Coffee Grind Size Analysis

Measures coffee particle size distribution from a photo using a US quarter as a calibration scale. Detects the quarter → computes px/mm scale → segments particles with YOLOv8-Seg → outputs D10/D50/D90 and grind classification (espresso → coarse).

---

## Quickstart (any machine)

```bash
git clone <repo-url> && cd truegrindapp
python setup.py
# Fill in ROBOFLOW_API_KEY in .env
uv run grind train
```

`uv run grind train` downloads the dataset automatically if it's not present, then trains. That's the whole flow.

For NVIDIA GPU machines:
```bash
python setup.py --cuda
```

---

## How it works

1. **Quarter detection** — Hough Circle Transform finds the quarter, computes `px/mm`
2. **Particle segmentation** — YOLOv8-Seg segments each particle with polygon masks
3. **Micron conversion** — `diameter_µm = (diameter_px / px_per_mm) × 1000`
4. **PSD stats** — D10, D50, D90, span `(D90−D10)/D50`, mean, std
5. **Grind classification** — rule-based from D50 thresholds

---

## Commands

```bash
# Train — downloads data automatically if data/ is missing
uv run grind train
uv run grind train --epochs 100 --weights yolov8s-seg.pt

# Inference
uv run grind infer photo.jpg --model runs/segment/.../best.pt
uv run grind infer photo.jpg --model best.pt --save-plot psd.png   # headless

# R2 dataset sync (requires credentials)
uv run r2-sync upload                        # upload ds/ → R2
uv run r2-sync --prefix data upload --src data  # upload prepared data/ → R2
uv run r2-sync download --dest ds            # download ds/ from R2
uv run r2-sync list
uv run r2-sync --prefix data manifest        # write manifest for public downloads
```

---

## Setup details

### Requirements
- Python 3.13+
- [uv](https://docs.astral.sh/uv/) — installed automatically by `setup.py`

### `.env` credentials

| Variable | Where to find it | Required for |
|---|---|---|
| `ROBOFLOW_API_KEY` | [app.roboflow.com](https://app.roboflow.com) → Settings → Roboflow API | Training (data download) |
| `R2_ACCESS_KEY_ID` | Cloudflare → R2 → Manage R2 API Tokens | R2 upload/download |
| `R2_SECRET_ACCESS_KEY` | Same token screen (shown once) | R2 upload/download |
| `R2_ACCOUNT_ID` | Cloudflare dashboard → Account ID | R2 upload/download |
| `R2_BUCKET_NAME` | Your R2 bucket name | R2 upload/download |
| `R2_PUBLIC_URL` | Cloudflare → R2 → bucket → Settings → Public Access | Credential-free downloads |

Copy `.env.example` → `.env` and fill in values.

---

## Device support

Auto-detected in order: **CUDA → MPS → CPU**

| Machine | Device |
|---|---|
| Mac (Apple Silicon) | MPS |
| Linux/Windows + NVIDIA | CUDA |
| Anything else | CPU |

CUDA wheels (cu130):
```bash
python setup.py --cuda
# or manually:
uv sync --extra cuda
```

---

## Project structure

```
truegrindapp/
├── grind_pipeline.py   # Core pipeline + CLI entrypoint
├── roboflow_prep.py    # Dataset download + merge (called automatically by train)
├── r2_sync.py          # Upload/download ↔ Cloudflare R2
├── setup.py            # One-command bootstrap
├── pyproject.toml      # uv project + script entrypoints
├── uv.lock             # Locked dependency versions
├── .env.example        # Credential template
├── ds/                 # Raw annotated images (gitignored, stored in R2)
├── data/               # Merged training dataset (gitignored, auto-built)
└── frontend/           # SvelteKit app
```

---

## Grind classification (D50 thresholds)

| Category | D50 |
|---|---|
| Espresso | < 400 µm |
| Moka pot | 400–500 µm |
| Filter | 500–700 µm |
| French press | 700–900 µm |
| Coarse | > 900 µm |
