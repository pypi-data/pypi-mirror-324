
import vlc
from typing import List

from console.logger import Logger

class RTSPCamera:
    def __init__(self, name) -> None:
        self._name = name
        self.isStreaming = False        
        self.init()
         
    def start_streaming(self, RTSP_url) -> None:
        media = self.instance.media_new(RTSP_url)
        self.media_player.set_media(media)
        self.media_player.play()
        self.isStreaming= True
        Logger().get_logger().info(f"{self._name} start streaming ...")
    
    def stop_streaming(self) -> None:
        self.media_player.stop()
        self.isStreaming= False
        Logger().get_logger().info(f"{self._name} stop streaming ...")
    
    def isCameraStreaming(self) -> bool:
        return self.isStreaming
    
    def cameraCurrentIndex(self) -> int:
        return 0
    
    def available_camerasInfo(self) -> List[str]:
        return ["Tapo Camera"]
    
    def init(self):
        # VLC instance and player
        Logger().get_logger().info(f"{self._name} Initializing RTSP Camera ...")
        self.instance = vlc.Instance()
        self.media_player = self.instance.media_player_new()
        