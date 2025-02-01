######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.9.1+obcheckpoint(0.1.6);ob(v1)                                                    #
# Generated on 2025-01-31T18:07:50.798103                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.exception

from ...exception import MetaflowException as MetaflowException

KUBERNETES_NAMESPACE: str

CLIENT_REFRESH_INTERVAL_SECONDS: int

class KubernetesClientException(metaflow.exception.MetaflowException, metaclass=type):
    ...

class KubernetesClient(object, metaclass=type):
    def __init__(self):
        ...
    def get(self):
        ...
    def list(self, flow_name, run_id, user):
        ...
    def kill_pods(self, flow_name, run_id, user, echo):
        ...
    def job(self, **kwargs):
        ...
    def jobset(self, **kwargs):
        ...
    ...

