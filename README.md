## FROGGER CV

Aplikasi ini sudah di-build menjadi `.exe`.

Silakan unduh file aplikasi siap pakainya di menu **Releases** yang ada di sebelah kanan, atau klik tautan langsung di bawah ini:

👉 **[https://github.com/Travis-Tandyawan/36240040-frogger-cv-game/releases/tag/v1.0.0]**

## PROJECT OVERVIEW  
Project ini merupakan modernisasi dari game klasik Frogger dengan mengimplementasikan teknologi Intelligent System dan Computer Vision.  
Alih-alih menggunakan keyboard, pemain mengontrol karakter katak menggunakan gestur pergerakan tangan di depan webcam secara real-time, dilengkapi dengan musuh AI berbasis A* dan penyesuaian kesulitan sistem Fuzzy.

## Fitur Utama:
1. Hand Tracking (Computer Vision)
   - Menggunakan MediaPipe untuk mendeteksi landmark jari telunjuk (Index Finger) sebagai penggerak karakter.
2. AI Predator (A* Search Algorithm)
   - Musuh (Elang) diprogram menggunakan algoritma A* untuk bernavigasi secara cerdas mengejar posisi pemain.
3. Dynamic Difficulty Adjustment (Fuzzy Logic)
   - Kesulitan permainan (kecepatan rintangan) disesuaikan secara otomatis menggunakan sistem pakar Fuzzy berdasarkan performa pemain.
4. Machine Learning Telemetry
   - Sistem otomatis mencatat data perilaku pemain ke telemetri_pemain.csv sebagai dataset untuk pemodelan eksperimen Machine Learning (CART).
5. Linear Interpolation (Lerp)
   - Pergerakan karakter yang halus dan responsif antar-koordinat grid.

## GAME OBJECTIVE
Tujuan Frogger CV adalah:
- Menyeberangi jalan raya bawah yang padat kendaraan.
- Melompat dari satu pijakan ke pijakan lain di sungai.
- Menyeberangi jalan raya atas dengan kecepatan rintangan yang menyesuaikan level kesulitan.
- Mencapai garis finish (tebing rumput hijau) dengan selamat sebelum tertangkap Elang.

## PROJECT ARCHITECTURE
```
+-----------------------+
|    Webcam Input       |
+-----------+-----------+
            | (Frames)
            v
+-----------------------+
|  OpenCV & MediaPipe   | <- Hand Landmark Detection (Landmark 8)
+-----------+-----------+
            | (X, Y Coordinates)
            v
+-----------------------+
|   Game Controller     | <- Menerjemahkan jarak ke perintah gerak
+-----------+-----------+
            |
    +-------+-------+
    |               |
    v               v
 Frogger State   AI & Fuzzy State <- (A* & Fuzzy Logic Engine)
    |               |
    +-------+-------+
            | (Update & Draw)
            v
+-----------------------+
|     Pygame Engine     | <- Visualisasi, Audio, & Data Logging
+-----------------------+
```
## DIRECTORY STRUCTURE
FROGGER_CV
```
│
├── assets/
│   ├── cars_sheet.png
│   ├── elang.png
│   ├── frogs_sheet.png
│   ├── hit.wav
│   ├── jump.ogg
│   ├── lose.ogg
│   └── win.wav
│
├── main.py
├── telemetri_pemain.csv
├── README.md
└── requirements.txt
```

## QUICK START
Menjalankan game dari source code:
python main.py

*Catatan: Pastikan webcam laptop/komputer tidak sedang digunakan oleh aplikasi lain saat menjalankan game ini.

## COMPUTER VISION EXECUTION
Cara mengontrol karakter:  
1. Titik Netral (Anchor): Angkat jari telunjuk ke depan kamera hingga terdeteksi (muncul titik merah).  
2. Trigger Gerakan (Threshold): Sentakkan jari menjauhi titik merah sejauh > 40 piksel.
- Atas   : Melompat Maju  
- Bawah  : Melompat Mundur  
- Kiri   : Melompat Kiri  
- Kanan  : Melompat Kanan  
3. Reset State: Kembalikan jari ke dalam radius titik merah (< 20 piksel) untuk lompatan berikutnya.

## PERFORMANCE EVALUATION
Metrik evaluasi sistem game ini meliputi:
- Game Performance: FPS stabil pada 30 FPS.
- AI Performance: Efisiensi jalur A* dalam navigasi.
- ML Data: Data log (Gerakan, Jarak, Waktu Survive) untuk evaluasi performa model regresi menggunakan R-squared, MSE, dan MAE.

## FUTURE IMPROVEMENTS
Beberapa pengembangan yang direkomendasikan:
- Penambahan sistem Skor dan Timer.
- Integrasi model prediktif Machine Learning langsung ke dalam game untuk simulasi tingkat kesulitan yang lebih kompleks.

## SYSTEM REQUIREMENTS
Minimum:  
CPU      : Prosesor Dual Core 2.0 GHz  
RAM      : 4 GB  
Python   : 3.8+  
Hardware : Webcam Terintegrasi / Eksternal

## Recommended:
CPU      : Prosesor Quad Core 2.5 GHz atau lebih baru  
RAM      : 8 GB  
Python   : 3.10+  
Hardware : Webcam 720p 30fps untuk deteksi gerakan optimal

## AUTHOR
Project : Frogger CV Intelligence Game  
Purpose : Machine Learning for Intelligent System Project   
Name    : Travis Tandyawan (36240040)
