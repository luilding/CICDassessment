pipeline {
    agent any
    stages {
        stage('Deploy') {
            steps {
                script {
                    // Check and stop active deployments if any
                    bat '''
                        set "deploymentId="
                        for /f %%i in ('aws deploy list-deployments --application-name SIT753 --deployment-group-name SIT753deploymentgroup --include-only-statuses InProgress --query "deployments[0]" --output text') do set deploymentId=%%i
                        if not "%deploymentId%"=="None" aws deploy stop-deployment --deployment-id %deploymentId%
                    '''

                    // Compress the entire workspace to maintain folder structure
                    bat 'powershell Compress-Archive -Path * -DestinationPath my_application.zip -Force'

                    // Upload the package to S3
                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'

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
