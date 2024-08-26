pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                script {
                    // Stop active deployments
                    bat '''
                        for /f "tokens=*" %%i in ('aws deploy list-deployments --application-name SIT753 --deployment-group-name SIT753deploymentgroup --include-only-statuses InProgress --query "deployments[0]" --output text') do (
                            if not "%%i"=="None" (
                                echo Stopping deployment: %%i
                                aws deploy stop-deployment --deployment-id %%i
                            )
                        )
                    '''
                    
                    // Create new deployment
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
