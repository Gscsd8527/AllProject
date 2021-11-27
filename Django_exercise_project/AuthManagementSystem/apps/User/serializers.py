from rest_framework import serializers
from .models import UserInfo
from Utils.utils import resp_error_status


class UserInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username', 'password', 'real_name', 'email')

    def validate_password(self, data):   # validate_ + 字段名来校验数据
        """
        校验 password 字段
        :param data:
        :return:
        """
        length = len(data)
        if length < 6:
            raise serializers.ValidationError(resp_error_status(msg="密码长度小于6位"))
        if data.isalpha():
            raise serializers.ValidationError(resp_error_status(msg="密码不能都为字符或者数字"))
        return data

    def create(self, validated_data):
        """
        将数据直接创建到数据库中
        :param validated_data:
        :return:
        """
        user = UserInfo.objects.create(**validated_data)
        return user
