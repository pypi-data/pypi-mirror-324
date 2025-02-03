from contextlib import suppress
from typing import TYPE_CHECKING

from grpc import RpcError
from magicgui.widgets import Container, ProgressBar, create_widget

if TYPE_CHECKING:
    import napari


# if we want even more control over our widget, we can use
# magicgui `Container`
class BiopbImageWidget(Container):
    def __init__(self, viewer: "napari.viewer.Viewer"):
        super().__init__()
        self._viewer = viewer
        # use create_widget to generate widgets from type annotations
        self._image_layer_combo = create_widget(
            label="Image", annotation="napari.layers.Image"
        )
        self._is3d = create_widget(label="3D", annotation=bool)

        self._server = create_widget(
            value="lacss.biopb.org",
            label="Server",
            annotation=str,
        )

        self._threshold = create_widget(
            value=0.4,
            label="Min Score",
            annotation=float,
            widget_type="FloatSlider",
        )
        self._threshold.min = 0
        self._threshold.max = 1

        self._size_hint = create_widget(
            value=35.0,
            label="Size Hint",
            annotation=float,
            widget_type="FloatSlider",
        )
        self._size_hint.min = 10
        self._size_hint.max = 200

        self._nms = create_widget(
            value=False,
            label="NMS",
            annotation=bool,
        )

        self._nms_iou = create_widget(
            value=0.4,
            label="NMS Iou",
            annotation=float,
            widget_type="FloatSlider",
        )
        self._nms_iou.min = 0.0
        self._nms_iou.max = 1.0
        self._nms_iou.visible = False

        def nms_changed() -> None:
            with suppress(AttributeError):
                self._nms_iou.visible = self._nms.value

        self._nms.changed.connect(nms_changed)

        self._run_button = create_widget(label="Run", widget_type="Button")
        self._run_button.changed.connect(self.run)

        self._progress_bar = ProgressBar(label="Running", value=0, step=1)
        self._progress_bar.visible = False

        self._elements = [
            self._image_layer_combo,
            self._is3d,
            self._server,
            self._threshold,
            self._size_hint,
            self._nms,
            self._nms_iou,
            self._run_button,
            self._progress_bar,
        ]

        # append into/extend the container with your widgets
        self.extend(self._elements)

    def snapshot(self):
        return {w.label: w.value for w in self._elements}

    def run(self):
        from ._grpc import grpc_call

        name = self._image_layer_combo.value.name + "_label"

        self._run_button.enabled = False
        self._run_button.visible = False

        self._progress_bar.visible = True
        self._progress_bar.value = 0

        try:
            labels = grpc_call(self)

            if name in self._viewer.layers:
                self._viewer.layers[name].data = labels
            else:
                self._viewer.add_labels(labels, name=name)

        except RpcError as err:
            print(err)
            # print(err.details())
        # except Exception as all_err:
        #     print(all_err)

        self._progress_bar.visible = False
        self._run_button.enabled = True
        self._run_button.visible = True
