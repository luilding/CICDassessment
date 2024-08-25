pipeline {
    agent any
    environment {
        DATADOG_API_KEY = credentials('datadog_api_key')
        DATADOG_APPLICATION_KEY = credentials('datadog_application_key')
    }
    stages {
        stage('Prepare Deployment Package') {
            steps {
               script {
                    // Create the corrected run_script.sh
                    bat '''
                    @echo off
                    (
                    echo #!/bin/bash
                    echo cd /opt/MyApp
                    echo python3 CVscript.py
                    ) > scripts\\run_script.sh
                    '''
                    
                    // Convert to Unix line endings
                    bat 'powershell -Command "(Get-Content scripts\\run_script.sh) | Set-Content -NoNewline scripts\\run_script.sh"'
                    
                    echo "Creating deployment package"
                    bat 'powershell Compress-Archive -Path CVscript.py,empire.jpg,appspec.yml,scripts\\run_script.sh -DestinationPath my_application.zip -Force'
                    
                    // Verify the contents of the zip file
                    bat 'powershell Expand-Archive -Path my_application.zip -DestinationPath temp_extract -Force'
                    bat 'dir /s temp_extract'
                    bat 'type temp_extract\\scripts\\run_script.sh'
                    bat 'rmdir /s /q temp_extract'
                }
            }
        }
        stage('Release') {
            steps {
                script {
                    def activeDeployment = bat(
                        script: '@echo off & aws deploy get-deployment-group --application-name SIT753 --deployment-group-name SIT753deploymentgroup --query "deploymentGroupInfo.latestDeploymentAttempted.deploymentId" --output text',
                        returnStdout: true
                    ).trim()
    
                    if (activeDeployment && activeDeployment != 'None') {
                        echo "An active deployment is already in progress: ${activeDeployment}. Stopping it to start a new deployment."
                        bat "aws deploy stop-deployment --deployment-id ${activeDeployment} --auto-rollback-enabled"
                    } else {
                        echo "No active deployment found. Proceeding with new deployment."
                    }
                    
                    echo "Uploading deployment package to S3"
                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'
                    
                    echo "Creating new deployment"
                    bat 'aws deploy create-deployment --application-name SIT753 --deployment-group-name SIT753deploymentgroup --s3-location bucket=sit753bucket,bundleType=zip,key=my_application.zip --file-exists-behavior OVERWRITE'
                }
            }
        }
        stage('Monitoring and Alerting') {
            steps {
                script {
                    def response = bat(
                        script: """
                            @echo off
                            curl -s -X GET "https://api.us5.datadoghq.com/api/v1/monitor" ^
                            -H "Content-Type: application/json" ^
                            -H "DD-API-KEY: %DATADOG_API_KEY%" ^
                            -H "DD-APPLICATION-KEY: %DATADOG_APPLICATION_KEY%"
                        """,
                        returnStdout: true
                    ).trim()
                    
                    echo "Raw API Response:"
                    echo response
                    
                    def jsonResponse = response.readLines().last() // Get the last line, which should be the JSON
                    
                    def monitors = readJSON text: jsonResponse
                    def alertingMonitors = monitors.findAll { it.overall_state == 'Alert' }
        
                    if (alertingMonitors) {
                        def monitorNames = alertingMonitors.collect { it.name }.join(", ")
                        echo "Warning: The following Datadog monitors are in alert state: ${monitorNames}"
                        
                        // Check if the memory alert is the only one triggered
                        if (alertingMonitors.size() == 1 && alertingMonitors[0].name.contains("Mem load is high")) {
                            echo "High memory usage detected. Please investigate, but continuing the pipeline."
                        } else {
                            error "Failing build due to triggered Datadog monitors: ${monitorNames}"
                        }
                    } else {
                        echo "No alerting monitors found."
                    }
                }
            }
        }
    }
}
