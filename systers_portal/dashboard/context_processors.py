from dashboard.models import Community


def communities_processor(request):
    communities = Community.objects.all().order_by('id')
    return {'communities': communities}
