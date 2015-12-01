#* coding: utf-8
import re
from solute.epfl.validators.text import TextValidator


class StreamingVideoUrlValidator(TextValidator):
    def __init__(self, value='value', error_message='Video Url is invalid!',
                 video_services=["youtube", "vimeo"], *args, **kwargs):
        """Validate a related Input field as a valid url of a streaming video service.
        Services to be regarded during validation can be passed in the video_services parameter.

        :param value: Where to get the value to be evaluated.
        :param error_message: Error message to be displayed upon failed validation.
        :param video_services: List of video services against which url validity is checked.
        """
        super(StreamingVideoUrlValidator, self).__init__(value=value, error_message=error_message,
                                                         video_services=video_services, *args, **kwargs)

    def validate(self, value=None, error_message=None, video_services=None, **kwargs):
        result = super(StreamingVideoUrlValidator, self).validate(value=value, error_message=error_message, **kwargs)

        if result is False:
            return False

        if not video_services:
            self.error_message = error_message
            return False
        if value:
            if "youtube" in video_services:
                youtube_match = re.compile(
                    ur'(?:http(?:s)?:\/\/)?(?:www\.)?'
                    ur'(?:m\.)?(?:youtu\.be\/|youtube\.com\/'
                    ur'(?:(?:watch)?\?(?:.*&)?v(?:i)?=|(?:embed|v|vi|user)\/))([^\?&\"\'>]+)')

                match = re.search(youtube_match, value)
                if match:
                    return True
            if "vimeo" in video_services:
                vimeo_match = re.compile(
                    ur'(?:http(?:s)?:\/\/)?(?:www\.)?'
                    ur'vimeo.com\/(.*)')
                match = re.search(vimeo_match, value)
                if match:
                    return True
            self.error_message = error_message
            return False

        return True

