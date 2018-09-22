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
{
  "name": "Album1",
  "code": "album1",
  "author": {
    "name": "Bob"
  },
  "tracks": [
    {
      "song": "track1",
      "index": 1,
      "long_label": "1: track1
    },
    {
      "song": "track2",
      "index": 2
      "long_label": "2: track2
    }
  ]
}
```
