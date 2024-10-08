from fastapi import FastAPI, Request, Response
from fastapi.responses import Response
import qrcode
from io import BytesIO

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

        if image_format not in ['JPEG', 'PNG', 'WEBP']:
            return Response(content='Invalid image format', status_code=400)

        qr = qrcode.make(text)

        img = qr.get_image()

        if size != 200:
            img = img.resize((size, size))

        with BytesIO() as buffer:
            img.save(buffer, format=image_format)
            img_data = buffer.getvalue()

        return Response(content=img_data, media_type=f'image/{image_format.lower()}')

    except Exception as e:
        return Response(content=str(e), status_code=500)
