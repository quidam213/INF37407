from graphene_django import DjangoObjectType
import graphene
from ogsl.models import Service, Layer, Feature

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
        return Service.objects.all().order_by('-created_at')

    def resolve_all_layers(root, info):
        return Layer.objects.all().order_by('-created_at')

    def resolve_all_features(root, info):
        return Feature.objects.all().order_by('-created_at')

class CreateService(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        description = graphene.String()

    service = graphene.Field(ServiceType)

    def mutate(self, info, name, description=None):
        service = Service(name=name, description=description)
        service.save()
        return CreateService(service=service)

class DeleteService(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    ok = graphene.Boolean()

    def mutate(self, info, id):
        service = Service.objects.get(pk=id)
        service.delete()
        return DeleteService(ok=True)

class Mutation(graphene.ObjectType):
    create_service = CreateService.Field()
    delete_service = DeleteService.Field()

schema = graphene.Schema(query=Query)