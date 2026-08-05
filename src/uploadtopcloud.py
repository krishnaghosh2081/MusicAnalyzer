import os
from datetime import datetime
from fastapi import  File, HTTPException
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
import uploadtodb

# Load .env file
load_dotenv()


cloudinary.config(
    cloud_name=os.getenv("CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET")
)

def upload_audio(name: str, file: bytes = File()):
    #print("===FiletoUpload===",file)
    
    # 2. Generate a unique name and save locally to buffer the file chunk stream
    timestamp = datetime.utcnow().strftime("%Y%m%d%H%M%S")

    try:
        # Stream file data from the request onto the server disk
       
        #print("===start cloudinary upload===")
        infileName=name.split(".")[0]
        result = cloudinary.uploader.upload_large(file,resource_type = "video",
            public_id = timestamp+"_"+infileName+"_guitar",
            chunk_size = 6000000,
            eager = [
            { "width": 300, "height": 300, "crop": "pad", "audio_codec": "none"},
            { "width": 160, "height": 100, "crop": "crop", "gravity": "south",
                "audio_codec": "none"}],
            eager_async = True)
         
        #print("===check pcloud upload===",result['secure_url'])
        
        db_result = uploadtodb.upload(result['secure_url'],name)
        #print("===db_result===",db_result)
        return {
            "status": "success",
            "db_id": str(db_result.inserted_id),
            "file_location": result['secure_url']
        }

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

   