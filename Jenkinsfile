pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat """
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install numpy opencv-python matplotlib  // Install required libraries
                    python CVscript.py

                    // Archive the generated image file
                    if exist "SIFT keypoints.png" (
                        echo "Artifact created successfully."
                        copy "SIFT keypoints.png" "%WORKSPACE%\\SIFT keypoints.png"
                    ) else (
                        echo "Artifact not created."
                        exit /b 1
                    )

                    //Remove the virtual environment
                    call venv\\Scripts\\deactivate
                    rmdir /s /q venv
                """
            }
        }
    }
}