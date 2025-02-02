# encoding=utf-8
"""environments classes and illumination fields


An environment class implements:
  
    - Green's tensors, describing environments and their boundary conditions.  
    - illumination fields specific for the environment


.. currentmodule:: torchgdm.env


Environment classes
-------------------

.. autosummary::
   :toctree: generated/

   EnvHomogeneous2D
   EnvHomogeneous3D
   EnvironmentBase


Illumination classes
--------------------

Only the illumination base class is defined here.

.. autosummary::
   :toctree: generated/

   IlluminationfieldBase


The illumination classes are defined in the subpackage of each environment.

.. autosummary::
   :toctree: generated/

   freespace_2d
   freespace_3d
  
"""
from .base_classes import IlluminationfieldBase, EnvironmentBase

from . import freespace_2d
from . import freespace_3d

from .freespace_2d import EnvHomogeneous2D
from .freespace_3d import EnvHomogeneous3D
