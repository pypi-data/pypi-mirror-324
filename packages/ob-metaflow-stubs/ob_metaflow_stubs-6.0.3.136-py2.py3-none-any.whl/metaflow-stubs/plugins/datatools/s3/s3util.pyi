######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.13.9.1+obcheckpoint(0.1.6);ob(v1)                                                    #
# Generated on 2025-01-31T18:07:50.873644                                                            #
######################################################################################################

from __future__ import annotations


from ....exception import MetaflowException as MetaflowException

DATATOOLS_CLIENT_PARAMS: dict

DATATOOLS_SESSION_VARS: dict

S3_RETRY_COUNT: int

RETRY_WARNING_THRESHOLD: int

TEST_S3_RETRY: bool

TRANSIENT_RETRY_LINE_CONTENT: str

TRANSIENT_RETRY_START_LINE: str

def get_s3_client(s3_role_arn = None, s3_session_vars = None, s3_client_params = None):
    ...

def aws_retry(f):
    ...

def read_in_chunks(dst, src, src_sz, max_chunk_size):
    ...

def get_timestamp(dt):
    """
    Python2 compatible way to compute the timestamp (seconds since 1/1/1970)
    """
    ...

