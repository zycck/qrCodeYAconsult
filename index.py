from flask import Flask, request, send_file
import qrcode
import base64
from io import BytesIO

app = Flask(__name__)


@app.route('/generate_qr_code', methods=['GET'])
def generate_qr_code():
    try:
        # Получаем параметры из URL запроса
        text = request.args.get('text')
        size = int(request.args.get('size', 200))
        image_format = request.args.get('format', 'PNG').upper()

        if not text:
            return 'Parameter "text" is required', 400

        if image_format not in ['JPEG', 'PNG', 'BASE64']:
            return 'Invalid image format', 400

        # Создаем QR-код
        qr = qrcode.make(text)

        # Изменяем размер QR-кода, если указан параметр size
        if size != 200:
            qr = qr.resize((size, size))

        # Если указан формат BASE64, возвращаем QR-код в формате base64
        if image_format == 'BASE64':
            with BytesIO() as buffer:
                qr.save(buffer, format='PNG')
                base64_encoded_img = base64.b64encode(
                    buffer.getvalue()).decode('utf-8')
            return base64_encoded_img

        # Иначе возвращаем изображение QR-кода в указанном формате
        with BytesIO() as buffer:
            qr.save(buffer, format=image_format)
            img_data = buffer.getvalue()

        return send_file(BytesIO(img_data), mimetype=f'image/{image_format.lower()}')

    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    app.run()
