pipeline {
    agent any

    environment {
        // To get sensitive details from Jenkins
        DATADOG_API_KEY = credentials('datadog_api_key')
        DATADOG_APPLICATION_KEY = credentials('datadog_application_key')
    }

    stages {
        stage('Release') {
            steps {
                script {
                    // Stopping any active deployments in AWS to avoid conflicts
                    bat '''
                        for /f "tokens=*" %%i in ('aws deploy list-deployments --application-name SIT753 --deployment-group-name SIT753deploymentgroup --include-only-statuses InProgress --query "deployments[0]" --output text') do (
                            if not "%%i"=="None" (
                                echo Stopping deployment: %%i
                                aws deploy stop-deployment --deployment-id %%i
                            )
                        )
                    '''
                    
                    // Create a new deployment in AWS CodeDeploy
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
    }
}
