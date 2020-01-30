from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status
from file_upload.serializers import UploadSerializer
from core_server.settings import BASE_DIR
from file_upload.services.AudioPrecheckService import AudioPrerequisites
import os
from azure.storage.blob import BlobServiceClient, BlobClient
from file_upload.config import Config
from file_upload.models import Upload
from pathlib import Path
import shutil
import subprocess
import json
import uuid

configObj = Config()

connect_str = configObj.getGlobals(key="connection_str")
container_to_upload = configObj.getGlobals(key="container")
account_url = configObj.getGlobals(key="account_url")


blob_service_client = BlobServiceClient.from_connection_string(connect_str)

class UploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        upload_serializer = UploadSerializer(data=request.data)
        #POST DATA IS SERIALIZED HERE
        if upload_serializer.is_valid():
            # Check if every data is valid with the required api parameters (models)
            upload_serializer.save()
            # serialize and convert model data to a serialized json
            # Fetch data from serialized json
            fileData = upload_serializer.data["file"]
            meetingId = upload_serializer.data["meeting_id"]
            filePath = fileData.strip("/")
            fullFile = os.path.join(BASE_DIR, filePath)
            fileParentFolder = Path(str(fullFile)).parent
            print("file path", fullFile)

            #########################################
            audioPrecheck = AudioPrerequisites().checkAudioPreq(file=fileData)
            if audioPrecheck:
                blob_client = blob_service_client.get_blob_client(
                    container=container_to_upload,
                    blob=fileData
                )
                with open(fileData, "rb") as data:
                    blob_client.upload_blob(data)
                print("\nUploading to Azure Storage as blob:\n\t" + fileData)
                url = BlobClient(
                    account_url=account_url,
                    blob_name=fileData,
                    container_name=container_to_upload
                ).url
                print(url)
                toConvertJson= str(fileParentFolder) + "/" + str(uuid.uuid4()) + ".json"
                """audiowaveform -i himono.wav -o test.json -z 256 -b 8"""
                subprocess.call(["audiowaveform", "-i", fileData, "-o", toConvertJson, "-z", "256", "-b", "8"])
                # save to database of filemodel
                print(toConvertJson)
                with open(toConvertJson, 'r') as f:
                    config = json.load(f)
                u_obj = Upload.objects.get(
                    meeting_id=meetingId
                )
                u_obj.file_url = url
                u_obj.waveform = config
                u_obj.save()
                convertResponse = {
                    "msg": "done",
                    "data": [],
                    "id": upload_serializer.data,
                    "time": upload_serializer.data["timestamp"],
                    "status": status.HTTP_200_OK
                }
                shutil.rmtree(fileParentFolder)
                # return upload response
                return Response(data=convertResponse, status=status.HTTP_200_OK)
            else:
                convertResponse = {
                    "msg": "invalid file type",
                    "data": [],
                    "id": upload_serializer.data,
                    "time": upload_serializer.data["timestamp"]
                }
                return Response(data=convertResponse, status=status.HTTP_400_BAD_REQUEST)
        else:
            # if some errors occurs

            return Response(data=upload_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




