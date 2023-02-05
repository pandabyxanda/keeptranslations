from rest_framework import serializers

from .models import Words


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Words
        fields = ('word', 'translation')
