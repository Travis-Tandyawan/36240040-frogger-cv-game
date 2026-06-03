import cv2
import mediapipe as mp
import pygame
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# 1. PERSIAPAN GAME (PYGAME)
pygame.init()
pygame.font.init()
pygame.mixer.init() 
lebar_layar, tinggi_layar = 800, 600
layar = pygame.display.set_mode((lebar_layar, tinggi_layar))
pygame.display.set_caption("Frogger CV - Final Version")
clock = pygame.time.Clock()

posisi_awal_x = 400
posisi_awal_y = 540
kodok_x = posisi_awal_x
kodok_y = posisi_awal_y
ukuran_kodok = 40
jarak_lompat = 40

# ANIMATION LOMPAT HALUS
target_x = posisi_awal_x
target_y = posisi_awal_y
is_jumping = False
kecepatan_lompat = 10  

status_game = "MENU" 
waktu_menang = 0
waktu_kalah = 0
suara_lose_diputar = False

font_judul = pygame.font.SysFont("Arial", 60, bold=True)
font_sedang = pygame.font.SysFont("Arial", 30, bold=True)
font_kecil = pygame.font.SysFont("Arial", 18)

# ASET KATAK DENGAN SISTEM AUTO-CENTER
lokasi_sheet_kodok = resource_path(os.path.join("assets", "frogs_sheet.png"))
sheet_kodok = pygame.image.load(lokasi_sheet_kodok).convert_alpha()
lebar_kodok_potong = sheet_kodok.get_width() // 6

frame_mentah = sheet_kodok.subsurface(pygame.Rect(0, 0, lebar_kodok_potong, sheet_kodok.get_height()))
batas_kodok = frame_mentah.get_bounding_rect()
kodok_padat = frame_mentah.subsurface(batas_kodok)

rasio = min(36 / kodok_padat.get_width(), 36 / kodok_padat.get_height())
dim_baru = (max(1, int(kodok_padat.get_width() * rasio)), max(1, int(kodok_padat.get_height() * rasio)))
kodok_skala = pygame.transform.scale(kodok_padat, dim_baru)

gambar_kodok = pygame.Surface((ukuran_kodok, ukuran_kodok), pygame.SRCALPHA)
offset_x = (ukuran_kodok - kodok_skala.get_width()) // 2
offset_y = (ukuran_kodok - kodok_skala.get_height()) // 2
gambar_kodok.blit(kodok_skala, (offset_x, offset_y))

# Aset Mobil
lokasi_sheet_mobil = resource_path(os.path.join("assets", "cars_sheet.png"))
sheet_mobil = pygame.image.load(lokasi_sheet_mobil).convert_alpha()
w_potong = sheet_mobil.get_width() // 2
h_potong = sheet_mobil.get_height() // 2
lebar_mobil = 80
tinggi_mobil = 40

mobil_1 = pygame.transform.scale(sheet_mobil.subsurface(pygame.Rect(0, 0, w_potong, h_potong)), (lebar_mobil, tinggi_mobil))
mobil_2 = pygame.transform.scale(sheet_mobil.subsurface(pygame.Rect(w_potong, 0, w_potong, h_potong)), (lebar_mobil, tinggi_mobil))
mobil_3 = pygame.transform.scale(sheet_mobil.subsurface(pygame.Rect(0, h_potong, w_potong, h_potong)), (lebar_mobil, tinggi_mobil))
mobil_4 = pygame.transform.scale(sheet_mobil.subsurface(pygame.Rect(w_potong, h_potong, w_potong, h_potong)), (lebar_mobil, tinggi_mobil))
jenis_mobil = [mobil_1, mobil_2, mobil_3, mobil_4]

# --- LOAD AUDIO ---
try: suara_lompat = pygame.mixer.Sound(resource_path(os.path.join("assets", "jump.ogg")))
except: suara_lompat = None
try: suara_menang = pygame.mixer.Sound(resource_path(os.path.join("assets", "win.wav")))
except: suara_menang = None
try: suara_hit = pygame.mixer.Sound(resource_path(os.path.join("assets", "hit.wav"))) 
except: suara_hit = None
try: suara_lose = pygame.mixer.Sound(resource_path(os.path.join("assets", "lose.ogg")))
except: suara_lose = None

