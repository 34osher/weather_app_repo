pipeline {
    agent { label 'agent1' }
    options {
        buildDiscarder logRotator(artifactDaysToKeepStr: '', artifactNumToKeepStr: '5', daysToKeepStr: '', numToKeepStr: '5')
    }

    stages {
        stage('Clean Workspace') {
            steps {
                // Clean the workspace
                //sh 'docker stop $(docker ps -aq) || echo "stop containers"'
                sh 'docker compose down -v || echo "delete if ther is images"'
                sh 'docker rm -f $(docker ps -aq) || echo "stop containers & delete"'
                sh 'docker rmi -f $(docker images -aq) || echo "delete if ther is images"'
                sh 'docker system prune -af'
                cleanWs()
            }
            post {
                failure {
                    script {
                        echo '+++++++ Clean fail!!! ++++++++'
                        def slackMessage = """
                        :bangbang: Clean fail!!! 

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
                        echo '+++++++  Checkout fail!!! ++++++++'
                        def slackMessage = """
                        :bangbang: Checkout fail!!! 

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
                        :bangbang: Builed fail!!! 

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
                //   test unittest
                sh 'echo "unit test website_reachable..."'
                sh 'python3 unitest_web_reachable.py'
            }
            post {
                failure {
                    script {
                        echo '+++++++ Test fail!!! ++++++++'
                        def slackMessage = """
                        :bangbang: Test Fail!

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

                    def version = new Date().format("yyyyMMddHHmm")
                    echo "Build successful! Version: ${version}"
                    sh 'echo "Pushing the image to DockerHub..."'

                    withCredentials([usernamePassword(credentialsId: 'doukerHub', passwordVariable: 'DOCKERHUB_PASSWORD', usernameVariable: 'DOCKERHUB_USERNAME')]) {
                        sh 'docker login -u $DOCKERHUB_USERNAME -p $DOCKERHUB_PASSWORD'
                        sh "docker tag osher-flask_app 34osher/weather_app:${version}"
                        sh "docker push 34osher/weather_app:${version}"
                    }
                }
            }
            post {
                failure {
                    script {
                        echo '+++++++ pushing to dockerhub fail!!! ++++++++'
                        def slackMessage = """
                        :bangbang: pushing to dockerhub Fail!

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
        stage('Deploy') {
            steps {
                sh 'echo "Deploy on instance..."' 
                sshagent(credentials: ['weather_app_instance']) {
                    sh 'ssh ubuntu@172.31.42.205 "rm  -r -f /home/ubuntu/deploy/*"'

                    sh 'scp ./deploy_compose/docker-compose.yaml ubuntu@172.31.42.205:/home/ubuntu/deploy/'
                    sh 'scp ./deploy_compose/deploy_script.sh ubuntu@172.31.42.205:/home/ubuntu/deploy/'

                    sh 'scp ./default.conf ubuntu@172.31.42.205:/home/ubuntu/deploy/'

                    sh 'ssh ubuntu@172.31.42.205 "./deploy/deploy_script.sh"'  
                }            
            }
            post {
                failure {
                    script {
                        echo '+++++++ Deploy on instance fail!!! ++++++++'
                        def slackMessage = """
                        :bangbang: Deploy on instance Fail!

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
        // stage('Clean after deploy Workspace') {
        //     steps {
        //         // Clean the workspace
        //         sh 'docker compose down -v'
        //         sh 'docker rmi -f $(docker images -aq)'
        //         sh 'docker system prune -af'
        //         cleanWs()
        //     }
        //     post {
        //         failure {
        //             script {
        //                 echo '+++++++ Clean after deploy fail!!! ++++++++'
        //                 def slackMessage = """
        //                 :bangbang: Clean after deploy fail!!! 

        //                 Project: ${env.JOB_NAME}
        //                 Build Number: ${env.BUILD_NUMBER}
        //                 Commit: ${env.GIT_COMMIT}
        //                 Build URL: ${env.BUILD_URL}
        //                 """
                        
        //                 slackSend(channel: 'weather-app', message: slackMessage)
        //             }
        //         }
        //     }
        //}
    
    }
    post {
        always {
            // Clean the workspace
            sh 'docker compose down -v'
            sh 'docker rmi -f $(docker images -aq)'
            sh 'docker system prune -af'
            cleanWs()
        }
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
                :bangbang: process FAILED !!!

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
