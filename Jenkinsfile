pipeline {
    agent { label 'agent1' }
    stages {
        stage('Clean Workspace') {
            steps {
                // Clean the workspace
                sh 'docker compose down -v'
                sh 'docker rmi -f $(docker images -aq)'
                cleanWs()
            }
            post {
                failure {
                    script {
                        echo '+++++++ Clean fail!!! ++++++++'
                        def slackMessage = """
                        :white_check_mark: Clean fail!!! 

                        Project: ${env.JOB_NAME}
                        Build Number: ${env.BUILD_NUMBER}
                        Commit: ${env.GIT_COMMIT}
                        Build URL: ${env.BUILD_URL}
                        """
                        
                        slackSend(channel: 'weather-app', message: slackMessage)
                    }
                }
            }
        }
        
        stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '**']], extensions: [], userRemoteConfigs: [[credentialsId: 'my_gitlab', url: 'http://172.31.45.131/root/weather_app_repo.git']])
            }
            post {
                failure {
                    script {
                        echo '+++++++ Checkout fail!!! ++++++++'
                        def slackMessage = """
                        :white_check_mark: Checkout fail!!! 

                        Project: ${env.JOB_NAME}
                        Build Number: ${env.BUILD_NUMBER}
                        Commit: ${env.GIT_COMMIT}
                        Build URL: ${env.BUILD_URL}
                        """
                        
                        slackSend(channel: 'weather-app', message: slackMessage)
                    }
                }
            }
        }

        stage('Build Project') {
            steps {
                // build the container
                sh 'echo "Building your project..."'
                sh 'docker compose up -d'
            }
            post {
                failure {
                    script {
                        echo '+++++++ Builed fail!!! ++++++++'
                        def slackMessage = """
                        :white_check_mark: Builed fail!!! 

                        Project: ${env.JOB_NAME}
                        Build Number: ${env.BUILD_NUMBER}
                        Commit: ${env.GIT_COMMIT}
                        Build URL: ${env.BUILD_URL}
                        """
                        
                        slackSend(channel: 'weather-app', message: slackMessage)
                    }
                }
            }
        }

        stage('Testing') {
            steps {
                // test unittest
                sh 'echo "unit test website_reachable..."'
                sh 'python3 unitest_web_reachable.py'
            }
            post {
                failure {
                    script {
                        echo '+++++++ Test fail!!! ++++++++'
                        def slackMessage = """
                        :white_check_mark: Test Fail!

                        Project: ${env.JOB_NAME}
                        Build Number: ${env.BUILD_NUMBER}
                        Commit: ${env.GIT_COMMIT}
                        Build URL: ${env.BUILD_URL}
                        """
                        
                        slackSend(channel: 'weather-app', message: slackMessage)
                    }
                }
            }
        }

        stage('Push to dockerhub') {
            steps {
                script {
                    sh 'echo "pushing to dockerhub..."'

                    def version = new Date().format("yyyy.MM.dd.HH.mm.ss")
                    echo "Build successful! Version: ${version}"
                    sh 'echo "Pushing the image to DockerHub..."'
                    sh 'docker login -u 34osher -p Osh753951'
                    sh "docker tag osher_weather_app_develop-flask_app 34osher/weather_app:${version}"
                    sh "docker push 34osher/weather_app:${version}"
                }
            }
            post {
                failure {
                    script {
                        echo '+++++++ pushing to dockerhub fail!!! ++++++++'
                        def slackMessage = """
                        :white_check_mark: pushing to dockerhub Fail!

                        Project: ${env.JOB_NAME}
                        Build Number: ${env.BUILD_NUMBER}
                        Commit: ${env.GIT_COMMIT}
                        Build URL: ${env.BUILD_URL}
                        """
                    
                        slackSend(channel: 'weather-app', message: slackMessage)
                    }
                }
            }
        }
        /* stage('Clean Workspace') {
            steps {
                // Clean the workspace
                sh 'docker compose down -v'
                sh 'docker rmi -f $(docker images -aq)'
                cleanWs()
            }
        } */
    
    }
    post {
        success {
            // Define post-build actions for a successful build
            script {
                echo '+++++++ process successed ++++++++'
                def slackMessage = """
                :white_check_mark: process successed !!!

                Project: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}
                Commit: ${env.GIT_COMMIT}
                Build URL: ${env.BUILD_URL}
                """
                
                slackSend(channel: 'weather-app', message: slackMessage)
            }
        }
        failure {
            // Define actions to be taken if the build fails
            script {
                echo '+++++++ process FAILED !!! ++++++++'
                def slackMessage = """
                :white_check_mark: process FAILED !!!

                Project: ${env.JOB_NAME}
                Build Number: ${env.BUILD_NUMBER}
                Commit: ${env.GIT_COMMIT}
                Build URL: ${env.BUILD_URL}
                """
                
                slackSend(channel: 'weather-app', message: slackMessage)
            }

        }
    }
}
