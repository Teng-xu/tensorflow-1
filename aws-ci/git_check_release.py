import argparse
import os
import subprocess
from datetime import datetime

parser = argparse.ArgumentParser(
    description='Git TF Release Update',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('--tf_version', default=2.4,
                    help='Tenforflow Version')
args = parser.parse_args()
tf_version = args.tf_version

def main():
    if(tf_version == 'master'):
        tf_branch = "development"
        git_branch = "master"
    else:
        tf_branch = f"r{tf_version}_aws"
        git_branch = f"r{tf_version}"
    os.system('git config --global user.name "AWS TF BOT"')
    os.system('git config --global user.email aws-tensorflow-bot@amazon.com')
    os.system('git clone codecommit::us-west-2://aws-tensorflow')
    os.chdir('aws-tensorflow/')
    os.system(f'git checkout {tf_branch}')
    os.system(f'git checkout -b {tf_branch}_git_sync')
    os.system('git remote add google https://github.com/tensorflow/tensorflow.git')
    print('git', 'pull', '--commit', 'google', git_branch)
    output = subprocess.run(['git', 'pull', '--commit', 'google', git_branch], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(output)
    os.system('git status')
    if ("Already up to date" in output):
        print('Branch already up to date.')
    else:
        dateTime = datetime.now()
        timestampStr = dateTime.strftime("%d%b%Y_%H%M%S")
        os.system(f'git push --set-upstream origin {tf_branch}_git_sync')
        os.system('aws codecommit create-pull-request --title "TF{tf_version} git sync" --description "Sync tf {tf_version} with vanilla tf branch" '
                  '--client-request-token {token} --targets repositoryName=aws-tensorflow,sourceReference={tf_branch}_git_sync,destinationReference={tf_branch}'
                  .format(tf_version=tf_version, token=timestampStr, tf_branch=tf_branch))


if __name__ == '__main__':
    main()
