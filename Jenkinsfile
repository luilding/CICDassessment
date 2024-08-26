pipeline {
    agent any

    stages {
        stage('Release') {
            steps {
                script {
                    // List the files to verify they exist
                    bat 'dir'

                    // Compress files into a zip
                    bat 'powershell Compress-Archive -Path CVscript.py,empire.jpg,appspec.yml,scripts\\* -DestinationPath my_application.zip -Force'

                    // Upload the zip to S3
                    bat 'aws s3 cp my_application.zip s3://sit753bucket/my_application.zip'

                    // Verify the S3 upload
                    bat 'aws s3 ls s3://sit753bucket/my_application.zip'
                }
            }
        }
    }
}
