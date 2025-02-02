from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtMultimediaWidgets import QVideoWidget

class WebCameraView(QWidget):
    
    def __init__(self, windowTitle):
        super().__init__()
        # Web Camera Video widget to display the stream
        self.streamWidget = QVideoWidget()
        
        # Set up layout
        layout = QVBoxLayout()
        layout.addWidget(self.streamWidget)
        
        # Web Camera Video widget to display the stream
        self.setLayout(layout)
        self.setWindowTitle(windowTitle)
        self.resize(640, 480)
        
        