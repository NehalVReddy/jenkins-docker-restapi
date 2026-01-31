pipeline {
    agent any

    environment {
        IMAGE_NAME = "jenkins-demo-app"
        JENKINS_URL = "http://localhost:8080"
        JOB_NAME = "Docker_App_Pipeline"
        USERNAME = "admin"
        API_TOKEN = credentials('jenkins-api-token')
    }

    stages {

        stage('Checkout from GitHub') {
            steps {
                git(
                    url: 'https://github.com/NehalVReddy/jenkins-docker-restapi.git',
                    credentialsId: 'github-pat',
                    branch: 'main'
                    )
                 }
            }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_NAME% .'
            }
        }

        stage('Run Container') {
            steps {
                bat '''
                docker rm -f demo || true
                docker run -d --name demo -p 5000:5000 %IMAGE_NAME%
                '''
            }
        }

        stage('Fetch Last 5 Jenkins Builds') {
            steps {
                bat """
                curl -s -u $USERNAME:$API_TOKEN \
                "$JENKINS_URL/job/$JOB_NAME/api/json?tree=builds[number,result,timestamp,duration,url]{0,5}" \
                > builds.json
                """
            }
        }

        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'builds.json'
            }
        }
    }
}
