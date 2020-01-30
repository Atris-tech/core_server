import magic
from file_upload.config import Config

configObj = Config()
class AudioPrerequisites:
    def checkAudioPreq(self, file):
        # in using magic python library we can check the video file type
        fileType = magic.from_file(file, mime=True)
        print("file type", fileType)
        allowedTypes = configObj.getGlobals(key="allowed-types")
        if fileType in allowedTypes:
            # we check if the file type is in valid file type set (can be found out in video_tools/VideoToolsGlobals.py)
            filePrereqCheck = True
            return filePrereqCheck
        else:
            filePrereqCheck = False
            return filePrereqCheck