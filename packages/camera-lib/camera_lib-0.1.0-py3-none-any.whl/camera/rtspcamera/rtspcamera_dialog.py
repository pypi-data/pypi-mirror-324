from PyQt5.QtWidgets import QDialog

from camera.rtspcamera.ui_rtspcamera_dialog import Ui_RSTP_Dialog


class RTSPCameraDialog(QDialog):
    
    
    def __init__(self):
        
        super().__init__()
    
        self._ui = Ui_RSTP_Dialog()
        self._ui.setupUi(self)
        
        