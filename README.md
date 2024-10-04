# Fotobox

Welcome to the **Fotobox** project! This project transforms a Raspberry Pi into a fully functional photo booth with an integrated web server. You can use this for events, parties, or any occasion where capturing memories is fun and essential. The system uses buttons connected to the GPIO pins for controlling the photo booth, a Pi Camera to take the pictures, a lamp to simulate a flash, and a web server that allows you to view and download images over Wi-Fi.

## Equipment Needed
To set up the Fotobox project, you will need the following hardware:
- **Raspberry Pi** (any model with GPIO pins and camera support, e.g., Raspberry Pi 4)
- **Raspberry Pi Camera Module** (e.g., Pi Camera v2)
- **Multiple push buttons** for controlling the photo booth (e.g., one button for capture, another for shutdown)
- **Lamp and relay** to simulate a camera flash
- **GPIO pins** to connect the buttons and the lamp/flash
- **Display** to show the real-time camera preview
- **Wi-Fi** or Ethernet connection for web access
- **Power supply** for the Raspberry Pi
- **SD card** with Raspberry Pi OS installed

### GPIO Pin Layout
Here are the specific GPIO pin connections used in the project:
- **Capture button**: Connected to GPIO pin 16 (physical pin 36)
- **Power off button**: Connected to GPIO pin 17 (physical pin 11)
- **Relay**: Connected to GPIO pin 18 (physical pin 12)

## Installation

### Prerequisites
1. Install Raspberry Pi OS (preferably **Raspberry Pi OS Lite**) on your Raspberry Pi.
2. Connect the **Raspberry Pi Camera Module**.
3. Set up the necessary hardware as described in the GPIO layout section.

### Steps to Install Fotobox

1. **Install System Dependencies**:
    Update the package list and install the required system packages:
    ```bash
    sudo apt-get update
    sudo apt-get install python3-setuptools \
                         python3-gpiozero \
                         python3-picamera2 \
                         python3-pil \
                         python3-numpy \
                         dnsmasq \
                         hostapd
    ```

2. **Install the Fotobox Software**:
    Clone the repository and install the Fotobox Python package:
    ```bash
    git clone https://github.com/nickhildebrandt/fotobox.git
    cd fotobox
    sudo python3 setup.py install
    ```

3. **Configure and Start System Services**:
    After installing the software, configure the required services:
    ```bash
    sudo systemctl daemon-reload
    sudo systemctl enable dnsmasq.service
    sudo systemctl unmask hostapd.service
    sudo systemctl enable hostapd.service
    sudo systemctl enable fotobox.service
    ```

4. **Reboot**:
    The photobooth services will start automatically after the reboot.
    ```bash
    sudo reboot
    ```

### Configuration: `/etc/fotobox.ini`

Once installed, you need to configure the Fotobox settings in the `/etc/fotobox.ini` file. Here is a sample configuration:

```ini
[DEFAULT]
width = 1920
height = 1080
fontsize = 80
welcometext = Press the button
countdown = Ready?, set, Cheese
```
- `width`: The width of the preview display (in pixels).
- `height`: The height of the preview display (in pixels).
- `fontsize`: The font size used for the welcome message and countdown.
- `welcometext`: The message displayed on the screen when idle.
- `countdown`: A comma-separated list of countdown steps before the photo is captured.

### Accessing the Web Interface

Once the services are configured and running, the Raspberry Pi will create an open Wi-Fi network called Fotobox. You can connect to this network from any device with Wi-Fi.

After connecting to the Fotobox Wi-Fi, open a web browser and enter the following IP address to access the web interface:

`http://10.10.10.1`

You will be able to view and download the photos directly from this interface.

## Contributing

Contributions are welcome! If you have ideas for improvements or additional features, feel free to open an issue or submit a pull request. Whether it's hardware integration, additional software features, or simply refining the existing code, every contribution is appreciated.
