from yta_general_utils.file.writer import FileWriter
from yta_general_utils.dataclasses import FileReturn
from typing import Union

import requests


def get_file(
    url: str,
    output_filename: Union[str, None] = None
):
    """
    This method sends a request to the provided 'url'
    if provided and obtains the file content (if 
    possible). It will write the obtained file locally
    as 'output_filename' if provided.

    This method returns the file content data as 
    obtained from the requested (.content field).
    """
    # # This code below is to write it by chunks, if
    # # the other way fails
    # CHUNK_SIZE = 8192
    
    # content = b''
    # with requests.get(url, stream = True) as response:
    #     response.raise_for_status()
    #     with open(output_filename, 'wb') if output_filename else nullcontext() as file:
    #         for chunk in response.iter_content(CHUNK_SIZE):
    #             content += chunk
    #             if file:
    #                 file.write(chunk)

    # return content

    content = requests.get(url).content

    if output_filename:
        FileWriter.write_binary_file(content, output_filename)

    return content

def download_file(
    url: str,
    output_filename: Union[str, None] = None
) -> FileReturn:
    """
    Receives a downloadable url as 'url' and downloads that
    file in our system as 'output_filename'.
    """
    if output_filename is None:
        raise Exception('No "output_filename" provided.')
    
    file = get_file(url, output_filename)
    
    return FileReturn(
        file,
        output_filename
    )