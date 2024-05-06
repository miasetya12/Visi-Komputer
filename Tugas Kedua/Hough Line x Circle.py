from tkinter import * 
from tkinter import filedialog
from tkinter import simpledialog
from PIL import ImageTk, Image 
from tkinter.filedialog import askopenfile
import cv2
import numpy as np
from tkinter import messagebox
root = Tk()
root.title("HOUGH TRANSFORM ")
ukurangambar = (350,350)

imageacces, converting, hasilhough, hasilgray, hasilcanny, hasilgaussian, hasilhoughcircle, hasilhoughP = dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict()

def box():
    # Membuat gambar baru dengan warna RGB serta ukuran gambar diatur
    imgconvert = Image.new("RGB", ukurangambar)
    # Mengkonversi gambar agar dapat di tampilkan oleh Tkinter
    converting["image"] = ImageTk.PhotoImage(imgconvert)

    # Membuat objek label Tkinter untuk menampilkan Original image
    labelinsert = Label(root, image= converting["image"])
    labelinsert.grid(row= 1, column=1)

    # Membuat objek label Tkinter untuk menampilkan Grayscale image
    labelconvertgray = Label(root, image= converting["image"])
    labelconvertgray.grid(row=7, column=1)
    
    # Membuat objek label Tkinter untuk menampilkan Gaussian image
    labelgaussian = Label(root, image= converting["image"])
    labelgaussian.grid(row=7, column=3)

    # Membuat objek label Tkinter untuk menampilkan Canny image
    labelcanny = Label(root, image= converting["image"])
    labelcanny.grid(row=7, column=2)

    # Membuat objek label Tkinter untuk menampilkan hasil Hough Transform
    labelhough = Label(root, image= converting["image"])
    labelhough.grid(row=7, column=4)
    

    # Membuat objek label Tkinter untuk menampilkan hasil Haough Transform namun letaknya di samping Original image
    labelfinal = Label(root, image= converting["image"])
    labelfinal.grid(row=1, column=2)

    # Membuat objek label Tkinter untuk menampilkan hasil Haough Transform namun letaknya di samping Original image
    labelfinal2 = Label(root, image= converting["image"])
    labelfinal2.grid(row=1, column=3)

    # Membuat objek label Tkinter untuk menampilkan hasil Haough Transform namun letaknya di samping Original image
    labelfinal3 = Label(root, image= converting["image"])
    labelfinal3.grid(row=1, column=4)

    
box()

def openimage():
    global original

    # Membuka dialog file
    root.imagefile = filedialog.askopenfilename(initialdir="", filetypes=(("png files", "*.png *.jpg *.jpeg"), ("all files", "*.*")))
    # Menyimpan path gambar
    fileadress = root.imagefile
    # Baca gambar menggunakan OpenCV
    imageinput = cv2.imread(fileadress)
    # Ubah gambar ke format RGB
    imageinput = cv2.cvtColor(imageinput, cv2.COLOR_BGR2RGB)
    # Ubah ukuran gambar
    imageinput = cv2.resize(imageinput, ukurangambar)
    # Ubah gambar ke format PIL untuk tampilan di Tkinter
    imageinput = Image.fromarray(imageinput)
    # Tampilkan gambar di Tkinter
    imageacces["image"] = ImageTk.PhotoImage(imageinput)
    labelinsert = Label(root, image=imageacces["image"])
    labelinsert.grid(row=1, column=1)
    # Ambil informasi pixel
    ambilpixel(imageinput)
    # Simpan gambar asli sebagai numpy array
    original = np.array(imageinput)

def ambilpixel(imageinput):
    global warna
    warna = []

    for garisX in range(imageinput.width):
        for garisY in range(imageinput.height):
            nilaiR = imageinput.getpixel((garisX,garisY))[0]
            nilaiG = imageinput.getpixel((garisX,garisY))[1]
            nilaiB = imageinput.getpixel((garisX,garisY))[2]
            warna.append([garisX, garisY, nilaiR, nilaiG, nilaiB])

def grayscale(image):
    # Konversi ke citra grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    # Ubah gambar grayscale ke format PIL untuk tampilan di Tkinter
    grayscale_image_pil = Image.fromarray(grayscale_image)

    # Tampilkan gambar grayscale di Tkinter
    hasilgray["image"] = ImageTk.PhotoImage(grayscale_image_pil)
    labelconvertgray = Label(root, image=hasilgray["image"])
    labelconvertgray.grid(row=7, column=1)
    return grayscale_image


