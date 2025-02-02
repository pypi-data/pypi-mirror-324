from enum import Enum

parsing_errors = []

def report_parsing_error(path, tag, message):
    # this is used in a test code, when individual elements like choices are parsed
    if path.startswith('::'):
        path = path[2:]
    parsing_errors.append(ParsingError(path, tag, message))

class ParsingErrorTag(Enum):
    NAME = 1
    CHILDREN = 2
    VALUE = 3
    LABEL = 3
    ASSIGNMENT = 4
    CONSTRAINT = 4
    ALIAS = 4

    def __str__(self) -> str:
        return self.name

class ParsingError:
    def __init__(self, path, tag, message):        
        self.path = path
        self.tag = tag
        self.message = message

    def __str__(self):
        return f"[{self.path}]: {self.message}"

    def __repr__(self):
        return str(self)

class ExitCodes(Enum):
    SUCCESS = 0

    CONFLICTING_PROGRAM_ARGS = 1
    MODEL_FILE_NOT_FOUND = 2
    YAML_PARSING_ERROR = 3
    MODEL_PARSING_ERROR = 4
    MODEL_VALIDATION_ERROR = 5
    TEST_FILE_NOT_FOUND = 6
    TEST_PARSING_ERROR = 7
    GENERATION_ERROR = 8

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value
    

