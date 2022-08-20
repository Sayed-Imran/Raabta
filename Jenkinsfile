pipeline {
    agent any
    environment {
        
        AWS_DEFAULT_REGION='ap-south-1'
    }
    stages {
        stage('Start AWS EC2 Instances') {
            steps {
                withCredentials([aws(accessKeyVariable:'AWS_ACCESS_KEY_ID',credentialsId:'aws-ec2-creds',secretKeyVaraiable:'AWS_SECRET_ACCESS_KEY')]) {
                  sh '''
	                aws ec2 start-instances --instance-ids 	i-04f26a216c4476e82
	                '''
                }
            }
        }
        stage('Building backend Docker Image'){
            agent{
                label 'docker'
            }
            steps{
                sh'''
                    docker system prune -f
                    docker build -t sayedimran/rabbta-backend:latest ./backend/
                '''
            }
        }
        stage('Pushing the backend Docker Image'){
            agent{
                label 'docker'
            }
            steps{
                sh'''
                    docker push sayedimran/raabta-backend:latest
                '''
            }
        }
        stage('Building frontend Docker Image'){
            agent{
                label 'docker'
            }
            steps{
                sh'''
                    docker system prune -f
                    docker build -t sayedimran/raabta-frontend:latest  ./frontend/
                '''
            }
        }
        stage('Pushing the frontend Docker Image'){
            agent{
                label 'docker'
            }
            steps{
                sh'''
                    docker push sayedimran/raabta-frontend:latest
                '''
            }
        }
        stage('Cleaning Up the temporary images'){
            agent{
                label 'docker'
            }
            steps{
                sh'''
                    docker system prune -f
                '''
            }
        }
	stage('Eliminating the existing containers'){
            steps{
                sh'''
                    docker stop backend frontend
		    docker rm backend frontend
		    docker rmi sayedimran/raabta-backend:latest sayedimran/raabta-frontend:latest
                '''
            }
        }
        stage('Pulling the backend and frontend Docker Image'){
            steps{
                sh'''
                    docker pull sayedimran/raabta-backend:latest
                    docker pull sayedimran/raabta-frontend:latest
                '''
            }
        }
        stage('Updating the backend and frontend containers'){
            steps{
                sh'''
                    docker run -dit -p 4411:4411 -e MONGO_URI='mongodb://udnbgfjsjvaqwo:1ed34db1de639f06b5395b79f1c03512853730833bb875b318853f9f2a970f2d@ec2-34-247-172-149.eu-west-1.compute.amazonaws.com:5432/d332rc4fce6ojq' -e PORT=27017 --name backend sayedimran/raabta-backend:latest
                    docker run -dit -p 80:3000 -e BACKEND_URI='http://raabta.crazeops.tech:8000/' --name frontend sayedimran/raabta-frontend:latest
                '''
            }
        }
        stage('Stop AWS EC2 Instances') {
            steps {
                withCredentials([aws(accessKeyVariable:'AWS_ACCESS_KEY_ID',credentialsId:'aws-ec2-creds',secretKeyVaraiable:'AWS_SECRET_ACCESS_KEY')]) {
                  sh '''
	                aws ec2 stop-instances --instance-ids 	i-04f26a216c4476e82
	                '''
                }
            }
        }
    }
}