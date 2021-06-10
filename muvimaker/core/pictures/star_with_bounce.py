import gizeh

from muvimaker import main_logger
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
                radius = self.radius[ind - j]

                if radius >= self.bounce_sensitive_radius * max(self.radius):
                    form = gizeh.star(
                        radius=radius * (self.radius_add + j) * self.radius_factor,
                        xy=self.center,
                        fill=None,
                        stroke=self.color[ind - j],
                        stroke_width=self.stroke_width(j),
                        **self.kwargs
                    )
                    form.draw(self.surface)