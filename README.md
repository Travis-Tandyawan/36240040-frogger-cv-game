FROGGER CV - MOTION CONTROLLED GAME

Version     : 1.0.0
Language    : Python 3.x
Category    : Computer Vision / Interactive Gaming
Framework   : Pygame, OpenCV, Google MediaPipe

PROJECT OVERVIEW
Project ini merupakan modernisasi dari game klasik Frogger 
dengan mengimplementasikan teknologi Computer Vision. 
Alih-alih menggunakan keyboard, pemain mengontrol karakter 
katak menggunakan gestur pergerakan tangan di depan webcam 
secara real-time.

Fitur Utama:
1. Hand Tracking Tracking
   - Menggunakan MediaPipe untuk mendeteksi landmark 
     tangan, khususnya jari telunjuk (Index Finger).
2. Procedural Animation
   - Animasi arus air sungai yang di-render secara prosedural.
3. Linear Interpolation (Lerp)
   - Pergerakan katak yang halus antar-koordinat (snap-to-grid).
4. Collision Detection
   - Deteksi tabrakan presisi dengan mobil dan logika pijakan 
     di atas batang kayu/daun teratai.

GAME OBJECTIVE
Tujuan Frogger CV adalah:
- Menyeberangi jalan raya bawah yang padat kendaraan.
- Melompat dari satu pijakan ke pijakan lain di sungai.
- Menyeberangi jalan raya atas yang memiliki mobil cepat.
- Mencapai garis finish (tebing rumput hijau) dengan selamat.
- Menggunakan gestur sentakan jari untuk melompat.

PROJECT ARCHITECTURE
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
|    Game Controller    | <- Menerjemahkan jarak ke perintah gerak
+-----------+-----------+
            |
    +-------+-------+
    |               |
    v               v
 Frogger State   Obstacle State
    |               |
    +-------+-------+
            | (Update & Draw)
            v
+-----------------------+
|     Pygame Engine     | <- Visualisasi & Audio
+-----------------------+

DIRECTORY STRUCTURE
FROGGER_CV
│
├── assets/
│   ├── cars_sheet.png
│   ├── frogs_sheet.png
│   ├── hit.wav
│   ├── jump.ogg
│   ├── lose.ogg
│   └── win.wav
│
├── main.py
├── README.md
└── requirements.txt
```

QUICK START
Menjalankan game dari source code:
python main.py

*Catatan: Pastikan webcam laptop/komputer tidak sedang
digunakan oleh aplikasi lain (seperti Zoom/Meet) saat 
menjalankan game ini.

COMPUTER VISION EXECUTION
Cara mengontrol karakter (Pengganti Keyboard):

1. Titik Netral (Anchor):
   Angkat jari telunjuk ke depan kamera hingga terdeteksi
   oleh sistem (ditandai dengan munculnya lingkaran merah).

2. Trigger Gerakan (Threshold):
   Sentakkan jari telunjuk menjauhi titik merah sejauh > 40 piksel.
   - Atas   : Melompat Maju
   - Bawah  : Melompat Mundur
   - Kiri   : Melompat Kiri
   - Kanan  : Melompat Kanan

3. Reset State:
   Kembalikan jari ke dalam radius titik merah (< 20 piksel)
   agar sistem siap menerima perintah lompatan berikutnya.

PERFORMANCE EVALUATION
Metrik evaluasi sistem game ini meliputi:
- FPS (Frames Per Second) dibatasi stabil pada 30 FPS.
- Latency deteksi MediaPipe pada RGB frame conversion.
- Keakuratan snap-to-grid (Magnet System) saat katak 
  mendarat di objek dinamis (batang kayu bergerak).

DEBUGGING
Kamera tidak menyala (Crash/Error):
- Pastikan indeks kamera di kode (cv2.VideoCapture(0)) 
  sudah sesuai. Ubah angka 0 menjadi 1 atau 2 jika 
  menggunakan webcam eksternal.

Suara tidak keluar:
- Pastikan ekstensi file di folder assets sesuai dengan
  yang didaftarkan di source code (.ogg atau .wav).

COMPUTER VISION CONCEPT
Sistem kendali menggunakan kalkulasi jarak Euclidean 
sederhana pada koordinat layar:

Δx = cx - anchor_x
Δy = cy - anchor_y

Dimana:
cx, cy = Posisi absolut jari telunjuk saat ini.
anchor_x, anchor_y = Posisi awal (netral) saat jari diangkat.
Threshold lompatan dieksekusi jika |Δx| > 40 atau |Δy| > 40.

FUTURE IMPROVEMENTS
Beberapa pengembangan yang direkomendasikan:

[GAMEPLAY]
- Menambahkan sistem Skor, Waktu mundur (Timer), dan Nyawa.
- Penambahan jenis rintangan baru (misal: buaya di sungai).
[ANALYTICS]
- Mengumpulkan dataset riwayat pergerakan landmark tangan pemain untuk mengevaluasi dan melatih model prediktif guna mendeteksi tingkat kelelahan (fatigue) atau penurunan akurasi berdasarkan perubahan pola kecepatan gestur.
[ENGINEERING]
- Pemisahan (Refactoring) kode menjadi struktur Object-Oriented 
  Programming (OOP) Class untuk Modul Player, Modul Rintangan, 
  dan Modul Kamera.

SYSTEM REQUIREMENTS
Minimum:
CPU      : Prosesor Dual Core 2.0 GHz
RAM      : 4 GB
Python   : 3.8+
Hardware : Webcam Terintegrasi / Eksternal

Recommended:
CPU      : Prosesor Quad Core 2.5 GHz atau lebih baru
RAM      : 8 GB
Python   : 3.10+
Hardware : Webcam 720p 30fps untuk deteksi gerakan optimal

REFERENCES
- Pygame Documentation (https://www.pygame.org/docs/)
- Google MediaPipe Solutions (Hand Tracking)
- OpenCV Python Tutorials

LICENSE
Personal / Academic Project

AUTHOR
Project : Frogger CV Interactive Game  
Purpose : Computer Vision Game Implementation  
Name    : Travis