# --- TATA LETAK: KENDARAAN ---
daftar_mobil = [
    {"x": 0, "y": 500, "speed": 4, "tipe": 0},     
    {"x": 400, "y": 460, "speed": -5, "tipe": 1},  
    {"x": 200, "y": 420, "speed": 5, "tipe": 2},   
    {"x": 600, "y": 140, "speed": -7, "tipe": 3},  
    {"x": 100, "y": 100, "speed": 6, "tipe": 0}    
]

# --- TATA LETAK: PLATFORM SUNGAI ---
daftar_platform = [
    {"x": 100, "y": 340, "speed": 3, "w": 160, "tipe": "kayu"},  
    {"x": 500, "y": 340, "speed": 3, "w": 160, "tipe": "kayu"},  
    {"x": 0, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 80, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 160, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 240, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 320, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 400, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 480, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 560, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 640, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 720, "y": 300, "speed": 0, "w": 40, "tipe": "daun"}, 
    {"x": 100, "y": 260, "speed": -4, "w": 160, "tipe": "kayu"},  
    {"x": 500, "y": 260, "speed": -4, "w": 160, "tipe": "kayu"},  
    {"x": 40, "y": 220, "speed": 0, "w": 40, "tipe": "daun"},  
    {"x": 120, "y": 220, "speed": 0, "w": 40, "tipe": "daun"},  
    {"x": 200, "y": 220, "speed": 0, "w": 40, "tipe": "daun"},  
    {"x": 280, "y": 220, "speed": 0, "w": 40, "tipe": "daun"},  
    {"x": 360, "y": 220, "speed": 0, "w": 40, "tipe": "daun"},  
    {"x": 440, "y": 220, "speed": 0, "w": 40, "tipe": "daun"},  
    {"x": 520, "y": 220, "speed": 0, "w": 40, "tipe": "daun"},  
    {"x": 600, "y": 220, "speed": 0, "w": 40, "tipe": "daun"},  
    {"x": 680, "y": 220, "speed": 0, "w": 40, "tipe": "daun"},   
    {"x": 760, "y": 220, "speed": 0, "w": 40, "tipe": "daun"}   
]

# 2. PERSIAPAN KAMERA
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

anchor_x, anchor_y = None, None
is_neutral = True
waktu_hilang = 0
batas_hilang = 15

