from setuptools import setup, find_packages

setup(
    name="thispackagedoesnotexist",
    version="0.4.5",
    packages=find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "python-socketio",
        "pyaudio",
        "requests",
        "websocket-client",
        "customtkinter",
        "psutil",
        "mss",
        "pillow",
        "opencv-python",
        "pywin32",
        "wmi"
    ],
)


