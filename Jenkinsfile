pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_VERSION = '1.29.2'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git branch: 'main', url: 'https://github.com/1901639/Lenguajes_ModernosPIA.git'
            }
        }

        stage('Setup Docker') {
            steps {
                sh '''
                if ! [ -x "$(command -v docker-compose)" ]; then
                  echo "Installing Docker Compose..."
                  sudo curl -L "https://github.com/docker/compose/releases/download/$DOCKER_COMPOSE_VERSION/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
                  sudo chmod +x /usr/local/bin/docker-compose
                fi
                '''
            }
        }

        stage('Build and Deploy') {
            steps {
                sh 'docker-compose down'
                sh 'docker-compose up --build -d'
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'curl -f http://localhost:5000 || exit 1'
            }
        }
    }

    post {
        success {
            script {
                echo 'App is running. Stop the containers manually when done.'
                echo 'Run the following command to stop the app:'
                echo '${DOCKER_COMPOSE_CMD} down'
            }
        }
        failure {
            sh '${DOCKER_COMPOSE_CMD} down || true'
        }
    }
}