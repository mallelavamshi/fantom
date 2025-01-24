pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'fastapi-app'
        DOCKER_TAG = "${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build and Deploy') {
            steps {
                script {
                    // Build the Docker image
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    
                    // Stop and remove existing container if it exists
                    sh '''
                        docker ps -q --filter "name=fastapi-app" | xargs -r docker stop
                        docker ps -aq --filter "name=fastapi-app" | xargs -r docker rm
                    '''
                    
                    // Run new container
                    sh """
                        docker run -d \
                            --name fastapi-app \
                            -p 8000:8000 \
                            --restart unless-stopped \
                            ${DOCKER_IMAGE}:${DOCKER_TAG}
                    """
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker image prune -f || true'
        }
    }
}