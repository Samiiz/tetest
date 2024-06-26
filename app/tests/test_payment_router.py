from httpx import AsyncClient
from tortoise.contrib.test import TestCase

from app import app
from app.models.categories import Category
from app.models.payments import Payment
from app.models.products import Product
from app.models.users import User


class TestPaymentRouter(TestCase):
    @staticmethod
    async def create_test_user() -> User:
        return await User.create(
            name="test_user",
            email="gudqls0516@naver.com",
            password="pw12345",
            gender="남",
            age=12,
            contact="test",
            nickname="nick",
            content="sdwdw",
        )

    @staticmethod
    async def create_test_category() -> Category:
        return await Category.create(item_id=2, parent_id=2, sqe=2, name="나는 카테고리")

    @staticmethod
    async def create_test_product(category_id: int, user_id: int) -> Product:
        return await Product.create(
            name="test_product",
            content="test content",
            bid_price=1,
            duration=1,
            modify=False,
            status="1",
            grade="상",
            category_id=category_id,
            user_id=user_id,
        )

    async def test_router_create_payment(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            # 테스트에 필요한 사용자 생성
            user_test = await self.create_test_user()
            category_test = await self.create_test_category()
            product_test = await self.create_test_product(user_id=user_test.id, category_id=category_test.id)

            # POST 요청에 사용될 데이터
            data = {"user_id": user_test.id, "total_amount": 100.0, "product_ids": [product_test.id]}

            # POST 요청을 보내고 응답을 받음
            response = await ac.post("/api/v1/payments/", json=data)

            # 응답 상태 코드 확인
            assert response.status_code == 201

    async def test_router_get_by_payment_id(self) -> None:
        async with AsyncClient(app=app, base_url="http://test") as ac:
            user_test = await self.create_test_user()
            category_test = await self.create_test_category()
            product_test = await self.create_test_product(user_id=user_test.id, category_id=category_test.id)
            payment_test = await Payment.create(
                user_id=user_test.id,
                total_amount=100.0,
            )
            await payment_test.products.add(product_test)
            # GET 요청을 보내고 응답을 받음
            response = await ac.get(f"/api/v1/payments/{payment_test.id}/")

            # 응답 상태 코드 확인
            assert response.status_code == 200

            # 응답 데이터 확인
            response_data = response.json()
            assert response_data["user_id"] == payment_test.user_id
            assert response_data["total_amount"] == payment_test.total_amount
            assert len(response_data["products"]) == 1
