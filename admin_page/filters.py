import django_filters
from upload.models import RefEtatEtape, RefEtapeEtude


class RefEtatEtapeFilter(django_filters.FilterSet):
	class Meta:
		model = RefEtatEtape
		fields = ['nom']


class RefEtapeEtudeFilter(django_filters.FilterSet):
	class Meta:
		model = RefEtapeEtude
		fields = ['nom', 'etude']