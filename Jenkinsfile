pipeline {
  agent any
  options {
    disableConcurrentBuilds()
    }
    environment {
        IMAGE_REPO = 'yasan30/week12'
        PYTHON_EXE = 'C:\Users\ch_sa\AppData\Local\Programs\Python\Python313\python.exe'
    }
    stages {
        stage('Checkout Code') {
            steps {
                checkout scm
                bat 'git status --short'
            }
        }
        stage('Run Selenium Tests') {
            steps {
                bat '"%PYTHON_EXE%" --version'
                bat '"%PYTHON_EXE%" -m pip install -r requirements.txt'
                bat '"%PYTHON_EXE%" -m pip install pytest selenium'

                bat '''
                    powershell -NoProfile -ExecutionPolicy Bypass -Command "$p = Start-Process -FilePath $env:PYTHON_EXE -ArgumentList 'app.py' -PassThru -WindowStyle Hidden; $p.Id | Out-File -Encoding ascii flask.pid"
                '''
                bat '''
                    powershell -NoProfile -Command "Start-Sleep -Seconds 5"
                '''

                bat '"%PYTHON_EXE%" -m pytest -v'
            }
            post {
                always {
                    bat '''
                        powershell -NoProfile -Command "if (Test-Path flask.pid) { $procId = [int](Get-Content flask.pid); Stop-Process -Id $procId -Force -ErrorAction SilentlyContinue; Remove-Item flask.pid -Force }"
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t week12:v1 .'
                bat 'docker tag week12:v1 %IMAGE_REPO%:v1'
            }
        }

        stage('Push Docker Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-creds',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    bat 'echo %DOCKERHUB_TOKEN% | docker login -u %DOCKERHUB_USER% --password-stdin'
                    bat 'docker push %IMAGE_REPO%:v1'
                    bat 'docker logout'
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                bat 'kubectl apply -f deployment.yaml'
                bat 'kubectl apply -f service.yaml'
                bat 'kubectl set image deployment/week12-deployment week12=%IMAGE_REPO%:v1'
                bat 'kubectl rollout status deployment/week12-deployment --timeout=120s'
                bat 'kubectl get pods'
                bat 'kubectl get services'
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check Console Output.'
        }
    }
}
