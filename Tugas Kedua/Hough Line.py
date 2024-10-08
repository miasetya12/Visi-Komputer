from tkinter import * 
from tkinter import filedialog
from tkinter import simpledialog
from PIL import ImageTk, Image 
from tkinter.filedialog import askopenfile
import cv2
import numpy as np
from tkinter import messagebox
root = Tk()
root.title("HOUGH LINE TRANSFORM ")
ukurangambar = (350,350)

imageacces, converting, hasilhough, hasilgray, hasilcanny, hasilgaussian = dict(), dict(), dict(), dict(), dict(), dict()

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

def convert():
    global grayscale_image # Variabel grayscale_image dideklarasikan sebagai global agar bisa diakses di luar fungsi
    # Konversi gambar asli menjadi citra grayscale
    grayscale_image = grayscale(original)
    # Menerapkan filter Gaussian pada citra grayscale
    gaussian_image = gaussian(grayscale_image)
    # Menerapkan deteksi tepi Canny pada citra hasil filter Gaussian
    canny_image = canny(gaussian_image)
    # Menerapkan transformasi Hough Circle pada citra hasil deteksi tepi Canny
    hough_transform (canny_image)   

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


def hough_transform(canny_image):
    global hasilhough

    try:
        # Mengonversi gambar original dan hasil Canny menjadi numpy array
        original_images = np.array(original)
        canny_img = np.array(canny_image)  

        # Menggunakan metode Hough Transform untuk mendeteksi garis-garis pada gambar Canny
        lines = cv2.HoughLines(canny_img, 1, np.pi / 180, 150)  

        # Jarak untuk menentukan panjang garis yang akan digambar
        k = 3000 

        # Melakukan iterasi untuk setiap garis yang terdeteksi
        for curline in lines:
            rho, theta = curline[0]

            # Menghitung vektor normal dan vektor tegak lurus terhadap garis
            dhat = np.array([[np.cos(theta)], [np.sin(theta)]])
            d = rho * dhat

            lhat = np.array([[-np.sin(theta)], [np.cos(theta)]])

            # Menghitung titik awal dan akhir garis yang akan digambar
            p1 = d + k * lhat
            p2 = d - k * lhat

            p1 = p1.astype(int)
            p2 = p2.astype(int)

            x1 = p1[0][0]
            y1 = p1[1][0]
            x2 = p2[0][0]
            y2 = p2[1][0]

            # Menggambar garis merah pada gambar original
            cv2.line(original_images, (x1, y1), (x2,y2), (255, 0, 0), 2)
        
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


# Membuat beberapa objek Label dalam GUI Tkinter untuk menampilkan teks pada antarmuka pengguna. 
label1 = Label(root, text = "Original Image")
label1.grid(row= 0, column= 1)
label1b = Label(root, text = "Final Result Image")
label1b.grid(row= 0, column= 2)
label2 = Label(root, text = "1. Grayscale Result")
label2.grid(row = 6, column= 1)
label3 = Label(root, text = "2. Gaussian Result")
label3.grid(row = 6, column=2)
label4 = Label(root, text = "3. Canny Result")
label4.grid(row = 6, column=3)
label5 = Label(root, text = "4. Hough Line Result")
label5.grid(row = 6, column=4)

# Membuat tiga tombol pada GUI Tkinter
tombolConvert = Button(root, text="Convert", command=convert) # Menjalankan fungsi convert() ketika tombol ini ditekan
tombolInputGambar = Button(root, text="Buka File", command=openimage) # Menjalankan fungsi openimage() ketika tombol ini ditekan
tombolReset = Button(root, text= "RESET", command= box) # Menjalankan fungsi box() ketika tombol ini ditekan, dan mengatur ulang GUI seperti semula

# Menempatkan tiga tombol pada posisi tertentu
# Parameter sticky=EW menunjukkan bahwa tombol akan menempel pada sisi timur dan barat dari selnya, yang berarti tombol akan memperluas ukurannya secara horizontal mengikuti lebar sel.
tombolInputGambar.grid(row=2, column=1,sticky=EW) 
tombolConvert.grid(row=2, column=2,sticky=EW)
tombolReset.grid(row=3, column=1,columnspan=2, sticky = EW)

root.mainloop()