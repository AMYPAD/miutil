from os import path
import matplotlib.pyplot as plt

from .imio import imread


class imscroll:
    """
    Slice through volumes by scrolling.
    Hold SHIFT to scroll faster.
    """

    _instances = []
    _SUPPORTED_KEYS = ["shift"]

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
        ndim = vol[0].ndim + 1
        if ndim == 3:
            vol = [vol]
        elif ndim != 4:
            raise IndexError("Expected vol.ndim in [3, 4] but got {}".format(ndim))

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
        self.key = {i: False for i in self._SUPPORTED_KEYS}
        self.fig.canvas.mpl_connect("scroll_event", self._scroll)
        self.fig.canvas.mpl_connect("key_press_event", self._on_key)
        self.fig.canvas.mpl_connect("key_release_event", self._off_key)
        imscroll._instances.append(self)  # prevents gc

    @classmethod
    def clear(cls, self):
        cls._instances.clear()

    def _on_key(self, event):
        if event.key in self._SUPPORTED_KEYS:
            self.key[event.key] = True

    def _off_key(self, event):
        if event.key in self._SUPPORTED_KEYS:
            self.key[event.key] = False

    def _scroll(self, event):
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
