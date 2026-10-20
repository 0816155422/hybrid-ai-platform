"""HAP local-only data preparation adapter (Phase 0 prototype)."""
from .local_files import CollectionBlocked, collect_local_file, normalize_structured_artifact

__all__ = ["CollectionBlocked", "collect_local_file", "normalize_structured_artifact"]
