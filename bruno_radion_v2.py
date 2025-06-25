from gpiozero import Button, RotaryEncoder, PWMLED
from signal import pause
import subprocess
import requests
import os
import time
import urllib.request
import hashlib
import socket

def is_connected():
    try:
        # We proberen een socketverbinding te maken met Google's DNS-server
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

print("Wachten op WiFi-verbinding...")

# Blijf proberen tot we verbinding hebben
while not is_connected():
    print("Geen WiFi, opnieuw proberen in 3 seconden...")
    time.sleep(3)

print("WiFi-verbinding gevonden. Script gaat verder.")
# WiFi-verbinding gevonden. Script gaat verde

# GPIO-knoppen met debounce:
reset_btn = Button(22, bounce_time=0.1)  # Drukknop op encoder

play_btn = Button(23, bounce_time=0.1)
next_btn = Button(24, bounce_time=0.1)
prev_btn = Button(12, bounce_time=0.1)  # nieuwe knop
encoder = RotaryEncoder(a=27, b=17, max_steps=0)      # CLK = 27, DT = 17

# Kleuren
led_r = PWMLED(5)
led_g = PWMLED(6)
led_b = PWMLED(13)

kleurwaarden = {
    "talk": (0, 1, 0),       # groen
    "music": (0, 0, 1),      # blauw
    "stream": (1, 0.5, 0),   # oranje
    "idle": (1, 0, 0),       # rood
}


os.system("pkill mpg123")

afspelen = False
huidige_track = 0
playlist = []
alle_playlists = ["talk", "music", "stream"]
playlist_index = 0
mpg123_proc = None


