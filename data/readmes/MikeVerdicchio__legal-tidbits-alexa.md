Legal Tidbits
=============

Introduction
------------
This repository contains the source code for an AWS Lambda Function for an Alexa Skill that gives a random fact about the U.S. legal system from a list of facts. All facts come from my notes from the Commercial Law undergraduate course at the University of Virginia.

It uses the alexa-skill-kit-sdk-factskill nodejs6.10 blueprint on Lambda, but it can be built using the commands below.



Setting up Alexa Skill
----------------------
To create the Alexa skill, you'll need the [interaction model](interaction_model.json), which contains the intents required. Feel free to edit the utterances as you'd like.

Keep note of your Application ID!



Building Deployment Package for AWS Lambda
------------------------------------------
* nodejs (6.10)
* npm
* zip

```
make
```

The above command will package up the source code and all the dependencies into a zip file that you can upload to Lambda.

You will also have to set an environment variable in your Lambda function:
* APPLICATION_ID = your skill ID (from above)



License
-------
The material in this repository is released under a GNU General Public License v2.0.

Copyright (c) 2018.