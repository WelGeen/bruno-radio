const knob = document.getElementById("knob");
const audio = document.getElementById("audio");
const lamp = document.getElementById("statusLamp");

let currentRotation = 0;
let isDragging = false;
let startAngle = 0;

function getAngle(x, y, centerX, centerY) {
  return Math.atan2(y - centerY, x - centerX) * (180 / Math.PI);
}

function startRotate(x, y) {
  const rect = knob.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  startAngle = getAngle(x, y, centerX, centerY);
  isDragging = true;
}

function doRotate(x, y) {
  if (!isDragging) return;

  const rect = knob.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  const angle = getAngle(x, y, centerX, centerY);
  let delta = angle - startAngle;

  if (delta > 180) delta -= 360;
  if (delta < -180) delta += 360;

  currentRotation += delta;

  knob.style.transform = `rotate(${currentRotation}deg)`;
  startAngle = angle;

  // Volume op basis van rotatie (0-360 graden => volume 0-1)
  const volume = Math.min(1, Math.max(0, currentRotation / 360));
  audio.volume = volume;
}

function stopRotate() {
  isDragging = false;
}

// Nieuwe variabele voor status
let isPlaying = false;


knob.addEventListener("click", () => {
  if (!isPlaying) {
    fetchAndPlaySequence('talk');
    isPlaying = true;
  } else {
    audio.pause();
    setLampStatus('off'); // Rood
    isPlaying = false;
  }
});

// Mouse
// Begin met draaien als muis boven knop komt
knob.addEventListener("mouseenter", e => {
  const rect = knob.getBoundingClientRect();
  const centerX = rect.left + rect.width / 2;
  const centerY = rect.top + rect.height / 2;
  startAngle = getAngle(e.clientX, e.clientY, centerX, centerY);
  isDragging = true;
});

// Stop met draaien als muis knop verlaat
knob.addEventListener("mouseleave", () => {
  isDragging = false;
});

document.addEventListener("mousemove", e => {
  doRotate(e.clientX, e.clientY);
});

document.addEventListener("touchmove", e => {
  const touch = e.touches[0];
  doRotate(touch.clientX, touch.clientY);
});
document.addEventListener("touchend", stopRotate);

// Spelerlogica
let currentPlaylist = [];
let currentIndex = 0;
let currentType = '';

function setLampStatus(status) {
  lamp.className = '';
  lamp.classList.add(status);
}


async function fetchStreamList(type) {
  const url = `stream.php?${type}`;
  const response = await fetch(url);
  const text = await response.text();

  try {
    const json = JSON.parse(text);
    return Array.isArray(json) ? json : [json];
  } catch (e) {
    return [url]; // fallback als het geen JSON is
  }
}

async function fetchAndPlaySequence(type) {
  currentType = type;
  setLampStatus('searching');  // Lamp knippert
  currentPlaylist = await fetchStreamList(type);
  currentIndex = 0;
  playCurrent();
}


function playCurrent() {
  if (!currentPlaylist[currentIndex]) {
    switch (currentType) {
      case 'talk': return fetchAndPlaySequence('music');
      case 'music': return fetchAndPlaySequence('stream');
      default: return;
    }
  }

  const url = currentPlaylist[currentIndex];
  audio.src = url;

  audio.play()
    .then(() => {
      setLampStatus('on');
    })
    .catch((err) => {
      console.warn("Stream failed, trying next:", url, err);
      // Probeer volgende stream
      currentIndex++;
      playCurrent();
    });
}



audio.addEventListener("ended", () => {
  currentIndex++;
  playCurrent();
});

audio.addEventListener("error", () => {
  console.warn("Audio error, skipping to next.");
  currentIndex++;
  playCurrent();
});

document.getElementById("nextBtn").addEventListener("click", () => {
  if (currentPlaylist.length > 0) {
    currentIndex = (currentIndex + 1) % currentPlaylist.length;
    playCurrent();
  }
});
document.getElementById("prevBtn").addEventListener("click", () => {
  if (currentPlaylist.length > 0) {
    currentIndex = (currentIndex - 1 + currentPlaylist.length) % currentPlaylist.length;
    playCurrent();
  }
});

document.getElementById("playPauseBtn").addEventListener("click", () => {
  if (audio.paused) {
    audio.play();
    setLampStatus('on');
    playPauseBtn.textContent = "Pause";
    isPlaying = true;
  } else {
    audio.pause();
    setLampStatus('off');
    playPauseBtn.textContent = "Play";
    isPlaying = false;
  }
});

