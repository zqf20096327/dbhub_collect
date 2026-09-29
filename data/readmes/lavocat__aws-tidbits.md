# aws-tidbits

This is a small collection code snippets that I've written or found useful in building tools for AWS.  These snippets are meant to be used as examples only

**boto_session.py** - Returns a boto3 session using the current IAM credentials of the EC2/ECS instance

**discover_hosts.py** - Returns a list of instances PrivateIPAddresses based on some filter parameters.  