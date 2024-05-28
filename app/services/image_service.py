from botocore.exceptions import NoCredentialsError
from fastapi import HTTPException, UploadFile

from app.configs import settings
from app.dtos.image_response import ImageResponse
from app.models.images import Image
from app.utils.s3_ import s3_client

s3 = s3_client()
MAX_FILE_SIZE = 5 * 1024 * 1024
ALLOWED_IMAGE_MIME_TYPES = ["image/jpeg", "image/png", "image/gif"]


async def service_upload_image(file: UploadFile, folder):
    file_contents = await file.read()
    file_size = len(file_contents)

    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds the allowed limit of 5MB")

    if file.content_type not in ALLOWED_IMAGE_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    try:
        s3_key = f"{folder}/{file.filename}"

        # 파일을 S3에 업로드
        s3.put_object(
            Bucket=settings.AWS_S3_BUCKET_NAME, Key=s3_key, Body=await file.read(), ContentType=file.content_type
        )
        # S3 URL 생성
        s3_url = f"https://{settings.AWS_S3_BUCKET_NAME}.s3.amazonaws.com/{s3_key}"
        return s3_url
    except NoCredentialsError:
        raise HTTPException(status_code=500, detail="AWS credentials not available")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def service_save_image(request_data: ImageResponse) -> None:
    url = await service_upload_image(request_data.file, request_data.component)
    request_data.url = url
    await Image.create_image(request_data)
    raise {"message": "Successfully saved Image"}
