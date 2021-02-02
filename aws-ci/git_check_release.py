import argparse
import os
import subprocess

parser = argparse.ArgumentParser(
    description='Git TF Release Update',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument('--tf_version', default=2.4,
                    help='Tenforflow Version')
args = parser.parse_args()


def main():
    tf_branch = "r{tf_version}_aws".format(tf_version=args.tf_version)
    git_branch = "r{tf_version}".format(tf_version=args.tf_version)
    os.system('git clone codecommit::us-west-2://aws-tensorflow')
    os.chdir('aws-tensorflow/')
    os.system('git checkout {tf_branch}'.format(tf_branch=tf_branch))
    os.system('git checkout -b r{tf_version}_aws_git'.format(tf_version=args.tf_version))
    os.system('git remote add google https://github.com/tensorflow/tensorflow.git')
    print('git', 'pull', '--commit', 'google', git_branch)
    output = subprocess.run(['git', 'pull', '--commit', 'google', git_branch], stdout=subprocess.PIPE).stdout.decode('utf-8')
    print(output)
    os.system('git status')
    if ("Already up to date" in output):
        print('Branch already up to date.')
    else:
        os.system('git push --set-upstream origin r{tf_version}_aws_git'.format(tf_version=args.tf_version))
        os.system('aws codecommit create-pull-request --title "TF{tf_version} git sync" --description "Sync tf {tf_version} with vanilla tf branch" '
                  '--client-request-token request_token --targets repositoryName=aws-tensorflow,sourceReference=r{tf_version}_aws_git,destinationReference={tf_branch}'
                  .format(tf_version=args.tf_version, tf_branch=tf_branch))


if __name__ == '__main__':
    main()
