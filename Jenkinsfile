pipeline{
    agent any
    tools {
        jdk 'jdk17'
        nodejs 'node16'
    }
    environment {
        SCANNER_HOME=tool 'sonar-scanner'
    }
    stages {
        stage ("Git Checkout Code"){
            steps{
                git branch: 'main', url: 'https://github.com/ganeshsnp987/Uptime-kuma.git'
            }
        }
        stage('Install Dependencies') {
            steps {
                sh "npm install"
            }
        }
        stage("Sonarqube Analysis "){
            steps{
                withSonarQubeEnv('sonar-server') {
                    sh ''' $SCANNER_HOME/bin/sonar-scanner -Dsonar.projectName=Chatbot \
                    -Dsonar.projectKey=Chatbot '''
                }
            }
        }
        stage('Sonar-quality-gate') {
            steps {
                script{
                    waitForQualityGate abortPipeline: false, credentialsId: 'Sonar'
                }
            }
        }
        stage('OWASP FS SCAN') {
            steps {
                dependencyCheck additionalArguments: '--scan ./ --disableYarnAudit --disableNodeAudit', odcInstallation: 'DP-Check'
                dependencyCheckPublisher pattern: '**/dependency-check-report.xml'
            }
        }
        stage('TRIVY FS SCAN') {
            steps {
                sh "trivy fs . > trivyfs.json"
            }
        }
        stage("Docker Build & Push"){
            steps{
                script{
                   withDockerRegistry(credentialsId: 'docker-cred', toolName: 'docker'){   
                       sh "docker build -t uptime ."
                       sh "docker tag uptime ganeshsnp987/uptime:latest"
                       sh "docker push ganeshsnp987/uptime:latest"
                    }
                }
            }
        }
        stage("TRIVY"){
            steps{
                sh "trivy image ganeshsnp987/uptime:latest > trivy.json" 
            }
        }
        stage ("Remove container") {
            steps{
                sh "docker stop uptime | true"
                sh "docker rm uptime | true"
             }
        }
        stage('Deploy to container'){
            steps{
                sh 'docker run -d --name uptime -v /var/run/docker.sock:/var/run/docker.sock -p 3001:3001 ganeshsnp987/uptime:latest'
            }
        }
    }
}
