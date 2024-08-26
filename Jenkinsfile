pipeline {
    agent any
    stages {
        stage('Release') {
            steps {
                script {
                    // Set the executable permission on run_script.sh using PowerShell
                    bat 'powershell -Command "Set-ItemProperty -Path .\\scripts\\run_script.sh -Name IsReadOnly -Value $false"'
                    
                    // Archive all the necessary files into a zip file
                    bat 'powershell Compress-Archive -Path CVscript.py,empire.jpg,appspec.yml,scripts -DestinationPath my_application.zip -Force'

                    // Upload the packaged application to the specified S3 bucket
                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'

                    // Create a new deployment in AWS CodeDeploy using the uploaded package
                    bat 'aws deploy create-deployment --application-name SIT753 --deployment-group-name SIT753deploymentgroup --s3-location bucket=sit753bucket,bundleType=zip,key=my_application.zip --file-exists-behavior OVERWRITE'
                }
            }
        }
    }
}
