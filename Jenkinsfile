pipeline {
  agent any
  stages {
    stage('Develop') {
      steps {
        sh 'open -a code'
      }
    }

    stage('Test') {
      parallel {
        stage('Test') {
          steps {
            echo 'test '
          }
        }

        stage('code') {
          steps {
            echo 'this is a test'
          }
        }

      }
    }

    stage('Release') {
      steps {
        echo 'test3'
      }
    }

  }
}