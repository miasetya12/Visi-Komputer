from tkinter import * 
from tkinter import filedialog
from tkinter import simpledialog
from PIL import ImageTk, Image 
from tkinter.filedialog import askopenfile
import cv2
import numpy as np
from tkinter import messagebox
root = Tk()
root.title("HOUGH CIRCLE TRANSFORM")
ukurangambar = (350,350)

imageacces, converting, hasilhough, hasilgray, hasilcanny, hasilgaussian = dict(), dict(), dict(), dict(), dict(), dict()

def box():
   
    imgconvert = Image.new("RGB", ukurangambar)
    converting["image"] = ImageTk.PhotoImage(imgconvert)

    labelinsert = Label(root, image= converting["image"])
    labelinsert.grid(row= 1, column=1)

    labelconvertgray = Label(root, image= converting["image"])
    labelconvertgray.grid(row=7, column=1)
    
    labelgaussian = Label(root, image= converting["image"])
    labelgaussian.grid(row=7, column=3)

    labelcanny = Label(root, image= converting["image"])
    labelcanny.grid(row=7, column=2)

    labelhough = Label(root, image= converting["image"])
    labelhough.grid(row=7, column=4)

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
    global hasilgaussian
    global convertgrays
    gray_image = np.array(grayscale_image)

    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0) 
    hasilgaussian["image"] = ImageTk.PhotoImage(Image.fromarray(blurred_image))
    
    labelgaussian = Label(root, image=hasilgaussian["image"])
    labelgaussian.grid(row=7, column=2)
    return blurred_image

def convert():
    global grayscale_image
    grayscale_image = grayscale(original)
    gaussian_image = gaussian(grayscale_image)
    canny_image = canny(gaussian_image)
    hough_transform (canny_image)   

def canny(gaussian_image):
    global canny_image
    gray_image = np.array(gaussian_image)
    canny = cv2.Canny(gray_image, 50, 150, apertureSize=3)
    canny_image = Image.fromarray(canny)
    hasilcanny["image"] = ImageTk.PhotoImage(canny_image)
    labelcanny = Label(root, image=hasilcanny["image"])
    labelcanny.grid(row=7, column=3)
    return canny_image


def hough_transform(canny_image):
    global hasilhough

    try:
        # Mengonversi gambar hasil Canny menjadi numpy array
        original_images = np.array(original)
        canny_img = np.array(canny_image)  

        # Menggunakan metode Hough Circle Transform untuk mendeteksi lingkaran pada gambar Canny
        circles = cv2.HoughCircles(canny_img, cv2.HOUGH_GRADIENT, dp=1, minDist=22, param1=50, param2=30, minRadius=22, maxRadius=50)

        if circles is not None:
            circles = np.uint16(np.around(circles))
            # Menggambar lingkaran pada gambar original untuk setiap lingkaran yang terdeteksi
            for i in circles[0, :]:
                center = (i[0], i[1])
                radius = i[2]
                # Gambar lingkaran pada gambar original
                cv2.circle(original_images, center, radius, (0, 255, 0), 2)

        
            # Konversi gambar hasil Hough Transform menjadi format yang dapat ditampilkan oleh Tkinter
            hasilhough["image"] = ImageTk.PhotoImage(Image.fromarray(original_images))
            
            # Menampilkan gambar hasil Hough Transform pada GUI Tkinter
            labelhough = Label(root, image=hasilhough["image"])
            labelhough.grid(row=7, column=4)
            labelfinal = Label(root, image=hasilhough["image"])
            labelfinal.grid(row=1, column=2)
        else:
            # Jika tidak terdeteksi lingkaran, tampilkan pesan popup bahwa tidak ada lingkaran yang terdeteksi
            messagebox.showinfo("Info", "Tidak ada lingkaran yang terdeteksi.")

    except Exception as e:
        # Jika terjadi kesalahan, tampilkan pesan kesalahan
        print("Error:", e)

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
label5 = Label(root, text = "4. Hough Circle Result")
label5.grid(row = 6, column=4)

tombolConvert = Button(root, text="Convert", command=convert)
tombolInputGambar = Button(root, text="Buka File", command=openimage)
tombolReset = Button(root, text= "RESET", command= box)


tombolInputGambar.grid(row=2, column=1,sticky=EW) 
tombolConvert.grid(row=2, column=2,sticky=EW)
tombolReset.grid(row=3, column=1,columnspan=2, sticky = EW)

root.mainloop()