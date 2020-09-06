import subprocess

stack_name = "myteststack"
out = subprocess.check_output('aws s3 rm s3://testbbucket31 --recursive', shell=True).decode("utf-8")
print(out)
out = subprocess.check_output('aws cloudformation delete-stack --stack-name  ' + stack_name, shell=True).decode("utf-8")
print(out)
print('delete start')