# coding: utf-8

from solute.epfl.components.link.link import Link


class Breadcrumb(Link):
    breadcrumb = True  #: The link is used as a breadcrumb per default.

    def __init__(self, page, cid, url=None, route=None, name=None, icon=None, **extra_params):
        """Convenience component that can be used for creating breadcrumbs.

        Usage:
        .. code-block:: python

            self.page.breadcrumbs.add_component(
                components.Breadcrump(
                    name='Home',
                    url='/',
                    slot='left'
                )
            )

        :param url: The url the breadcrumb points to. Used as src attribute of the A-Tag.
        :param route: The route this link points to. Used to look up the url for the src attribute of the A-Tag.
        :param name: The name displayed for this breadcrumb.
        :param icon: The icon to be displayed in front of the text.
        """
        super(Breadcrumb, self).__init__(page, cid, url=url, route=route, name=name, icon=icon, **extra_params)
