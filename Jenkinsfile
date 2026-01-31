pipeline {
    agent any

    environment {
        IMAGE_NAME = "jenkins-demo-app"
        JENKINS_URL = "http://localhost:8080"
        JOB_NAME = "pipe"
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
                withCredentials([string(credentialsId: 'jenkins-api-token', variable: 'API_TOKEN')]) {
                    bat '''
                    curl -s -u %USERNAME%:%API_TOKEN% ^
                    "%JENKINS_URL%/job/%JOB_NAME%/api/json" ^
                    > builds.json
                    '''
                }
            }
        }
        stage('Extract Last 5 Builds') {
            steps {
                powershell '''
                $json = Get-Content builds.json -Raw | ConvertFrom-Json
        
                $last5 = $json.builds | Select-Object -First 5
        
                $last5 | ConvertTo-Json -Depth 6 | Out-File last5_builds.json
                '''
            }
        }



        stage('Debug builds.json') {
            steps {
                bat 'type builds.json'
            }
        }


        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'builds.json'
            }
        }
    }
}
