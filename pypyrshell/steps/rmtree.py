import shutil
import logging
import os
from pypyr.context import Context
from pypyr.errors import KeyInContextHasNoValueError, KeyNotInContextError
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass()
class RemoveTreeParams:
    path: str
    ignore_errors: bool = False


def run_step(context: Context) -> None:
    """Remove a tree.

     Args:
         context:  pypyr.context.Context. Mandatory. Should contain keys for:
            - remove: dict, Mandatory.  Keys for:
                - path: os.PathLike, Mandatory.  tree to remove
                - ignore_errors: bool, Optional:  Ignore errors (default: False)
     Returns:
         None.
     Raises:
         pypyr.errors.KeyNotInContextError: required missing in context.
         pypyr.errors.KeyInContextHasNoValueError: key exists but is None.
         NotADirectoryError: path does not exist or is not a directory
     """
    context.assert_key_has_value(key='remove', caller=__name__)
    rm_context = context.get_formatted('remove')

    # validate there are no extra keys
    parameters = RemoveTreeParams.__annotations__.keys()
    for key in rm_context:
        if key not in parameters:
            raise KeyError(f"Unexpected key {key} in remove")

    # validate required key is present
    if 'path' not in rm_context:
        raise KeyNotInContextError('path key missing required in rmtree')

    params = RemoveTreeParams(**rm_context)

    # validate types
    if not isinstance(params.path, str):
        raise TypeError("expected value associated with key path to be a str")
    if not isinstance(params.ignore_errors, bool):
        raise TypeError("expected value associated with key ignore_errors to be a bool")

    # validate path is correct
    if not os.path.exists(params.path):
        raise NotADirectoryError("path not found in rmtree")
    if not os.path.isdir(params.path):
        raise NotADirectoryError("path is not a directory in rmtree")

    # execute rmtree
    logger.info(f"rmtree path={params.path} ignore_errors={params.ignore_errors}")
    shutil.rmtree(params.path, ignore_errors=params.ignore_errors)
