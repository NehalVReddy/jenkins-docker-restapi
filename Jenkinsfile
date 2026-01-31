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

        // stage('Fetch Last 5 Jenkins Builds') {
        //     steps {
        //         withCredentials([string(credentialsId: 'jenkins-api-token', variable: 'API_TOKEN')]) {
        //             bat '''
        //             curl -s -u %USERNAME%:%API_TOKEN% ^
        //             "%JENKINS_URL%/job/%JOB_NAME%/api/json" ^
        //             > builds.json
        //             '''
        //         }
        //     }
        // }
        stage('Fetch Last 5 Jenkins Builds') {
            steps {
                withCredentials([string(credentialsId: 'jenkins-api-token', variable: 'API_TOKEN')]) {
                    powershell '''
                        $counterFile = "counter.txt"
                        if (!(Test-Path $counterFile)) {
                            Set-Content $counterFile "0"
                        }
        
                        $count = [int](Get-Content $counterFile) + 1
                        Set-Content $counterFile $count
        
                        $outputFile = "last5_builds.json$count"
                        Write-Host "Saving build info to $outputFile"
        
                        $auth = [Convert]::ToBase64String(
                            [Text.Encoding]::ASCII.GetBytes("admin:$env:API_TOKEN")
                        )
        
                        Invoke-WebRequest `
                            -Uri "http://localhost:8080/job/pipe/api/json?tree=builds[number,result,timestamp,duration,url]{0,5}" `
                            -Headers @{ Authorization = "Basic $auth" } `
                            -OutFile $outputFile
                    '''
                }
            }
        }




        stage('Debug builds.json') {
            steps {
                bat 'type builds.json'
            }
        }


        stage('Archive Results') {
            steps {
                archiveArtifacts artifacts: 'build.json,last5_builds.json*', fingerprint: true
            }
        }
    }
}
