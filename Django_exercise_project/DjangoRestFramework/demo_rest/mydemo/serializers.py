from .models import User
from rest_framework import serializers
from .models import User
class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        # fields = ('name', 'sex', 'age', 'addr')
        fields = '__all__'
    # 重写create方法，在视图中接收前端传过来参数并创建保存
    def create(self, validated_data):
        return User.objects.create(**validated_data)