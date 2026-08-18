<!-- generated-by: gsd-doc-writer -->
> [简体中文（主文档）](README.md) | English copy

# Backlot — the living storyboard

Backlot is a read-only local board for watching an OpenMontage production unfold: pipeline stages light up, the script appears as a screenplay page, the scene filmstrip fills as assets arrive, and decisions, spend, activity, and renders stay visible. Every state is derived from files the pipeline already writes under `projects/<id>/`.

## Open the board

```bash
python -m backlot open <project-id>   # start the server if needed and open one project
python -m backlot open                # open the library view for all projects
python -m backlot serve --port 4750   # run the server in the foreground
```

`open` is idempotent and non-blocking for production: it reuses a running server, and the production should continue if the board cannot start.

## How live updates work

Backlot never writes to project directories and does not require an agent to synchronize the UI. `watchfiles` observes `projects/`; after a file changes, SSE tells the browser to refetch board state.

| Board element | Disk source |
|---|---|
| Identity and stage order | `project.json` + `pipeline_defs/<type>.yaml` |
| Stage states, gates, and versions | `checkpoint_<stage>.json` + `history/` |
| Script card and full preview | `artifacts/script.json` |
| Scene filmstrip cards | `scene_plan × script × asset_manifest` join |
| Generating shimmer and activity | `events.jsonl` (written by `BaseTool` instrumentation) |
| Cost meter | Checkpoint `cost_snapshot` |
| Renders | `renders/*.mp4`, with a compatibility heuristic for `.mp4` files at the project root |

Projects without checkpoints degrade to a disk-discovery view that can still show media, snapshots, and renders. A completed run can be replayed from checkpoint history and event timestamps.

The UI defaults to Simplified Chinese. Use the top-right control to switch to English; the choice is stored in browser local storage.

## Artifact and error presentation contract

Backlot provides Chinese presentation labels for canonical artifact types and top-level fields in `schemas/artifacts/`, while leaving JSON keys, enum values, and source content unchanged. The stage drawer still shows byte-faithful source data for diagnosis and cross-tool compatibility.

New failed checkpoints may provide `error_message` (localized user summary), `technical_error` (unaltered diagnostic detail), `error_category` (canonical category), and `next_actions` (localized recovery steps). The legacy `error` field remains supported as a fallback technical error. The stage rail shows only a user-facing summary; the original technical error is expandable in the stage detail.

## Run the demo

Watch the live updates without running a real production:

```bash
python scripts/backlot_simulate_run.py          # simulate a production in about one minute
python -m backlot open backlot-demo-run
```

Add `--fast` for a short automated check, or `--cleanup` to remove the demo project when the simulation finishes.
