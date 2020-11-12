import matplotlib.pyplot as plt


class imscroll:
    instances = []

    def __init__(self, vol, view='t', **kwargs):
        """
        Scroll through 2D slices of a 3D volume using the mouse.
        Args:
            vol (str or numpy.ndarray): path to file or a numpy array.
            view (str): z, t, transverse/y, c, coronal/x, s, sagittal.
            **kwargs: passed to `matplotlib.pyplot.imshow()`.
        """
        if isinstance(vol, str) and os.path.exists(vol):
            im = imio.getnii(vol)
        elif isinstance(vol, np.ndarray):
            im = vol.copy()
        else:
            raise ValueError('unrecognised vol')

        view = view.lower()
        if view in ['c', 'coronal', 'y']:
            im = im.transpose(1,0,2)
        elif view in ['s', 'saggital', 'x']:
            im = im.transpose(2,0,1)

        self.index = im.shape[0] // 2
        self.fig, self.ax = plt.subplots()
        self.ax.imshow(im[self.index], **kwargs)
        self.vol = im
        self.fig.canvas.mpl_connect('scroll_event', self.scroll)
        imscroll.instances.append(self)  # prevents gc

    @classmethod
    def clear(cls, self):
        cls.instances.clear()

    def scroll(self, event):
        self.set_index(self.index + (1 if event.button == "up" else -1))

    def set_index(self, index):
        self.index = index % self.vol.shape[0]
        self.ax.images[0].set_array(self.vol[self.index])
        self.ax.set_title(f"slice #{self.index}")
        self.fig.canvas.draw()
