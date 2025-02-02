import matplotlib.cm as cmap
from matplotlib.colors import Normalize, rgb2hex, hex2color


class GridColormap(dict):
    def __init__(self, colormap, vmin, vmax, ncolors=32):
        if colormap and isinstance(colormap, str):
            colormap = cmap.ScalarMappable(
                Normalize(vmin, vmax), getattr(cmap, colormap, "jet")
            )
        if not isinstance(colormap, cmap.ScalarMappable):
            raise ("colormap must be a matplotlib colormap name or a ScalarMappable")
        domain = [vmin + i * (vmax - vmin) / ncolors for i in range(ncolors)]
        super().__init__(
            {
                "scale": [rgb2hex(c) for c in colormap.to_rgba(domain)],
                "domain": domain,
            }
        )
