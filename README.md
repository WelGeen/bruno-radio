# 🎵 Bruno Box – Dementia-Friendly Interactive Radio (Prototype v8)

This project explores the design of an **interactive radio prototype** aimed at supporting **people with dementia**. The device offers a **simple, intuitive, and familiar interface** that lowers cognitive load while providing **comforting audio content** in a structured sequence: talk → music → stream.

It uses a **Raspberry Pi 4** with physical controls, LED feedback, and dynamic audio playlists sourced online. The behavior is predictable, offering **hands-on interaction** through rotary encoders and push buttons, as well as a **web-based simulation** for prototyping and testing.

---

## 🧠 Key Goals

- Reduce cognitive load through a **clear sequence** and **consistent visual feedback**
- Avoid complex UI: interaction is limited to a **rotary knob** and **three buttons**
- Support **autonomy and engagement** without menus or screens
- Provide content types that are emotionally supportive and easy to listen to

---

## 💻 Web Simulation Features (Prototype Logic)

These features are also mirrored in the physical Raspberry Pi version.

### 🎛️ Rotary Knob (Volume Control + Toggle)

- **Rotate knob** to adjust volume (0–1 scale)
- **Click the knob**:
  - Starts playback with `talk` content if off
  - Toggles play/pause if already playing

### 🎶 Content Playback Logic

- Starts with `talk`, then automatically moves to:
  - ➡️ `music`
  - ➡️ `stream`
- Each type is fetched via a playlist (`.json`) from the web
- Automatically skips broken or invalid stream URLs

### ⏮️⏯️⏭️ Button Controls

- ⏮️ **Prev**: Previous track
- ⏯️ **Play/Pause**: Toggle playback
- ⏭️ **Next**: Next track

### 💡 Visual Feedback (LED Behavior)

| Playback Status   | Center LED Color | Behavior     |
|-------------------|------------------|--------------|
| Stopped/Idle      | 🔴 Red           | Solid        |
| Playing           | 🟢 Green         | Solid        |
| Searching Stream  | 🟡 Yellow        | Blinking     |

| Content Type | Ring/Frame Color | Description     |
|--------------|------------------|-----------------|
| `talk`       | Orange           | Voice/spoken    |
| `music`      | Lime             | Music tracks    |
| `stream`     | Light Blue       | External streams|

---

## 📦 Raspberry Pi 4 – Physical Prototype

### 🧰 Hardware Requirements

- Raspberry Pi 4 (Raspberry Pi OS)
- Rotary encoder (e.g., KY-040)
- 3 push buttons (Play, Next, Previous)
- 1 push button (Reset)
- RGB LED (PWM capable)
- USB DAC or 3.5mm headphone output

### 🧪 GPIO Pinout

| Function        | GPIO Pin | Description        |
|-----------------|----------|--------------------|
| Rotary A (CLK)  | 27       | Rotary encoder A   |
| Rotary B (DT)   | 17       | Rotary encoder B   |
| Rotary Button   | 22       | Reset button       |
| Play Button     | 23       | Play/Pause toggle  |
| Next Button     | 24       | Next track         |
| Prev Button     | 12       | Previous track     |
| LED Red         | 5        | PWM Red            |
| LED Green       | 6        | PWM Green          |
| LED Blue        | 13       | PWM Blue           |

🖥️ Software Installation
Step 1: Install dependencies
bash
Copy
Edit
sudo apt update
sudo apt install -y python3 python3-pip mpg123 ffmpeg
sudo pip3 install gpiozero requests
Step 2: Clone or copy the script
Save the file to e.g. /home/jurgen/Desktop/bruno_box_v8.py

▶️ Run the Script
bash
Copy
Edit
cd /home/jurgen/Desktop
python3 bruno_box_v8.py
🔁 Run on Startup (via crontab)
To run the script automatically on boot:

Open the root crontab:

bash
Copy
Edit
sudo crontab -e
Add the following line at the bottom:

bash
Copy
Edit
@reboot /usr/bin/python3 /home/jurgen/Desktop/bruno_box_v8.py >> /home/jurgen/bruno_log.txt 2>&1 &
Reboot to test:

bash
Copy
Edit
sudo reboot
🌐 Internet & Playlist Logic
The script waits for a working Wi-Fi connection before starting

It fetches playlists dynamically from:

arduino
Copy
Edit
https://chrisgeene.nl/bruno/stream.php
.mp4 files are automatically downloaded and converted to .mp3 via ffmpeg

Files are cached temporarily in /tmp/

🎛️ Physical Controls Summary
🔘 Rotary encoder: volume up/down

⏯️ Play button (GPIO 23): start/pause

⏮️ Prev button (GPIO 12): previous track

⏭️ Next button (GPIO 24): skip track

🔄 Reset button (GPIO 22): reset to first playlist

🌈 RGB LED: reflects current mode and state

🧹 Optional: Clean up temporary audio files
To avoid storage bloat:

bash
Copy
Edit
rm /tmp/*.mp3 /tmp/*.mp4
🛠️ Troubleshooting
No sound? Test manually:

bash
Copy
Edit
mpg123 -a hw:2,0 test.mp3
No Wi-Fi? Ensure DNS and Wi-Fi are active before script starts

Buttons not working? Check GPIO wiring and pinout

ffmpeg errors? Make sure your Pi has enough free space and permissions

📜 License
MIT License — free to use, adapt, remix or contribute.
Feel free to submit issues or pull requests.
