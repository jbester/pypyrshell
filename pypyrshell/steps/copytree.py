import shutil
import logging
import os
from pypyr.context import Context
from pypyr.errors import KeyNotInContextError
from dataclasses import dataclass, field
from typing import List

logger = logging.getLogger(__name__)


@dataclass()
class CopyTreeParams:
    source: str
    destination: str
    follow_symlinks: bool = True
    dirs_exist_ok: bool = False
    ignore: List[str] = field(default_factory=list)


def run_step(context: Context) -> None:
    """Copy a tree.

     Args:
         context:  pypyr.context.Context. Mandatory. Should contain keys for:
            - copy: dict, Mandatory.  Keys for:
                - source: os.PathLike, Mandatory.  Source file
                - destination: os.PathLike, Mandatory.  Destination file or folder
                - follow_symlinks: bool, Optional:  Follow symlinks (default: True)
                - ignore: list of strings, Optional: glob patterns to ignore
                - dirs_exist_ok: bool, Optional:  raise an exception in case dst or any missing parent directory exists.
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
    parameters = CopyTreeParams.__annotations__.keys()
    for key in copy_context:
        if key not in parameters:
            raise KeyError(f"Unexpected key {key} in copy")
    # validate required parameters are there
    required_keys = ['source', 'destination']
    for key in required_keys:
        if key not in copy_context:
            raise KeyNotInContextError(f"missing required key '{key}' in copy")
    params = CopyTreeParams(**copy_context)

    ignore_patterns = params.ignore
    # implicitly convert a str to a single element list
    if isinstance(params.ignore, str):
        params.ignore = [ignore_patterns]
    # validate there aren't any other types in the list
    if not all(map(lambda x: isinstance(x, str), params.ignore)):
        raise TypeError("ignore expected to be a list of strings")
    ignore_patterns = shutil.ignore_patterns(*params.ignore)

    # validate parameter types
    if not isinstance(params.source, str):
        raise TypeError(f'source expected to be of type str')

    if not isinstance(params.destination, str):
        raise TypeError(f'destination expected to be of type str')

    if not isinstance(params.follow_symlinks, bool):
        raise TypeError("follow_symlinks expected to be bool")

    if not isinstance(params.dirs_exist_ok, bool):
        raise TypeError("dirs_exist_ok expected to be bool")

    # verify source exists
    if not os.path.exists(params.source):
        raise FileNotFoundError(f"{copy_context['source']} file missing")

    # execute copy
    logger.info(f"copytree source={params.source} dest={params.destination} ignore={params.ignore} " 
                f"symlinks={params.follow_symlinks} dirs_exist_ok={params.dirs_exist_ok}")
    shutil.copytree(params.source, params.destination,
                    ignore=ignore_patterns,
                    symlinks=params.follow_symlinks,
                    dirs_exist_ok=params.dirs_exist_ok)