def convert_mp4_to_audio(input_url, output_format="mp3"):
    try:
        # Hash op basis van de URL
        url_hash = hashlib.md5(input_url.encode()).hexdigest()
        local_filename = f"/tmp/{url_hash}.mp4"
        output_path = f"/tmp/{url_hash}.{output_format}"

        # Als bestand al bestaat, overslaan
        if os.path.exists(output_path):
            print(f"✅ Bestaat al, sla over: {output_path}")
            return output_path

        # Downloaden
        print("⬇️ Downloaden:", input_url)
        urllib.request.urlretrieve(input_url, local_filename)

        # Converteren
        subprocess.run(
            ["ffmpeg", "-y", "-i", local_filename, output_path],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        print(f"🎧 Omgezet naar: {output_path}")
        return output_path
    except Exception as e:
        print("❌ Fout bij conversie:", e)
        return None


def haal_playlist_op(content_type):
    try:
        response = requests.get(f"https://xxxxx?{content_type}")
        if response.status_code == 200:
            data = response.json()
            print(f"\n🎧 Playlist '{content_type}' opgehaald ({len(data)} tracks):")
            nieuwe_playlist = []

            for i, track_url in enumerate(data, start=1):
                print(f"  {i}. {track_url}")
                if track_url.endswith(".mp4"):
                    geconverteerd_pad = convert_mp4_to_audio(track_url, "mp3")
                    if geconverteerd_pad:
                        nieuwe_playlist.append(geconverteerd_pad)
                else:
                    nieuwe_playlist.append(track_url)

            return nieuwe_playlist
        else:
            print("Fout bij ophalen:", response.status_code)
            return []
    except Exception as e:
        print("Fout bij ophalen:", e)
        return []


def speel_track(url):
    global mpg123_proc, huidige_track

    print(f"▶️ Spelen: {url}")
    mpg123_proc = subprocess.Popen(
        ["mpg123", "-a", "hw:2,0", "-R"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True
    )
    mpg123_proc.stdin.write(f"LOAD {url}\n")
    mpg123_proc.stdin.flush()

    while True:
        output = mpg123_proc.stdout.readline()
        if output.startswith("@P 0"):  # einde afspelen
            print("✅ Track afgelopen.")
            huidige_track += 1
            break
        elif output == "":
            break

def play_pause():
    global afspelen, mpg123_proc

    if mpg123_proc:
        try:
            mpg123_proc.stdin.write("P\n")
            mpg123_proc.stdin.flush()
            afspelen = not afspelen
            print("⏯️ Pauze-toggle:", "▶️ Spelen" if afspelen else "⏸️ Pauze")
        except Exception as e:
            print("❌ Pauze mislukt:", e)

def volgende_track():
    global huidige_track, mpg123_proc
    if mpg123_proc:
        try:
            mpg123_proc.stdin.write("Q\n")
            mpg123_proc.stdin.flush()
        except:
            pass
    huidige_track += 1
    print("⏭️ Naar volgende track...")

def vorige_track():
    global huidige_track, mpg123_proc
    if mpg123_proc:
        try:
            mpg123_proc.stdin.write("Q\n")
            mpg123_proc.stdin.flush()
        except:
            pass
    if huidige_track > 0:
        huidige_track -= 1
        print("⏮️ Naar vorige track...")
    else:
        print("⏮️ Je bent al bij het begin van de playlist.")
        
def volume_omhoog():
    subprocess.run(["amixer", "sset", "Master", "2%+"], stdout=subprocess.DEVNULL)
    print("🔊 Volume omhoog")

def volume_omlaag():
    subprocess.run(["amixer", "sset", "Master", "2%-"], stdout=subprocess.DEVNULL)
    print("🔉 Volume omlaag")

def reset_app():
    global huidige_track, mpg123_proc, afspelen, playlist_index,alle_playlists
    afspelen = False
    
    if mpg123_proc:
        try:
            mpg123_proc.stdin.write("Q\n")
            mpg123_proc.stdin.flush()
        except:
            pass
        
    huidige_track = 0
    playlist_index = 0
    time.sleep(0.5)
    print("⏭️ Naar begin...")
    

def wacht_op_knoppen():
    reset_btn.when_pressed = reset_app
    play_btn.when_pressed = play_pause
    next_btn.when_pressed = volgende_track
    prev_btn.when_pressed = vorige_track
    encoder.when_rotated_counter_clockwise = volume_omlaag
    encoder.when_rotated_clockwise = volume_omhoog
    
def set_led_kleur(r, g, b):
    led_r.value = r
    led_g.value = g
    led_b.value = b

def knipper_kleur(r, g, b, duur=1.5):
    set_led_kleur(r, g, b)
    time.sleep(0.2)
    set_led_kleur(0, 0, 0)
    time.sleep(0.2)
    set_led_kleur(r, g, b)
    time.sleep(0.2)
    set_led_kleur(0, 0, 0)
    time.sleep(0.2)

def hoofdloop():
    global playlist, huidige_track, playlist_index, kleurwaarden, alle_playlists
    
    print(f"▶️ playlist_index: {playlist_index}")
    print(f"▶️ alle_playlists: {alle_playlists}")
    while playlist_index < len(alle_playlists):
        content_type = alle_playlists[playlist_index]
        print(f"▶️ content_type: {content_type}")
        rgb = kleurwaarden.get(content_type, kleurwaarden["idle"])
        # tijdelijk knipperen om aan te geven dat er geladen wordt
        knipper_kleur(*rgb)
        # zet vaste kleur na knipperen
        set_led_kleur(*rgb)

        playlist = haal_playlist_op(content_type)
        huidige_track = 0
        
        while huidige_track < len(playlist):
            if reset_btn.is_pressed:
                reset_app()
                return  # break out of current loop
            speel_track(playlist[huidige_track])

        playlist_index += 1

    print("✅ Alle playlists afgespeeld.")

# Start
rgb = kleurwaarden.get("idle")
# tijdelijk knipperen om aan te geven dat er geladen wordt
knipper_kleur(*rgb)
 # zet vaste kleur na knipperen
set_led_kleur(*rgb)

wacht_op_knoppen()
print("🕹️ Druk op Play (GPIO 23) of Reset (GPIO 22) om te starten...")

# Wacht tot een van de twee knoppen wordt ingedrukt
while True:
    if play_btn.is_pressed or reset_btn.is_pressed:
        break
    time.sleep(0.1)

# Eventuele visuele feedback
knipper_kleur(*kleurwaarden["talk"])
print("🟢 Start hoofdloop...")
hoofdloop()


