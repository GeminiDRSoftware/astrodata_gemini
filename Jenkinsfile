// Not ready.  Just an example for later.

pipeline {
    agent any

    environment {
        ADGEMINI_STORE_TESTDATA = '/rtfperm/jenkins/astrodata_gemini/'
    }

    stages {
        stage('Test') {
            steps {
                sh 'nox'
            }
        }
    }
}