from muvi_maker import main_logger
import gizeh
import numpy as np
import math
import moviepy.editor as mpy
import os
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from moviepy.video.io.bindings import mplfig_to_npimage
# import pyqtgraph as pg

default_picture = f'{os.path.dirname(os.path.realpath(__file__))}/default/default.jpg'

logger = main_logger.getChild(__name__)


class Video:

    def __init__(self, sound, framerate, duration, screen_size=[1280, 720], cmap='plasma'):
        self.sound = sound
        self.framerate = framerate
        self.duration = duration
        self.screen_size = [int(s)/2 for s in screen_size]
        self.percussion_power = self.sound.get_percussive_power()
        self.harmonic_power = self.sound.get_harmonic_power()
        self.chroma = self.sound.get_chroma()
        self.harmonic = abs(self.sound.get_harmonic())
        self.color = None
        self.cmap = cm.get_cmap(cmap)
        self.get_smoothed_color()

    def get_color(self):
        logger.debug(f'getting color')
        self.color = [self.cmap(np.argmax(c)/len(c)) for c in self.chroma]

    def get_smoothed_color(self):
        max_inds = [np.argmax(c)/len(c) for c in self.chroma]
        l = list()
        for i in range(len(max_inds)):
            h, b = np.histogram(max_inds[i:i + 10])
            l.append(b[np.argmax(h)])
        self.color = [self.cmap(li) for li in l]
