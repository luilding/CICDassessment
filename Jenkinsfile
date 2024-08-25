pipeline {
    agent any

    environment {
        DATADOG_API_KEY = credentials('datadog_api_key')
        DATADOG_APPLICATION_KEY = credentials('datadog_application_key')
    }

    stages {
       
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
                        def alertDetails = alertingMonitors.collect { monitor ->
                            return """
                            Monitor Name: ${monitor.name}
                            Message: ${monitor.message}
                            Query: ${monitor.query}
                            Current State: ${monitor.overall_state}
                            """
                        }.join("\n\n")

                        echo "Triggered Alerts:\n${alertDetails}"
                        
                        // Send an email alert with details of each monitor alert
                        mail to: 'team@example.com',
                             subject: "Datadog Alerts: Issues Detected in Production",
                             body: "The following monitors have triggered alerts:\n\n${alertDetails}"
                    } else {
                        echo "No alerting monitors found."
                    }
                }
            }
        }
    }
}

    }
}
