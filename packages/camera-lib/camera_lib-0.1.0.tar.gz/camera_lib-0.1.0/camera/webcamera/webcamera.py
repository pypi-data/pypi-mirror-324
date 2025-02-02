from PyQt5.QtMultimedia import QCamera, QCameraInfo
from console.logger import Logger

class WebCamera:
    def __init__(self, name: str, cameraIdx: int) -> None:
        """
        Initialize the WebCamera instance.
        
        Args:
            cameraIdx (int): The index of the camera to use.
        """
        self._name = name
        self._cameraIdx = cameraIdx  # Camera index in the system (e.g., /dev/video0 index is 0)
        self._isStreaming = False
        self.camera = None  # Placeholder for the QCamera instance
        
        if not self.init():
            raise ValueError(f"Failed to initialize camera with index {self._cameraIdx}")
        
        if not name:
            self._name = self.get_camera_default_name()

    def __del__(self):
        """Ensure the camera is properly stopped and released."""
        if self.camera and self._isStreaming:
            self.stop_streaming()
        if self.camera:
            del self.camera
            
    def name(self) -> str:
        return self._name

    def start_streaming(self) -> bool:
        """
        Start the camera streaming.

        Returns:
            bool: True if streaming started successfully, False otherwise.
        """
        if self.camera and not self._isStreaming:
            try:
                self.camera.start()
                self._isStreaming = True
                Logger().get_logger().info(f"{self._name} start streaming ...")
                return True
            except Exception as e:
                Logger().get_logger().error(f"Failed to start streaming: {e}")
        return False

    def stop_streaming(self) -> bool:
        """
        Stop the camera streaming.

        Returns:
            bool: True if streaming stopped successfully, False otherwise.
        """
        if self.camera and self._isStreaming:
            try:
                self.camera.stop()
                self._isStreaming = False
                Logger().get_logger().info(f"{self._name} stop streaming ...")
                return True
            except Exception as e:
                print(f"Failed to stop streaming: {e}")
        return False

    def is_streaming(self) -> bool:
        """
        Check if the camera is streaming.

        Returns:
            bool: True if streaming, False otherwise.
        """
        return self._isStreaming

    def get_current_index(self) -> int:
        """
        Get the index of the currently assigned camera.

        Returns:
            int: The camera index.
        """
        return self._cameraIdx

    def init(self) -> bool:
        """
        Initializes the camera with the specified index.

        Returns:
            bool: True if the camera was initialized successfully, False otherwise.
        """
        Logger().get_logger().info("Initializing web camera...")
        cameras_list = QCameraInfo.availableCameras()
        if not cameras_list:
            Logger().get_logger().warning("No camera available")
            return False

        if self._cameraIdx < 0 or self._cameraIdx >= len(cameras_list):
            Logger().get_logger().warning(f"Invalid camera index: {self._cameraIdx}")
            return False

        try:
            self.camera = QCamera(cameras_list[self._cameraIdx])
            return True
        except Exception as e:
            Logger().get_logger().error(f"Failed to initialize camera: {e}")
            return False
        
    def get_camera_default_name(self) -> str:
        return QCameraInfo.availableCameras()[self._cameraIdx].description() + " "+ QCameraInfo.availableCameras()[self._cameraIdx].deviceName()
