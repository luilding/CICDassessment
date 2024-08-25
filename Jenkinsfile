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

            echo "Raw API Response: ${response}"

            def monitors = readJSON(text: response)
            def alertingMonitors = monitors.findAll { it.overall_state == 'Alert' }

            if (alertingMonitors) {
                def alertDetails = alertingMonitors.collect { monitor ->
                    return "Monitor Name: ${monitor.name}\nMessage: ${monitor.message}\nQuery: ${monitor.query}\nCurrent State: ${monitor.overall_state}"
                }.join("\n\n")

                echo "Triggered Alerts:\n${alertDetails}"
                
                mail to: 'lguilding@deakin.edu.au',
                     subject: "Datadog Alerts: Issues Detected in Production",
                     body: "The following monitors have triggered alerts:\n\n${alertDetails}"
            } else {
                echo "No alerting monitors found."
            }
        }
    }
}
