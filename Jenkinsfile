pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat """
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    
                    python CVscript.py
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
        stage('Code Quality Analysis') {
            steps {
                bat """
                    call venv\\Scripts\\activate
                    pylint CVscript.py > pylint_report.txt || exit 0
                    flake8 --output-file=flake8_report.txt || exit 0
                    bandit -r . -f txt -o bandit_report.txt || exit 0
                """
            }
            post {
                always {
                    archiveArtifacts artifacts: '*.txt', allowEmptyArchive: false
                }
            }
        }
        stage('Docker Build') {
            steps {
                bat """
                    docker-compose down || exit 0
                    docker rm -f comp_v_app || exit 0 
                    docker-compose up --build
                """
            }
        }
        stage('Release') {
            steps {
                script {
                    bat 'powershell Compress-Archive -Path CVscript.py,empire.jpg,appspec.yml,scripts\\* -DestinationPath my_application.zip -Force'


                    bat 'aws deploy create-deployment --application-name YourAppName --deployment-group-name YourDeploymentGroup --file-exists-behavior OVERWRITE --file my_application.zip'
                }
            }
        }
    }
    post {
        always {
            bat """
                REM Deactivate the virtual environment
                call venv\\Scripts\\deactivate
                REM Optionally remove the virtual environment directory
                rmdir /s /q venv
            """
        }
        failure {
            echo 'Pipeline failed. Notifying team...'
        }
    }
}
