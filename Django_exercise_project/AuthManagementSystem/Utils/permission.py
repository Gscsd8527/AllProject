from apps.User.models import UserInfo

class ChcekPremission:
    """
    校验权限,判断权限大于多少才能操作
    """
    def has_permission(self, request, view):
        user_id = request.user['user_id']
        user = UserInfo.objects.filter(id=user_id).first().role.all()
        p_v = [_.title_id for _ in user]
        # print(p_v)
        min_v = min(p_v)
        if min_v < 2:
            print('您的最大权限小于 2, 允许执行')
            return True
        print('您的最大权限大于2， 不允许执行')
        return False

