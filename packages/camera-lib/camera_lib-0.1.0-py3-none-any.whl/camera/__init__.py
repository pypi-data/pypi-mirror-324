"""
Camera package

This package provides support for various types of cameras (e.g., web cameras, RTSP cameras).
It follows an MVC architecture to separate concerns and supports extensible camera types.
"""

from .webcamera.webcamera_controller import WebCameraController
from .rtspcamera.rtspcamera_controller import RTSPCameraController

# Define package metadata
__version__ = "0.1.0"
__author__ = "Mohamed Lamine KARTOBI"
__license__ = "MIT"

print("******************************** Welcome to the Camera perception environment ********************************")
print(f"Camera package {__version__}")