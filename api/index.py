import os

# Configure rembg home directory for serverless environment BEFORE importing rembg
# Vercel functions only have write access to /tmp
os.environ['U2NET_HOME'] = '/tmp/.u2net'

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI with root_path to handle Vercel rewrites correctly
app = FastAPI(root_path="/api")

# Allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Remoover API is running"}

@app.post("/remove-bg")
async def remove_background(file: UploadFile = File(...)):
    image_data = await file.read()
    # Use 'u2netp' model which is much smaller and acceptable for general use
    # This prevents Vercel function timeouts
    model_name = "u2netp"
    session = new_session(model_name)
    result = remove(image_data, session=session)
    return StreamingResponse(BytesIO(result), media_type="image/png")

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("index:app", host="0.0.0.0", port=8000, reload=True)
