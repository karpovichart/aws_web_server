import subprocess
import argparse
import sys
import os
import time
from random import choice
from string import ascii_letters

random_pass = ''.join(choice(ascii_letters) for i in range(12))
stack_name = "myteststack"
parser = argparse.ArgumentParser(
    description="This script create stack")
parser.add_argument('-a', '--ami', nargs='?', default='ami-04932daa2567651e7', help="AMI ID")
cred = parser.parse_args(sys.argv[1:])
out = ""
ami = 'ami-04932daa2567651e7'
try:
    out = subprocess.check_output('aws ec2 describe-images --image-ids ' + cred.ami, shell=True).decode("utf-8")
except subprocess.CalledProcessError as e:
    print(out)

    if out.find("Linux/UNIX") > 0:
        ami = cred.ami
        print('use user ami')
    else:
        print('use default ami')
query = "aws cloudformation create-stack --stack-name " + stack_name + " --template-body file:///" + os.getcwd() + "/CloudFormation.yaml  --capabilities CAPABILITY_NAMED_IAM --parameters --parameters ParameterKey=AMI,ParameterValue=" + ami + " ParameterKey=DBPswd,ParameterValue=" + random_pass
out = subprocess.check_output(query, shell=True).decode("utf-8")
print(out)
old = ""
print("start")
# while old.find("CREATE_COMPLETE\tAWS::CloudFormation::Stack") == -1:
#     time.sleep(10)
#     query = "aws cloudformation describe-stack-events  --stack-name " + stack_name + " --max-items 1"
#     out = subprocess.check_output(query, shell=True).decode("utf-8")
#     if old.find(out) == -1:
#         old = out
#         print(old)
