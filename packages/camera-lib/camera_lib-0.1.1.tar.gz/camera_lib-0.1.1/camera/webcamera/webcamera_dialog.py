from PyQt5.QtWidgets import QDialog
from PyQt5.QtMultimedia import QCameraInfo, QCamera

from typing import List

from camera.webcamera.ui_webcamera_dialog import Ui_WebCameraDialog

class WebCameraDialog(QDialog):
    
    def __init__(self, cameraList: List['QCameraInfo']):
        super().__init__()
        
        # Setup Dialog UI
        self._ui = Ui_WebCameraDialog()
        self._ui.setupUi(self)
        
        self._cameraInfoList = []
        self._currentCameraIndex = 0
        
        # Fill camera index combo box
        # for cameraInfo in cameraList:
        #     self._cameraInfoList.append(cameraInfo.deviceName())
        # self._ui.cameraIndexcomboBox.addItems(self._cameraInfoList)
        
        # for idx, camera_info in enumerate(cameraList):
        #     self.comboBox.addItem(f"Camera {idx}: {camera_info.description()} (Device: {camera_info.deviceName()})", idx)
        
        for idx, _ in enumerate(cameraList):
            self._ui.cameraIndexcomboBox.addItem(str(idx))
                    
        self._ui.cameraIndexcomboBox.currentIndexChanged.connect(self.updateCameraIndex)
        
        # Fill supported resolutions combo box
        
        
        # Fill supported frame rates

        
        
        # Manage Window
        self.setWindowTitle("Web Camera Settings")
        
    def currentCameraIndex(self) -> int:
        return self._currentCameraIndex
    
    
    def updateCameraIndex(self, index):
        self._currentCameraIndex = int(self._ui.cameraIndexcomboBox.itemText(index))
        
        
        
        # Connect buttons to custom slots
    #     self._ui.buttonBox.accepted.connect(self.on_ok_pressed)
    #     self._ui.buttonBox.rejected.connect(self.on_cancel_pressed)
    
    # def on_ok_pressed(self):
    #     print("OK was pressed")
    #     self.accept()  # Close the dialog with Accepted state

    # def on_cancel_pressed(self):
    #     print("Cancel was pressed")
    #     self.reject()  # Close the dialog with Rejected state