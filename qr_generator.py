import qrcode

def generate_qr(url, filename="qr_code.png"):
    # Crear el código QR
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Crear la imagen del código QR
    img = qr.make_image(fill="black", back_color="white")
    
    # Guardar la imagen
    img.save(filename)
    print(f"Código QR generado y guardado como {filename}")

if __name__ == "__main__":
    app_url = "http://192.168.0.13:8000"  # URL de la app web
    generate_qr(app_url)
