# * encoding: utf-8

from solute.epfl.core.epflcomponentbase import ComponentBase


class EmbeddedVideo(ComponentBase):
    template_name = "embedded_video/embedded_video.html"

    video_id = None  #: The id of the video, could easy be found at the end of the youtube or vimeo url

    video_type = None  #: The type of the video use one of the constants below

    width = None  #: The iframe width if None 100% is used

    height = None  #: The iframe height if None 100% is used

    VIDEO_TYPE_YOUTUBE = "Youtube"  #: Constant for video_type youtube
    VIDEO_TYPE_VIMEO = "Vimeo"  #: Constant for video_type vimeo

    def __init__(self, page, cid, video_id=None, video_type=None, width=None, height=None, **extra_params):
        """Embeddeds a video iframe from youtube or vimeo using the video id

        :param video_id: The id of the video, could easy be found at the end of the youtube or vimeo url
        :param video_type: The type of the video use one of the constants
        :param width: The iframe width if None 100% is used
        :param height: The iframe height if None 100% is used
        """
        super(EmbeddedVideo, self).__init__(page, cid, video_id=video_id, video_type=video_type, width=width,
                                            height=height, **extra_params)

