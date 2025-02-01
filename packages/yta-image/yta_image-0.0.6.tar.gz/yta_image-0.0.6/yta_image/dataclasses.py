from dataclasses import dataclass
from typing import Union


@dataclass
class ImageResult:
    """
    Class to contain the result of any of our methods
    with images. This will return the image itself 
    and the 'output_filename' if generated.
    """

    image: any
    """
    The image once it's been modified.
    """
    output_filename: Union[str, None]
    """
    The filename in which the image has been stored
    once it's been modified, if requested. Sometimes
    you need the image stored as a file apart from
    being modified, and sometimes you don't.
    """

    def __init__(
        self,
        image: any,
        output_filename: Union[str, None],
    ):
        self.image = image
        self.output_filename = output_filename
