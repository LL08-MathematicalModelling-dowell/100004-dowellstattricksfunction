from rest_framework import serializers

class inputfields(serializers.Serializer):
    Process_id = serializers.IntegerField()
    processSequenceId = serializers.IntegerField()
    title = serializers.CharField()
    CSV = serializers.CharField(required=False,allow_blank=True)
    seriesvalues = serializers.DictField(required=False,allow_null=True)