#!/usr/bin/python
from mayavi import mlab
import numpy as np
from scipy import interpolate
from mayavi.api import Engine

__author__ = 'C.A. Miermans (Arnold-Sommerfeld-Center for Theoretical Physics, LMU Munich)'
__date__ = '03-03-2018'
__credits__ = 'C.A. Miermans, C.P. Broedersz'
__license__ = 'GPL'
__version__ = '1.0.0'
__email__ = "c.miermans@lmu.de"
__status__ = "Production"

class TubePlot:
    """
    Class to generate pretty 3d pictures of polymers, based on inputted polymer coordinates.
    """
    def __init__(self, polymer_coordinates, color_scheme='dark'):
        self.engine = Engine()
        self.engine.start()
        self.engine.new_scene()
        self.scene = self.engine.current_scene
        assert color_scheme in ('dark', 'light')  # we right now only have two color schemes
        self.color_scheme = color_scheme
        self.polymer_coordinates = polymer_coordinates
        self.L = self.get_polymer_length()
        self.set_colors()
        self.make_new_fig()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        mlab.clf()
        mlab.close()

    @staticmethod
    def _hex_to_rgb_(val):
        return tuple(int(val.lstrip('#')[i:i + 2], 16) / 256 for i in (0, 2, 4))

    def set_colors(self):
        """
        Based on the private variable self.color_scheme this method sets various other private variables such as the polymer color etc.
        """
        if self.color_scheme == 'dark':
            self.color_polymer = (.8, .8, .8)
        else:
            self.color_polymer = (.5, .5, .5)

    def make_new_fig(self):
        """
        Constructs a figure object with the correct background color based on the color scheme.
        """
        
        mlab.figure(figure=self.scene).scene.background = (.1, .1, .1) if self.color_scheme == 'dark' else (1., 1., 1.)

    def get_polymer_length(self):
        """
        :return: Length of the polymer, of type integer. Based on the raw_attributes.
        """
        return len(self.polymer_coordinates)

    @staticmethod
    def make_coordinates_circular(coordinates):
        """
        Add a coordinate at the end that is equal to the first coordinate.
        :param coordinates: Nx3 numpy array of coordinates in space
        """
        return np.concatenate([coordinates, [coordinates[0, :]]])  # add the first coordinate for constructing a circular interpolation

    @staticmethod
    def translate_coordinates_by_center_of_mass(coordinates):
        """
        Returns coordinates displaced by their center of mass
        :param coordinates: Nx3 numpy array of integer coordinates
        :returns: Nx3 numpy array of displaced coordinates
        """
        return coordinates - np.mean(coordinates, axis=0, dtype=int)

    @staticmethod
    def compute_interpolation(coordinates, interpolation_factor=20):
        """
        Returns an interpolated version of the :param coordinates.
        :param coordinates: Nx3 numpy array of coordinates in space
        :param interpolation_factor: Number of coordinates to return per input coordinate (sets degree of smoothness for the interpolation)
        :returns: N*interpolation x 3 numpy array of coordinates, where now the last coordinate is equal to the first
        """
        # circular_coordinates = self.make_coordinates_circular(coordinates)
        n = len(coordinates)
        N = interpolation_factor * n
        t_old = np.arange(n)
        f = interpolate.interp1d(t_old, coordinates, axis=0, kind='cubic')
        t_new = np.linspace(0, n - 1, num=N, endpoint=True)
        return f(t_new)

    def draw_tube(self, coordinates, color=None, opacity=1., tube_radius=0.5):
        """
        Draws a Mayavi tubeplot on the canvas. Coordinates are retrieved using a different method in this same class.
        """
        mlab.plot3d(coordinates[:, 0], coordinates[:, 1], coordinates[:, 2], np.abs(2*np.arange(-len(coordinates)/2,+len(coordinates)/2))/len(coordinates), tube_radius=tube_radius, tube_sides=40, opacity=opacity, colormap='Spectral', figure=self.scene)

    def draw_all(self):
        """
        Draw polymer, proteins, origin, terminus etc.
        """
        coordinates = self.polymer_coordinates
        coordinates_circular = self.make_coordinates_circular(coordinates)
        coordinates_interpolated = self.compute_interpolation(coordinates_circular)
        self.draw_tube(coordinates_interpolated)

    def add_text(self, string):
        """
        Adds some interesting text to the current mayavi-canvas.
        :param string: String to put in the image
        """
        c = (1.,1.,1.) if self.color_scheme == 'dark' else (0.,0.,0.)
        mlab.text(0.025,0.025, string, color=c, width=0.3)

if __name__ == '__main__':
    import os, h5py
    wd = '/Users/C.Miermans/projects/chromosome/kmc/data/slip-link/ea052/ea052/width_160/Np_32/Thu_Dec_21_15-10-35_2017/'
    os.chdir(wd)
    sample_file_name = 'raw_data.h5'
    sample_file = h5py.File(sample_file_name, mode='r')

    sample_group = sample_file[list(sample_file)[0]]
    X = TubePlot(sample_group, color_scheme='light')

    X.draw_all()
    X.engine.save_visualization('Np_32.mv2')
    mlab.show()
    # X.draw_and_save(names, '')