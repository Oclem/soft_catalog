import boto3
import re
from flask import Flask, render_template, request
app = Flask(__name__)
@app.route('/', methods=['GET','POST'])
def your_view():
    ec2 = boto3.client('ec2', region_name='eu-west-3')
    response = ec2.describe_instances(
            Filters = [
                {
                    'Name': 'tag:cluster',
                    'Values': ['student-cloud']
                },
                {   'Name': 'tag:orga',
                    'Values':['konexio']
                }
            ]
            )
    select_list = []
    for reservation in (response["Reservations"]):
        for name in reservation["Instances"]:
          tags = name["Tags"]
          for tag in tags:
              if tag["Key"] == "Name":
                  name = tag["Value"]
                  select_list.append(name)
    if request.method == 'POST':
        stud_list = []
        soft_list = []
        print(request.form.getlist('check'))
        for select in request.form.getlist('check'):
            stud = re.search('cloud', select)
            if stud is not None:
                stud_list.append(select)
            else:
                soft_list.append(select)
        print(stud_list)
        print(soft_list)

        with open('hosts', 'w') as f:
            f.write('[konexio]\n')
            for i in stud_list:
                f.write('%s.lan\n'%i)
        svc_install = """
        - name: Install Soft
          apt:
            name: %s
            state: present
        """
        with open("orga_customize/roles/konexio/student/tasks/main.yml", 'w') as f:
            for soft in soft_list:
                f.write(svc_install % soft)
    #your_list= [1,2,3,4]
    return render_template('view.html', students_list=select_list)

