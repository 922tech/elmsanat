from action_serializer import ModelActionSerializer
from .models.models import Post


class PostSerializer(ModelActionSerializer):
    class Meta:
        model = Post
        fields = ('__all__')
        action_fields = {"list": {"fields": fields}}

