from Api.models import DataSets
from rest_framework import serializers
from rest_framework.response import Response

class DataSetsSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataSets
        fields = "__all__"

    # def validate(self, attrs):
    #     print('attrs = ', attrs)
    #     A = attrs['title']
    #     print('A=  ', A)
    #     if '英研制' in A:
    #         # raise serializers.ValidationError('评论量不能大于阅读量')
    #         raise serializers.ValidationError({'aa': '评论量不能大于阅读量', 'code': 300})
    #     return attrs