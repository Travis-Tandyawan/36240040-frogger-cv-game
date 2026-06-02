# 🐸 Frogger CV - Gesture Controlled Arcade Game

Sebuah reka ulang (remake) dari game arcade klasik "Frogger", di mana pemain mengendalikan karakter menggunakan **pergerakan ujung jari telunjuk secara real-time (Computer Vision)**, bukan menggunakan keyboard atau controller.

Proyek ini dibangun menggunakan Python dan mengimplementasikan *Natural User Interface* (NUI) dengan membaca landmark tangan manusia.

## 🚀 Fitur Utama
* **Index Finger Tracking**: Mendeteksi dan melacak pergerakan ujung jari telunjuk (Landmark 8) menggunakan kecerdasan buatan.
* **Win State & Auto-Reset**: Dilengkapi layar kemenangan ("KAMU MENANG!") dan *timer* 3 detik untuk mengulang permainan secara otomatis bergaya mesin *arcade*.
* **Dynamic Grid Movement**: Pemetaan gerakan (Maju, Mundur, Kiri, Kanan) yang sejajar dan presisi ke sistem petak (grid) game 2D.
* **Anti-Jitter Mechanism**: Menggunakan sistem "Anchor & Neutral Zone" untuk mencegah lompatan ganda yang tidak disengaja.

## 🛠️ Teknologi yang Digunakan
* **Python 3.x**
* **OpenCV**: Untuk penangkapan *frame* dari webcam dan manipulasi gambar matriks.
* **MediaPipe**: Model *Machine Learning* ringan dari Google untuk pelacakan titik *landmark* tangan.
* **Pygame**: *Engine* utama untuk render grafis 2D, deteksi kolisi (tabrakan), dan logika *game loop*.

## 📥 Cara Instalasi dan Bermain (Untuk Developer)
1. *Clone* repositori ini:
   ```bash
   git clone [https://github.com/Travis-Tandyawan/frogger-cv-game.git](https://github.com/Travis-Tandyawan/frogger-cv-game.git)
2. Buat Virtual Environment (opsional tapi direkomendasikan) dan instal dependensi:
   ```Bash
   pip install opencv-python mediapipe==0.10.14 pygame
3. Jalankan Game
   ```Bash
   python main.py

🎮 Kontrol (Gerakan Tangan)
Game ini menggunakan sistem Sentakan (Flick) berbasis titik tengah (Netral).
1. Angkat jari telunjuk Anda ke depan kamera hingga lingkaran merah (titik tengah/netral) muncul.
2. MAJU: Sentakkan jari ke atas melewati lingkaran merah, lalu segera kembalikan jari ke lingkaran merah.
3. MUNDUR: Sentakkan jari ke bawah, lalu kembalikan ke tengah.
4. KIRI/KANAN: Sentakkan jari ke kiri/kanan, lalu kembalikan ke tengah.
5. Seberangi jalan raya dan sungai hingga mencapai garis finish di paling atas untuk memenangkan permainan!

