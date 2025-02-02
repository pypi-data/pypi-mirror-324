from setuptools import setup, find_packages

setup(
    name="camera-lib",
    version="0.1.0",  # Update the version as needed
    packages=find_packages(where='.'),  # This will include the camera package and its submodules
    install_requires=[],  # Add any dependencies you might have
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Use the license you're applying
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Specify the Python versions your package supports
)
