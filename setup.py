from setuptools import setup, find_packages
import os

setup(
    name="fotobox",
    version="1.0.0",
    description="Turn your Raspberry Pi into a photo booth with a web server.",
    author="Nick Hildebrandt",
    packages=find_packages(),
    include_package_data=True,
    data_files=[
        ('/etc/', ['config/fotobox.ini']),
        ('/etc/systemd/system/', ['config/fotobox.service']),
        ('/etc/hostapd/', ['config/hostapd.conf']),
        ('/etc/network/interfaces.d/', ['config/wlan0']),
        ('/etc/', ['config/dnsmasq.conf'])

    ],
    entry_points={
        'console_scripts': [
            'fotobox=fotobox.__main__:main',
        ],
    },
)
