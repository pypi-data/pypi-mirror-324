from camera.rtspcamera import *
from camera.cameratype import CameraType

from console.logger import Logger

class RTSPCameraController:
    def __init__(self):
        self._dialog = RTSPCameraDialog()
        self._devices = {}  # Dictionary to store multiple camera instances
        self._views = {}  # Dictionary to store multiple views

        # Connect dialog buttons
        self._dialog._ui.buttonBox.accepted.connect(self.on_ok_pressed)
        self._dialog._ui.buttonBox.rejected.connect(self.on_cancel_pressed)

    def type(self) -> CameraType:
        return CameraType.RTSP

    def on_ok_pressed(self):
        user = self._dialog._ui.userLineEdit.text()
        password = self._dialog._ui.passwordLineEdit.text()
        ip_address = self._dialog._ui.ipLineEdit.text()
        port = self._dialog._ui.portLineEdit.text()
        stream = self._dialog._ui.streamLineEdit.text()

        rtsp_url = f"rtsp://{user}:{password}@{ip_address}:{port}/stream{stream}"
        camera_name = self._dialog._ui.cameraNameLineEdit.text()

        if camera_name in self._devices:
            Logger().get_logger().warning(f"Camera {camera_name} is already added.")
            return

        # Create camera and view
        device = RTSPCamera(camera_name)
        view = RTSPCameraView(camera_name)
        
        # Store references
        self._devices[camera_name] = device
        self._views[camera_name] = view

        view.setMediaPlayer(device.media_player)
        view.show()
        device.start_streaming(rtsp_url)

        Logger().get_logger().info(f"Added RTSP camera: {camera_name}")
        self._dialog.accept()

    def on_cancel_pressed(self):
        self._dialog.reject()

    def showDialogSettings(self):
        self._dialog.show()

    def get_device_names(self):
        return list(self._devices.keys())
