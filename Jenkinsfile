pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat """
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install numpy opencv-python matplotlib pytest
                    
                    python CVscript.py

                    REM Check if the artifact was created
                    if exist "SIFT keypoints.png" (
                        echo "Artifact created successfully."
                    ) else (
                        echo "Artifact not created."
                        exit /b 1
                    )

                    REM Remove the virtual environment
                    call venv\\Scripts\\deactivate
                    rmdir /s /q venv
                """
            }
        }
        stage('Archive Artifact') {
            steps {
                archiveArtifacts artifacts: 'SIFT keypoints.png', allowEmptyArchive: false
            }
        }
        stage('Test') {
            steps {
                bat """
                    call venv\\Scripts\\activate
                    pytest --junitxml=results.xml
                """
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }
    }
}
