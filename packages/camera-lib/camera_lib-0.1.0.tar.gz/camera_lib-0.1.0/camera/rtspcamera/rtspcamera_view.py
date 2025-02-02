from PyQt5.QtWidgets import QWidget

import sys

LINUX="linux"
WINDOWS="win32"
MACOS="darwin"


class RTSPCameraView(QWidget):
    def __init__(self, windowTitle):

        super().__init__()
        
        self.setWindowTitle(windowTitle)
        self.resize(640, 480)
        
    
    def setMediaPlayer(self, media_player):
        # Embed VLC video in PyQt widget
        self.media_player = media_player
        
        if sys.platform.startswith(LINUX):  # For Linux systems
            self.media_player.set_xwindow(self.winId())
        elif sys.platform == WINDOWS:  # For Windows systems
            self.media_player.set_hwnd(self.winId())
        elif sys.platform == MACOS:  # For macOS systems
            self.media_player.set_nsobject(int(self.winId()))