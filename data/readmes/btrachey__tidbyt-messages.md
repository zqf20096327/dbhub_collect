#  Tidbyt Messages
Code for a container intended to be run in AWS Lambda. Takes input and generates a scrolling message 
for display on a Tidbyt device. API token and device ID are stored as env variables in the Lambda 
function, which is why they are harvested from the environment in the python code. Example execution:
```
curl -XPOST "https://api.brianwtracey.com/message" \
  -d '{"replacements":{"MESSAGE_TEXT":"Hello world how are you today?", "HEX_COLOR":"cc7ba6"}}'
```

