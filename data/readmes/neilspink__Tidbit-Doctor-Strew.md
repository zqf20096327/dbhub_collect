# Twitter Discord Bot

Mention @Tidbit in your Discord chat and the bot will take what you wrote and search Twitter. It uses the 10 longest
words you wrote in the message. 

![example showing input text and resulting text from bot](example.png)

## Docker
 
docker build -t neilspink/tidbit . 
docker run -d neilspink/tidbit

