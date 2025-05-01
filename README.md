
### 📝 **Project Description (for a prototype)**

**“This project explores the design of an interactive radio prototype aimed at supporting people with dementia. The radio provides a simplified and familiar interface that reduces cognitive load, while offering comforting audio content through a sequence of talk, music, and stream sources. Its behavior is designed to be predictable and intuitive, including visual feedback and automated transitions between content types to help users stay engaged without complex interaction.”**

Zeker! Hier is een volledige en actuele **functie- en interface-lijst** van je interactieve radio-project, inclusief alle recente aanpassingen:


## 📻 **Radio Prototype V2 – Functionaliteitenoverzicht (versie 2)**

### 🎛️ **Draaiknop (volume control + toggle)**

- **Beweeg muis boven de knop** → je kunt draaien om het volume aan te passen.
- **Verlaat de knop** → draaien stopt.
- **Rotatie = visueel oneindig** (draait door boven 360°).
- **Volume wordt berekend op basis van rotatiehoek** (0–1 schaal).
- **Klik op de knop**:
  - Start de radio als die uit is (met `talk`-content).
  - Pauzeert de radio als die aan staat.

---

### 🎶 **Contentlogica & afspelen**

- Start met `talk`, daarna automatisch:
  - ➡️ `music`
  - ➡️ `stream`
- Per type wordt een JSON-array van URLs opgehaald (via `stream.php`).
- Elk item wordt automatisch afgespeeld, en bij einde wordt naar het volgende gegaan.
- Als een stream **fout geeft** (bv. Mixed Content of kapotte URL):
  - Wordt automatisch overgeslagen.
- Navigatie mogelijk met:
  - ⏮️ **PREV**-knop: naar vorig item
  - ⏭️ **NEXT**-knop: naar volgend item
  - ▶️/⏸️ **PLAY/PAUSE**-knop: pauzeer/hervat huidig item

---

### 💡 **Statuslampje (linksonder)**

Toont zowel **afspeelstatus** als **contenttype**:

| Speelstatus     | Kleur lampje | Gedrag        |
|-----------------|--------------|---------------|
| Uit             | 🔴 Rood       | Vast          |
| Speelt          | 🟢 Groen      | Vast          |
| Zoekt stream    | 🟡 Geel       | Knipperend    |

| Contenttype     | Randkleur lamp | Beschrijving     |
|-----------------|----------------|------------------|
| talk            | Oranje          | Spreekinhoud     |
| music           | Lime            | Muziekstreams    |
| stream          | Lichtblauw      | Externe streams  |

---

### 📃 **Afspeellijst (bovenaan zichtbaar)**

- Bovenin de pagina staat een lijst (`<ul>`) van alle streams in de huidige afspeellijst.
- Huidige item wordt:
  - ✅ **Vetgedrukt**
  - ✅ **Groen gekleurd**

---

### 🖱️ **Bedieningsknoppen (iconen)**

- ⏮️ **Prev**: vorige item in lijst  
- ▶️ / ⏸️ **Play/Pause**: toggle afspelen  
- ⏭️ **Next**: volgende item in lijst  

(Play-knop wisselt automatisch tussen `▶` en `⏸`)

---

### 💻 **Layout / Styling**

- Container (`#container`) heeft ronde bovenhoeken (50vmin) en strakke onderhoeken (2vmin).
- Volume-slider en stopknop zijn **verwijderd** (niet meer nodig).



| Status         | Lampje            | Gedrag       |
|----------------|-------------------|--------------|
| **Zoekt stream** | Geel (knipperend) | Tijdens `fetch()` |
| **Speelt af**    | Groen             | Tijdens afspelen  |
| **Radio uit**    | Rood              | Na pauze of stoppen  |

