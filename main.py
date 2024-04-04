from fastapi import FastAPI, Request, Response
from fastapi.responses import Response
import qrcode
import base64
from io import BytesIO
from PIL import Image

app = FastAPI()


@app.get('/generate_qr_code')
async def generate_qr_code(request: Request, response: Response):
    try:
        # Получаем параметры из URL запроса
        text = request.query_params.get('text')
        size = int(request.query_params.get('size', 200))
        image_format = request.query_params.get('format', 'PNG').upper()

        if not text:
            return Response(content='Parameter "text" is required', status_code=400)

        if image_format not in ['JPEG', 'PNG', 'BASE64']:
            return Response(content='Invalid image format', status_code=400)

        # Создаем QR-код
        qr = qrcode.make(text)

        # Переводим QR-код в формат изображения
        img = qr.get_image()

        # Изменяем размер QR-кода, если указан параметр size
        if size != 200:
            img = img.resize((size, size))

        # Если указан формат BASE64, возвращаем QR-код в формате base64
        if image_format == 'BASE64':
            with BytesIO() as buffer:
                img.save(buffer, format='PNG')
                base64_encoded_img = base64.b64encode(
                    buffer.getvalue()).decode('utf-8')
            return Response(content=base64_encoded_img, media_type='text/plain')

        # Иначе возвращаем изображение QR-кода в указанном формате
        with BytesIO() as buffer:
            img.save(buffer, format=image_format)
            img_data = buffer.getvalue()

        return Response(content=img_data, media_type=f'image/{image_format.lower()}')

    except Exception as e:
        return Response(content=str(e), status_code=500)
