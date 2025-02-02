from typing import Union


class ErrorMessage:
    """
    Class to encapsulate the different error
    messages we need.
    """

    @staticmethod
    def parameter_is_not_a_class(parameter_name: str):
        return f'The provided "{parameter_name}" parameter is not a class.'
    
    @staticmethod
    def parameter_not_provided(parameter_name: str):
        return f'The parameter "{parameter_name}" was not provided.'
    
    @staticmethod
    def parameter_is_not_string(parameter_name: str):
        return f'The parameter "{parameter_name}" provided is not a string.'
    
    @staticmethod
    def parameter_is_not_boolean(parameter_name: str):
        return f'The "{parameter_name}" parameter is not boolean.'
    
    @staticmethod
    def parameter_is_not_positive_number(parameter_name: str):
        return f'The parameter "{parameter_name}" provided is not a valid and positive number.'
    
    @staticmethod
    def parameter_is_file_that_doesnt_exist(parameter_name: str):
        return f'The "{parameter_name}" parameter provided is not a file that exists.'
    
    @classmethod
    def parameter_is_not_file_of_file_type(parameter_name: str, file_type: 'FileType'):
        return f'The "{parameter_name}" provided is not a {file_type.value} filename.'
    
    @staticmethod
    def parameter_is_not_valid_url(parameter_name: str):
        return f'The provided "{parameter_name}" parameter is not a valid url.'
    
    @staticmethod
    def parameter_is_not_class(parameter_name: str, class_names: Union[list[str], str]):
        # TODO: Check if 'class_names' is not array of str nor str
        if isinstance(class_names, str):
            class_names = [class_names]

        class_names = ', '.join(class_names)
        return f'The provided "{parameter_name}" parameter is not one of the next classes: {class_names}'

    @staticmethod
    def parameter_is_not_name_of_ytaenum_class(name: str, enum):
        return f'The provided YTAEnum name "{name}" is not a valid {enum.__class__.__name__} YTAEnum name.'
    
    @staticmethod
    def parameter_is_not_value_of_ytaenum_class(value: any, enum):
        return f'The provided YTAEnum value "{value}" is not a valid {enum.__class__.__name__} YTAEnum value.'
    
    @staticmethod
    def parameter_is_not_name_nor_value_of_ytaenum_class(name_or_value: any, enum):
        return f'The provided YTAEnum name or value "{name_or_value}" is not a valid {enum.__class__.__name__} YTAEnum name or value.'
    
    @staticmethod
    def parameter_is_not_name_nor_value_nor_enum_of_ytaenum_class(name_or_value_or_enum: any, enum):
        return f'The provided YTAEnum name, value or instance "{name_or_value_or_enum}" is not a valid {enum.__class__.__name__} YTAEnum name, value or instance.'