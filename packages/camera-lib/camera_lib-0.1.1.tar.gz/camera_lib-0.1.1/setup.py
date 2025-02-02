from setuptools import setup, find_packages


VERSION = "0.1.1"
DESC = "A camera package for Web and Wi-Fi cameras management"
LONG_DESC = "A camera package for Web and Wi-Fi cameras management for start/stop streaming, Web Cameras are based on PyQt5, Wi-Fi cameras are based on VLC"

setup(
    name="camera-lib",
    version=VERSION,  # Update the version as needed
    packages=find_packages(where='src/camera'),  # This will include the camera package and its submodules
    install_requires=['PyQt5', 'vlc'],  # Add any dependencies you might have
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Use the license you're applying
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python versions your package supports
)
