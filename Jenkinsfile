pipeline {
    agent any
    stages {
        stage('Package') {
            steps {
                script {
                    bat 'powershell Compress-Archive -Path CVscript.py,empire.jpg,appspec.yml,scripts -DestinationPath my_application.zip -Force'
                }
            }
        }
        stage('Upload to S3') {
            steps {
                script {
                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'
                }
            }
        }
        stage('Deploy') {
            steps {
                script {
                    bat 'aws deploy create-deployment --application-name SIT753 --deployment-group-name SIT753deploymentgroup --s3-location bucket=sit753bucket,bundleType=zip,key=my_application.zip --file-exists-behavior OVERWRITE'
                }
            }
        }
    }
}
