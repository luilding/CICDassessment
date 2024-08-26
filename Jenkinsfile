pipeline {
    agent any
    stages {
        stage('Release') {
            steps {
                script {
                    // Package the application files
                    bat 'powershell Compress-Archive -Path CVscript.py,empire.jpg,appspec.yml,scripts\\* -DestinationPath my_application.zip -Force'

                    // Upload the package to S3
                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'

                    // Check for active deployments and capture the deployment ID
                    def activeDeployment = bat(script: 'aws deploy list-deployments --application-name SIT753 --deployment-group-name SIT753deploymentgroup --include-only-statuses InProgress --query "deployments[0]" --output text', returnStdout: true).trim()

                    // If an active deployment is found, stop it
                    if (activeDeployment != "None") {
                        echo "Stopping active deployment: ${activeDeployment}"
                        bat "aws deploy stop-deployment --deployment-id ${activeDeployment}"
                    }

                    // Create a new deployment in CodeDeploy
                    bat 'aws deploy create-deployment --application-name SIT753 --deployment-group-name SIT753deploymentgroup --s3-location bucket=sit753bucket,bundleType=zip,key=my_application.zip --file-exists-behavior OVERWRITE'
                }
            }
        }
    }
}
