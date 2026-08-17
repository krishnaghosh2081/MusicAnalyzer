# MusicAnalyzer - Stem separation
 This backend API made with Python , Fast API , Demucs. This api when triggered from outside will start to work as a kafka consumer and collect the message from the topic. After that using the information it will collect the song details from database and download the song to be analyzed in a tmp dir. Then it will start stem seperation using Meta's demucs model and finaly store the Guitar part to cloud storage and save the link to database again to be used by the frontend application. This api can also be hosted with Docker image.

# Create a .env file and add this with data
CLOUD_NAME,CLOUDINARY_KEY,CLOUDINARY_SECRET,CONNECT_DB