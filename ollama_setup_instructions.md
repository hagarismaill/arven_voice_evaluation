**# Setup Instructions (ARVEN Environment)**

***1. Install Ollama: ***

Download and install Ollama for Windows. Verify with** `ollama --version`.**

***2. Download the Model:***

**Run ollama pull llama3.1:8b**

     Verify it exists with ollama list

***3. Install Python Libraries:***

**Run pip install requests psutil**

*4. Verify API:*

**Run python api_hello.py **

to confirm the local API (127.0.0.1:11434) is responding.

*5. Run the Benchmark:*

Ensure the internet is disabled by :. 

**ipconfig**

then 

**run python ollama_benchmark.py.**