@Library('xcnt-jenkins-scripts') _

def project = 'xcnt-infrastructure'
def appName = 'cname-record-setter'
def label = "${appName}_${env.BRANCH_NAME}"

dockerBuildRuntime(label: label) {
    def myRepo = checkout scm
    def image = "eu.gcr.io/${project}/${appName}"
    def imageWithTag = ""

    stage('Build image') {
        loginToDocker()
        container('docker') {
            imageWithTag = buildImage(image, env.BRANCH_NAME, myRepo.GIT_COMMIT)
        }
    }

    stage('Run PEP8') {
        container('docker') {
            try {
                sh """
                docker run -i ${imageWithTag} python -m pycodestyle --config pycodestyle . > pep8_report.txt
                """
            } finally {
                recordIssues enabledForFailure: true, tool: pep8(pattern: '**/pep8_report.txt'), qualityGates: [[threshold: 1, type: 'TOTAL', unstable: true]]
            }
        }
    }

    stage('Publish') {
      publishImage(image, env.BRANCH_NAME, myRepo.GIT_COMMIT)
      publishImageToPublicDocker(image, env.BRANCH_NAME, myRepo.GIT_COMMIT)
    }
}
