from setuptools import setup, find_packages

setup(
    name="thispackagedoesnotexist",
    version="0.3.8",
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "customtkinter",
        "requests",
        "WMI",
        "PyAudio",
        "pillow",
        "opencv-python",
        "psutil",
        "websockets",
        "websocket-client",
        "mss"
    ],
)


