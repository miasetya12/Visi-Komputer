import cv2

# Baca gambar
gambar = cv2.imread('apel.jpg')

# Pastikan gambar telah terbaca dengan benar
if gambar is None:
    print("Gagal membaca gambar.")
else:
    # Mendapatkan dimensi gambar
    tinggi, lebar, _ = gambar.shape

    # Loop melalui setiap piksel
    for i in range(tinggi):
        for j in range(lebar):
            # Dapatkan nilai piksel untuk setiap saluran warna
            B, G, R = gambar[i, j]

            # Hitung intensitas piksel menggunakan rumus Grayscale
            # source rumus: https://repository.mikroskil.ac.id/id/eprint/391/3/BAB%20II.pdf
            intensitas = 0.2989 * R + 0.5870 * G + 0.1140 * B

            # Tampilkan nilai intensitas piksel
            print(f'Piksel ({i}, {j}): Intensitas = {intensitas:.2f}')
