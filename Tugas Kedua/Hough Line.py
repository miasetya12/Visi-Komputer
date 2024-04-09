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
    root.imagefile = filedialog.askopenfilename(initialdir="", filetypes=(("png files", "*.png *.jpg *.jpeg"), ("all files", "*.*")))
    fileadress = root.imagefile

    imageinput = Image.open(fileadress).resize((ukurangambar))
    imageacces["image"] = ImageTk.PhotoImage(imageinput)
    labelinsert = Label(root, image=imageacces["image"])
    labelinsert.grid(row=1, column=1)
    
    ambilpixel(imageinput)

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

def grayscale():
    global gray
    global convertgrays
    convertgrays = Image.new("RGB", ukurangambar)
    loadgrayscale = convertgrays.load()

    for data in warna:
        x,y,r,g,b = data
        gray = ((r+g+b)//3) 
        loadgrayscale[x,y]=(gray,gray,gray)
        
    hasilgray["image"] = ImageTk.PhotoImage(convertgrays)
    labelconvertgray = Label(root, image=hasilgray["image"])
    labelconvertgray.grid(row=7, column=1)
    return convertgrays

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
    grayscale_image = grayscale()
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

tombolConvert = Button(root, text="Convert", command=convert)
tombolInputGambar = Button(root, text="Buka File", command=openimage)
tombolReset = Button(root, text= "RESET", command= box)


tombolInputGambar.grid(row=2, column=1,sticky=EW) 
tombolConvert.grid(row=2, column=2,sticky=EW)
tombolReset.grid(row=3, column=1,columnspan=2, sticky = EW)

root.mainloop()