def gaussian(grayscale_image):
    global hasilgaussian # Deklarasi variabel sebagai global untuk menyimpan hasil gambar gaussian
    global convertgrays

    # Konversi gambar grayscale menjadi array numpy
    gray_image = np.array(grayscale_image)
    # Menerapkan filter gaussian pada gambar grayscale dengan kernel 5x5 dan std 0
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0) 
    # Konversi gambar hasil filter Gaussian menjadi format yang dapat ditampilkan oleh Tkinter
    hasilgaussian["image"] = ImageTk.PhotoImage(Image.fromarray(blurred_image))
    # Buat label Tkinter yang menampilkan gambar hasil filter Gaussian
    labelgaussian = Label(root, image=hasilgaussian["image"])
    labelgaussian.grid(row=7, column=2) # Menempatkan label di baris ke-7 dan kolom ke-2 di GUI
    return blurred_image # Mengembalikan gambar hasil filter Gaussian

def convert_line():
    global grayscale_image # Variabel grayscale_image dideklarasikan sebagai global agar bisa diakses di luar fungsi
    # Konversi gambar asli menjadi citra grayscale
    grayscale_image = grayscale(original)
    # Menerapkan filter Gaussian pada citra grayscale
    gaussian_image = gaussian(grayscale_image)
    # Menerapkan deteksi tepi Canny pada citra hasil filter Gaussian
    canny_image = canny(gaussian_image)
    # Menerapkan transformasi Hough Circle pada citra hasil deteksi tepi Canny
    hough_line (canny_image)   

def convert_lineP():
    global grayscale_image # Variabel grayscale_image dideklarasikan sebagai global agar bisa diakses di luar fungsi
    # Konversi gambar asli menjadi citra grayscale
    grayscale_image = grayscale(original)
    # Menerapkan filter Gaussian pada citra grayscale
    gaussian_image = gaussian(grayscale_image)
    # Menerapkan deteksi tepi Canny pada citra hasil filter Gaussian
    canny_image = canny(gaussian_image)
    # Menerapkan transformasi Hough Circle pada citra hasil deteksi tepi Canny
    hough_lineP (canny_image)  

def convert_circle():
    global grayscale_image # Variabel grayscale_image dideklarasikan sebagai global agar bisa diakses di luar fungsi
    # Konversi gambar asli menjadi citra grayscale
    grayscale_image = grayscale(original)
    # Menerapkan filter Gaussian pada citra grayscale
    gaussian_image = gaussian(grayscale_image)
    # Menerapkan deteksi tepi Canny pada citra hasil filter Gaussian
    canny_image = canny(gaussian_image)
    # Menerapkan transformasi Hough Circle pada citra hasil deteksi tepi Canny
    hough_circle (canny_image)  

def canny(gaussian_image):
    global canny_image

    # Mengonversi gambar hasil filter Gaussian menjadi array numpy
    gray_image = np.array(gaussian_image)
    # Menerapkan deteksi tepi Canny pada gambar grayscale
    # Parameter yg diperlukan adalah gambar hasil gaussian, ambang bawah (50), ambang atas (150)
    canny = cv2.Canny(gray_image, 50, 150, apertureSize=3) # apertureSize=3, menggunakan kernel Sobel 3x3 untuk menghitung gradien
    # Konversi gambar hasil deteksi tepi Canny ke format yang dapat ditampilkan oleh Tkinter
    canny_image = Image.fromarray(canny)
    # Simpan gambar hasil deteksi tepi Canny dalam kamus hasilcanny untuk ditampilkan di GUI
    hasilcanny["image"] = ImageTk.PhotoImage(canny_image)
    # Membuat label Tkinter yang menampilkan gambar hasil deteksi tepi Canny
    labelcanny = Label(root, image=hasilcanny["image"])
    labelcanny.grid(row=7, column=3)
    return canny_image # Mengembalikan gambar hasil deteksi tepi Canny


