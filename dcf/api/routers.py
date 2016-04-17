from rest_framework import routers


from dcf.api.viewsets import GroupViewSet, SectionViewSet

router = routers.DefaultRouter()
router.register(r'groups', GroupViewSet)
router.register(r'sections', SectionViewSet)
