import shutil
import logging
import os
from dataclasses import dataclass
from pypyr.context import Context
from pypyr.errors import KeyNotInContextError

logger = logging.getLogger(__name__)


@dataclass()
class CopyFileParams:
    source: str
    destination: str
    follow_symlinks: bool = True


def run_step(context: Context) -> None:
    """Copy a file.

     Args:
         context:  pypyr.context.Context. Mandatory. Should contain keys for:
            - copy: dict, Mandatory.  Keys for:
                - source: str, Mandatory.  Source file
                - destination: str, Mandatory.  Destination file or folder
                - follow_symlinks: bool, Optional:  Follow symlinks (default: True)
     Returns:
         None.
     Raises:
         pypyr.errors.KeyNotInContextError: required missing in context.
         TypeError: key, value exists in context but has incorrect type
         KeyError: key exists in context but isn't used
     """
    context.assert_key_has_value(key='copy', caller=__name__)
    copy_context = context.get_formatted('copy')

    # validate only expected parameters are present
    parameters = CopyFileParams.__annotations__.keys()
    for key in copy_context:
        if key not in parameters:
            raise KeyError(f"Unexpected key {key} in copy")

    # validate required parameters are there
    if 'source' not in copy_context:
        raise KeyNotInContextError("missing required key 'source' in copy")
    if 'destination' not in copy_context:
        raise KeyNotInContextError("missing required key 'destination' in copy")

    params = CopyFileParams(**copy_context)

    # validate parameters are the expected type
    if not isinstance(params.source, str):
        raise TypeError(f'source expected to be of type str')

    if not isinstance(params.destination, str):
        raise TypeError(f'destination expected to be of type str')

    if not isinstance(params.follow_symlinks, bool):
        raise TypeError(f'follow_symlinks expected to be of type bool')

    # verify source exists
    if not os.path.exists(copy_context['source']):
        raise FileNotFoundError(f"{copy_context['source']} file missing")

    logger.info(f"copy file source={params.source} dest={params.destination} follow_symbols={params.follow_sylinks}")
    # execute copy
    shutil.copyfile(params.source, params.destination, follow_symlinks=params.follow_symlinks)
