"""Tests for the profiles app."""
import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Profile


@pytest.mark.django_db
class TestProfilesModels:
    """Test cases for profiles models."""

    def test_profile_str(self):
        """Profile.__str__ returns the related username."""
        user = User.objects.create_user(username='TestUser', password='pass1234')
        profile = Profile.objects.create(user=user, favorite_city='Paris')
        assert str(profile) == 'TestUser'


@pytest.mark.django_db
class TestProfilesViews:
    """Test cases for profiles views."""

    def test_index_returns_200_and_context(self, client):
        """Index view returns 200 with profiles_list in context."""
        user = User.objects.create_user(username='IndexUser', password='pass1234')
        Profile.objects.create(user=user, favorite_city='Nice')
        response = client.get(reverse('profiles:index'))
        assert response.status_code == 200
        assert 'profiles_list' in response.context
        assert response.context['profiles_list'].count() == 1

    def test_profile_detail_returns_200_and_context(self, client):
        """Profile detail view returns 200 with correct profile."""
        user = User.objects.create_user(username='DetailUser', password='pass1234')
        profile = Profile.objects.create(user=user, favorite_city='Lyon')
        response = client.get(reverse('profiles:profile', kwargs={'username': 'DetailUser'}))
        assert response.status_code == 200
        assert response.context['profile'] == profile

    def test_profile_detail_404_for_nonexistent(self, client):
        """Profile detail view returns 404 for unknown username."""
        response = client.get(reverse('profiles:profile', kwargs={'username': 'Nobody'}))
        assert response.status_code == 404


class TestProfilesUrls:
    """Test cases for profiles URL resolution."""

    def test_index_url_resolves(self):
        """Index URL resolves to profiles root."""
        assert reverse('profiles:index') == '/profiles/'

    def test_profile_url_resolves(self):
        """Profile URL resolves with username."""
        url = reverse('profiles:profile', kwargs={'username': 'someone'})
        assert url == '/profiles/someone/'
