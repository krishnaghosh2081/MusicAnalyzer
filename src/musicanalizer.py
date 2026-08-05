from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
import uvicorn
from pathlib import Path
import tempfile
import separate as sp 
import os, zipfile
import shutil
import uploadtopcloud



app = FastAPI(title="Audio Separator")


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.post("/separate")
async def separate_audio(
    file: UploadFile = File(...),
    vocals_only: bool = Form(False),
    output_path: str =Form("/Users/krishnaghosh/Desktop/Learning/WBS-Final-Project/musicanalizer-api/stems"),
    model: str = Form("htdemucs_6s"),
):

    """Upload audio,  separate stems as ZIP."""


    with tempfile.TemporaryDirectory() as tmpdir:
        # Save upload
        input_path = f"{tmpdir}/input{Path(file.filename).suffix}"
        with open(input_path, "wb") as f:
            f.write(await file.read())
        
        # Separate
        result = sp.separate(input_path, output_dir=tmpdir, vocals_only=vocals_only, model=model)

        #print
        #for stem_name, stem_path in result.items():
            #print("===FileName1===",stem_name)
            #print("===FilePath1===",stem_path)
            

        # Package stems as ZIP
        #zip_path = f"{tmpdir}/stems.zip"
        #with zipfile.ZipFile(zip_path, "w") as zf:
        for stem_name, stem_path in result.items():
            if Path(stem_path).exists():
                # move file to folder
                shutil.move(stem_path, output_path+"/updated/")
        

        # Package stems as ZIP
        name = f"{output_path}"
        zip_name='output.zip'
        zip_path =  name+"/"+zip_name

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
            for folder_name, subfolders, filenames in os.walk(output_path+"/updated"):
                for filename in filenames:
                    file_path = os.path.join(folder_name, filename)
                    uploadtopcloud.upload_audio(file.filename,file_path)
                    zip_ref.write(file_path, arcname=os.path.relpath(file_path, name))

        zip_ref.close()

        #return FileResponse(Path(name), media_type="application/zip",
                        #  filename=f"{zip_name}")
       

        return JSONResponse(content={"message": "File transformed"}, media_type="application/json")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)    