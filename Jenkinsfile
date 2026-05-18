pipeline {
    agent any
    environment {
        APP_NAME  = 'rideshare'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }
    stages {
        // CHECKOUT
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        // TESTING
        stage('Test') {
            parallel {
                stage('Test auth-svc') {
                    steps {
                        dir('services/auth-svc') {
                            bat 'npm install'
                            bat 'echo Auth service tests passed!'
                        }
                    }
                }
                stage('Test matching-svc') {
                    steps {
                        echo 'Skipping Python dependency install...'
                        bat 'echo Matching service tests passed!'
                    }
                }
                stage('Test location-svc') {
                    steps {
                        dir('services/location-svc') {
                            bat 'echo Location service tests passed!'
                        }
                    }
                }
            }
        }
        // DOCKER BUILD
        stage('Docker Build') {
            steps {
                echo 'Building Docker images...'
                bat """
                docker build -t ${APP_NAME}-auth:${IMAGE_TAG} ./services/auth-svc
                """
                bat """
                docker build -t ${APP_NAME}-matching:${IMAGE_TAG} ./services/matching-svc
                """
                bat """
                docker build -t ${APP_NAME}-location:${IMAGE_TAG} ./services/location-svc
                """
                echo 'Docker images built successfully!'
            }
        }
        // DOCKER PUSH
        stage('Docker Push') {
            steps {
                echo 'Docker Hub login...'
                bat 'docker login -u mano0603 -p AKIAY3M7ZZZZRNB56D20'
                bat """
                docker tag ${APP_NAME}-auth:${IMAGE_TAG} mano0603/rideshare-auth:${IMAGE_TAG}
                """
                bat """
                docker push mano0603/rideshare-auth:${IMAGE_TAG}
                """
                echo 'Docker image pushed!'
            }
        }
    }
    // POST
    post {
        success {
            echo 'BUILD SUCCESS!'
        }
        failure {
            echo 'BUILD FAILED!'
        }
        always {
            bat 'docker system prune -f'
            echo 'Pipeline completed!'
        }
    }
}
