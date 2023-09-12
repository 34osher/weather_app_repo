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
                // Replace this with actual build commands for your project
                sh 'echo "Building your project..."'
            }
        }
    }
    post {
        success {
            // Define post-build actions for a successful build
            echo 'Build successful!'
        }
        failure {
            // Define actions to be taken if the build fails
            echo 'Build failed!'
        }
    }
}
