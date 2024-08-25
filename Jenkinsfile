pipeline {
    agent any

    environment {
        DATADOG_API_KEY = credentials('datadog_api_key')
        DATADOG_APPLICATION_KEY = credentials('datadog_application_key')
    }

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

                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'

                    bat 'aws deploy create-deployment --application-name SIT753 --deployment-group-name SIT753deploymentgroup --s3-location bucket=sit753bucket,bundleType=zip,key=my_application.zip --file-exists-behavior OVERWRITE'
                }
            }
        }
        stage('Monitoring and Alerting') {
            steps {
                script {

                    def monitors = sh(script: """
                        curl -s -X GET "https://api.us5.datadoghq.com/api/v1/monitor" \
                        -H "Content-Type: application/json" \
                        -H "DD-API-KEY: ${env.DATADOG_API_KEY}" \
                        -H "DD-APPLICATION-KEY: ${env.DATADOG_APPLICATION_KEY}"
                    """, returnStdout: true).trim()

                    def alerts = readJSON(text: monitors).findAll { it.overall_state == 'Alert' }

                    if (alerts) {
                        error "Failing build: ${alerts.collect { it.name }.join(', ')}"
                    }
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
            mail to: 'lguilding@deakin.edu.au',
                 subject: "Jenkins Build Failed: ${env.JOB_NAME}",
                 body: "The build failed due to triggered monitors in Datadog."
        }
    } 
}
