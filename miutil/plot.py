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

    def __init__(self, vol, view="t", fig=None, **kwargs):
        """
        Scroll through 2D slices of a 3D volume using the mouse.
        Args:
            vol (str or numpy.ndarray): path to file or a numpy array.
            view (str): z, t, transverse/y, c, coronal/x, s, sagittal.
            fig (matplotlib.pyplot.Figure): will be created if unspecified.
            **kwargs: passed to `matplotlib.pyplot.imshow()`.
        """
        if isinstance(vol, str) and path.exists(vol):
            vol = imread(vol)

        view = view.lower()
        if view in ["c", "coronal", "y"]:
            vol = vol.transpose(1, 0, 2)
        elif view in ["s", "saggital", "x"]:
            vol = vol.transpose(2, 0, 1)

        self.index = vol.shape[0] // 2
        if fig is not None:
            self.fig, self.ax = fig, fig.subplots()
        else:
            self.fig, self.ax = plt.subplots()
        self.ax.imshow(vol[self.index], **kwargs)
        self.ax.set_title("slice #{self.index}".format(self=self))
        self.vol = vol
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
        self.index = index % self.vol.shape[0]
        self.ax.images[0].set_array(self.vol[self.index])
        self.ax.set_title("slice #{self.index}".format(self=self))
        self.fig.canvas.draw()
