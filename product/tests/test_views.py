import pytest
from django.urls import resolve, reverse

from .factories import ProductFactory

pytestmark = pytest.mark.django_db


class TestProductListView:
    def test_reverse_resolve(self):
        assert reverse("product:list") == "/product/"
        assert resolve("/product/").view_name == "product:list"

        url = reverse("product:list_by_category", kwargs={"slug": "test-slug"})
        assert url == "/product/category/test-slug/"

        view_name = resolve("/product/category/test-slug/").view_name
        assert view_name == "product:list_by_category"

    def test_status_code(self, client, category):
        response = client.get(reverse("product:list"))
        assert response.status_code == 200

        response = client.get(
            reverse("product:list_by_category", kwargs={"slug": category.slug})
        )
        assert response.status_code == 200


class TestProductDetailView:
    def test_reverse_resolve(self, product):
        url = reverse("product:detail", kwargs={"slug": product.slug})
        assert url == f"/product/{product.slug}/"

        view_name = resolve(f"/product/{product.slug}/").view_name
        assert view_name == "product:detail"

    def test_status_code(self, client):
        product = ProductFactory(is_available=True)
        url = reverse("product:detail", kwargs={"slug": product.slug})
        response = client.get(url)
        assert response.status_code == 200