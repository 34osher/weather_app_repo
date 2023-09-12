pipeline {
    agent { label 'agent1' }
    stages {
        stage('Clean Workspace') {
            steps {
                // Clean the workspace
                cleanWs()
            }
        }
        
        stage('Checkout')
        {
            steps {
                checkout scmGit(branches: [[name: '**']], extensions: [], userRemoteConfigs: [[credentialsId: 'my_gitlab', url: 'http://172.31.45.131/root/weather_app_repo.git']])
            }
        }
        stage('Build Project') {
            steps {
                // build the container
                sh 'echo "Building your project..."'
                sh 'docker compose up -d'
            }
        }
        stage('Testing') {
            steps {
                // test unittest
                sh 'echo "unit test website_reachable..."'
                sh 'python3 unitest_web_reachable.py'
            }   
        }
       
    }
    post {
        success {
            // Define post-build actions for a successful build
            echo 'Build successful!'
            stage('Push to DockerHub') {
                steps {
                     // DockerHub
                     sh 'echo "Pushing the image to DockerHub..."'
                     sh 'docker login -u 34osher -p Osh753951'
                     sh 'docker tag weather_app:1 34osher/weather_app1:2'
                     sh 'docker push 34osher/osher_repo:latest'
                }   
            }
        }
        failure {
            // Define actions to be taken if the build fails
            echo 'Build failed!'
        }
    }
}
