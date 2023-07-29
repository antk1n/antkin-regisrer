from rest_framework import serializers
from OsauhingAPP.models import Isikud, Osauhing_Isikud, Osauhing

# serializerid iga mudeli kohta

class IsikudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Isikud
        fields = (
                'id',
                'isikutyyp',
                'isosauhing',
                'nimi',
                'perenimi',
                'kood'
                )
        

class OsauhingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Osauhing
        fields = (
                'id',
                'isik',
                'asutamisekp',
                'kogukapital'
                )
        
class Osauhing_IsikudSerializer(serializers.ModelSerializer):
    class Meta:
        model = Osauhing_Isikud
        fields = (
                'id',
                'osauhing',
                'isik',
                'osauhinguOsa',
                'isasutaja'
                )
