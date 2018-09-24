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


class AlbumLikeChoiceSerializer(serializers.Serializer):
    """Note: this is not a ModelSerializer. We accept any object that has a
    name, code, and pk :-)

    No need for Meta because this is not a ModelSerializer
    """

    label = serializers.SerializerMethodField()
    code = serializers.SerializerMethodField()
    internal_id = serializers.SerializerMethodField()

    def get_label(self, obj):
        return obj.name

    def get_code(self, obj):
        return obj.code

    def get_internal_id(self, obj):
        return obj.pk


class UrlInputSerializer(serializers.Serializer):
    site_name = serializers.CharField()
    url = serializers.URLField()


class SimpleAjaxFormSerializer(serializers.Serializer):

    your_website = serializers.URLField(required=False)
    age = serializers.IntegerField()
    interest = serializers.ChoiceField(
        choices=(("key1", "Interest 1"), ("key2", "Interest 2")))
    # Because of https://github.com/encode/django-rest-framework/issues/3383
    # there is currently no way to set choices dynamically. You should validate
    # a choice with a validate method instead.
    answer = serializers.CharField(required=False)
    best_url = UrlInputSerializer(required=False)
    urls = UrlInputSerializer(many=True, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Can run arbitrary code such as a query set!
        self.answer_choices = ["bob", "alice", "carl"]

    def validate_answer(self, value):
        if value not in self.answer_choices:
            raise serializers.ValidationError
        return value
