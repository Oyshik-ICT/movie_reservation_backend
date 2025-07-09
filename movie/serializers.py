from rest_framework import serializers
from .models import Movie
from actor.models import Actor_Detail

class BulkActorPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if not hasattr(self.root, "_prefetched_actor"):
            actor_ids = []

            if hasattr(self.root, "initial_data") and "actor" in self.root.initial_data:
                if hasattr(self.root.initial_data, 'getlist'):
                    actor_ids = self.root.initial_data.getlist("actor")
                else:
                    actor_ids = self.root.initial_data["actor"]

            if actor_ids:
                    actors = self.get_queryset().filter(id__in=actor_ids)

                    self.root._prefetched_actor = {
                        str(actor.pk): actor
                        for actor in actors
                    }

        if hasattr(self.root, "_prefetched_actor") and str(data) in self.root._prefetched_actor:
                return self.root._prefetched_actor[str(data)]
            
        return super().to_internal_value(data)



class MovieSerializer(serializers.ModelSerializer):
    actor = BulkActorPrimaryKeyRelatedField(queryset=Actor_Detail.objects.all(), many=True)
    class Meta:
        model = Movie
        fields = ["id", "title", "description", "genre", "language", "actor", "poster", "release_date"]

        extra_kwargs = {"id": {"read_only": True}}

    def update(self, instance, validated_data):
        update_fields = []
        actors_data = validated_data.pop("actor", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
            update_fields.append(attr)

        if update_fields:
            instance.save(update_fields=update_fields)

        if actors_data:
             instance.actor.set(actors_data)

        return instance
                  
              