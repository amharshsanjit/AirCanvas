# AirCanvas
"Draw in the air. Create without limits." ✨
## 🧠 Code Overview

This project uses computer vision + hand tracking to enable real-time air drawing using a webcam 🎥✨

---

## ✋ Hand Detection

- Uses MediaPipe to detect and track hand landmarks in real-time  
- Extracts key finger points from each frame 🧩  
- Works efficiently for single-hand tracking  

---

## 🤌 Gesture Recognition

- Finger tip indices used: `[8, 12, 16, 20]`  
- Gestures are detected by comparing finger positions:

| Gesture | Action |
|--------|--------|
| ☝️ 1 Finger | Drawing ✍️ |
| ✌️ 2 Fingers | Eraser 🧽 |
| 🤟 3 Fingers | Change Color 🎨 |
| 🖐️ 4+ Fingers | Pause ⏸️ |

---

## 🎨 Drawing System

- Uses OpenCV to create a virtual canvas  
- Smooth lines are drawn by connecting previous & current finger positions  
- Canvas is merged with live webcam feed 🔄  

---

## 🧽 Eraser Functionality

- Erasing is done by drawing black circles ⚫ on the canvas  
- Eraser size is configurable using `ERASER_RADIUS`  
- Provides smooth and natural erase experience  

---

## 🔵 Circle Detection

- Tracks finger movement points over time 📍  
- Detects circular patterns using:
  - Center (mean of points)  
  - Distance variance threshold  
- Automatically converts rough circle → perfect circle ⭕✨  

---

## 🌈 Color Handling

- Supports multiple colors: **Red, Green, Blue, Cyan** 🎨  
- Colors switch dynamically using gesture control  
- Displays current color indicator on screen 🟥🟩🟦  

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| ESC | Exit 🚪 |
| C | Clear Canvas 🧹 |
