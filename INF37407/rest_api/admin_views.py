from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.db.models import Count
from .models import Service, Layer, Feature

@staff_member_required
def stats_view(request):
    services_count = Service.objects.count()
    layers_count = Layer.objects.count()
    features_count = Feature.objects.count()

    features_by_service = (
        Feature.objects.values('layer__service__name')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    features_by_geom = (
        Feature.objects.values('geometry_type')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    features_by_date = (
        Feature.objects.extra(select={'day': "date(created_at)"})
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )

    context = {
        'services_count': services_count,
        'layers_count': layers_count,
        'features_count': features_count,
        'features_by_service': features_by_service,
        'features_by_geom': features_by_geom,
        'features_by_date': features_by_date,
        'title': 'Statistiques d’utilisation',
    }

    return render(request, 'admin/stats.html', context)
