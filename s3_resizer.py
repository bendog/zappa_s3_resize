import boto3
from io import BytesIO
from PIL import Image

import config
from logger import logger


def resize_image(img, width, height, ext):
    """Builds an image according to params."""

    # if not already loaded, load
    if type(img) == str:
        img = Image.open(img)

    # work out conversion size
    if width == 0 and height != 0:
        hpercent = (height / float(img.size[1]))
        width = int((float(img.size[0]) * float(hpercent)))
    elif width != 0 and height == 0:
        wpercent = (width / float(img.size[0]))
        height = int((float(img.size[1]) * float(wpercent)))
    elif width == 0 and height == 0:
        width = img.size[0]
        height = img.size[1]

    # if the outbound file is not png, convert to RGB
    if ext != 'png':
        if img.mode != "RGB":
            img = img.convert("RGB")

    # resize
    img = img.resize((width, height), Image.ANTIALIAS)

    # save to buffer
    buffer = BytesIO()
    image_format = "jpeg" if ext == "jpg" else ext

    img.save(buffer, format=image_format.capitalize())

    return buffer.getvalue()


def save_to_s3(bucket, file_key_name, file_data):
    """ take the file contents and save it to S3 """
    s3 = boto3.resource('s3')
    s3.Object(bucket, file_key_name).put(Body=file_data)


def process_s3_event(event, context):
    """
    Process the new s3 event
    """
    logger.debug("event:%s" % event)
    logger.debug("context:%s" % context)

    # Get the uploaded file's information
    bucket = event['Records'][0]['s3']['bucket']['name']  # sourced from zappa_settings.json
    key = event['Records'][0]['s3']['object']['key']  # Will be the file path of whatever file was uploaded.

    # check the filetype is alowed
    if key.split('.')[-1].lower() not in config.ALLOWED_EXTENTIONS:
        raise NotImplementedError('Unsupported file extention in %s:%s' % (bucket, key))

    # Get the bytes from S3
    s3_client = boto3.client('s3')
    logger.info("loading file %s:%s to /tmp/%s" % (bucket, key, key))
    s3_client.download_file(bucket, key, '/tmp/' + key)  # Download this file to writable tmp space.

    # process the image file
    original_image_data = Image.open('/tmp/' + key)

    for prefix, width, height, ext in config.IMAGE_CONVERSIONS:
        resize_data = resize_image(original_image_data, width, height, ext)
        new_file_key = ".".join(key.split('.')[:-1]) + ".%s" % ext  # new file key should have the new ext
        save_to_s3(bucket, '%s/%s' % (prefix, new_file_key), resize_data)
        logger.info("saving file %s:%s/%s" % (bucket, prefix, new_file_key))

    pass
