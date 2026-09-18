import logging

from django.shortcuts import render, get_object_or_404

from .models import Profile

logger = logging.getLogger(__name__)


def index(request):
    """List all profiles."""
    profiles_list = Profile.objects.all()
    logger.info("Profiles index viewed: %s profiles", len(profiles_list))
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """Display a single user's profile."""
    profile = get_object_or_404(Profile, user__username=username)
    logger.info("Profile detail viewed: username=%s", username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
