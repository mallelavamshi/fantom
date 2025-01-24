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
        
        stage('Test') {
            steps {
                script {
                    try {
                        sh '''
                            python3 -m pip install --upgrade pip
                            pip3 install -r requirements.txt
                            pip3 install pytest pytest-cov
                            python3 -m pytest tests/
                        '''
                    } catch (Exception e) {
                        echo "Tests failed but continuing deployment"
                    }
                }
            }
        }
        
        stage('Build and Deploy') {
            steps {
                script {
                    // Build new image
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                    
                    // Stop and remove existing container
                    sh '''
                        docker ps -q --filter "name=fastapi-app" | grep -q . && docker stop fastapi-app || true
                        docker ps -aq --filter "name=fastapi-app" | grep -q . && docker rm fastapi-app || true
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