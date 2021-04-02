from .base_form import BaseForm
from .base_picture import BasePicture


@BasePicture.register_subclass('circle')
class Circle(BaseForm):

    @property
    def form(self):
        return 'circle'
