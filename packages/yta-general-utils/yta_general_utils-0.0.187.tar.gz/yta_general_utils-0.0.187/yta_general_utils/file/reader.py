from yta_general_utils.file.checker import FileValidator
from yta_general_utils.programming.parameter_validator import PythonValidator
from yta_general_utils.file.enums import FileTypeX
from yta_general_utils.file.reader import FileReader
from yta_general_utils.programming.parameter_validator import PythonValidator
from moviepy import VideoFileClip
from pydub import AudioSegment
from PIL import Image
from typing import Union

import json
import io


class FileReader:
    """
    Class to simplify and encapsulate the functionality related
    with reading files.
    """

    @staticmethod
    def read_json(
        filename: str
    ):
        """
        Reads the provided 'filename' and returns the information 
        as a json (if possible).

        Parameters
        ----------
        filename : str
            File path from which we want to read the information.
        """
        if not PythonValidator.is_string(filename) or not FileValidator.file_exists(filename):
            raise Exception('The provided "filename" is not a valid string or filename.')
        
        with open(filename, encoding = 'utf-8') as json_file:
            return json.load(json_file)
        
    @staticmethod
    def read_lines(
        filename: str
    ):
        """
        Read the content of the provided 'filename'
        if valid and return it as it decomposed in
        lines.

        Parameters
        ----------
        filename : str
            File path from which we want to read the information.
        """
        if not PythonValidator.is_string(filename) or not FileValidator.file_exists(filename):
            raise Exception('The provided "filename" is not a valid string or filename.')
        
        with open(filename, 'r', encoding = 'utf-8') as file:
            return file.readlines()
        
    @staticmethod
    def read(
        filename: str
    ):
        """
        Read the content of the provided 'filename'
        if valid and return it as it is.

        Parameters
        ----------
        filename : str
            File path from which we want to read the information.
        """
        if not PythonValidator.is_string(filename) or not FileValidator.file_exists(filename):
            raise Exception('The provided "filename" is not a valid string or filename.')
        
        with open(filename, 'r', encoding = 'utf-8') as file:
            return file.read()

    @staticmethod
    def parse_file_content(
        file_content: Union[bytes, bytearray, io.BytesIO],
        file_type: FileTypeX
    ) -> Union[VideoFileClip, str, AudioSegment, Image.Image]:
        """
        Parse the provided 'file_content' with the given
        'file_type' and return that content able to be
        handled.

        This method is capable to detect videos, subtitles,
        audio and images.
        """
        if not PythonValidator.is_instance(file_content, [bytes, bytearray, io.BytesIO]):
            raise Exception('The provided "file_content" parameter is not bytes or bytearray.')
        
        file_type = FileTypeX.to_enum(file_type)
        
        if PythonValidator.is_instance(file_content, [bytes, bytearray]):
            # If bytes, load as a file in memory
            file_content = io.BytesIO(file_content)

        return {
            FileTypeX.VIDEO: VideoFileClip(file_content),
            FileTypeX.SUBTITLE: file_content.getvalue().decode('utf-8'),
            FileTypeX.TEXT: file_content.getvalue().decode('utf-8'),
            FileTypeX.AUDIO: AudioSegment.from_file(file_content),
            FileTypeX.IMAGE: Image.open(file_content)
        }[file_type]

    @staticmethod
    def parse_filename(
        filename: str,
    ) -> Union[VideoFileClip, str, AudioSegment, Image.Image]:
        """
        Identify the provided 'filename' extension and open
        it according to the detected file type.

        This method is capable to detect videos, subtitles,
        audio and images.
        """
        return {
            FileTypeX.VIDEO: VideoFileClip(filename),
            FileTypeX.SUBTITLE: FileReader.read(filename),
            FileTypeX.TEXT: FileReader.read(filename),
            FileTypeX.AUDIO: AudioSegment.from_file(filename),
            FileTypeX.IMAGE: Image.open(filename)
        }.get(FileTypeX.get_type_from_filename(filename), None)