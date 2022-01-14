import shutil
import logging
import os
from pypyr.context import Context
from pypyr.errors import KeyInContextHasNoValueError, KeyNotInContextError
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass()
class RemoveParams:
    path: str


def run_step(context: Context) -> None:
    """Remove a file.

     Args:
         context:  pypyr.context.Context. Mandatory. Should contain keys for:
            - remove: dict, Mandatory.  Keys for:
                - path: os.PathLike, Mandatory.  tree to remove
                - ignore_errors: bool, Optional:  Ignore errors (default: False)
     Returns:
         None.
     Raises:
         pypyr.errors.KeyNotInContextError: required missing in context.
         TypeError: key, value exists in context but has incorrect type
         KeyError: key exists in context but is not expected
     """
    context.assert_key_has_value(key='remove', caller=__name__)
    rm_context = context.get_formatted('remove')

    # validate there are no extra keys
    parameters = RemoveParams.__annotations__.keys()
    for key in rm_context:
        if key not in parameters:
            raise KeyError(f"Unexpected key {key} in remove")

    # get and validate required key
    if 'path' not in rm_context:
        raise KeyNotInContextError('path key missing required in rmtree')

    params = RemoveParams(*rm_context)

    # validate key types
    if not isinstance(params.path, str):
        raise TypeError('expected value associated with key path to be of type str')

    logger.info(f"unlink path={params.path}")
    os.unlink(params.path)
