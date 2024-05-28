from fastapi import APIRouter

from app.dtos.image_response import ImageResponse
from app.services.image_service import service_save_image

router = APIRouter(prefix="/api/v1/image", tags=["image"], redirect_slashes=False)


@router.post("/upload")
async def save_image(request_data: ImageResponse) -> None:
    return await service_save_image(request_data)