git add
    def _ind(self, t):
        return int(math.floor(t*self.framerate))
    
    def _t(self, ind):
        return ind/self.framerate

    def make_frame_per_frame(self, ind):

        surface = gizeh.Surface(int(self.screen_size[0] * 2), int(self.screen_size[1] * 2))

        middle = (self.screen_size[0], self.screen_size[1])
        max_radius = min(self.screen_size) / 2
        radius = self.percussion_power / max(self.percussion_power) * max_radius
        log_radius = np.log(radius)
        log_radius = log_radius / max(log_radius) * max_radius

        def stars(this_ind, center, this_surface, radius_factor=1):

            star = gizeh.star(
                radius=radius[this_ind] * 2,
                nbranches=10, xy=center, fill=self.color[this_ind]
            )
            star.draw(this_surface)

            if this_ind > 1:
                outer_star1 = gizeh.star(
                    radius=radius[this_ind - 1] * 3 * radius_factor,
                    nbranches=10,
                    xy=center,
                    fill=None,
                    stroke=self.color[this_ind - 1],
                    stroke_width=8,
                )
                outer_star1.draw(this_surface)

            if this_ind > 2:
                outer_star2 = gizeh.star(
                    radius=radius[this_ind - 2] * 4 * radius_factor,
                    nbranches=10,
                    xy=center,
                    fill=None,
                    stroke=self.color[this_ind - 2],
                    stroke_width=4
                )
                outer_star2.draw(this_surface)

            if this_ind > 3:
                outer_star3 = gizeh.star(
                    radius=radius[this_ind - 3] * 5 * radius_factor,
                    nbranches=10,
                    xy=center,
                    fill=None,
                    stroke=self.color[this_ind - 3],
                    stroke_width=1
                )
                outer_star3.draw(this_surface)

        circle = gizeh.circle(log_radius[ind] / 4, xy=middle, fill=self.color[ind])
        circle.draw(surface)
        stars(ind, middle, surface)

        n = self.framerate * 5
        circle_radius = min(self.screen_size)
        circle = [(math.cos(2 * math.pi / n * x) * circle_radius + self.screen_size[0],
                   math.sin(2 * math.pi / n * x) * circle_radius + self.screen_size[1])
                  for x in range(n + 1)]

        n_stars = 5

        if self.harmonic_power[ind] > max(self.harmonic_power) / 2:
            circle_ind = ind % (n - 1)
            for stari in range(n_stars):
                stars(ind, circle[(circle_ind + math.floor(n * stari / n_stars)) % (n - 1)], surface)
            # stars(ind, circle[circle_ind], surface)
            # stars(ind, circle[(circle_ind + math.floor(n * 1/4)) % (n-1)], surface)
            # stars(ind, circle[(circle_ind + math.floor(n * 2/4)) % (n-1)], surface)
            # stars(ind, circle[(circle_ind + math.floor(n * 3/4)) % (n-1)], surface)

        return surface.get_npimage()

    def make_frame_per_time(self, t):
        ind = self._ind(t)
        return self.make_frame_per_frame(ind)

    def make_video(self, filename):
        """ to be implemented in subclasses! """
        
        # logger.info(f'No make video function in subclass. Making default video which is really boring.')
        #
        # middle = (self.screen_size[0], self.screen_size[1])
        # max_radius = min(self.screen_size)/2
        # radius = self.percussion_power / max(self.percussion_power) * max_radius
        # log_radius = np.log(radius)
        # log_radius = log_radius/max(log_radius) * max_radius
        #
        # small_stars_radius = self.harmonic_power / max(self.harmonic_power) * max_radius / 8
        #
        # def make_frame(t):
        #
        #     ind = self._ind(t)
        #     surface = gizeh.Surface(int(self.screen_size[0]*2), int(self.screen_size[1]*2))
        #
        #     def stars(this_ind, center, this_surface, radius_factor=1):
        #
        #         star = gizeh.star(
        #             radius=radius[this_ind]*2,
        #             nbranches=10, xy=center, fill=self.color[this_ind]
        #         )
        #         star.draw(this_surface)
        #
        #         if this_ind > 1:
        #             outer_star1 = gizeh.star(
        #                 radius=radius[this_ind-1]*3*radius_factor,
        #                 nbranches=10,
        #                 xy=center,
        #                 fill=None,
        #                 stroke=self.color[this_ind-1],
        #                 stroke_width=8,
        #             )
        #             outer_star1.draw(this_surface)
        #
        #         if this_ind > 2:
        #             outer_star2 = gizeh.star(
        #                 radius=radius[this_ind-2]*4*radius_factor,
        #                 nbranches=10,
        #                 xy=center,
        #                 fill=None,
        #                 stroke=self.color[this_ind-2],
        #                 stroke_width=4
        #             )
        #             outer_star2.draw(this_surface)
        #
        #         if this_ind > 3:
        #             outer_star3 = gizeh.star(
        #                 radius=radius[this_ind-3]*5*radius_factor,
        #                 nbranches=10,
        #                 xy=center,
        #                 fill=None,
        #                 stroke=self.color[this_ind-3],
        #                 stroke_width=1
        #             )
        #             outer_star3.draw(this_surface)
        #
        #     circle = gizeh.circle(log_radius[ind] / 4, xy=middle, fill=self.color[ind])
        #     circle.draw(surface)
        #     stars(ind, middle, surface)
        #
        #     n = self.framerate * 5
        #     circle_radius = min(self.screen_size)
        #     circle = [(math.cos(2*math.pi/n * x) * circle_radius + self.screen_size[0], math.sin(2*math.pi/n * x) * circle_radius + self.screen_size[1])
        #               for x in range(n+1)]
        #
        #     n_stars = 5
        #
        #     if self.harmonic_power[ind] > max(self.harmonic_power)/2:
        #         circle_ind = ind % (n-1)
        #         for stari in range(n_stars):
        #             stars(ind, circle[(circle_ind + math.floor(n * stari/n_stars)) % (n-1)], surface)
        #         #stars(ind, circle[circle_ind], surface)
        #         #stars(ind, circle[(circle_ind + math.floor(n * 1/4)) % (n-1)], surface)
        #         #stars(ind, circle[(circle_ind + math.floor(n * 2/4)) % (n-1)], surface)
        #         #stars(ind, circle[(circle_ind + math.floor(n * 3/4)) % (n-1)], surface)
        #
        #     return surface.get_npimage()

        clip = mpy.VideoClip(self.make_frame_per_time, duration=self.duration)
        # clip.size = self.screen_size
        logger.debug(f'clip size is {clip.size}')
        logger.debug(f'setting {self.sound.filename} as audio')
        audio = mpy.AudioFileClip(self.sound.filename)
        clip_with_audio = clip.set_audio(audio)
        clip_with_audio.write_videofile(filename, fps=self.framerate)

    def make_param_video(self, storage, filename=None, test_ind=None):

        logger.debug(f'making chromogram video')
        # power = self.sound.get_power()

        fig = plt.figure()
        
        # power_ax = fig.add_subplot(212)
        # ax2 = fig.add_subplot(313, sharex=ax1)
        spectrum_ax = fig.add_subplot(111)

        power_color = 'blue'
        
        # for p in [1, -1]:
        #     power_ax.bar(np.linspace(0, len(power)-1, len(power))/len(power) * self.duration, p*power,
        #                  color=power_color, alpha=0.5)
        # power_line = power_ax.axvline(0, color='k')
        # power_line_y = power_line.get_data()[1]

        freq_line, = spectrum_ax.plot(self.sound.frange, [0]*len(self.sound.frange), color=power_color)
        spectrum_ax.set_xscale('log')
        spectrum_ax.set_yscale('log')
        spectrum_ax.set_ylim([1e-4, max(self.harmonic.flatten())])
        spectrum_ax.set_xlabel('f [Hz]')
        
        # axs[1].imshow(chroma, cmap=chroma_cmap, alpha=0.5)
        plt.tight_layout()

        def update(ind):

            # ind = self._ind(t)
            # t = self._t(ind)

            # --------------------         display power             ------------------- #
            # power_line.set_data(([t]*len(power_line_y), power_line_y))

            # --------------------    display complete chromogram   ------------------- #
            # axs[1].axvline(t, color='k')

            # --------------------   display current chromogram      ------------------- #
            freq_line.set_data(self.sound.frange, self.harmonic[ind])

            return mplfig_to_npimage(fig)

        anim = animation.FuncAnimation(fig, update, interval=1000/self.framerate, frames=len(self.harmonic))
        anim_name = f'{storage}/params.mp4'
        anim.save(anim_name)

        if test_ind:
            return update(self._t(test_ind))

        clip = mpy.VideoFileClip(anim_name)
        # clip = mpy.VideoClip(update, duration=self.duration)
        clip.size = self.screen_size
        logger.debug(f'setting {self.sound.filename} as audio')
        audio = mpy.AudioFileClip(self.sound.filename)
        clip_with_audio = clip.set_audio(audio)
        # clip_with_audio_fps = clip_with_audio.set_fps(self.framerate)
        
        if not filename:
            return clip_with_audio
        else:
            clip.write_videofile(filename, fps=self.framerate)
