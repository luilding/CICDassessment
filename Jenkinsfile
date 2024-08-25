pipeline {
    agent any

    environment {
        DATADOG_API_KEY = credentials('datadog_api_key')
        DATADOG_APPLICATION_KEY = credentials('datadog_application_key')
    }

    stages {
       
        stage('Monitoring and Alerting') {
            steps {
                script {
                    def response = bat(
                        script: """
                            curl -s -X GET "https://api.us5.datadoghq.com/api/v1/monitor" ^
                            -H "Content-Type: application/json" ^
                            -H "DD-API-KEY: %DATADOG_API_KEY%" ^
                            -H "DD-APPLICATION-KEY: %DATADOG_APPLICATION_KEY%"
                        """,
                        returnStdout: true
                    ).trim()
                    
                    echo "Raw API Response:"
                    echo response
                    
                    def jsonResponse = response.readLines().last() // Get the last line, which should be the JSON
                    
                    def monitors = readJSON text: jsonResponse
                    def alertingMonitors = monitors.findAll { it.overall_state == 'Alert' }
        
                    if (alertingMonitors) {
                        def monitorNames = alertingMonitors.collect { it.name }.join(", ")
                        error "Failing build due to triggered Datadog monitors: ${monitorNames}"
                    } else {
                        echo "No alerting monitors found."
                    }
                }
            }
        }
    }
}
