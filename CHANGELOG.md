# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [0.5.15] - 2026-01-29

### Changed
- PyPI package renamed from `nginx-crossplane` to `ngxparse` for a shorter name that doesn't imply nginx is bundled.
- Docker image names changed to `ngxparse` on both Docker Hub and GHCR.

### Migration
```bash
pip uninstall nginx-crossplane
pip install ngxparse
# import crossplane  # unchanged
# crossplane parse   # CLI unchanged
```

## [0.5.8] - 2025-12-26

### Added
- GitHub Actions release workflow gated on tests that:
  - builds and attaches `sdist`/`wheel` artifacts to a GitHub Release
  - publishes the distribution to PyPI
  - builds and pushes a multi-arch Docker image running the `crossplane` CLI

### Changed
- PyPI distribution name differs from the import/CLI name (`crossplane`).
- Packaging no longer imports `crossplane` during builds to avoid import-time side effects.

## [0.5.9] - 2025-12-26

### Changed
- Renamed PyPI distribution to `nginx-crossplane` (because `crossplane-ng` is already taken by another fork: `https://github.com/qosmio/crossplane`).

## [0.5.10] - 2025-12-26

### Fixed
- Packaging: fix metadata parsing in `setup.py` so editable installs work in CI (PEP 517/660).

## [0.5.11] - 2025-12-26

### Fixed
- CI: run Python 3.6 tests in a `python:3.6` container on `ubuntu-latest` (avoid `ubuntu-20.04` runner queue/hangs).

## [0.5.12] - 2025-12-26

### Fixed
- CI/Packaging: `pyproject.toml` build-system requirements now use env markers so Python 3.6 doesn't try to install `setuptools>=61`.

## [0.5.13] - 2025-12-26

### Added
- Docker image publishing to GitHub Container Registry (GHCR) in addition to Docker Hub.

## [0.5.14] - 2025-12-26

### Changed
- GHCR image name is now `ghcr.io/dvershinin/crossplane` (Docker Hub remains `${DOCKER_USERNAME}/nginx-crossplane`).


