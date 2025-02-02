import os
from deepface import DeepFace
import cv2
import numpy as np
import time
import pandas as pd

class AdvancedFaceRecognition:
    def __init__(self, dataset_path, model_name="VGG-Face"):  # Changed default model to VGG-Face for better compatibility
        self.dataset_path = dataset_path
        self.model_name = model_name
        self.db_path = dataset_path
        print(f"Initializing face recognition system with {model_name} model...")
        
    def run_recognition(self):
        video_capture = cv2.VideoCapture(0)
        if not video_capture.isOpened():
            print("Error: Could not open video capture device")
            return

        print(f"Starting face recognition using {self.model_name}...")
        print("Press 'q' to quit")
        
        frame_count = 0
        start_time = time.time()
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                print("Error: Could not read frame")
                break
                
            frame_count += 1
            
            # Process every 3rd frame to improve performance
            if frame_count % 3 != 0:
                cv2.imshow('Advanced Face Recognition', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                continue
                
            try:
                # First, detect faces
                faces = DeepFace.extract_faces(
                    img_path=frame,
                    detector_backend="opencv",
                    enforce_detection=False
                )
                
                if faces:  # If faces were detected
                    # Try to recognize each detected face
                    results = DeepFace.find(
                        img_path=frame,
                        db_path=self.db_path,
                        model_name=self.model_name,
                        enforce_detection=False,
                        detector_backend="opencv",
                        distance_metric="cosine"
                    )
                    
                    if isinstance(results, list) and len(results) > 0:
                        df = results[0]
                        if isinstance(df, pd.DataFrame) and not df.empty:
                            # Process each detected face
                            for i, face in enumerate(faces):
                                if 'facial_area' in face:
                                    region = face['facial_area']
                                    x = region['x']
                                    y = region['y']
                                    w = region['w']
                                    h = region['h']
                                    
                                    # Get identity if available
                                    person_name = "Unknown"
                                    confidence = 0
                                    
                                    if i < len(df):
                                        row = df.iloc[i]
                                        if 'identity' in row:
                                            identity_path = row['identity']
                                            person_name = os.path.basename(os.path.dirname(identity_path))
                                            # Calculate confidence (1 - distance for cosine metric)
                                            if 'distance' in row:
                                                confidence = (1 - row['distance']) * 100
                                    
                                    # Draw rectangle around face
                                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                                    
                                    # Add name and confidence
                                    label = f"{person_name}"
                                    if confidence > 0:
                                        label += f" ({confidence:.1f}%)"
                                        
                                    cv2.rectangle(frame, (x, y-35), (x+w, y), (0, 255, 0), cv2.FILLED)
                                    cv2.putText(frame, label, (x+6, y-6), 
                                              cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
                
            except Exception as e:
                print(f"Frame processing error: {str(e)}")
                continue
            
            # Calculate and display FPS
            if frame_count % 30 == 0:
                fps = frame_count / (time.time() - start_time)
                cv2.putText(frame, f"FPS: {fps:.2f}", (10, 30), 
                           cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2)
            
            # Display the frame
            cv2.imshow('Advanced Face Recognition', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        video_capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    dataset_path = "faces_dataset"
    
    recognition_system = AdvancedFaceRecognition(
        dataset_path=dataset_path,
        model_name="VGG-Face"  # Using VGG-Face for better reliability
    )
    
    recognition_system.run_recognition()