
### 📝 **Project Description (for a prototype)**

**“This project explores the design of an interactive radio prototype aimed at supporting people with dementia. The radio provides a simplified and familiar interface that reduces cognitive load, while offering comforting audio content through a sequence of talk, music, and stream sources. Its behavior is designed to be predictable and intuitive, including visual feedback and automated transitions between content types to help users stay engaged without complex interaction.”**


## 🎛️ **Draaiknop (knob)**

- **Draaien = volumeregeling**
  - Zodra de muis boven de knop komt (`mouseenter`), wordt draaien geactiveerd.
  - Zolang de muis erboven blijft, kan er worden gedraaid.
  - Bij verlaten van de knop (`mouseleave`) stopt het volume-aanpassen.
  - De knop **draait visueel eindeloos door** (geen reset bij 360°).
  - Volume is altijd tussen 0 en 1 op basis van het aantal graden rotatie.

- **Klikken op de knop = aan/uit toggle**
  - Als de radio **uit staat**, start deze met het afspelen van een streamlijst van type `'talk'`.
  - Als de radio **aan staat**, pauzeert hij de audio en schakelt de radio uit.

---

## 📻 **Streamlogica**

1. Bij inschakelen (via knop-klik):
   - **Laadt streams van type `'talk'`**
   - Speelt deze één voor één af.
   - Als de lijst is afgespeeld → automatisch door naar `'music'`.
   - Na `'music'` → automatisch door naar `'stream'`.

2. **Mixed Content (HTTP in HTTPS) wordt opgevangen**
   - Als een stream geblokkeerd wordt (bv. geen HTTPS), wordt deze automatisch overgeslagen.
   - Audio gaat dan door naar de volgende stream in de lijst.

3. **Bij audiofouten (404, timeouts, etc.)**
   - Automatisch door naar volgende item in de lijst.

---

## 🎚️ **Knoppen en bediening**

- **Play-knop**:
  - Pauzeert/hervat de huidige stream (toggle).
  - Label verandert naar "Pause"/"Play".

- **Next/Prev-knoppen**:
  - Navigeren door de huidige lijst van streams (indien beschikbaar).

- **Stop-knop en volume-slider zijn verwijderd**:
  - Stoppen gebeurt via knopklik.
  - Volume wordt nu uitsluitend met de draaiknop geregeld.

---

## 💡 **Statuslampje (indicator links onder)**

Toont de **status van de radio**:

| Status         | Lampje            | Gedrag       |
|----------------|-------------------|--------------|
| **Zoekt stream** | Geel (knipperend) | Tijdens `fetch()` |
| **Speelt af**    | Groen             | Tijdens afspelen  |
| **Radio uit**    | Rood              | Na pauze of stoppen  |

