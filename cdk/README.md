
# AWSome IaC with CDK

The backend for the contact form is hosted on AWS. The infra as code (IaC) is a CDK Python project.

## Get started

This project is set up like a standard Python project. To create the virtualenv a `python3` executable
in your path with access to the `venv` package is required.

To create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

At this piont you can see the what CDK will do during a deployment.

```
$ cdk diff
```

Deploy if everything looks good.

```
$ cdk deploy
```
