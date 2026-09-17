"""Tests for the lettings app."""
import pytest
from django.urls import reverse

from .models import Address, Letting


@pytest.mark.django_db
class TestLettingsModels:
    """Test cases for lettings models."""

    def test_address_str(self):
        """Address.__str__ returns formatted address."""
        address = Address.objects.create(
            number=123,
            street="Main St",
            city="Beverly Hills",
            zip_code=90210,
            country_iso_code="USA"
        )
        assert str(address) == "123 Main St"

    def test_letting_str(self):
        """Letting.__str__ returns letting title."""
        address = Address.objects.create(
            number=456,
            street="Oak Ave",
            city="New York",
            zip_code=10001,
            country_iso_code="USA"
        )
        letting = Letting.objects.create(title="Cozy Apartment", address=address)
        assert str(letting) == "Cozy Apartment"


@pytest.mark.django_db
class TestLettingsViews:
    """Test cases for lettings views."""

    def test_index_returns_200_and_context(self, client):
        """Index view returns 200 with lettings_list in context."""
        address = Address.objects.create(
            number=111,
            street="Test St",
            city="Testville",
            zip_code=12345,
            country_iso_code="Testland"
        )
        Letting.objects.create(title="Test Listing", address=address)
        response = client.get(reverse('lettings:index'))
        assert response.status_code == 200
        assert 'lettings_list' in response.context
        assert response.context['lettings_list'].count() == 1

    def test_letting_detail_returns_200_and_context(self, client):
        """Letting detail view returns 200 with correct context."""
        address = Address.objects.create(
            number=789,
            street="Detail Rd",
            city="Detailtown",
            zip_code=54321,
            country_iso_code="Detailia"
        )
        letting = Letting.objects.create(title="Detailed Property", address=address)
        url = reverse('lettings:letting', kwargs={'letting_id': letting.id})
        response = client.get(url)
        assert response.status_code == 200
        assert response.context['title'] == "Detailed Property"
        assert response.context['address'] == address

    def test_letting_detail_404_for_nonexistent(self, client):
        """Letting detail view returns 404 for nonexistent ID."""
        url = reverse('lettings:letting', kwargs={'letting_id': 9999})
        response = client.get(url)
        assert response.status_code == 404


@pytest.mark.django_db
class TestLettingsUrls:
    """Test cases for lettings URL resolution."""

    def test_index_url_resolves(self):
        """Index URL resolves to index view."""
        url = reverse('lettings:index')
        assert url == '/lettings/'

    def test_letting_url_resolves(self):
        """Letting URL resolves to letting view with ID."""
        url = reverse('lettings:letting', kwargs={'letting_id': 42})
        assert url == '/lettings/42/'
