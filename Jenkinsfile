pipeline {
    agent any
    stages {
        stage('Package and Deploy') {
            steps {
                script {
                    // Package the application files
                    bat 'powershell Compress-Archive -Path CVscript.py,empire.jpg,appspec.yml,scripts\\* -DestinationPath my_application.zip -Force'
                    
                    // Upload the package to S3
                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'
                    
                    // Create a new deployment in CodeDeploy, ignoring application stop failures
                    bat '''
                        aws deploy create-deployment ^
                        --application-name SIT753 ^
                        --deployment-group-name SIT753deploymentgroup ^
                        --s3-location bucket=sit753bucket,bundleType=zip,key=my_application.zip ^
                        --file-exists-behavior OVERWRITE ^
                        --ignore-application-stop-failures
                    '''
                }
            }
        }
    }
}
