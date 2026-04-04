from jet.dashboard.dashboard import Dashboard
from jet.dashboard import modules

class CustomIndexDashboard(Dashboard):
    columns = 2

    def init_with_context(self, context):
        self.children.append(modules.LinkList(
            title='Liên kết nhanh',
            children=[
                {'title': 'Trang chính', 'url': '/', 'external': False},
                {'title': 'Docs Jet', 'url': 'https://django-jet-reboot.readthedocs.io/', 'external': True},
            ]
        ))
        self.children.append(modules.AppList(
            title='Ứng dụng',
            exclude=('django.contrib.*',),
        ))
        self.children.append(modules.ModelList(
            title='Gần đây',
            models=('users.models.CustomUser',)
        ))
