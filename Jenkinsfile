pipeline {
    agent any

    environment {
        // Define environment variables
        DB_PASSWORD = '1a.2b.3c,'
    }

    stages {
        stage('Checkout Code') {
            steps {
                // Checkout your repository
                git branch: 'main', url: 'https://github.com/1901639/Lenguajes_ModernosPIA.git'
            }
        }

        stage('Build and Run Services') {
            steps {
                // Ensure Docker Compose is up-to-date
                sh 'docker-compose --version'

                // Build and start the containers
                sh 'docker-compose up --build -d'
            }
        }

        stage('Wait for Services to Initialize') {
            steps {
                // Wait for MySQL to be ready
                script {
                    def retries = 10
                    def success = false

                    for (int i = 0; i < retries; i++) {
                        try {
                            sh 'docker exec $(docker ps -q -f name=mysql-db) mysqladmin ping -u root --password=${DB_PASSWORD}'
                            success = true
                            break
                        } catch (Exception e) {
                            echo "Database not ready yet. Retrying in 5 seconds..."
                            sleep(5)
                        }
                    }

                    if (!success) {
                        error "Database failed to initialize within timeout"
                    }
                }
            }
        }

        stage('Test Application') {
            steps {
                // Optionally, run a health check or test the Flask app
                sh 'curl -f http://localhost:5000 || exit 1'
            }
        }
    }

    post {
        always {
            // Stop and remove containers after execution
            sh 'docker-compose down'
        }
    }
}
