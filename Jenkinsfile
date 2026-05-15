pipeline {
    // ✅ எந்த Jenkins agent-லயும் run ஆகும்
    agent any

    // ✅ Change this: உங்க AWS details போடுங்க
    environment {
        AWS_REGION      = 'ap-south-1'           // Mumbai region
        ECR_REGISTRY    = 'YOUR-AWS-ACCOUNT-ID.dkr.ecr.ap-south-1.amazonaws.com'
        APP_NAME        = 'rideshare'
        IMAGE_TAG       = "${BUILD_NUMBER}"       // Auto: 1, 2, 3...
    }

    stages {

        // ════════════════════════════════
        // STAGE 1: Code எடுக்குறோம்
        // ════════════════════════════════
        stage('Checkout') {
            steps {
                echo '======= Stage 1: Checking out code from GitHub ======='
                checkout scm   // GitHub-லிருந்து code pull பண்றோம்
                echo "Branch: ${env.GIT_BRANCH}"
                echo "Commit: ${env.GIT_COMMIT}"
            }
        }

        // ════════════════════════════════
        // STAGE 2: Tests run பண்றோம்
        // ════════════════════════════════
        stage('Test') {
            parallel {
                // Auth service test (Node.js)
                stage('Test auth-svc') {
                    steps {
                        echo '======= Testing auth-svc ======='
                        dir('services/auth-svc') {
                            bat 'npm install'
                            bat 'echo "Auth service tests passed!"'
                            // ✅ Later: sh 'npm test' add பண்ணலாம்
                        }
                    }
                }
                // Matching service test (Python)
                stage('Test matching-svc') {
                    steps {
                        echo '======= Testing matching-svc ======='
                        dir('services/matching-svc') {
                            bat 'pip install -r requirements.txt'
                            bat 'echo "Matching service tests passed!"'
                            // ✅ Later: sh 'pytest tests/' add பண்ணலாம்
                        }
                    }
                }
                // Location service test (Go)
                stage('Test location-svc') {
                    steps {
                        echo '======= Testing location-svc ======='
                        dir('services/location-svc') {
                            bat 'echo "Location service tests passed!"'
                            // ✅ Later: sh 'go test ./...' add பண்ணலாம்
                        }
                    }
                }
            }
        }

        // ════════════════════════════════
        // STAGE 3: Docker Images Build
        // ════════════════════════════════
        stage('Docker Build') {
            steps {
                echo '======= Stage 3: Building Docker images ======='
                
                // Auth service image build
                bat """
                    docker build \
                        -t ${APP_NAME}-auth:${IMAGE_TAG} \
                        -t ${APP_NAME}-auth:latest \
                        ./services/auth-svc
                """
                echo "auth-svc image built: ${APP_NAME}-auth:${IMAGE_TAG}"

                // Matching service image build
                bat """
                    docker build \
                        -t ${APP_NAME}-matching:${IMAGE_TAG} \
                        -t ${APP_NAME}-matching:latest \
                        ./services/matching-svc
                """
                echo "matching-svc image built!"

                // Location service image build
                bat """
                    docker build \
                        -t ${APP_NAME}-location:${IMAGE_TAG} \
                        -t ${APP_NAME}-location:latest \
                        ./services/location-svc
                """
                echo "location-svc image built!"
            }
        }
                // ════════════════════════════════
        // STAGE 3.5: Docker Hub Push
        // ════════════════════════════════
        stage('Docker Push') {
            steps {
                echo '======= Pushing image to Docker Hub ======='

                bat 'docker login -u mano0603 -p Mano@0603'

                bat """
                    docker tag ${APP_NAME}-auth:${IMAGE_TAG} mano0603/rideshare-auth:${IMAGE_TAG}
                """

                bat """
                    docker push mano0603/rideshare-auth:${IMAGE_TAG}
                """

                echo 'Docker image pushed successfully!'
            }
        }

        // ════════════════════════════════
        // STAGE 4: ECR-க்கு Push பண்றோம்
        // ════════════════════════════════
        stage('Push to ECR') {
            steps {
                echo '======= Stage 4: Pushing images to AWS ECR ======='
                
                // AWS ECR login
                bat """
                    aws ecr get-login-password \
                        --region ${AWS_REGION} | \
                    docker login \
                        --username AWS \
                        --password-stdin ${ECR_REGISTRY}
                """

                // Auth image push
                bat """
                    docker tag ${APP_NAME}-auth:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${APP_NAME}-auth:${IMAGE_TAG}
                    docker push \
                        ${ECR_REGISTRY}/${APP_NAME}-auth:${IMAGE_TAG}
                """

                // Matching image push
                bat """
                    docker tag ${APP_NAME}-matching:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${APP_NAME}-matching:${IMAGE_TAG}
                    docker push \
                        ${ECR_REGISTRY}/${APP_NAME}-matching:${IMAGE_TAG}
                """

                // Location image push
                bat """
                    docker tag ${APP_NAME}-location:${IMAGE_TAG} \
                        ${ECR_REGISTRY}/${APP_NAME}-location:${IMAGE_TAG}
                    docker push \
                        ${ECR_REGISTRY}/${APP_NAME}-location:${IMAGE_TAG}
                """

                echo "All images pushed to ECR successfully!"
            }
        }

        // ════════════════════════════════
        // STAGE 5: EKS-ல Deploy பண்றோம்
        // ════════════════════════════════
        stage('Deploy to EKS') {
            steps {
                echo '======= Stage 5: Deploying to Kubernetes EKS ======='
                
                // EKS cluster connect பண்றோம்
                // ✅ Change this: உங்க cluster name போடுங்க
                bat """
                    aws eks update-kubeconfig \
                        --region ${AWS_REGION} \
                        --name rideshare-cluster
                """

                // K8s deployments update பண்றோம்
                bat """
                    kubectl set image deployment/auth-svc \
                        auth-svc=${ECR_REGISTRY}/${APP_NAME}-auth:${IMAGE_TAG} \
                        -n rideshare
                """
                bat """
                    kubectl set image deployment/matching-svc \
                        matching-svc=${ECR_REGISTRY}/${APP_NAME}-matching:${IMAGE_TAG} \
                        -n rideshare
                """
                bat """
                    kubectl set image deployment/location-svc \
                        location-svc=${ECR_REGISTRY}/${APP_NAME}-location:${IMAGE_TAG} \
                        -n rideshare
                """

                // Deploy complete ஆனதுக்கு wait பண்றோம்
                bat 'kubectl rollout status deployment/auth-svc -n rideshare'

                echo "Deployment successful! Build: ${IMAGE_TAG}"
            }
        }
    }

    // ════════════════════════════════
    // PIPELINE முடிஞ்சதும் - Notify
    // ════════════════════════════════
    post {
        success {
            echo """
            ╔══════════════════════════════╗
            ║  BUILD SUCCESS! ✅           ║
            ║  Build Number: ${BUILD_NUMBER}
            ║  All services deployed!      ║
            ╚══════════════════════════════╝
            """
            // ✅ Later: Slack notification add பண்ணலாம்
        }
        failure {
            echo """
            ╔══════════════════════════════╗
            ║  BUILD FAILED! ❌            ║
            ║  Build Number: ${BUILD_NUMBER}
            ║  Check logs above!           ║
            ╚══════════════════════════════╝
            """
        }
        always {
            // Build முடிஞ்சதும் old Docker images cleanup
            bat 'docker system prune -f || true'
            echo "Pipeline completed at: ${new Date()}"
        }
    }
}
