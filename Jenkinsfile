pipeline {
    agent any
    stages {
        stage('Stop Existing Deployments') {
            steps {
                script {
                    // List and stop current deployments in one step
                    bat(script: '''
                        for /f "tokens=*" %%i in ('aws deploy list-deployments --application-name SIT753 --deployment-group-name SIT753deploymentgroup --query "deployments[?status==\'InProgress\']" --output text') do (
                            echo Stopping deployment: %%i
                            aws deploy stop-deployment --deployment-id %%i
                        )
                    ''', returnStatus: true)
                }
            }
        }
        stage('Release') {
            steps {
                script {
                    // List the files to verify they exist
                    bat 'dir'
                    // Compress files into a zip (without the non-existent scripts directory)
                    bat 'powershell Compress-Archive -Path CVscript.py,empire.jpg,appspec.yml,run_script.sh -DestinationPath my_application.zip -Force'
                    // Upload the zip to S3
                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'
                    // Verify the S3 upload
                    bat 'aws s3 ls s3://sit753bucket/my_application.zip'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    // Start a new deployment
                    bat '''
                        aws deploy create-deployment --application-name SIT753 --deployment-group-name SIT753deploymentgroup --s3-location bucket=sit753bucket,bundleType=zip,key=my_application.zip --file-exists-behavior OVERWRITE
                    '''
                }
            }
        }
    }
}
