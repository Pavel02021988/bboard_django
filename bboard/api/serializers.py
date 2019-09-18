from rest_framework import serializers
from easy_thumbnails.files import get_thumbnailer
from main.models import Bb, Comment

# сериализатор формирующий список рубрик
class BbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at')

# сведения о выбранном объявлении
class BbDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bb
        fields = ('id', 'title', 'content', 'price', 'created_at', 'contacts', 'image')

# список комментариев и добавление коммента
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('bb', 'author', 'content', 'created_at')
