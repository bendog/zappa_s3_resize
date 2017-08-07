import os


PYTHON_LOG_LEVEL = os.environ.get('PYTHON_LOG_LEVEL', 'warning')

# IMAGE_CONVERSIONS is a list of tuples, with the following values
# Prefix for the saved version
# Width of new image
# Height of the new image
# new extention
IMAGE_CONVERSIONS = [
    ('button', 30, 0, 'jpg'),
    ('preview', 320, 0, 'jpg'),
]
