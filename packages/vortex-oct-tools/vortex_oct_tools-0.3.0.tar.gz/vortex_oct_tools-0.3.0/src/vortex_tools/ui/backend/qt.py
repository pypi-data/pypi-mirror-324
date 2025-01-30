from typing import List, Tuple, Iterable, Optional
from enum import Enum, IntFlag
from math import floor, ceil

import numpy as np

from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QCursor, QMouseEvent, QEnterEvent, QWheelEvent, QKeyEvent, QPainter, QTransform, QImage, QPixmap, QPaintEvent, QPen, QColor
from qtpy.QtCore import Qt, QEvent, QPoint, QPointF, QRect, QRectF, Signal

from .base import BaseImageWidget

__all__ = ['NumpyImageWidget', 'NumpyImageViewer']

class NumpyImageWidget(BaseImageWidget, QWidget):
    class Scaling(Enum):
        Absolute = 0
        Relative = 1
        Percentile = 2

    class Sizing(Enum):
        Fixed = 0
        Fit = 1
        Stretch = 2

    class Flip(IntFlag):
        Horizontal = 2**0
        Vertical = 2**1

    __safe_update = Signal(bool, name='request_update')

    def __init__(self, *args, **kwargs):
        '''
        Efficiently display a Numpy array as a color-mapped image.

        Set the displayed array using the `data` property.
        The array may be edited in-place.
        Call `invalidate()` to request regeneration of the display image when editing the array in place.

        transform `QTransform`: `None`
            Transformation to apply to the displayed image.
            The origin is the center of the display.
            This transformation is applied after the image has been initially scaled.
        scaling `Scaling`: `Relative`
            Interpretation of range.
            `Absolute` indicates fixed values.
            `Relative` indicates values relative to the range of the input data as a ratio in [0, 1].
            `Percentile` indicates percentiles of the input data as a ratio in [0, 1].
        sizing `Iterable[Sizing]`: [`Fit`, `Fit`]
            Control sizing of image within widget in the horizontal and vertical directions, respectively.
            `Fixed` does not scale with the display.
            `Stretch` fills the direction with the image.
            `Fit` uses the largest length of that dimension while respecting the other settings.
        centerlines `bool`: `False`
            Draw horizontal and vertical centerlines through widget.
        crosshairs `bool`: `False`
            Draw horizontal and vertical lines through the cursor.
        probe `bool`: `False`
            Draw a tooltip that indicates the location, value, and color under the cursor.
        probe_format `str`:
            Format string for `str.format` used to generate probe text.
            Available format fields are `row`, `column`, `value`, `red`, `green`, `blue`, and `alpha`.
        pan `Tuple[float, float]`: `(0, 0)`
            Offset in pixels of the image center from the center of the widget.
        angle `float`: `0`
            Angle in degrees of rotation about the image center.
        zoom `float`: `1`
            Scale factor of the image.
        flip `Flip`: 0
            Flags to control horizontal or vertical flipping of the image.
        cursor_width_hint `int`: `16`
            The assumed size of the cursor in pixels if it cannot be obtained programmatically.
        '''

        self._transform = kwargs.pop('transform', None)
        if not self._transform:
            self._transform = QTransform()

        self._range_mode: NumpyImageWidget.Scaling = kwargs.pop('scaling', NumpyImageWidget.Scaling.Absolute)
        self._size_mode: Iterable[NumpyImageWidget.Sizing] = kwargs.pop('sizing', [NumpyImageWidget.Sizing.Fit, NumpyImageWidget.Sizing.Fit])

        self._centerlines: bool = kwargs.pop('centerlines', False)
        self._crosshairs: bool = kwargs.pop('crosshairs', False)
        self._statistics: bool = kwargs.pop('statistics', False)

        self._probe: bool = kwargs.pop('probe', False)
        self._probe_format: str = kwargs.pop('probe_format', '({row}, {column}) = {value:g}\n[{red}, {green}, {blue}, {alpha}]')

        self._pan: Tuple[float, float] = kwargs.pop('pan', (0, 0))
        self._angle: float = kwargs.pop('angle', 0)
        self._zoom: float = kwargs.pop('zoom', 1)
        self._flip: int = kwargs.pop('flip', 0)

        self._cursor_width_hint: int = kwargs.pop('cursor_width_hint', 16)

        self._vmin = 0
        self._vmax = 0

        self._enable_keyboard: bool = kwargs.pop('enable_keyboard', False)

        self.__pixmap: Optional[QPixmap] = None
        self.__pixmap_draw_rect: Optional[QRectF] = None

        super().__init__(*args, **kwargs)

        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)

        self.__safe_update.connect(self.update)
        self.update(safe=True)

    def paintEvent(self, e: QPaintEvent) -> None:
        painter = QPainter(self)

        mouse: QPoint = QPoint(self.mapFromGlobal(QCursor.pos()))

        # background
        super().paintEvent(e)

        # foreground
        if self.pixmap:
            self._draw_image(painter)

        if self._centerlines:
            self._draw_inverted_lines(painter, QPointF(self.width() / 2, self.height() / 2))

        if self._crosshairs and self.rect().contains(mouse) and self.pixmap:
            self._draw_inverted_lines(painter, QPointF(mouse))

        if self.pixmap and self._probe:
            self._draw_probe(painter, QPointF(mouse))

        if self._debug or self._statistics:
            self._draw_stats(painter)

    def keyPressEvent(self, e: QKeyEvent) -> None:
        if self._enable_keyboard:
            if e.key() == Qt.Key.Key_P:
                self._probe = not self._probe
            elif e.key() == Qt.Key.Key_C:
                self._crosshairs = not self._crosshairs
            elif e.key() == Qt.Key.Key_L:
                self._centerlines = not self._centerlines
            elif e.key() == Qt.Key.Key_S:
                self._statistics = not self._statistics

            self.update()

    @property
    def _mouse_responsive(self) -> bool:
        return self._crosshairs or self._probe

    def enterEvent(self, e: QEnterEvent) -> None:
        if self._mouse_responsive:
            self.update(safe=True)

        super().enterEvent(e)

    def leaveEvent(self, e: QEvent) -> None:
        if self._mouse_responsive:
            self.update(safe=True)

        super().leaveEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self._mouse_responsive:
            self.update(safe=True)

        super().mouseMoveEvent(e)

    def invalidate(self) -> None:
        '''
        Clear the cached image.
        This is required for changes to the underlying data buffer to display.
        '''
        self.__pixmap = None
        self.__pixmap_draw_rect = None

    def update(self, safe=False) -> None:
        '''
        Call `update()` through the signal/slot mechanism by default.
        This simplifies calling update from background threads.
        '''
        if safe:
            self.setMouseTracking(self._mouse_responsive)

            super().update()
        else:
            self.__safe_update.emit(True)

    @property
    def pixmap(self) -> QPixmap:
        '''QPixmap representation of drawn image'''
        if self.__pixmap is None:
            self._make_and_cache_image()

        # get from cache
        return self.__pixmap

    def _draw_image(self, painter: QPainter) -> None:
        painter.save()
        painter.setTransform(self._make_draw_transform())
        painter.drawPixmap(self.__pixmap_draw_rect, self.pixmap, QRectF(self.pixmap.rect()))
        painter.restore()

    def _draw_inverted_lines(self, painter: QPainter, point: QPointF) -> None:
        painter.save()
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Exclusion)
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawLine(QPointF(0, point.y()), QPointF(self.width(), point.y()))
        painter.drawLine(QPointF(point.x(), 0), QPointF(point.x(), self.height()))
        painter.restore()

    def _draw_probe(self, painter: QPainter, point: QPointF) -> None:
        # map to data
        (row, col) = self._map_window_to_data(point)

        # check bounds
        if row < 0 or row >= self.data.shape[0]:
            return
        if col < 0 or col >= self.data.shape[1]:
            return

        value = self.data[row, col]
        rgba = self._colormap(value, bytes=True)

        lines = self._probe_format.format(
            row=row, column=col, value=value,
            red=rgba[0], green=rgba[1], blue=rgba[2], alpha=rgba[3]
        ).splitlines()

        cursor_width = self.cursor().pixmap().size().width() if not self.cursor().pixmap().isNull() else self._cursor_width_hint

        anchors_offsets = {
            (True, True): (BaseImageWidget.Anchor.TopLeft, QPointF(cursor_width + 4,  4)),
            (True, False): (BaseImageWidget.Anchor.TopRight, QPointF(-4,  4)),
            (False, True): (BaseImageWidget.Anchor.BottomLeft, QPointF(4,  -4)),
            (False, False): (BaseImageWidget.Anchor.BottomRight, QPointF(-4,  -4)),
        }
        (anchor, offset) = anchors_offsets[(
            point.y() < self.height() / 2,
            point.x() < self.width() / 2,
        )]

        self._draw_multiline_text_overlay(painter, point + offset, lines, padding=[2, 4, -2, 2], anchor=anchor)

    def _make_and_cache_image(self) -> None:
        if self.data is None:
            return

        shape = self.data.shape

        xform = self._make_draw_transform(shape)
        img_rect = QRectF(-shape[1] / 2, -shape[0] / 2, shape[1], shape[0])
        wnd_rect = xform.mapRect(img_rect)

        # clip to displayed region
        tl = wnd_rect.topLeft()
        br = wnd_rect.bottomRight()

        tl.setX(np.clip(tl.x(), 0, self.width()))
        tl.setY(np.clip(tl.y(), 0, self.height()))
        br.setX(np.clip(br.x(), 0, self.width()))
        br.setY(np.clip(br.y(), 0, self.height()))

        win_roi_rect = QRectF(tl, br)

        img_roi_rect = xform.inverted()[0].mapRect(win_roi_rect)
        img_roi_rect.translate(shape[1] / 2.0, shape[0] / 2.0)

        start = np.asanyarray([
            np.clip(floor(img_roi_rect.topLeft().y()), 0, shape[0]),
            np.clip(floor(img_roi_rect.topLeft().x()), 0, shape[1])
        ])
        end = np.asanyarray([
            np.clip(ceil(img_roi_rect.bottomRight().y()), 0, shape[0]),
            np.clip(ceil(img_roi_rect.bottomRight().x()), 0, shape[1])
        ])

        # check if nothing to draw
        if (end - start).min() <= 0 or win_roi_rect.width() <= 0 or win_roi_rect.width() <= 0:
            return

        # extract region of interest
        step = (end - start + 1) // np.asanyarray([ win_roi_rect.height(), win_roi_rect.width() ]).round().astype(int)
        step = np.where(step < 1, 1, step)
        data = self.data[start[0]:end[0]:step[0], start[1]:end[1]:step[1], ...]

        # determine scale bounds on full data
        if self._range_mode == NumpyImageWidget.Scaling.Absolute:
            (self._vmin, self._vmax) = self._range
        elif self._range_mode == NumpyImageWidget.Scaling.Relative:
            self._vmin = self.data.min()
            self._vmax = self.data.max()
        elif self._range_mode == NumpyImageWidget.Scaling.Percentile:
            (self._vmin, self._vmax) = np.percentile(self.data, self._range)
        else:
            raise ValueError(f'unknown data range mode: {self._range_mode}')

        # apply scale and colormap
        data = (data.astype(np.float32) - self._vmin) / (self._vmax - self._vmin)
        data = self._colormap(data, bytes=True)

        # determine image format
        data = np.squeeze(data)
        if data.ndim in [1, 2]:
            color = False
            alpha = False
        elif data.ndim == 3:
            color = data.shape[2] >= 3
            alpha = data.shape[2] in [2, 4]
        else:
            raise ValueError(f'invalid image dimensions: {data.ndim}')

        # match Qt optimized image format
        data = np.atleast_3d(data)
        if color:
            if alpha:
                # native format already
                pass
            else:
                data = np.concatenate((data, np.full(data.shape[:2], 255)))
        else:
            if alpha:
                data = np.take(data, [0, 0, 0, 1], axis=2)
            else:
                data = np.concatenate((data, data, data, np.full(data.shape[:2], 255)[..., None]))

        # convert to QImage
        # data = cbook._unmultiplied_rgba8888_to_premultiplied_argb32(memoryview(data))
        # self.__pixmap = QPixmap.fromImage(QImage(data, data.shape[1], data.shape[0], QImage.Format_ARGB32_Premultiplied))
        self.__pixmap = QPixmap.fromImage(QImage(data, data.shape[1], data.shape[0], QImage.Format_RGBA8888))
        self.__pixmap_draw_rect = QRectF(QPointF(start[1], start[0]), QPointF(end[1], end[0])).translated(-shape[1] / 2, -shape[0] / 2)

    def _make_draw_transform(self, shape: Optional[Iterable[int]]=None) -> QTransform:
        if shape is None:
            shape = self.data.shape
        (image_height, image_width) = shape

        xform = QTransform()

        def _sign(bit):
            return -1 if (self._flip & bit) else 1

        # start by drawing a 1x1 image in the widget center
        xform.translate(self.width() / 2 + self._pan[0], self.height() / 2 + self._pan[1])
        xform.rotate(self._angle)
        xform.scale(
            self._zoom * _sign(NumpyImageWidget.Flip.Horizontal) / image_width,
            self._zoom * _sign(NumpyImageWidget.Flip.Vertical) / image_height
        )

        (xs, ys) = self._size_mode

        if xs == NumpyImageWidget.Sizing.Fixed:
            width = image_width
        elif xs == NumpyImageWidget.Sizing.Stretch:
            width = self.width()
        elif xs == NumpyImageWidget.Sizing.Fit:
            width = None
        else:
            raise ValueError(f'unknown size mode: {xs}')

        if ys == NumpyImageWidget.Sizing.Fixed:
            height = image_height
        elif ys == NumpyImageWidget.Sizing.Stretch:
            height = self.height()
        elif ys == NumpyImageWidget.Sizing.Fit:
            height = None
        else:
            raise ValueError(f'unknown size mode: {ys}')

        if height and width:
            pass
        elif height:
            width = self._aspect * height
        elif width:
            height = width / self._aspect
        else:
            # fit image into widget
            s = min([self.width() / (image_height * self._aspect), self.height() / image_height])
            height = s * image_height
            width = self._aspect * height

        # scale up to actual display size
        xform.scale(width, height)

        # return composed with user transform
        return xform * self._transform

    def _make_additional_stats(self) -> List[str]:
        lines = []
        if self.__pixmap is None:
            lines += ['Image: None']
        else:
            lines += [f'Image: {self.__pixmap.height()} x {self.__pixmap.width()}']
        lines += ['']
        lines += [f'Range: {self._vmin} - {self._vmax}']
        lines += [f'Pan: ({self._pan[0]}, {self._pan[1]})']
        lines += [f'Angle: {self._angle}']
        lines += [f'Flip: {self._flip % 4}']
        lines += [f'Zoom: {self._zoom:.2g}']
        return lines

    def _make_window_transform(self) -> QTransform:
        xform = self._make_draw_transform()
        xform.translate(-self.data.shape[1] / 2, -self.data.shape[0] / 2)
        xform = xform.inverted()[0]
        return xform

    def _map_window_to_data(self, window_point: QPointF) -> QPointF:
        image_point = self._make_window_transform().map(window_point)
        row = int(floor(image_point.y()))
        col = int(floor(image_point.x()))
        return (row, col)

