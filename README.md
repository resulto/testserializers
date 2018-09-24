# Django REST Framework - Serializers

This repository experiments with Django REST Framework serializers.

## Installation instructions

```
git clone https://github.com/resulto/testserializers.git
cd testserializers
pip install -r requirements.txt
# Optional but recommended!
pip install ipython
./manage.py migrate
./manage.py loaddata music_db.json
./manage.py shell
```

## Nested Model Serializers

```python
from music.models import Track, Author, Album
from music.serializers import AlbumSerializer
import json
album = Album.objects.get(pk=1)
album_serializer = AlbumSerializer(album)
print(json.dumps(album_serializer.data, indent=2))

# {
#   "name": "Album1",
#   "code": "album1",
#   "author": {
#     "name": "Bob"
#   },
#   "tracks": [
#     {
#       "song": "track1",
#       "index": 1,
#       "long_label": "1: track1
#     },
#     {
#       "song": "track2",
#       "index": 2
#       "long_label": "2: track2
#     }
#   ]
# }
```


## Serializing arbitrary objects

```python
from music.models import Track, Author, Album
from music.serializers import AlbumLikeChoiceSerializer
import json
# No need to convert to list, an iterable like a QuerySet is fine.
albums = Album.objects.all()
album_choice_serializer = AlbumLikeChoiceSerializer(albums, many=True)
print(json.dumps(album_choice_serializer.data, indent=2))

# [
#   {
#     "label": "Album1",
#     "code": "album1",
#     "internal_id": 1
#   },
#   {
#     "label": "Album2",
#     "code": "album2",
#     "internal_id": 2
#   },
#   {
#     "label": "Album3",
#     "code": "album3",
#     "internal_id": 3
#   }
# ]
```


## Validating simple JSON input

```python
from music.serializers import SimpleAjaxFormSerializer
import json

valid_data1 = {
    "your_website": "http://www.example.com",
    "age": 10,
    "interest": "key2"
}

# Extra data is valid. No need to remove it from the dict.
valid_data2 = {
    "age": 9,
    "interest": "key1",
    "extra": "extra"
}

valid_data3 = {
    "age": 9,
    "interest": "key1",
    "extra": "extra",
    "answer": "bob"
}

invalid_data1 = {
}

invalid_data2 = {
    "age": "nine",
    "interest": "key3",
    "your_website": "hello"
}

invalid_data3 = {
    "age": 9,
    "interest": "key1",
    "extra": "extra",
    "answer": "test"
}

serializer = SimpleAjaxFormSerializer(data=valid_data1)
serializer.is_valid()
# True

serializer.validated_data
# OrderedDict([('your_website', 'http://www.example.com'),
#             ('age', 10),
#             ('interest', 'key2')])

serializer = SimpleAjaxFormSerializer(data=valid_data2)
serializer.is_valid()
# True

serializer = SimpleAjaxFormSerializer(data=valid_data3)
serializer.is_valid()
# True

serializer = SimpleAjaxFormSerializer(data=invalid_data1)
serializer.is_valid()
# False
serializer.validated_data
# {}

serializer = SimpleAjaxFormSerializer(data=invalid_data2)
serializer.is_valid()
# False
serializer.validated_data
# {}

serializer = SimpleAjaxFormSerializer(data=invalid_data3)
serializer.is_valid()
# False
serializer.validated_data
# {}
serializer.errors
# {'answer': [ErrorDetail(string='Invalid input.', code='invalid')]}

```


## Validating complex JSON input

```python
valid_data4 = {
    "age": 9,
    "interest": "key1",
    "extra": "extra",
    "best_url": {
        "site_name": "test",
        "url": "http://www.example.com"
    },
    "urls": [
        {
            "site_name": "test",
            "url": "http://www.example.com"
        }
    ]
}

serializer = SimpleAjaxFormSerializer(data=valid_data4)
serializer.is_valid()
# True
serializer.validated_data
# OrderedDict([('age', 9),
#              ('interest', 'key1'),
#              ('best_url',
#               OrderedDict([('site_name', 'test'),
#                            ('url', 'http://www.example.com')])),
#              ('urls',
#               [OrderedDict([('site_name', 'test'),
#                             ('url', 'http://www.example.com')])])])

invalid_data4 = {
    "age": 9,
    "interest": "key1",
    "extra": "extra",
    "best_url": {
        "site_name": "test",
        "url": "test3"
    },
    "urls": [
        {
            "site_name": "test",
            "url": "test4"
        }
    ]
}


serializer = SimpleAjaxFormSerializer(data=invalid_data4)
serializer.is_valid()
# False
serializer.validated_data
# {}
serializer.errors
# {'best_url': {'url': [ErrorDetail(string='Enter a valid URL.', code='invalid')]}, 'urls': [{'url': [ErrorDetail(string='Enter a valid URL.', code='invalid')]}]}
```
