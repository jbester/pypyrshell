import shutil
import logging
from dataclasses import dataclass
from pypyr.context import Context
from pypyr.errors import KeyInContextHasNoValueError, KeyNotInContextError

logger = logging.getLogger(__name__)


@dataclass()
class MoveParams:
    source: str
    destination: str


def run_step(context: Context) -> None:
    """Move a file or directory recursively

     Args:
         context:  pypyr.context.Context. Mandatory. Should contain keys for:
            - move: dict, Mandatory.  Keys for:
                - source: str, Mandatory.  Source file
                - destination: str, Mandatory.  Destination file or folder
     Returns:
         None.
     Raises:
         pypyr.errors.KeyNotInContextError: required missing in context.
         pypyr.errors.KeyInContextHasNoValueError: key exists but is None.
         TypeError: key, value exists in context but has incorrect type
         KeyError: key exists in context but is not expected

     """
    context.assert_key_has_value(key='move', caller=__name__)
    move_context = context.get_formatted('move')

    # validate only expected parameters are present
    parameters = MoveParams.__annotations__.keys()
    for key in move_context:
        if key not in parameters:
            raise KeyError(f"Unexpected key {key} in move")
    for key in parameters:
        if key not in move_context:
            raise KeyNotInContextError(f"required key '{key}' is missing in move context")

    params = MoveParams(**move_context)
    # check keys are of the correct type
    if not isinstance(params.source, str):
        raise TypeError('expected value associated with key source to be of type str')
    if not isinstance(params.destination, str):
        raise TypeError('expected value associated with key destination to be of type str')

    # execute move
    logger.info(f"move source={params.source} destiantion={params.destination}")
    shutil.move(params.source, params.destination)
