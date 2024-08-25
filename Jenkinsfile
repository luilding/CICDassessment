pipeline {
    agent any
    environment {
        DATADOG_API_KEY = credentials('datadog_api_key')
        DATADOG_APPLICATION_KEY = credentials('datadog_application_key')
    }
    stages {
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
                    
                    echo "Creating a new deployment with the updated appspec.yml."
                    bat 'powershell Compress-Archive -Path CVscript.py,empire.jpg,appspec.yml,scripts\\* -DestinationPath my_application.zip -Force'
                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'
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
                        error "Failing build due to triggered Datadog monitors: ${monitorNames}"
                    } else {
                        echo "No alerting monitors found."
                    }
                }
            }
        }
    }
}
