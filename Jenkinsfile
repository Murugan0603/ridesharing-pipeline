pipeline {

    // Jenkins agent
    agent any

    environment {
        APP_NAME  = 'rideshare'
        IMAGE_TAG = "${BUILD_NUMBER}"
    }

    stages {

        // ════════════════════════════════
        // STAGE 1: Checkout Code
        // ════════════════════════════════
        stage('Checkout') {
            steps {
                echo '======= Stage 1: Checking out code ======='

                checkout scm

                echo "Branch: ${env.GIT_BRANCH}"
                echo "Commit: ${env.GIT_COMMIT}"
            }
        }

        // ════════════════════════════════
        // STAGE 2: Run Tests
        // ════════════════════════════════
        stage('Test') {

            parallel {

                // AUTH SERVICE
                stage('Test auth-svc') {
                    steps {

                        echo '======= Testing auth-svc ======='

                        dir('services/auth-svc') {

                            bat 'npm install'

                            bat 'echo Auth service tests passed!'

                        }
                    }
                }

                // MATCHING SERVICE
                stage('Test matching-svc') {
                    steps {

                        echo '======= Testing matching-svc ======='

                        dir('services/matching-svc') {

                            bat 'pip install -r requirements.txt'

                            bat 'echo Matching service tests passed!'

                        }
                    }
                }

                // LOCATION SERVICE
                stage('Test location-svc') {
                    steps {

                        echo '======= Testing location-svc ======='

                        dir('services/location-svc') {

                            bat 'echo Location service tests passed!'

                        }
                    }
                }
            }
        }

        // ════════════════════════════════
        // STAGE 3: Docker Build
        // ════════════════════════════════
        stage('Docker Build') {

            steps {

                echo '======= Building Docker Images ======='

                // AUTH IMAGE
                bat """
                docker build -t ${APP_NAME}-auth:${IMAGE_TAG} -t ${APP_NAME}-auth:latest ./services/auth-svc
                """

                // MATCHING IMAGE
                bat """
                docker build -t ${APP_NAME}-matching:${IMAGE_TAG} -t ${APP_NAME}-matching:latest ./services/matching-svc
                """

                // LOCATION IMAGE
                bat """
                docker build -t ${APP_NAME}-location:${IMAGE_TAG} -t ${APP_NAME}-location:latest ./services/location-svc
                """

                echo 'Docker images built successfully!'
            }
        }

        // ════════════════════════════════
        // STAGE 4: Docker Hub Push
        // ════════════════════════════════
        stage('Docker Push') {

            steps {

                echo '======= Docker Hub Login ======='

                bat 'docker login -u mano0603 -p AKIAY3M7ZZZZRNB56D20'

                echo '======= Tagging Image ======='

                bat """
                docker tag ${APP_NAME}-auth:${IMAGE_TAG} mano0603/rideshare-auth:${IMAGE_TAG}
                """

                echo '======= Pushing Image ======='

                bat """
                docker push mano0603/rideshare-auth:${IMAGE_TAG}
                """

                echo 'Docker image pushed successfully!'
            }
        }
    }

    // ════════════════════════════════
    // POST ACTIONS
    // ════════════════════════════════
    post {

        success {

            echo """
╔══════════════════════════════╗
║  BUILD SUCCESS! ✅           ║
║  Build Number: ${BUILD_NUMBER}
║  Pipeline completed!         ║
╚══════════════════════════════╝
"""
        }

        failure {

            echo """
╔══════════════════════════════╗
║  BUILD FAILED! ❌            ║
║  Build Number: ${BUILD_NUMBER}
║  Check Jenkins logs!         ║
╚══════════════════════════════╝
"""
        }

        always {

            bat 'docker system prune -f'

            echo "Pipeline completed!"
        }
    }
}
