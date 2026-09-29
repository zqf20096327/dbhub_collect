# From 
https://www.youtube.com/watch?v=CKNfKbIkYvM&t=1021s
# Register and create table on TiDB
TiDB free tier
    https://tidbcloud.com/free-trial/?utm_campaign=9756033-slg_0325_influencercampaign_apac&utm_source=influencer&utm_medium=paid_media&utm_content=melivecode
create table courses
   https://gist.github.com/KarnYong/26e89f2fb8d81942f42777a9e9da5d1f
    select db -> connect -> copy connection string & pw  
    save connection string in .env
# install ollama from web
https://ollama.com
# install llm (run on terminal)
ollama pull mistral
# install embeding (run on terminal)
ollama pull bge-m3

# in Project
# activate virtual env
source .venv/bin/activate  
# install dependencies 
uv pip install -r pyproject.toml
# Run memory.py to add collections to vector db 'langchain_agent_memory'
python3 memoty.py
# Run agent.py to start chat with agent
python3 agent.py
# Run UI
streamlit run streamlit_ui.py

http://localhost:8501/
