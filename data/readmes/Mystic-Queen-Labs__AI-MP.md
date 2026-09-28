# AI Member of Parliament
[YouTube](https://youtu.be/yOWYG1xiyyA)

An event-driven agentic system that reimagines the role of a Member of Parliament in assisting residents during Meet-the-People sessions. 
- Drafts appeal letters to relevant organisations
- Summarises residents' concerns to Parliament
- Reacts to events such as policy updates, news, parliamentary announcements
- (Beta) Escalates issues to [supervisor agents](https://github.com/Mystic-Queen-Labs/AI-MP/blob/main/backend/agent.py#L521)
- (Beta) [Unsafe execution](https://github.com/Mystic-Queen-Labs/AI-MP/blob/main/backend/agent.py#L360) allows the agent to generate arbitrary code to accomplish the task

### Set up
Create the [`aimp`](https://github.com/Mystic-Queen-Labs/AI-MP/blob/main/database/create_database.sql) database and then two TiDB tables [`mpt`](https://github.com/Mystic-Queen-Labs/AI-MP/blob/main/database/create_mpt.sql) and [`events`](https://github.com/Mystic-Queen-Labs/AI-MP/blob/main/database/create_events_table.sql).
Fill in `.env` with the relevant environmental variables.

```shell
brew install redis

git clone https://github.com/Mystic-Queen-Labs/AI-MP.git
cd AI-MP
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

### Running

##### Backend

```shell
brew services start redis
redis-cli ping # should return PONG

cd backend
python3 smtp_server.py   # start the SMTP server at port 8025
python3 -m uvicorn api:app --reload --port 8000   # start FastAPI at port 8000
python3 -m celery -A tasks:celery_app worker --loglevel=info # celery for asynchronous queue
```

##### Frontend

```shell
# if want to serve frontend on a http server
cd frontend
python3 -m http.server 8090
```


### Tear down
```shell
brew services stop redis
```

### Testing
```shell
curl -X POST http://127.0.0.1:8000/receive_email \
  -H "Content-Type: application/json" \
  -d '{
    "mailfrom": "xxx@xxx.gov.sg",
    "rcpttos": "daniel_wong@parl.gov.sg",
    "data": "Subject:Re:Task ID 7796dc95-3a61-4b8c-9032-644ab7f5a765 – Urgent Appeal for Financial Assistance with SP Utility Bills for Mr XXX (SYYYYYYYZ); Content:Request approved. Will reach out soon."
}'
```
