from packaging import version

try:
    import matplotlib
    from matplotlib import pyplot

except ImportError:
    matplotlib = None
    pyplot = None


def _register_colormaps():
    colors = [
        "#1102d8",
        "#3007ba",
        "#500b9d",
        "#6f0e81",
        "#8d1364",
        "#ac1748",
        "#cb1b2b",
        "#ea1e0f",
        "#f83605",
        "#fa600f",
        "#fb8817",
        "#fdb120",
        "#ffda29",
        "#ffed4d",
        "#fff380",
        "#fffbb4",
    ]

    create = matplotlib.colors.LinearSegmentedColormap.from_list

    colormap = create(name="micpy", colors=colors, N=1024)
    colormap_r = create(name="micpy_r", colors=colors[::-1], N=1024)

    if version.parse(matplotlib.__version__) >= version.parse("3.7"):
        register = matplotlib.colormaps.register
        register(colormap)
        register(colormap_r)
    else:
        register = matplotlib.cm.register_cmap
        register("micpy", colormap)
        register("micpy_r", colormap_r)


def configure():
    if not matplotlib:
        return

    try:
        _register_colormaps()
    except ValueError:
        pass
