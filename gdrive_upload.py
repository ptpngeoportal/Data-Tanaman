from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io

# Ganti dengan ID folder Google Drive tujuan
FOLDER_ID = "1Xf1aQgs0AOWdFPihv2ESmmsFl-FoRUDg"

def upload_to_drive(uploaded_file, file_name):
    try:
        # Load service account credentials
        creds = service_account.Credentials.from_service_account_file("credentials.json")

        # Build Drive API service
        service = build("drive", "v3", credentials=creds)

        # Buat metadata file
        file_metadata = {
            "name": file_name,
            "parents": [FOLDER_ID]
        }

        # Siapkan media untuk diupload
        media = MediaIoBaseUpload(io.BytesIO(uploaded_file.read()), mimetype=uploaded_file.type)

        # Eksekusi upload
        uploaded = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        file_id = uploaded.get("id")
        file_url = f"https://drive.google.com/file/d/{file_id}/view"

        return file_url
    except Exception as e:
        return f"Gagal upload: {e}"
