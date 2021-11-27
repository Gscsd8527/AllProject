from rest_framework import serializers
from .models import Information
from apps.User.models import UserInfo


class UserInfoSerializers(serializers.ModelSerializer):
    """
    限定关联显示的字段，只返回一个 username 回去
    """
    class Meta:
        model = UserInfo
        fields = ('username', )


class InformationSerializers(serializers.ModelSerializer):
    # user = UserInfoSerializers()  # 指定要的关联字段  这个字段嵌套了一层

    user = serializers.SlugRelatedField(slug_field='username', read_only=True)  # 这个字段可以不用嵌套

    class Meta:
        model = Information
        fields = "__all__"
        # depth = 1  # depth标识嵌套的级数 : 如果要限制参数，那么就注销这个

