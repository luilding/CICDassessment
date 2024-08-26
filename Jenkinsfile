pipeline {
    agent any

    environment {
        //To get sensitive details from Jenkins
        DATADOG_API_KEY = credentials('datadog_api_key')
        DATADOG_APPLICATION_KEY = credentials('datadog_application_key')
    }

    stages {
        stage('Build') {
            steps {
                //Setting up and starting a Python virtual environment as well as installing the script dependencies
                bat """
                    python -m venv venv
                    call venv\\Scripts\\activate
                    pip install --upgrade pip && pip install -r requirements.txt
                    
                    python CVscript.py
                """
                
                //Archiving the build artifact
                archiveArtifacts artifacts: 'SIFT keypoints.png', allowEmptyArchive: false
            }
        }

        stage('Test') {
            steps {
                //Activating the virtual environment to run tests on the code, using python specifc pytest
                bat """
                    call venv\\Scripts\\activate
                    pytest --junitxml=results.xml
                """
            }
            post {
                always {
                    //Provide test results to Jenkins
                    junit 'results.xml'
                }
            }
        }

        stage('Code Quality Analysis') {
            steps {
                //Running python code quality tools and static analysis: pylint, flake8 and bandit
                bat """
                    call venv\\Scripts\\activate
                    pylint CVscript.py > pylint_report.txt || exit 0
                    flake8 --output-file=flake8_report.txt || exit 0
                    bandit -r . -f txt -o bandit_report.txt || exit 0
                """
            }
            post {
                always {
                    //Archiving the code quality reports
                    archiveArtifacts artifacts: '*.txt', allowEmptyArchive: false
                }
            }
        }

        stage('Deploy with Docker') {
            steps {
                // Deploy the application into a Docker container and run the script in the background
                bat """
                    docker-compose down || exit 0
                    docker rm -f comp_v_app || exit 0 
                    docker-compose up --build -d
        
                    // Run the script in the background inside the Docker container
                    docker exec -d comp_v_app bash -c "export SLEEP_TIME=600 && nohup python CVscript.py &"
                """
            }
        }


        stage('Release') {
            steps {
                script {
                    //Stopping any active deployments in aws to avoid conflicts
                    bat '''
                        for /f "tokens=*" %%i in ('aws deploy list-deployments --application-name SIT753 --deployment-group-name SIT753deploymentgroup --include-only-statuses InProgress --query "deployments[0]" --output text') do (
                            if not "%%i"=="None" (
                                echo Stopping deployment: %%i
                                aws deploy stop-deployment --deployment-id %%i
                            )
                        )
                    '''
                    
                    //Create a new deployment in aws codedeploy
                    bat '''
                        aws deploy create-deployment ^
                        --application-name SIT753 ^
                        --deployment-group-name SIT753deploymentgroup ^
                        --s3-location bucket=sit753bucket,bundleType=zip,key=my_application.zip ^
                        --file-exists-behavior OVERWRITE
                    '''
                }
            }
        }

        stage('Monitoring and Alerting') {
            steps {
                script {
                    //Checking Datadog monitor views for any alerts in the prod environment
                    def response = bat(
                        script: """
                            curl -s -X GET "https://api.us5.datadoghq.com/api/v1/monitor" ^
                            -H "Content-Type: application/json" ^
                            -H "DD-API-KEY: %DATADOG_API_KEY%" ^
                            -H "DD-APPLICATION-KEY: %DATADOG_APPLICATION_KEY%"
                        """,
                        returnStdout: true
                    ).trim()
                    
                    echo "Raw API Response:"
                    echo response
                    
                    //Parse the JSON response from Datadog API
                    def jsonResponse = response.readLines().last() 
                    
                    //Find monitors that are currently alerting
                    def monitors = readJSON text: jsonResponse
                    def alertingMonitors = monitors.findAll { it.overall_state == 'Alert' }
        
                    //If any monitors are currently alerting, generate email notification including the alert details
                    if (alertingMonitors) {
                        def alertDetails = alertingMonitors.collect { monitor ->
                            return """
                            Monitor Name: ${monitor.name}
                            Message: ${monitor.message}
                            Query: ${monitor.query}
                            Current State: ${monitor.overall_state}
                            """
                        }.join("\n\n")

                        echo "Triggered Alerts:\n${alertDetails}"
                        
                        //Sending the email with details of the alerts
                        mail to: 'lguilding@deakin.edu.au',
                             subject: "Datadog Alerts: Issues Detected in Production",
                             body: "The following monitors have triggered alerts:\n\n${alertDetails}"
                    } else {
                        //If no alerts are found, log that it is fine
                        echo "No alerting monitors found."
                    }
                }
            }
        }
    }
}
