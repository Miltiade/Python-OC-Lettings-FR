import logging

from django.shortcuts import render, get_object_or_404

from .models import Letting

logger = logging.getLogger(__name__)


def index(request):
    """List all lettings."""
    lettings_list = Letting.objects.all()
    logger.info("Lettings index viewed: %s listings", len(lettings_list))
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """Display a single letting's details."""
    letting = get_object_or_404(Letting, id=letting_id)
    logger.info("Letting detail viewed: id=%s", letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)
