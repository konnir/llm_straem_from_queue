<p align="left">
<!--   <img src="https://github.com/konnir/x_grammar_spelling/assets/119952960/f415aef0-dd6b-4223-81be-9ce5d677b53a" alt="anyword_logo" width="150" style="margin-left: 50px;"/> -->
  <img src="https://github.com/konnir/x_grammar_spelling/assets/119952960/aaae3161-5d93-4e82-87bf-1ac468f1817a" alt="Nir_Kon_Logo_inverted (1)" width="100"/>
</p>

# Stream Vs Queue in LLM Stream Response
- The purpose of this repository is to compare the time difference between direct stream LLM responses and reading them from Queues. 
- In this Demo any token is published to the queue for demonstaration. In real use it's wise to decide on full sentence or line break for queue write and read.

Demo UI: [http://parallel.nir-kon.com](https://loading-proxy-iu5vx2gsqa-uc.a.run.app/get?url=https://parallel-llm-queue-iu5vx2gsqa-uc.a.run.app)
- `*. (Please allow about 1 minute for the machine to wake up)`
- `**. (it's a stream delicate demo, if not working for the first time give it a few tries and it will work)`

![image](https://github.com/konnir/llm_straem_from_queue/assets/119952960/c68a35f3-3941-40f6-8b48-9342c009f5cc)

How to use?
- clone code
- create a GCP Pub/Sub queue and subscription
- add file "message_queue_config.yaml" with: project, llm_stram, subscription
- open-ai - add ".env" file with your "OPENAI_API_KEY=" to "./llm/open_ai"
- Start llm_stream_server.py
- "index.html" - change to your IP or GCP server (pay attention it is set up to the demo service as stream soruce !!!)
- Inside: llm_queue_server.py
- Start llm_queue_server.py

Licence: 
- All work done by the author is free to use without any warranty.
- Any third parties code, models and others belong to their authors and legal entities, it's user responsibility to check and get any needed approval.
- The purpose of this code and demo is for reaserch only. 
