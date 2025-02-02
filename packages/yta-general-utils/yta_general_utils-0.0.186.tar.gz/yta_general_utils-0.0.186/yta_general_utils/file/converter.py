from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.file.enums import FileType
from pydub import AudioSegment
from PIL import Image
from typing import Union

import io


# TODO: Please, rename this as this name is not
# very descriptive because you expect to be able
# to turn mp3 to wav files or similar. Maybe
# BinaryFileHandler (?)
class FileConverter:
    """
    Class to simplify the way we work with file
    conversions.
    """

    @staticmethod
    def binary_to_type(
        file: Union[bytes, bytearray, io.BytesIO],
        file_type: FileType
    ) -> Union[Image.Image, AudioSegment, io.BytesIO]:
        """
        Parses the provided binary or file in memory 'file'
        and turn it into its specific format according to 
        the provided 'file_type'.
        """
        if not PythonValidator.is_instance(file, [bytes, bytearray, io.BytesIO]):
            raise Exception('The provided "file" parameter is not bytes or bytearray.')
        
        file_type = FileType.to_enum(file_type)
        
        if PythonValidator.is_instance(file, [bytes, bytearray]):
            # If bytes, load as a file in memory
            file = io.BytesIO(file)

        return {
            FileType.AUDIO: AudioSegment.from_file(file),
            FileType.IMAGE: Image.open(file),
            # TODO: I don't know how to handle a video file properly,
            # I think I need to write it and read as a file but this
            # is not what I expect to receive here
            FileType.VIDEO: file
        }[file_type]