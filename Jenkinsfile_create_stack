pipeline {
    agent any
     environment {
       AWS_DEFAULT_REGION = 'eu-central-1'

    }

    parameters {
        string(defaultValue: "ami-04932daa2567651e7", description: 'AMI', name: 'AMI')
    }

    stages {
         stage("clean up workspace"){
                        steps{
                            dir("aws_web_server") {
                                deleteDir()
                            }
                        }
                    }
                    stage("download files from git") {
                        steps{
                         sh("git clone https://github.com/karpovichart/aws_web_server.git")
                        }
                    }
        stage("create_stack") {
            steps {
                dir("aws_web_server") {
                                sh("python3 createStack.py -a ${params.AMI}")
                            }
            }
        }
    }
}