"""
When we handle files with our system we obtain them
in different formats. Sometimes we get them from urls
so they are just a bytes array, and sometimes we 
obtain an image, for example, that has been previously
loaded with its corresponding library.

We try to treat all those files in the same way so we
have created this class to interact with them and make
easier the way we handle them.
"""
from yta_general_utils.file.converter import FileConverter
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.file.enums import FileTypeX
from moviepy import VideoFileClip
from dataclasses import dataclass
from typing import Union

import io


@dataclass
class FileReturn:
    """
    This dataclass has been created to handle a file
    that has been created or downloaded, so we are
    able to return the file itself and also the 
    filename in the same return.
    """

    # TODO: Set valid types
    file: Union[bytes, bytearray, io.BytesIO, any]
    """
    The file content as raw as it was obtained by
    our system, that could be binary or maybe an
    actually parsed file.
    """
    filename: str
    """
    The filename of the obtained file.
    """

    @property
    def file_converted(self):
        """
        The file parsed according to its type. This
        can be the same as 'file' attribute if it
        was obtained in a converted format.
        """
        # Sometimes the file that has been set is
        # already converted, so we just send it
        # as it is
        if PythonValidator.is_instance(self.file, [bytes, bytearray, io.BytesIO]):
            return self.file

        # I do not handle videos in 'binary_to_type'
        # because it is a very difficult process
        if FileTypeX.VIDEO.is_filename_valid(self.filename):
            return VideoFileClip(self.filename)
        
        return FileConverter.binary_to_type(
            self.file,
            self.filename.split('.')[-1]
        )

    def __init__(
        self,
        file: any,
        filename: str
    ):
        self.file = file
        self.filename = filename

