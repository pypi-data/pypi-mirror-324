from setuptools import setup, find_packages

VERSION = "0.1.5"
DESC = "A camera package for Web and Wi-Fi cameras management"
LONG_DESC = "A camera package for Web and Wi-Fi cameras management for start/stop streaming. Web Cameras are based on PyQt5, Wi-Fi cameras are based on VLC."

setup(
    name="camera-lib",
    version=VERSION,  # Auto-generated timestamp version
    packages=find_packages(where='src'),  # This ensures proper package discovery
    package_dir={"": "camera"},  # Maps packages correctly under "src/"
    install_requires=[],  # Dependencies
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Adjust as needed
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify supported Python versions
)
