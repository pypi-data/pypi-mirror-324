######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.8.1+obcheckpoint(0.1.6);ob(v1)                                                    #
# Generated on 2025-01-30T21:59:34.677286                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

class AirflowException(metaflow.exception.MetaflowException, metaclass=type):
    def __init__(self, msg):
        ...
    ...

class NotSupportedException(metaflow.exception.MetaflowException, metaclass=type):
    ...

