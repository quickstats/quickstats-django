from . import models


def subscriptions(request):
    if request.user.is_authenticated:
        return {
            "subscriptions": models.Subscription.objects.filter(
                owner=request.user
            ).values_list("widget_id", flat=True)
        }
    return {"subscriptions": []}
