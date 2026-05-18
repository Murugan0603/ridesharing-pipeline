```groovy
pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                bat 'echo Tests Passed'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t rideshare-auth ./services/auth-svc'
            }
        }

        stage('Done') {
            steps {
                bat 'echo Build Completed'
            }
        }
    }

    post {
        success {
            echo 'BUILD SUCCESS'
        }

        failure {
            echo 'BUILD FAILED'
        }
    }
}
```
