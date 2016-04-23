from rest_framework import routers


from dcf.api.viewsets import GroupViewSet, SectionViewSet, ItemViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'sections', SectionViewSet)
router.register(r'items', ItemViewSet)
