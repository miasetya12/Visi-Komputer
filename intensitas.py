import cv2

# Baca gambar
img = cv2.imread('doraemon.jpg')

# Periksa apakah gambar berhasil dibaca
if img is not None:
    # Loop melalui setiap piksel dalam gambar
    tinggi, lebar, _ = img.shape
    for y in range(tinggi):
        for x in range(lebar):
            # Dapatkan nilai intensitas piksel pada koordinat (x, y)
            intensitas_piksel = img[y, x]
            print(f'Koordinat: ({x}, {y}), Intensitas: {intensitas_piksel}')

else:
    print('Gagal membaca gambar. Pastikan nama dan path file gambar benar.')