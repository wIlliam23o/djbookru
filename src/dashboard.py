from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from admin_tools.dashboard import modules, Dashboard, AppIndexDashboard
from django.conf import settings

# to activate your index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_INDEX_DASHBOARD = 'src.dashboard.CustomIndexDashboard'
OFFLINE = getattr(settings, 'OFFLINE', False)

class CustomIndexDashboard(Dashboard):
    """
    Custom index dashboard for src.
    """
    def __init__(self, **kwargs):
        Dashboard.__init__(self, **kwargs)

        # append an app list module for "Administration"
        self.children.append(modules.AppList(
            title=_('Administration'),
            include_list=('django.contrib',),
            css_classes=['collapse', 'open'],
        ))
        
        # append an app list module for "Applications"
        self.children.append(modules.AppList(
            title=_('Applications'),
            exclude_list=('django.contrib',),
            css_classes=['collapse', 'open'],
        ))

        #append a link list module for "quick links"
        self.children.append(modules.LinkList(
            column=2,
            title=_('Quick links'),
            layout='inline',
            draggable=False,
            deletable=False,
            collapsible=False,
            children=[
                {
                    'title': _('Filebrowser'),
                    'url': reverse('fb_browse'),
                },                      
                {
                    'title': _('Return to site'),
                    'url': '/',
                },
                {
                    'title': _('Markdown: Syntax'),
                    'url': 'http://daringfireball.net/projects/markdown/syntax',                
                },
                {
                    'title': _('Change password'),
                    'url': reverse('admin:password_change'),
                },
                {
                    'title': _('Logout'),
                    'url': reverse('admin:logout')
                },
            ]
        ))
        
        if not OFFLINE:
            # append a feed module
            self.children.append(modules.Feed(
                column=2,
                title=_('Latest Django News'),
                feed_url='http://www.djangoproject.com/rss/weblog/',
                limit=5
            ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass


# to activate your app index dashboard add the following to your settings.py:
#
# ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'src.dashboard.CustomAppIndexDashboard'

class CustomAppIndexDashboard(AppIndexDashboard):
    """
    Custom app index dashboard for src.
    """
    def __init__(self, *args, **kwargs):
        AppIndexDashboard.__init__(self, *args, **kwargs)

        # we disable title because its redundant with the model list module
        self.title = ''

        # append a model list module
        self.children.append(modules.ModelList(
            title=self.app_title,
            models=self.models,
        ))

        # append a recent actions module
        self.children.append(modules.RecentActions(
            column=2,
            title=_('Recent Actions'),
            include_list=self.get_app_content_types(),
        ))

    def init_with_context(self, context):
        """
        Use this method if you need to access the request context.
        """
        pass
