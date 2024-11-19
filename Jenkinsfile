pipeline {
    agent any

    environment {
        DOCKER_COMPOSE_VERSION = '1.29.2' // Specify your Docker Compose version
    }

    stages {
        stage('Clone Repository') {
            steps {
                // Clone the repository containing the Dockerized Flask app
                git 'https://github.com/1901639/Lenguajes_ModernosPIA.git'
            }
        }

        stage('Setup Docker') {
            steps {
                // Install Docker Compose if not already installed
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
                // Build and run the containers
                sh 'docker-compose down' // Stop existing containers (if any)
                sh 'docker-compose up --build -d'
            }
        }

        stage('Verify Deployment') {
            steps {
                // Check that the Flask app is running
                sh 'curl -f http://localhost:5000 || exit 1'
            }
        }
    }

    post {
        always {
            // Clean up containers after pipeline completion
            sh 'docker-compose down'
        }
    }
}