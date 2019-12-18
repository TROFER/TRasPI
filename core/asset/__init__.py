from core.asset.font import Font
from core.asset.template import Template
from core.asset.image import Image

__all__ = ["Font", "Template"]

Font("std", 11, path="bitocra-full.bdf")
Template("std", path="default.template")
