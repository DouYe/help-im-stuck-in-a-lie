# Cleanup/publication evidence — 2026-09-30

T28 is completed. This folder contains the initial inventories, identity-checked MP3 deletion receipts, local-layout audit, early-workspace comparison, bounded prepublication check and one-time cleanup scripts. These are records; do not rerun destructive cleanup scripts on a later revision. Source inputs were moved or removed as authorized, so repeat runs are not expected to work.

The authoritative current guide is `../../../docs/REPOSITORY_GUIDE.md`. New song state is `../../../docs/AUDIO_STATUS.md`. Current media/source are indexed by `../../../coordination/REPOSITORY_MANIFEST.json`; publication checks by `../../../coordination/REPOSITORY_VERIFICATION.json`.

`repository_manifest.py` is a reusable non-destructive exception: after deliberately adding/changing tracked files, stage the intended files, run it to refresh the manifest, stage the manifest and commit together. Its `verify` mode checks a clean clone. It reads staged LFS pointer blobs directly so duplicate media paths are all included, even if an older Git LFS listing omits duplicates before the first commit.
