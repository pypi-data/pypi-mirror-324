from dataclasses import dataclass

class SynthesizersList(list):
    """Representation of the list of `Synthesizer` objects.

    The list inherits directly from Python `list`. The list does not
    communicate with the backend and thus, represent a snapshot at the
    moment it is created.
    """
    @dataclass(init=False)
    class ListItem:
        id: str
        name: str = ...
        creation_date: str = ...
        status: str = ...
        def __init__(self, **_) -> None: ...
