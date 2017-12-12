# ** entry/rubric/serializers.py **
from rest_framework import serializers

from entry.rubric.models import Rubric


class RubricListSerializer(serializers.HyperlinkedModelSerializer):
    children = serializers.HyperlinkedIdentityField(view_name='rubric-children-list')

    class Meta:
        model = Rubric
        fields = ('url', 'id', 'name', 'slug', 'parent', 'level', 'parent_id', 'children')


class RubricDetailSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Rubric
        fields = ('url', 'id', 'name', 'description', 'slug', 'parent', 'children')


class RubricListDisplaySerializer(serializers.ModelSerializer):
    # url = serializers.CharField(source='get_absolute_url', read_only=True)

    class Meta:
        model = Rubric
        fields = ('url', 'id', 'name', 'slug')
