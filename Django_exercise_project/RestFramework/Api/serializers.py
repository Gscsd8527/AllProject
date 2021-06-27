from Api.models import DataSets
from rest_framework import serializers
from rest_framework.response import Response

class DataSetsSerializers(serializers.ModelSerializer):
    class Meta:
        model = DataSets
        fields = "__all__"
        extra_kwargs = {
            'title': {
                'help_text': '这是标题',
                # 'min_length': 4,
                # 'max_length': 20,
                # 'error_messages': {
                #     'min_length': '4个字符',
                #     'max_length': '20个字符'
                # }
            },
            'date': {
                # 这是备注
                'help_text': '这是时间'
            },
            'source': {
                # 这是备注
                'help_text': '这是来源'
            }
        }


    # def validate(self, attrs):
    #     print('attrs = ', attrs)
    #     A = attrs['title']
    #     print('A=  ', A)
    #     if '英研制' in A:
    #         # raise serializers.ValidationError('评论量不能大于阅读量')
    #         raise serializers.ValidationError({'aa': '评论量不能大于阅读量', 'code': 300})
    #     return attrs