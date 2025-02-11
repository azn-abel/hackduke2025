# ShotIQ: AI Basketball Coach!
ShotIQ is a web application for analyzing basketball shooting form using video analysis and AI-powered feedback.  Users can upload a video of their shooting form, and the system will process the video to identify key angles and provide personalized feedback to align themselves to optimal shooting form. 

## Features
* **Video Upload:** Upload MP4 videos of your basketball shot.
* **Pose Estimation:**  The system uses MediaPipe to track body pose in real-time.
* **Angle Calculation:** Key angles (elbow, knee, ankle) are calculated during different phases of the shot.
* **AI-Powered Feedback:**  An AI model generates concise, actionable coaching advice based on the calculated angles and scientific literature.
* **Processed Video Output:**  A processed video with angle overlays is provided for review.
* **Intuitive Interface:**  The frontend offers a user-friendly experience for video upload and feedback viewing.

## Usage
1. **Upload Video:** Navigate to the application and upload an MP4 video of your basketball shot.
2. **Processing:** The system will process your video for your analysis.
3. **View Results:** Once processed, you will see the raw and processed videos, along with personalized feedback from the AI coach.

## Installation
This project consists of a frontend and a backend.  You will need to set up both components in two different terminals.
Also, note that usage requires an OpenAI API key, which requires an OpenAI subscription.

### Backend

1. **Clone the Repository:**
   ```bash
   git clone <repository_url>
   ```
2. **Navigate to the Backend Directory:**
   ```bash
   cd backend
   ```
3. **Create a Virtual Environment:** (Instructions for macOS, Windows, and other systems are provided in the backend/README.md file)
4. **Install Dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
5. **Set Environment Variables:** Set the `OPENAI_API_KEY` environment variable with your OpenAI API key.  This key is required for the AI feedback functionality.
6. **Run the Backend:**
   ```bash
   fastapi dev main.py
   ```

### Frontend

1. **Navigate to the Frontend Directory:**
   ```bash
   cd frontend
   ```
2. **Install Dependencies:**
   ```bash
   npm install
   ```
3. **Run the Development Server:**
   ```bash
   npm run dev
   ```

# Tech Stack
* **Backend:**
    * **Python:** The programming language for the backend logic.
    * **FastAPI:** A modern, fast (high-performance), web framework for building APIs with Python.
    * **OpenAI API:** Used for generating AI-powered coaching feedback.
    * **MediaPipe:** A framework for building multimodal applied ML pipelines.  Used for pose estimation.
    * **opencv-python:** For video processing.
    * **pandas:** For data manipulation and analysis.
    * **numpy:** For numerical computation.
    * **dotenv:** For securely managing environment variables.
* **Frontend:**
    * **Next.js:** A React framework for building web applications.
    * **React:** A JavaScript library for building user interfaces.
    * **Tailwind CSS:** A utility-first CSS framework.
    * **showdown:** A Markdown to HTML converter.  
