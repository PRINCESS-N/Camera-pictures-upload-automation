import os
import time
import shutil
import subprocess

 
WATCH_FOLDER = "watch"  
UPLOADED_FOLDER = "uploaded"   
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

def upload_image(image_path):
    """Upload an image using curl command."""
    try:
        
        result = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{image_path}", UPLOAD_URL],
            capture_output=True,
            text=True
        )

        
        if result.returncode == 0 and "success" in result.stdout.lower():
            print(f"Successfully uploaded: {image_path}")
            return True
        else:
            print(f"Failed to upload: {image_path}")
            print(f"Response: {result.stdout}")
            print(f"Error Output: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error uploading image {image_path}: {e}")
        return False

def monitor_and_upload():
    """Monitor the folder, upload images, and move them to 'uploaded' folder."""
    while True:
        
        files = [f for f in os.listdir(WATCH_FOLDER) if os.path.isfile(os.path.join(WATCH_FOLDER, f))]
        for file in files:
            file_path = os.path.join(WATCH_FOLDER, file)
            
            if upload_image(file_path):
                
                uploaded_path = os.path.join(UPLOADED_FOLDER, file)
                shutil.move(file_path, uploaded_path)
                print(f"Moved {file} to {UPLOADED_FOLDER}")
        
         
        time.sleep(30)

if __name__ == "__main__":
    
    os.makedirs(WATCH_FOLDER, exist_ok=True)
    os.makedirs(UPLOADED_FOLDER, exist_ok=True)

    print("Monitoring folder for new images...")
    monitor_and_upload()
