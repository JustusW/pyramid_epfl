# * encoding: utf-8

from solute.epfl.core import epflacl
from solute.epfl.components import Box, Form, TextInput, Text, Link, Image, Button


class LoginBox(Box):
    title = 'Login'  #: Default title for the login box.
    hover_box = True  #: Show the login box hovering in the center of the page.

    unauthorized_warning = 'You are not authorized to see this page!'  #: Default Warning for a forbidden page.
    unauthorized_title = 'Forbidden View'  #: Default title for a forbidden page.

    return_path = '/'  #: Path for the return link on the forbidden page.
    return_text = 'Return to Home'  #: Text for the return link on the forbidden page.

    img_path = None  #: Path to an image to be displayed above the login form.
    img_width = None  #: Width a potential image will be displayed with.
    img_height = None  #: Height a potential image will be displayed with.

    def __init__(self, page, cid, **kwargs):
        """Convenience component handling user login by forwarding it to a custom page function.
        """

    def init_struct(self):
        self.node_list = [
            Form(
                cid='login_form',
                handle_submit=None,
                node_list=[
                    TextInput(
                        name='username',
                        label='Username',
                        placeholder='Username',
                    ),
                    TextInput(
                        name='password',
                        label='Password',
                        placeholder='Password',
                        password=True
                    ),
                    Button(
                        event_name='submit',
                        color='primary',
                        value='Login'
                    )
                ]
            )
        ]

        if epflacl.epfl_check_role('system.Authenticated', self.page.request):
            self.title = self.unauthorized_title
            self.node_list = [
                Text(
                    value=self.unauthorized_warning
                ),
                Link(
                    url=self.return_path,
                    name=self.return_text
                )
            ]

        if self.img_path:
            self.node_list.insert(0, Image(
                image_path=self.img_path,
                width=self.img_width,
                height=self.img_height,
                padding=True
            ))

    def handle_submit(self):
        values = self.page.login_form.get_values()

        if self.page.login(username=values['username'], password=values['password']):
            self.page.jump(self.page.request.matched_route.name)
