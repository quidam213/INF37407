from graphene_django import DjangoObjectType
import graphene
from rest_api.models import Service, Layer, Feature

class ServiceType(DjangoObjectType):
    class Meta:
        model = Service
        fields = '__all__'

class LayerType(DjangoObjectType):
    class Meta:
        model = Layer
        fields = '__all__'

class FeatureType(DjangoObjectType):
    class Meta:
        model = Feature
        fields = '__all__'

class Query(graphene.ObjectType):
    all_services = graphene.List(ServiceType)
    all_layers = graphene.List(LayerType)
    all_features = graphene.List(FeatureType)

    def resolve_all_services(root, info):
        return Service.objects.all()

    def resolve_all_layers(root, info):
        return Layer.objects.all()

    def resolve_all_features(root, info):
        return Feature.objects.all()

class CreateService(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        url = graphene.String(required=True)
        description = graphene.String(required=False)

    service = graphene.Field(ServiceType)

    def mutate(self, info, name, url, description=None):
        service = Service(name=name, url=url, description=description)
        service.save()
        return CreateService(service=service)

class DeleteService(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        try:
            service = Service.objects.get(pk=id)
            service.delete()
            return DeleteService(ok=True)
        except Service.DoesNotExist:
            return DeleteService(ok=False)

class Mutation(graphene.ObjectType):
    create_service = CreateService.Field()
    delete_service = DeleteService.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
