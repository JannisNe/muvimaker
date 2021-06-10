import gizeh

from .base_form import BaseForm
from .base_picture import BasePicture


@BasePicture.register_subclass('circle')
class Circle(BaseForm):

    def draw(self, ind):
        circle = gizeh.circle(
            r=self.radius[ind],
            xy=self.center,
            fill=self.color[ind],
            **self.kwargs
        )
        circle.draw(self.surface)
