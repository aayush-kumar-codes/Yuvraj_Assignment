from rest_framework.routers import SimpleRouter

from .views import ListLocationViewSet

router = SimpleRouter()
router.register(r'countries', ListLocationViewSet)