# Interactive Text Adventure Game

A small, self-contained CLI text adventure. Follow the design document in `Interactive Text Adventure Game – Design Document` for full behavior details.

## Requirements

- Python 3.10+

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (Not yet needed; placeholder if dependencies are added later)
```

## Running the Game

```bash
python app/game.py
```

You can also use the demo script (will be implemented later) to capture a guided playthrough:

```bash
bash scripts/demo.sh | tee -a traces/run-log.txt
```

## Saving Traces

Copy agent conversation logs or run outputs into files under the `traces/` directory. The demo script above illustrates appending to `traces/run-log.txt`.
