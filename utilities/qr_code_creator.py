import qrcode
import base64
import io


def generate_qr_code(url: str, debug: bool = False) -> str:
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=5,
        border=2,
    )

    if debug:
        qr.add_data(f"http://localhost:8000")
    else:
        qr.add_data(url)

    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="#f5f5f5")
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format="PNG")
    img_byte_arr.seek(0)

    encoded_img = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded_img}"
