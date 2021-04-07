import gizeh

from muvi_maker import main_logger
from .base_bounce import BaseBounce
from .star import Star
from .base_picture import BasePicture


logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('star_with_bounce')
class StarWithBounce(Star, BaseBounce):

    def draw(self, ind):
        super().draw(ind)

        for i in range(self.multiplicity):
            j = i + 1
            if ind > j:
                form = gizeh.star(
                    radius=self.radius[ind - j] * (self.radius_add + j) * self.radius_factor,
                    xy=self.center,
                    fill=None,
                    stroke=self.color[ind - j],
                    stroke_width=self.stroke_width(j),
                    **self.kwargs
                )
                form.draw(self.surface)