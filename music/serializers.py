from rest_framework import serializers

from music.models import Author, Track, Album


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ("name", )


class TrackSerializer(serializers.ModelSerializer):
    long_label = serializers.SerializerMethodField()

    def get_long_label(self, obj):
        return "{0}: {1}".format(obj.index, obj.song)

    class Meta:
        model = Track
        fields = ("song", "index", "long_label")


class AlbumSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ("name", "code", "author", "tracks")
