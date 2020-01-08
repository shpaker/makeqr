import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wifi_qrcode",
    version="1.0.0",
    author="Aleksandr Shpak",
    author_email="shpaker@gmail.com",
    description="Generate WiFi Access QR Codes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['fire>=0.2.1', 'qrcode[pil]>=6.1'],
    url="https://github.com/shpaker/wifi_qrcode",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Topic :: Communications',
    ],
    entry_points={'console_scripts': [
        'wifi_qrcode=wifi_qrcode.app:main',
    ]})
