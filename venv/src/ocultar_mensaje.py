from PIL import Image
import os

MENSAJE_OCULTO = "Proyecto By Sary Vargas"

def ocultar_mensaje(imagen_path, mensaje=MENSAJE_OCULTO):
    """Inserta un mensaje en los LSB de la imagen PNG o JPG."""
    img = Image.open(imagen_path).convert("RGB")
    pixels = list(img.getdata())
    bits = []

    # Convertir mensaje a bits + carácter nulo al final
    for c in mensaje + "\0":
        ascii_val = ord(c)
        for i in range(7, -1, -1):
            bits.append((ascii_val >> i) & 1)

    new_pixels = []
    bit_idx = 0
    for pixel in pixels:
        r, g, b = pixel
        if bit_idx < len(bits):
            r = (r & ~1) | bits[bit_idx]; bit_idx += 1
        if bit_idx < len(bits):
            g = (g & ~1) | bits[bit_idx]; bit_idx += 1
        if bit_idx < len(bits):
            b = (b & ~1) | bits[bit_idx]; bit_idx += 1
        new_pixels.append((r, g, b))

    img.putdata(new_pixels)
    img.save(imagen_path)
    print(f"Mensaje oculto insertado en {imagen_path}")
    print("Mensaje a insertar:", MENSAJE_OCULTO)
    print("Número de bits:", len(bits))

if __name__ == "__main__":
    img_path = os.path.join(os.path.dirname(__file__), "gracias.png")
    ocultar_mensaje(img_path)
