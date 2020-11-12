from os import path
import matplotlib.pyplot as plt

from .imio import imread


class imscroll:
    """
    Slice through volumes by scrolling.
    Hold SHIFT to scroll faster.
    CTRL+click to select points to plot profiles between.
    """

    _instances = []
    _SUPPORTED_KEYS = ["control", "shift"]

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
        self.picked = []
        self._annotes = []
        self.key = {i: False for i in self._SUPPORTED_KEYS}
        self.fig.canvas.mpl_connect("scroll_event", self._scroll)
        self.fig.canvas.mpl_connect("key_press_event", self._on_key)
        self.fig.canvas.mpl_connect("key_release_event", self._off_key)
        self.fig.canvas.mpl_connect("button_press_event", self._on_click)
        imscroll._instances.append(self)  # prevents gc

    @classmethod
    def clear(cls, self):
        cls._instances.clear()

    def _on_key(self, event):
        key = {"ctrl": "control"}.get(event.key, event.key)
        if key in self._SUPPORTED_KEYS:
            self.key[key] = True

    def _off_key(self, event):
        key = {"ctrl": "control"}.get(event.key, event.key)
        if key in self._SUPPORTED_KEYS:
            self.key[key] = False

    def _scroll(self, event):
        self.set_index(self.index + event.step * (10 if self.key["shift"] else 1))

    def set_index(self, index):
        self.index = index % self.index_max
        for ax, vol, t in zip(self.axs, self.vols, self.titles):
            ax.images[0].set_array(vol[self.index])
            ax.set_title(t or "slice #{}".format(self.index))
        for ann in self._annotes:
            ann.remove()
        self._annotes = []
        self.fig.canvas.draw()

    def _on_click(self, event):
        if not self.key["control"]:
            return
        self.picked.append((event.xdata, event.ydata))
        if len(self.picked) < 2:
            return

        import numpy as np
        import scipy.ndimage as ndi

        (x0, y0), (x1, y1) = self.picked[:2]
        num = int(np.round(np.hypot(y1 - y0, x1 - x0))) + 1
        x, y = np.linspace(x0, x1, num), np.linspace(y0, y1, num)
        z = ndi.map_coordinates(
            event.inaxes.images[0].get_array(), np.vstack((x, y)), order=1
        )
        self.picked = []
        self.key["control"] = False

        self._annotes.append(event.inaxes.plot([x0, x1], [y0, y1], "ro-")[0])
        plt.figure()
        plt.plot(x, z, "r-")
        plt.xlabel("x")
        plt.ylabel("Intensity")
        plt.show()
