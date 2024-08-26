pipeline {
    agent any

    environment {
        //To get sensitive details from Jenkins
        DATADOG_API_KEY = credentials('datadog_api_key')
        DATADOG_APPLICATION_KEY = credentials('datadog_application_key')
    }

    stages {
        stage('Deploy with Docker') {
            steps {
                //Deploying the application into a Docker container in detached mode
                bat """
                    docker-compose down || exit 0
                    docker rm -f comp_v_app || exit 0 
                    docker-compose up --build -d
                """
            }
        }

        stage('Monitoring and Alerting with Datadog') {
            steps {
                script {
                    //Checking Datadog monitor views for any alerts related to the running Docker container
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
                    
                    //Parse the JSON response from Datadog API
                    def jsonResponse = response.readLines().last() 
                    
                    //Find monitors that are currently alerting
                    def monitors = readJSON text: jsonResponse
                    def alertingMonitors = monitors.findAll { it.overall_state == 'Alert' }
        
                    //If any monitors are currently alerting, generate email notification including the alert details
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
                        
                        //Sending the email with details of the alerts
                        mail to: 'lguilding@deakin.edu.au',
                             subject: "Datadog Alerts: Issues Detected in Production",
                             body: "The following monitors have triggered alerts:\n\n${alertDetails}"
                    } else {
                        //If no alerts are found, log that it is fine
                        echo "No alerting monitors found."
                    }
                }
            }
        }
    }
}
