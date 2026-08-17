from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from pathlib import Path
import tempfile
import separate as sp 
import os, zipfile
import shutil
import uploadtopcloud
import os
import urllib.request
import urllib.parse
import uploadtodb


app = FastAPI(title="Audio Separator")


@app.get("/")
def root():
    return {"message": "Hello World"}

def createDir():
    directory_name = "audio_downloads"
    target_dir = Path(directory_name).resolve()
    target_dir.mkdir(parents=True, exist_ok=True) 

    return directory_name

def download(mp3_url,directory_name):

    

    try:
    # 2. Parse the URL and extract the true file name path
        parsed_url = urllib.parse.urlparse(mp3_url)
    
    # Path(parsed_url.path).name grabs the very last segment (e.g., 'SoundHelix-Song-1.mp3')
        original_filename = Path(parsed_url.path).name
    
    # Fallback in case the URL path is empty or unreadable
        if not original_filename:
            original_filename = "downloaded_track.mp3"
        
    except Exception:
        original_filename = "downloaded_track.mp3"

    

    target_dir = Path(directory_name).resolve()
    destination_path = target_dir / original_filename

    opener = urllib.request.build_opener()
    #opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
    urllib.request.install_opener(opener)

    print("Starting MP3 download...")

    try:
        # 4. Download and write the audio file to disk
        urllib.request.urlretrieve(mp3_url, destination_path)
    
    # 5. Output the location of your downloaded MP3
        print("\nMP3 download completed successfully!")
        print(f"Absolute file path: {destination_path}")

    except Exception as e:
        print(f"\nFailed to download audio file. Error: {e}")



    return destination_path



def cleanDir(dirname):
    """Clean the given directory"""
    for folder_name,subfolders, filenames in os.walk(dirname):
            for filename in filenames:
                file_path = os.path.join(folder_name, filename)
                if filename.startswith('.'):
                                continue
                if(filename.split(".")[1]!="txt"):
                    #print("==files===",filename)
                    os.remove(file_path)          

#@app.post("/separate")
def separate_audio(consumedid):

    """Upload audio,  separate stems WAV."""
    #print("===consumedid===",consumedid)
    output_path= createDir()
    cleanDir(output_path)
    #print("===output_path===",output_path)
    model="htdemucs_6s"
                  
    db_result = uploadtodb.getInfo(consumedid)
    #print("===db_result===",db_result)
   # "db_id"= str(db_result.inserted_id)

    #if db_result:
    stemType=db_result["stemType"]
    inputFile=db_result["inputFile"]

    input_path=  download(inputFile,output_path)
    #print("===input_path===",input_path)

    finalfilename=str(input_path).split("/")[-1]
    #print("===finalfilename===",finalfilename)
        
        # Separate
    result = sp.separate(input_path, output_dir=output_path, fileToupload=stemType, model=model)
    
    for stem_name, stem_path in result.items():
            #print("===FileName1===",stem_name)
            print("===FilePath1===",stem_path)
            if Path(stem_path).exists():
                if(stem_path.split(".")[1]=="wav"):
                    uploadtopcloud.upload_audio(finalfilename,consumedid,stem_path)                     


       
    #cleanDir(output_path)
    return JSONResponse(content={"message": "File transformed"}, media_type="application/json")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)    