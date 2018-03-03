# mayavi_tubeplot

![example image](https://github.com/kmiermans/mayavi_tubeplot/blob/master/snapshot.png)

## Summary
This class makes a pretty 3d visualization of a polymer using Mayavi2 (Mayavi2 is a free, open-source 3d plotting package based on VTK)
This class was e.g. used in Miermans&Broedersz, 2018 (in preparation).

## Usage
Usage is very simple. After you've loaded the necessary modules, simply use, as an example:
```
from mayavi import mlab
coordinates = [[4, 9, -1],[4, 8, -1],[4, 8, -2],[4, 8, -3],[5, 8, -3],[5, 7, -3],[4, 7, -3],[3, 7, -3],[3, 6, -3],[3, 6, -4],[ 4, 6, -4],[ 5, 6, -4],[ 5, 7, -4],[ 6, 7, -4],[ 6, 8, -4],[ 6, 9, -4],[ 5, 9, -4],[ 5, 10, -4],[ 5, 10, -3],[ 6, 10, -3],[ 6, 10, -2],[ 6, 9, -2],[ 6, 9, -1],[ 6, 10, -1],[ 5, 10, -1],[ 5, 11, -1],[ 5, 11, 0],[ 5, 10, 0],[ 5, 10, 1],[ 5, 9, 1],[ 5, 9, 2],[ 4, 9, 2],[ 4, 9, 1],[ 3, 9, 1],[ 3, 10, 1],[ 3, 10, 0],[ 4, 10, 0],[ 4, 9, 0],[ 5, 9, 0],[ 5, 9, -1]]
X = TubePlot(coordinates, color_scheme='light')
X.draw_all()
mlab.show()
```
and you're done! Possibly, you might wish to save the 3d model to inspect later. In that case you would simple add the line
``` X.engine.save_visualization('my_first_3d_model.mv2') ``` after ``` X.draw_all() ```.

## Installation
Installing Mayavi2 can be difficult due to its dependencies. Especially installing VTK can be rather tricky, and is not for the faint hearted. Personally, I would strongly recommend downloading the free (for non-commercial use) **Enthought Suite** (http://code.enthought.com/). Mayavi2 is maintained by Enthought, and therefore the Enthought suite offers a ready-to-use Python development environment that comes with its own copy of VTK and Mayavi. For more information, see http://docs.enthought.com/mayavi/mayavi/installation.html.