def hough_line(canny_image):
    # Cocok untuk mendeteksi garis lurus pada citra biner
    # Tidak memberikan informasi tentang koordinat titik-titik garis yang terdeteksi
    
    global hasilhough

    # documentations: https://docs.opencv.org/4.x/d9/db0/tutorial_hough_lines.html
    
    try:
        # Mengonversi gambar original dan hasil Canny menjadi numpy array
        original_images = np.array(original)
        canny_img = np.array(canny_image)

        # Menggunakan metode Hough Transform untuk mendeteksi garis-garis pada gambar Canny
        lines = cv2.HoughLines(canny_img, 1, np.pi / 180, 100)  
        # nilai 1 = Resolusi jarak rho adalah 1 pixel
        # np.pi / 180 = Resolusi sudut theta dalam radian
        # 100 = ambang batas (threshold) untuk mendeteksi garis.  
        # akan ada 2 kolom output 
        print(f'ini lines: {lines}')

        # Melakukan iterasi untuk setiap garis yang terdeteksi
        for curline in lines:
            rho, theta = curline[0]
            print(f'ini rho: {rho}')
            print(f'ini theta: {theta}')
            # Cth Rho = 202 artinya garis yang direpresentasikan oleh titik tersebut memiliki jarak sejauh 202.0 piksel dari titik asal (0,0) ke garis tersebut
            # Cth Theta = 1.5707963705062866 artinya titik tersebut memiliki orientasi sebesar 1.5 radian dari sumbu x positif ke arah sumbu y positif

            a = np.cos(theta)
            b = np.sin(theta)

            # Menghitung koordinat garis yang dideteksi
            x0 = a*rho
            y0 = b*rho

            # Jarak untuk menentukan panjang garis yang akan digambar
            k = 1000

            # Menghitung titik awal dan akhir garis yang akan digambar
            pt1 = (int(x0 + k*(-b)), int(y0 + k*(a)))
            pt2 = (int(x0 - k*(-b)), int(y0 - k*(a)))

            # Menggambar garis merah pada gambar original
            cv2.line(original_images, (pt1), (pt2), (255, 0, 0), 2)
            # 2 = ketebalan garis

        # Print jumlah garis yang terdeteksi
        print(f"Jumlah garis yang terdeteksi: {len(lines)}")

        # Konversi gambar hasil Hough Transform menjadi format yang dapat ditampilkan oleh Tkinter
        hasilhough["image"] = ImageTk.PhotoImage(Image.fromarray(original_images))
        
        # Menampilkan gambar hasil Hough Transform pada GUI Tkinter
        labelhough = Label(root, image=hasilhough["image"])
        labelhough.grid(row=7, column=4)
        labelfinal = Label(root, image=hasilhough["image"])
        labelfinal.grid(row=1, column=2)

    except Exception as e:
            # Jika tidak terdeteksi garis, tampilkan pesan popup bahwa tidak ada garis yang terdeteksi
            messagebox.showinfo("Info", "Tidak ada garis yang terdeteksi.")


def hough_lineP(canny_image):
    # Lebih cocok untuk mendeteksi garis-garis yang tidak lurus
    # Memberikan koordinat titik-titik awal dan akhir dari setiap garis yang terdeteksi

    global hasilhoughP
    try:
        original_images = np.array(original)
        canny_img = np.array(canny_image)

        # Menggunakan metode Hough Transform probabilistik untuk mendeteksi garis-garis pada gambar Canny
        lines = cv2.HoughLinesP(canny_img, 1, np.pi / 180, 50, 1000,10)
        # 50 = threshold (ambang batas yang digunakan dalam deteksi garis)
        # 100 = minLineLength (panjang minimum yang diperlukan untuk sebuah garis. Garis-garis yang lebih pendek dari nilai ini akan diabaikan)
        # 50 = maxLineGap (celah maksimum yang diizinkan di antara titik-titik pada garis untuk tetap dianggap sebagai bagian dari garis yang sama. 
        # Jika jarak antara dua titik lebih besar dari nilai ini, maka dua bagian garis tersebut dianggap terpisah.

        print(lines)

        # Melakukan iterasi untuk setiap garis yang terdeteksi
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(original_images, (x1, y1), (x2, y2), (255, 0, 0), 2)
        # (x1, y1) adalah koordinat titik awal dari garis
        # (x2, y2) adalah koordinat titik akhir dari garis

        # Print jumlah garis yang terdeteksi
        print(f"Jumlah garis yang terdeteksi: {len(lines)}")

        # Konversi gambar hasil Hough Transform menjadi format yang dapat ditampilkan oleh Tkinter
        hasilhoughP["image"] = ImageTk.PhotoImage(Image.fromarray(original_images))
        
        # Menampilkan gambar hasil Hough Transform pada GUI Tkinter
        labelhough = Label(root, image=hasilhoughP["image"])
        labelhough.grid(row=7, column=4)
        labelfinal2 = Label(root, image=hasilhoughP["image"])
        labelfinal2.grid(row=1, column=3)

    except Exception as e:
        # Jika tidak terdeteksi garis, tampilkan pesan popup bahwa tidak ada garis yang terdeteksi
        messagebox.showinfo("Info", "Tidak ada garis yang terdeteksi.")



