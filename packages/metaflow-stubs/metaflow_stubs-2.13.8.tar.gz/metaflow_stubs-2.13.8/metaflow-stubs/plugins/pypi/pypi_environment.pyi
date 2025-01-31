######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.8                                                                                 #
# Generated on 2025-01-30T22:35:29.244311                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.pypi.conda_environment

from .conda_environment import CondaEnvironment as CondaEnvironment

class PyPIEnvironment(metaflow.plugins.pypi.conda_environment.CondaEnvironment, metaclass=type):
    ...

