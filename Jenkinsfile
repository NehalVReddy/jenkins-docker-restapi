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
                    $baseFile = "last5_builds.json"
        
                    # Find existing files
                    $existing = Get-ChildItem "$baseFile*" -ErrorAction SilentlyContinue
        
                    if ($existing) {
                        $numbers = $existing.Name |
                            ForEach-Object {
                                if ($_ -match 'json(\\d+)$') { [int]$matches[1] }
                            }
                        $next = ($numbers | Measure-Object -Maximum).Maximum + 1
                    } else {
                        $next = 1
                    }
        
                    $outputFile = "$baseFile$next"
        
                    Write-Host "Saving build info to $outputFile"
        
                    curl -s -u admin:$env:API_TOKEN `
                      "http://localhost:8080/job/Docker_App_Pipeline/api/json?tree=builds[number,result,timestamp,duration,url]{0,5}" `
                      > $outputFile
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