def hough_circle(canny_image):
    global hasilhoughcircle

    try:
        # Mengonversi gambar hasil deteksi tepi Canny menjadi array numpy
        canny_img = np.array(canny_image)  

        # Mendeteksi lingkaran menggunakan metode Hough Circle
        circles = cv2.HoughCircles(canny_img, cv2.HOUGH_GRADIENT, dp=1, minDist=70, param1=100, param2=30, minRadius=10, maxRadius=50)

        # print fungsi cv2.HoughCircles() untuk mengetahui daftar lingkaran yang terdeteksi beserta koordinat pusat dan radiusnya
        print(circles)

        # Menggambar lingkaran yang terdeteksi pada gambar original
        # if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            # Menggambar lingkaran pada gambar original
            cv2.circle(original, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
            # Menggambar titik tengah lingkaran
            cv2.circle(original, (circle[0], circle[1]), 2, (0, 0, 255), 3)

        # Konversi gambar hasil Hough Circle menjadi format yang dapat ditampilkan oleh Tkinter
        hasilhoughcircle["image"] = ImageTk.PhotoImage(Image.fromarray(original))
        
        # Menampilkan gambar hasil Hough Circle pada GUI Tkinter
        labelhoughcircle = Label(root, image=hasilhoughcircle["image"])
        labelhoughcircle.grid(row=7, column=4)
        labelfinal3 = Label(root, image=hasilhoughcircle["image"])
        labelfinal3.grid(row=1, column=4)

    except Exception as e:
        # Jika tidak terdeteksi lingkaran, tampilkan pesan popup bahwa tidak ada lingkaran yang terdeteksi
        messagebox.showinfo("Info", "Tidak ada lingkaran yang terdeteksi.")


# Membuat beberapa objek Label dalam GUI Tkinter untuk menampilkan teks pada antarmuka pengguna. 
label1 = Label(root, text = "Original Image")
label1.grid(row= 0, column= 1)
label1b = Label(root, text = "Final Result Hough Line Image")
label1b.grid(row= 0, column= 2)
label1bb = Label(root, text = "Final Result Hough Line P Image")
label1bb.grid(row= 0, column= 3)
label1bbb = Label(root, text = "Final Result Hough Circle Image")
label1bbb.grid(row= 0, column= 4)
label2 = Label(root, text = "1. Grayscale Result")
label2.grid(row = 6, column= 1)
label3 = Label(root, text = "2. Gaussian Result")
label3.grid(row = 6, column=2)
label4 = Label(root, text = "3. Canny Result")
label4.grid(row = 6, column=3)
label5 = Label(root, text = "4. Hough Result")
label5.grid(row = 6, column=4)

# Membuat tiga tombol pada GUI Tkinter
tombolConvertLine = Button(root, text="Convert Hough Line", command=convert_line) # Menjalankan fungsi convert() ketika tombol ini ditekan
tombolConvertLineP = Button(root, text="Convert Hough P Line", command=convert_lineP)
tombolInputGambar = Button(root, text="Buka File", command=openimage) # Menjalankan fungsi openimage() ketika tombol ini ditekan
tombolReset = Button(root, text= "RESET", command= box) # Menjalankan fungsi box() ketika tombol ini ditekan, dan mengatur ulang GUI seperti semula
tombolConvertCircle = Button(root, text="Convert Hough Circle", command=convert_circle) 

# Menempatkan tiga tombol pada posisi tertentu
# Parameter sticky=EW menunjukkan bahwa tombol akan menempel pada sisi timur dan barat dari selnya, yang berarti tombol akan memperluas ukurannya secara horizontal mengikuti lebar sel.
tombolInputGambar.grid(row=2, column=1,sticky=EW)
tombolConvertLine.grid(row=2, column=2,sticky=EW)
tombolReset.grid(row=3, column=1, sticky = EW)
tombolConvertCircle.grid(row=2, column=4,sticky=EW)
tombolConvertLineP.grid(row=2, column=3,sticky=EW)

root.mainloop()