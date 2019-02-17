pipeline {
    agent any

    environment { 
        SSH_KEY = credentials('path/to/key')
        SSH_USER = credentials('user')
        DOCKER_REGISTRY=’https://syst14/flask-crud'
    }

    stages {
        stage('Clean Workspace before build') {
            steps {
                cleanWs()
            }
        }
        stage('configure nodes') {
            ansiblePlaybook( 
            playbook: 'networksetup-plb.yml',
            inventory: env.INVENTORY_LIST + ',',
            credentialsId: env.SSH_KEY,
            hostKeyChecking: false,
            extras: '-u ' + env.SSH_USER
            )
        }
        stage('configure cluster') {
            ansiblePlaybook( 
            playbook: 'swarm.yml',
            inventory: env.INVENTORY_LIST + ',',
            credentialsId: env.SSH_KEY,
            hostKeyChecking: false,
            extras: '-u ' + env.SSH_USER
            )
        }
        stage('Build image') {
             steps {
        sh 'docker build -f "Dockerfile" -t syst14/flask-crud:latest .'
        }
        }
        stage('Publish') {
        steps {
            withDockerRegistry("${DOCKER_REGISTRY}", 'docker-registry-credentials') {
                sh 'docker push syst14/flask-crud:latest'
            }
        }
        }
        stage('Deploy'){
            stage('configure cluster') {
            ansiblePlaybook( 
            playbook: 'swarmapp.yml',
            inventory: env.INVENTORY_LIST + ',',
            credentialsId: env.SSH_KEY,
            hostKeyChecking: false,
            extras: '-u ' + env.SSH_USER
            )
            }
        }
    }
    post {
        always {
            cleanWs()
            }
        }
}