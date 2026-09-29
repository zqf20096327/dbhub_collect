# Mem0 + TiDB Demo

### 1. Install dependencies

Because PR has not been merged yet, you need to clone PR locally.

```bash
cd ..
git clone https://github.com/Mini256/mem0.git
git checkout support-tidb-vector
poetry insatll
```

Go back test-mem0

```bash
cd ../test-mem0
poetry insatll
```

### 2. Prepare a TiDB cluster

#### 2.1 (Option1) TiDB on local

```bash
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
tiup playground v8.5.0 --tag local-test
```

#### 2.1 (Option1) TiDB Cloud Serverless

1. Go to [TiDB Cloud](https://tidbcloud.com/console/clusters)
2. Create a serverless cluster in a few seconds

### 3. Setup environment variable

Fill in the connection information of TiDB cluster and the OpenAI API Key into **.env** file:

```bash
cp .env.example .env
vi .env
```

### 4. Run the script

```bash
python main.py
```

Test:

Provide some information with the AI:

```bash
(.venv) ~/Projects/test-mem0
python main.py
Chat with AI (type 'exit' to quit)
You: hello, my name is Mini256
AI: Hello, Mini256! How can I assist you today?
You: today is 2025-01-01, and my birthday is 2000-01-01
AI: Happy birthday, Mini256! Today, you turn 25 years old. I hope you have a wonderful celebration!
You: exit
Goodbye!
```

Open another session:

```bash
(.venv) ~/Projects/test-mem0
python main.py
Chat with AI (type 'exit' to quit)
You: Am I an adult?
AI: Yes, since your birthday is January 1, 2000, you turned 25 years old on January 1, 2025. You are considered an adult.
You: Do you remember my name?
AI: Yes, your name is Mini256.
You: exit
Goodbye!
```