class NumpyImageViewer(NumpyImageWidget):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('enable_keyboard', True)
        kwargs.setdefault('centerlines', False)
        kwargs.setdefault('crosshairs', True)
        kwargs.setdefault('probe', True)

        self._angle_key_step: float = kwargs.pop('angle_key_step', 30)
        self._angle_mouse_step: float = kwargs.pop('angle_mouse_step', 0.2)
        self._zoom_key_step: float = kwargs.pop('zoom_key_step', 0.1)
        self._zoom_mouse_step: float = kwargs.pop('zoom_mouse_step', 0.01)

        self._range_step: int = kwargs.pop('range_step', 1)

        super().__init__(*args, **kwargs)

        self._mouse_down_position: Optional[QPoint]=None
        self._mouse_down_pan: Optional[Tuple[float, float]]=None
        self._mouse_down_angle: Optional[float]=None

    def keyPressEvent(self, e: QKeyEvent) -> None:
        shift = (e.modifiers() & Qt.KeyboardModifier.ShiftModifier) == Qt.KeyboardModifier.ShiftModifier
        sign = 1 if not shift else -1

        # display transform
        if e.key() == Qt.Key.Key_R:
            self._angle += sign * self._angle_key_step
            self.invalidate()
        elif e.key() == Qt.Key.Key_F:
            self._flip += sign
            self.invalidate()
        elif e.key() == Qt.Key.Key_Z:
            if shift:
                factor = 1 - self._zoom_key_step
            else:
                factor = 1 + self._zoom_key_step
            self._zoom *= factor
            self._pan = [self._pan[0] * factor, self._pan[1] * factor]
            self.invalidate()

        # display range
        elif e.key() == Qt.Key.Key_BracketLeft:
            self._range[0] -= self._range_step
            self.invalidate()
        elif e.key() == Qt.Key.Key_Minus:
            self._range[0] += self._range_step
            self.invalidate()
        elif e.key() == Qt.Key.Key_BracketRight:
            self._range[1] -= self._range_step
            self.invalidate()
        elif e.key() == Qt.Key.Key_Equal:
            self._range[1] += self._range_step
            self.invalidate()

        # display reset
        elif e.key() == Qt.Key.Key_Home:
            self._angle = 0
            self._flip = 0
            self._zoom = 1
            self._pan = [0, 0]
            self.invalidate()

        e.accept()

        super().keyPressEvent(e)
        self.update(safe=True)

    def mousePressEvent(self, e: QMouseEvent) -> None:
        if e.buttons() & (Qt.MouseButton.LeftButton | Qt.MouseButton.RightButton):
            self._mouse_down_position = e.position()

            if e.buttons() & Qt.MouseButton.LeftButton:
                self._mouse_down_pan = self._pan
                self._mouse_down_angle = None
            if e.buttons() & Qt.MouseButton.RightButton:
                self._mouse_down_pan = None
                self._mouse_down_angle = self._angle

            e.accept()

        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e: QMouseEvent) -> None:
        self._mouse_down_position = None
        self._mouse_down_pan = None
        self._mouse_down_angle = None

        e.accept()

        super().mouseReleaseEvent(e)

    def mouseMoveEvent(self, e: QMouseEvent) -> None:
        if self._mouse_down_position:
            delta = e.position() - self._mouse_down_position

            if self._mouse_down_pan is not None:
                self._pan = [self._mouse_down_pan[0] + delta.x(), self._mouse_down_pan[1] + delta.y()]
                self.invalidate()
            if self._mouse_down_angle is not None:
                self._angle = self._mouse_down_angle + delta.y() * self._angle_mouse_step
                self.invalidate()

            e.accept()

        super().mouseMoveEvent(e)
        self.update(safe=True)

    def wheelEvent(self, e: QWheelEvent) -> None:
        delta = e.angleDelta().y()

        if delta >= 0:
            factor = (1 + self._zoom_mouse_step)**delta
        else:
            factor = (1 - self._zoom_mouse_step)**-delta
        self._zoom *= factor
        self._pan = [self._pan[0] * factor, self._pan[1] * factor]
        self.invalidate()

        e.accept()

        super().wheelEvent(e)
        self.update(safe=True)
