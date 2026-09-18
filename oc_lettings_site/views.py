import logging

from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request):
    """Render the site homepage."""
    logger.info("Homepage viewed")
    return render(request, 'index.html')
