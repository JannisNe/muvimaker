import gizeh

from muvi_maker import main_logger
from .base_bounce import BaseBounce
from .circle import Circle
from .base_picture import BasePicture

logger = main_logger.getChild(__name__)


@BasePicture.register_subclass('circle_with_bounce')
class CircleWithBounce(Circle, BaseBounce):

    def draw(self, ind):
        super().draw(ind)

        for i in range(self.multiplicity):
            j = i + 1
            if ind > j:
                form = gizeh.circle(
                    r=self.radius[ind - j] * (self.radius_add + j) * self.radius_factor,
                    xy=self.center,
                    fill=None,
                    stroke=self.color[ind - j],
                    stroke_width=self.stroke_width(j),
                    **self.kwargs
                )
                form.draw(self.surface)