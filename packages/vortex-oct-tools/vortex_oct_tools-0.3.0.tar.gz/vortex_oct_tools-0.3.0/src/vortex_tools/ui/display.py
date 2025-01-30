from typing import Iterable, List

import numpy

try:
    import cupy
except ImportError:
    # allow CPU-only acquisitions to use widgets without installing CuPy
    class cupy:
        ndarray: object

__all__ = ['EndpointImageWidget', 'EnFaceImageWidget', 'RasterEnFaceWidget', 'RadialEnFaceWidget', 'SpiralEnFaceWidget', 'CrossSectionImageWidget']

import os
_BACKEND = os.environ.get('VORTEX_TOOLS_UI_BACKEND', 'numpy')
if _BACKEND == 'matplotlib':
    from vortex_tools.ui.backend.mpl import MatplotlibImageWidget as BackendImageWidget
elif _BACKEND in ['numpy', 'numpy-static']:
    if _BACKEND == ['numpy-static']:
        from vortex_tools.ui.backend.qt import NumpyImageWidget as BackendImageWidget
    else:
        from vortex_tools.ui.backend.qt import NumpyImageViewer as BackendImageWidget
    Scaling = BackendImageWidget.Scaling
    Sizing = BackendImageWidget.Sizing
    __all__ += ['Scaling', 'Sizing']
else:
    import warnings
    warnings.warn(f'unknown VORTEX_TOOLS_UI_BACKEND={_BACKEND}')
    from vortex_tools.ui.backend import NumpyImageWidget as BackendImageWidget

class EndpointImageWidget(BackendImageWidget):
    def __init__(self, endpoint, *args, **kwargs):
        kwargs.setdefault('range', [0, 40])
        kwargs.setdefault('scaling', BackendImageWidget.Scaling.Absolute)

        super().__init__(*args, **kwargs)
        self._endpoint = endpoint

        self._bscan_idxs = []

    def notify_segments(self, bscan_idxs: Iterable[int]):
        self._bscan_idxs.extend(bscan_idxs)
        self.update()

class EnFaceImageWidget(EndpointImageWidget):
    def __init__(self, *args, **kwargs):
        self._section = kwargs.pop('section', None)

        super().__init__(*args, **kwargs)

    def paintEvent(self, e):
        if self.data is None or self.data.shape != self._image_shape():
            if self._endpoint.tensor.shape:
                self.data = numpy.zeros(self._image_shape(), dtype=self._endpoint.tensor.dtype)

        if self._bscan_idxs:
            idxs = sorted(set(self._bscan_idxs))
            self._bscan_idxs.clear()

            self._update_image(self._endpoint, idxs)
            # regenerate cached image
            self.invalidate()

        # actually draw
        super().paintEvent(e)

    def _image_shape(self):
        return tuple(self._endpoint.tensor.shape[:2])

    def _apply_sectioning(self, vol):
        if self._section is None:
            return vol
        else:
            return vol[..., slice(*self._section)]

    def _update_image(self, endpoint, bscan_idxs):
        with endpoint.tensor as volume:
            if isinstance(volume, cupy.ndarray):
                with endpoint.stream:
                    self.data = self._apply_sectioning(volume).max(axis=2).get()
                endpoint.stream.synchronize()
            else:
                self.data = self._apply_sectioning(volume).max(axis=2)

    def _make_additional_stats(self) -> List[str]:
        lines = super()._make_additional_stats()
        lines.append(f'Section: {self._section}')
        return lines

class RasterEnFaceWidget(EnFaceImageWidget):
    def __init__(self, *args, **kwargs):
        title = kwargs.pop('title', 'Raster En Face')

        super().__init__(*args, **kwargs)

        self.setWindowTitle(title)

    def _update_image(self, endpoint, bscan_idxs):
        with endpoint.tensor as volume:
            bscan_idxs = [i for i in bscan_idxs if i < volume.shape[0]]
            if isinstance(volume, cupy.ndarray):
                with endpoint.stream:
                    self.data[bscan_idxs, ...] = self._apply_sectioning(volume)[bscan_idxs, ...].max(axis=2).get()
                endpoint.stream.synchronize()
            else:
                self.data[bscan_idxs, ...] = self._apply_sectioning(volume)[bscan_idxs, ...].max(axis=2)

class RadialEnFaceWidget(EnFaceImageWidget):
    def __init__(self, *args, **kwargs):
        title = kwargs.pop('title', 'Radial En Face')

        super().__init__(*args, **kwargs)

        self.setWindowTitle(title)

class SpiralEnFaceWidget(EnFaceImageWidget):
    def __init__(self, *args, **kwargs):
        title = kwargs.pop('title', 'Spiral En Face')

        super().__init__(*args, **kwargs)

        self.setWindowTitle(title)

class CrossSectionImageWidget(EndpointImageWidget):
    def __init__(self, *args, **kwargs):
        self._fixed = kwargs.pop('fixed', None)

        self._downsample = kwargs.pop('downsample', None)
        if self._downsample is not None:
            self._downsample = numpy.asanyarray(self._downsample, int)

        title = kwargs.pop('title', 'Cross-Section')

        super().__init__(*args, **kwargs)

        self.setWindowTitle(title)

    def _image_shape(self):
        shape = super()._image_shape()

        if self._downsample is not None:
            shape = tuple(shape / self._downsample)

        return shape

    def _apply_downsampling(self, a):
        if self._downsample is None:
            return a
        else:
            ds = self._downsample
            return a.reshape((a.shape[0] // ds[0], ds[0], a.shape[1] // ds[1], ds[1])).swapaxes(1, 2).reshape((a.shape[0] // ds[0], a.shape[1] // ds[1], -1)).mean(axis=-1)

    def paintEvent(self, e):
        if self.data is not None:
            try:
                # synchronize GPU, if possible
                self._endpoint.stream.synchronize()
            except AttributeError:
                pass

        # actually draw
        super().paintEvent(e)

    def notify_segments(self, bscan_idxs: Iterable[int]):
        # ignore if no data available
        if not len(self._endpoint.tensor.shape):
            return

        # choose which segment to display
        if self._fixed is None:
            idx = bscan_idxs[-1]
        elif self._fixed in bscan_idxs:
            idx = self._fixed
        else:
            return

        # generate the cross-section
        with self._endpoint.tensor as volume:
            if isinstance(volume, cupy.ndarray):
                # asynchronous on GPU
                with self._endpoint.stream:
                    self.data = self._apply_downsampling(volume[idx].T).get()
            else:
                self.data = self._apply_downsampling(volume[idx].T)

        # request a redraw
        # NOTE: image cache is already invalidated above
        self.update()

    def _make_additional_stats(self) -> List[str]:
        lines = super()._make_additional_stats()
        lines.append(f'Downsample: {self._downsample}')
        return lines
