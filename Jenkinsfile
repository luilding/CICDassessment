pipeline {
    agent any

    environment {
        DATADOG_API_KEY = credentials('datadog_api_key')
        DATADOG_APPLICATION_KEY = credentials('datadog_application_key')
    }

    stages {
        stage('Deploy') {
            steps {
                script {
                    // Deploy the application
                    bat """
                        docker-compose down || exit 0
                        docker rm -f comp_v_app || exit 0 
                        docker-compose up -d --build
                    """
                    
                    // Wait for the application to start and for Datadog to collect initial metrics
                    sleep time: 1, unit: 'MINUTES'
                }
            }
        }

        stage('Verify Datadog Monitoring') {
            steps {
                script {
                    // Query Datadog for basic container metrics
                    def response = bat(
                        script: """
                            curl -s -X GET "https://api.datadoghq.com/api/v1/query?from=%{time.to_i - 300}&to=%{time.to_i}&query=avg:docker.cpu.usage{container:comp_v_app}" ^
                            -H "Content-Type: application/json" ^
                            -H "DD-API-KEY: %DATADOG_API_KEY%" ^
                            -H "DD-APPLICATION-KEY: %DATADOG_APPLICATION_KEY%"
                        """,
                        returnStdout: true
                    ).trim()
                    
                    echo "Datadog API Response:"
                    echo response
                    
                    // Check if we received data
                    def jsonResponse = readJSON text: response
                    if (jsonResponse.series && jsonResponse.series[0].pointlist) {
                        echo "Successfully received metrics from Datadog for container comp_v_app"
                        echo "Datadog is monitoring the Docker container"
                    } else {
                        error "No data received from Datadog. Check your configuration and ensure Datadog is monitoring your Docker container."
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up
            bat 'docker-compose down'
        }
    }
}
