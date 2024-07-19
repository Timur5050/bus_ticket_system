from django.urls import path

from station.views import BusViewSet

bus_list = BusViewSet.as_view(actions={"get": "list", "post": "create"})

bus_detail = BusViewSet.as_view(actions={
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy"
        })

urlpatterns = [
    path("buses/", bus_list, name="bus_list"),
    path("buses/<int:pk>/", bus_detail, name="bus_detail"),
]
app_name = "station"
