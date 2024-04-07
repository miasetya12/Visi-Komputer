from PIL import Image

def reflect_vertical(gambar, nama_gambar_disave):
    citra = Image.open(gambar)
    #pixel = citra.load()

    ukuran_horizontal = citra.size[0]
    ukuran_vertikal = citra.size[1]

    x0 = 146

    # buat citra baru
    citra_new = Image.new("RGB", (ukuran_horizontal, ukuran_vertikal))
    #pixel_new = citra_new.load()

    for y in range(ukuran_vertikal):
        for x in range(ukuran_horizontal):

            # rumus dari web anis
            x_new = -x + (2 * x0)

            # pastikan gak lewat batas gambar (gak ngerti mksdnya tapi harus)
            if 0 <= x_new < ukuran_horizontal:
                # ambil pixel gambar asli dan pake untuk ke pixel baru
                pixel_new = citra.getpixel((x,y))
                citra_new.putpixel((x_new, y), pixel_new)
    
    citra_new.save(nama_gambar_disave)


reflect_vertical('garis.PNG', 'garis_reflect_vertical.PNG')



