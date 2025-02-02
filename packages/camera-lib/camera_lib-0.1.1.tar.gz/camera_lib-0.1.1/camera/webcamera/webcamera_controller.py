from PyQt5.QtMultimedia import QCameraInfo

from PyQt5.QtWidgets import QMessageBox

from camera.webcamera import *
from camera.cameratype import CameraType

class WebCameraController:
    
    def __init__(self):
        # Store multiple cameras and views
        self._cameraList = QCameraInfo.availableCameras()
        self._devices = {}  # Dictionary to store WebCamera instances
        self._views = {}    # Dictionary to store WebCameraView instances

        # Create dialog for camera selection
        self._dialog = WebCameraDialog(self._cameraList)

        # Connect dialog buttons
        self._dialog._ui.buttonBox.accepted.connect(self.on_ok_pressed)
        self._dialog._ui.buttonBox.rejected.connect(self.on_cancel_pressed)

    def on_ok_pressed(self):
        name = self._dialog._ui.cameraNameLineEdit.text()
        index = self._dialog.currentCameraIndex()

        if not name:
            name = QCameraInfo.availableCameras()[index].description() + " " + QCameraInfo.availableCameras()[index].deviceName() # Assign a default name if none is given

        if name in self._devices:
            QMessageBox.warning(None, "Warning", f"A camera named '{name}' is already in use.")
            return

        # Create and store new camera and view
        self._devices[name] = WebCamera(name, index)
        self._views[name] = WebCameraView(name)

        # Set the viewfinder
        if self._devices[name].camera.isAvailable():
            self._devices[name].camera.setViewfinder(self._views[name].streamWidget)
            self._devices[name].start_streaming()
            self._views[name].show()
            self._dialog.accept()
        else:
            QMessageBox.critical(None, "Error", "Camera is not available!")
            del self._devices[name]  # Remove camera if unavailable
            del self._views[name]  # Remove associated view

    def on_cancel_pressed(self):
        self._dialog.reject()

    def showDialogSettings(self):
        self._dialog.show()

    def type(self) -> CameraType:
        return CameraType.WEB

    def stop_camera(self, name):
        """Stop and remove a camera by name."""
        if name in self._devices:
            self._devices[name].stop_streaming()
            self._devices[name].camera.deleteLater()
            del self._devices[name]

        if name in self._views:
            self._views[name].close()
            del self._views[name]

    def stop_all_cameras(self):
        """Stop and remove all cameras."""
        for name in list(self._devices.keys()):  # Use list to avoid modifying during iteration
            self.stop_camera(name)
            
    def get_device_name(self):
        return self._deviceName
        

