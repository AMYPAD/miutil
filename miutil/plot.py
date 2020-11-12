from os import path
import matplotlib.pyplot as plt

from .imio import imread


class imscroll:
    """
    Slice through volumes by scrolling.
    Hold SHIFT to scroll faster.
    """

    instances = []
    SUPPORTED_KEYS = ["shift"]

    def __init__(self, vol, view="t", fig=None, titles=None, **kwargs):
        """
        Scroll through 2D slices of 3D volume(s) using the mouse.
        Args:
            vol (str or numpy.ndarray or list or dict): path to file or
                a (list/dict of) array(s).
            view (str): z, t, transverse/y, c, coronal/x, s, sagittal.
            fig (matplotlib.pyplot.Figure): will be created if unspecified.
            titles (list): list of strings (overrides `vol.keys()`).
            **kwargs: passed to `matplotlib.pyplot.imshow()`.
        """
        if isinstance(vol, str) and path.exists(vol):
            vol = imread(vol)
        if hasattr(vol, "keys"):
            keys = list(vol.keys())
            vol = [vol[i] for i in keys]
            if titles is None:
                titles = keys
        if vol[0].ndim == 2:
            vol = [vol]
        elif vol[0].ndim != 3:
            raise IndexError("Expected vol.ndim in [3, 4] but got {}".format(vol.ndim))

        self.titles = titles or [None] * len(vol)

        view = view.lower()
        if view in ["c", "coronal", "y"]:
            vol = [i.transpose(1, 0, 2) for i in vol]
        elif view in ["s", "saggital", "x"]:
            vol = [i.transpose(2, 0, 1) for i in vol]

        self.index_max = min(map(len, vol))
        self.index = self.index_max // 2
        if fig is not None:
            self.fig, axs = fig, fig.subplots(1, len(vol))
        else:
            self.fig, axs = plt.subplots(1, len(vol))
        self.axs = [axs] if len(vol) == 1 else list(axs.flat)
        for ax, i, t in zip(self.axs, vol, self.titles):
            ax.imshow(i[self.index], **kwargs)
            ax.set_title(t or "slice #{}".format(self.index))
        self.vols = vol
        self.key = {i: False for i in self.SUPPORTED_KEYS}
        self.fig.canvas.mpl_connect("scroll_event", self.scroll)
        self.fig.canvas.mpl_connect("key_press_event", self.on_key)
        self.fig.canvas.mpl_connect("key_release_event", self.off_key)
        imscroll.instances.append(self)  # prevents gc

    @classmethod
    def clear(cls, self):
        cls.instances.clear()

    def on_key(self, event):
        if event.key in self.SUPPORTED_KEYS:
            self.key[event.key] = True

    def off_key(self, event):
        if event.key in self.SUPPORTED_KEYS:
            self.key[event.key] = False

    def scroll(self, event):
        self.set_index(
            self.index
            + (1 if event.button == "up" else -1) * (10 if self.key["shift"] else 1)
        )

    def set_index(self, index):
        self.index = index % self.index_max
        for ax, vol, t in zip(self.axs, self.vols, self.titles):
            ax.images[0].set_array(vol[self.index])
            ax.set_title(t or "slice #{}".format(self.index))
        self.fig.canvas.draw()
