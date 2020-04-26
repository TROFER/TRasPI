from core.asset.font import Font
from core.asset.image import Template
from core.asset.res_pool import Pool

class AssetPool(Pool):
    template = Template("default")
    font = Font("bitocra-full", 11) # Default
    bitocra7 = Font("bitocra7", 7)
    bitocra4 =  Font("4thD", 4)