# 3. LOOPING UTAMA
while True:
    success, frame = cap.read()
    if not success: break
        
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    command = "DIAM"
    
    if results.multi_hand_landmarks:
        waktu_hilang = 0 
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            pergelangan = hand_landmarks.landmark[8] 
            h, w, _ = frame.shape
            cx, cy = int(pergelangan.x * w), int(pergelangan.y * h)
            
            if anchor_x is None or anchor_y is None:
                anchor_x, anchor_y = cx, cy
                
            cv2.circle(frame, (anchor_x, anchor_y), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(frame, (cx, cy), 8, (0, 255, 0), cv2.FILLED)
            
            jarak_x = cx - anchor_x
            jarak_y = cy - anchor_y
            
            if is_neutral and status_game == "MAIN" and not is_jumping:
                goyang = False
                if jarak_y < -40:
                    command = "MAJU"; target_y = kodok_y - jarak_lompat; target_x = round(kodok_x / 40) * 40; is_jumping = True; is_neutral = False; goyang = True
                elif jarak_y > 40:
                    command = "MUNDUR"; target_y = kodok_y + jarak_lompat; target_x = round(kodok_x / 40) * 40; is_jumping = True; is_neutral = False; goyang = True
                elif jarak_x > 40:
                    command = "KANAN"; target_x = (round(kodok_x / 40) * 40) + jarak_lompat; target_y = kodok_y; is_jumping = True; is_neutral = False; goyang = True
                elif jarak_x < -40:
                    command = "KIRI"; target_x = (round(kodok_x / 40) * 40) - jarak_lompat; target_y = kodok_y; is_jumping = True; is_neutral = False; goyang = True
                
                if goyang and suara_lompat:
                    suara_lompat.play()
            else:
                if abs(jarak_x) < 20 and abs(jarak_y) < 20:
                    is_neutral = True
    else:
        waktu_hilang += 1
        if waktu_hilang > batas_hilang:
            anchor_x, anchor_y = None, None
            is_neutral = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cap.release(); cv2.destroyAllWindows(); pygame.quit(); sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                cap.release(); cv2.destroyAllWindows(); pygame.quit(); sys.exit()
            if event.key == pygame.K_RETURN and status_game == "MENU":
                status_game = "MAIN" 
                kodok_x, kodok_y = posisi_awal_x, posisi_awal_y 
                target_x, target_y = posisi_awal_x, posisi_awal_y
                is_jumping = False

    # LOGIKA UTAMA GAMEPLAY
    if status_game in ["MAIN", "MENANG", "KALAH"]:
        for mobil in daftar_mobil:
            mobil["x"] += mobil["speed"]
            if mobil["speed"] > 0 and mobil["x"] > lebar_layar: 
                mobil["x"] = mobil["x"] - lebar_layar - lebar_mobil
            elif mobil["speed"] < 0 and mobil["x"] < -lebar_mobil: 
                mobil["x"] = mobil["x"] + lebar_layar + lebar_mobil

        for plat in daftar_platform:
            plat["x"] += plat["speed"]
            if plat["speed"] > 0 and plat["x"] > lebar_layar: 
                plat["x"] = plat["x"] - lebar_layar - plat["w"]
            elif plat["speed"] < 0 and plat["x"] < -plat["w"]: 
                plat["x"] = plat["x"] + lebar_layar + plat["w"]

        if status_game == "MAIN":
            if is_jumping:
                if kodok_x < target_x:
                    kodok_x += kecepatan_lompat
                    if kodok_x > target_x: kodok_x = target_x
                elif kodok_x > target_x:
                    kodok_x -= kecepatan_lompat
                    if kodok_x < target_x: kodok_x = target_x

                if kodok_y < target_y:
                    kodok_y += kecepatan_lompat
                    if kodok_y > target_y: kodok_y = target_y
                elif kodok_y > target_y:
                    kodok_y -= kecepatan_lompat
                    if kodok_y < target_y: kodok_y = target_y

                if kodok_x == target_x and kodok_y == target_y:
                    is_jumping = False

            kodok_x = max(0, min(lebar_layar - ukuran_kodok, kodok_x))
            kodok_y = max(0, min(tinggi_layar - ukuran_kodok, kodok_y))
            if not is_jumping:
                target_x = kodok_x
                target_y = kodok_y

            kotak_kodok = pygame.Rect(kodok_x, kodok_y, ukuran_kodok, ukuran_kodok)

            for mobil in daftar_mobil:
                kotak_mobil = pygame.Rect(mobil["x"], mobil["y"], lebar_mobil, tinggi_mobil)
                if kotak_kodok.colliderect(kotak_mobil):
                    status_game = "KALAH"
                    waktu_kalah = pygame.time.get_ticks()
                    suara_lose_diputar = False
                    if suara_hit: suara_hit.play() 

            if status_game == "MAIN" and not is_jumping and (220 <= kodok_y <= 340):
                nempel_platform = False
                kodok_tengah_x = kodok_x + (ukuran_kodok // 2)
                
                for plat in daftar_platform:
                    if kodok_y == plat["y"]:
                        if plat["x"] <= kodok_tengah_x <= (plat["x"] + plat["w"]):
                            nempel_platform = True
                            kodok_x += plat["speed"]  
                            target_x = kodok_x        
                            break
                            
                if not nempel_platform:
                    status_game = "KALAH"
                    waktu_kalah = pygame.time.get_ticks()
                    suara_lose_diputar = False
                    if suara_hit: suara_hit.play() 
                    
            if status_game == "MAIN" and not is_jumping and kodok_y <= 60:
                status_game = "MENANG"
                waktu_menang = pygame.time.get_ticks()
                if suara_menang: suara_menang.play()

    # LOGIKA DRAWING (MENGGAMBAR ARENA)
    if status_game == "MENU":
        layar.fill((34, 139, 34)) 
        pygame.draw.rect(layar, (80, 80, 80), (0, 240, lebar_layar, 130))
        for i in range(0, lebar_layar, 60):
            pygame.draw.rect(layar, (255, 255, 255), (i, 300, 30, 10))
            
        gambar_kodok_besar = pygame.transform.scale(gambar_kodok, (120, 120))
        layar.blit(gambar_kodok_besar, (lebar_layar//2 - 60, 40))
        
        teks_judul_shadow = font_judul.render("FROGGER CV", True, (0, 0, 0))
        layar.blit(teks_judul_shadow, (lebar_layar//2 - teks_judul_shadow.get_width()//2 + 4, 164))
        teks_judul = font_judul.render("FROGGER CV", True, (50, 255, 50))
        layar.blit(teks_judul, (lebar_layar//2 - teks_judul.get_width()//2, 180))
        
        teks_enter = font_sedang.render("Tekan ENTER Untuk Mulai", True, (255, 255, 0))
        layar.blit(teks_enter, (lebar_layar//2 - teks_enter.get_width()//2, 385))
        
        kotak_gelap = pygame.Surface((lebar_layar, 160))
        kotak_gelap.set_alpha(210); kotak_gelap.fill((0, 0, 0)); layar.blit(kotak_gelap, (0, 440))

        teks_panduan1 = font_sedang.render("PANDUAN BERMAIN:", True, (255, 255, 255))
        teks_panduan2 = font_kecil.render("1. Angkat jari telunjuk ke kamera hingga muncul titik merah.", True, (200, 200, 200))
        teks_panduan3 = font_kecil.render("2. Sentakkan jari melewati titik merah (Atas/Bawah/Kiri/Kanan) untuk lompat.", True, (200, 200, 200))
        teks_panduan4 = font_kecil.render("3. Kembalikan jari telunjuk ke titik merah untuk lompatan berikutnya.", True, (200, 200, 200))
        teks_panduan5 = font_kecil.render("4. Klik ESC kapan saja untuk KELUAR dari aplikasi game.", True, (255, 100, 100)) 
        
        layar.blit(teks_panduan1, (20, 445))
        layar.blit(teks_panduan2, (20, 485))
        layar.blit(teks_panduan3, (20, 512))
        layar.blit(teks_panduan4, (20, 540))
        layar.blit(teks_panduan5, (20, 568))

    elif status_game in ["MAIN", "MENANG", "KALAH"]:
        layar.fill((30, 30, 30)) 
        
        pygame.draw.rect(layar, (44, 160, 44), (0, 0, lebar_layar, 100))       
        for i in range(0, lebar_layar, 60):
            pygame.draw.circle(layar, (25, 100, 25), (i + 30, 95), 35) 
            pygame.draw.circle(layar, (44, 160, 44), (i + 30, 90), 28) 

        pygame.draw.rect(layar, (45, 45, 45), (0, 100, lebar_layar, 80)) 
        for x in range(0, lebar_layar, 40):
            pygame.draw.rect(layar, (230, 230, 230), (x, 140, 15, 2))
            
        pygame.draw.rect(layar, (100, 100, 100), (0, 180, lebar_layar, 40))    
        for i in range(0, lebar_layar, 40):
            warna_pembatas = (220, 220, 220) if (i // 40) % 2 == 0 else (40, 40, 40)
            pygame.draw.rect(layar, warna_pembatas, (i, 215, 40, 5))
        
        pygame.draw.rect(layar, (0, 100, 255), (0, 220, lebar_layar, 160)) 
        waktu_sekarang = pygame.time.get_ticks()
        for baris in range(4):
            y_ombak = 235 + (baris * 40)
            arah = 1 if baris % 2 == 0 else -1
            geser = int((waktu_sekarang / 15 * arah) % 40) 
            for x_ombak in range(-40, lebar_layar + 40, 40):
                pygame.draw.line(layar, (100, 200, 255), (x_ombak + geser, y_ombak), (x_ombak + geser + 15, y_ombak), 2)

        pygame.draw.rect(layar, (100, 100, 100), (0, 380, lebar_layar, 40))    
        for i in range(0, lebar_layar, 40):
            warna_pembatas = (220, 220, 220) if (i // 40) % 2 == 0 else (40, 40, 40)
            pygame.draw.rect(layar, warna_pembatas, (i, 380, 40, 5)) # <-- FIX: Ditambahkan argumen 'layar'

        # JALAN RAYA BAWAH
        pygame.draw.rect(layar, (45, 45, 45), (0, 420, lebar_layar, 120)) 
        for x in range(0, lebar_layar, 40):
            pygame.draw.rect(layar, (230, 230, 230), (x, 460, 15, 2))
            pygame.draw.rect(layar, (230, 230, 230), (x, 500, 15, 2))

        pygame.draw.rect(layar, (100, 100, 100), (0, 540, lebar_layar, 60))    
        for i in range(0, lebar_layar, 40):
            warna_pembatas = (220, 220, 220) if (i // 40) % 2 == 0 else (40, 40, 40)
            pygame.draw.rect(layar, warna_pembatas, (i, 540, 40, 5))
        
        for plat in daftar_platform:
            if plat["tipe"] == "kayu":
                pygame.draw.rect(layar, (120, 80, 45), (plat["x"], plat["y"], plat["w"], 40), border_radius=15)
                pygame.draw.rect(layar, (60, 40, 20), (plat["x"], plat["y"], plat["w"], 40), width=3, border_radius=15)
                pygame.draw.line(layar, (90, 60, 30), (plat["x"]+15, plat["y"]+10), (plat["x"]+plat["w"]-15, plat["y"]+10), 2)
                pygame.draw.line(layar, (90, 60, 30), (plat["x"]+10, plat["y"]+20), (plat["x"]+plat["w"]-20, plat["y"]+20), 2)
                pygame.draw.line(layar, (90, 60, 30), (plat["x"]+15, plat["y"]+30), (plat["x"]+plat["w"]-10, plat["y"]+30), 2)
            
            elif plat["tipe"] == "daun":
                pusat_x = plat["x"] + plat["w"] // 2
                pusat_y = plat["y"] + 20
                radius = 18
                pygame.draw.circle(layar, (50, 205, 50), (pusat_x, pusat_y), radius)
                pygame.draw.circle(layar, (0, 100, 0), (pusat_x, pusat_y), radius, width=2)
                warna_air = (0, 100, 255)
                pygame.draw.polygon(layar, warna_air, [(pusat_x, pusat_y), (pusat_x - 12, pusat_y + radius + 2), (pusat_x + 12, pusat_y + radius + 2)])
        
        for mobil in daftar_mobil:
            gambar_terpilih = jenis_mobil[mobil["tipe"]] 
            if mobil["speed"] > 0:
                layar.blit(pygame.transform.flip(gambar_terpilih, True, False), (mobil["x"], mobil["y"]))
            else:
                layar.blit(gambar_terpilih, (mobil["x"], mobil["y"]))
                
        if status_game != "KALAH" or (pygame.time.get_ticks() - waktu_kalah) > 500:
            layar.blit(gambar_kodok, (kodok_x, kodok_y))

        if status_game == "KALAH":
            waktu_sekarang = pygame.time.get_ticks()
            durasi = waktu_sekarang - waktu_kalah

            if durasi < 500:
                pusat_x = kodok_x + (ukuran_kodok // 2)
                pusat_y = kodok_y + (ukuran_kodok // 2)
                pygame.draw.circle(layar, (255, 50, 0), (pusat_x, pusat_y), int(durasi * 0.15))  
                pygame.draw.circle(layar, (255, 150, 0), (pusat_x, pusat_y), int(durasi * 0.10)) 
                pygame.draw.circle(layar, (255, 255, 0), (pusat_x, pusat_y), int(durasi * 0.05)) 

            font_besar = pygame.font.SysFont("Arial", 75, bold=True)
            teks_kalah = font_besar.render("GAME OVER!", True, (255, 50, 50))
            layar.blit(teks_kalah, (lebar_layar//2 - teks_kalah.get_width()//2, tinggi_layar//2 - 50))
            
            if durasi > 400 and not suara_lose_diputar:
                if suara_lose: suara_lose.play()
                suara_lose_diputar = True
            
            if durasi > 2500:
                status_game = "MAIN"
                kodok_x, kodok_y = posisi_awal_x, posisi_awal_y
                target_x, target_y = posisi_awal_x, posisi_awal_y
                is_jumping = False

        if status_game == "MENANG":
            font_besar = pygame.font.SysFont("Arial", 80, bold=True)
            teks_menang = font_besar.render("YOU WIN!", True, (50, 255, 50))
            layar.blit(teks_menang, (lebar_layar//2 - 190, tinggi_layar//2 - 50))
            if pygame.time.get_ticks() - waktu_menang > 3000:
                status_game = "MENU"
                kodok_x, kodok_y = posisi_awal_x, posisi_awal_y
                target_x, target_y = posisi_awal_x, posisi_awal_y
                is_jumping = False

    pygame.display.update()
    clock.tick(30)
    cv2.putText(frame, f"PERINTAH: {command}", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Kamera Deteksi CV", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release(); cv2.destroyAllWindows(); pygame.quit()