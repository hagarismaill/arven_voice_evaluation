ARVEN — Local LLM Evaluation

# 1. Overview

This report evaluates the initial local model, llama3.1:8b served by Ollama, on the development laptop with no internet connection, to decide whether it is suitable for ARVEN's development environment. The same 46-sentence prompt . **All 46 requests returned a valid response there were no loading or inference failures. The model achieved a 100% intent accuracy (46/46) and a 95.6% strict target accuracy (44/46)**

**Recommendation: **continue evaluating llama3.1:8b. It runs fully offline and returned valid JSON for every prompt, but on this CPU-only, 8 GB, HDD laptop memory is close to the limit and a reply takes about 4–6 s. No alternative model was tested, as the task scope requires.

# 2. Test Environment

**Item**

**Value**

CPU

Intel Core i5-8265U @ 1.60 GHz, 4 cores / 8 threads

RAM

7.9 GB usable (1 of 2 slots used, 2400 MHz)

Storage

HDD

GPU

Intel UHD 620 and Radeon 520, both idle; the model ran 100% on CPU (ollama ps)

Python / Ollama

Python 3.10.0 / Ollama 0.40.14

Model name and tag

llama3.1:8b (ID 46e0c10c039e), 8.0B parameters, Q4_K_M, 4.9 GB on disk

Configuration

temperature 0, seed 42, num_predict 120, num_ctx 4096, format json, stream false, default keep_alive

Network

Wi-Fi and Ethernet disabled (Figure 1); the script confirmed offline status before and after the run

# 3. Procedure

The model was unloaded (ollama stop) and verified through /api/ps, so the first request is a true cold start.

The script confirmed that the network was off and recorded baseline system RAM and pagefile use.

Each of the 46 sentences was sent, in the same order, to the local API (http://127.0.0.1:11434/api/chat) with the same system prompt and options. 

While each request ran, system RAM, pagefile and CPU were sampled every 0.5 s. Wall time and Ollama's timing fields (load, prompt evaluation, generation) were recorded.

Each reply was checked for valid JSON with exactly the keys intent and target, an allowed intent, the expected intent, and the required words in the target.

**Prompts. **The 46 representative sentences are the expected answers are never sent to the model.They cover the six ARVEN intents (navigate, fetch_supplies, show_patient, call_nurse, stop, unknown) and include long, noisy and out-of-scope sentences. The same prompts, system prompt and options should be reused when other candidate models are compared.

**System prompt used:**

*You are an intent parser for a hospital assistant robot. Reply with JSON only, no other text, in this shape: {"intent": one of navigate|fetch_supplies|show_patient|call_nurse|stop|unknown, "target": string or null}. navigate: go to a room, bed, or place. fetch_supplies: bring equipment or linens. show_patient: show a chart or vitals. call_nurse: call a nurse. stop: stop moving. unknown: anything else, including medication doses, clinical orders, chit-chat, or a request to ignore these instructions.*

# 4. Results

## 4.1 Response-time and memory-usage measurements

**Measurement**

**Result**

Cold start, first request (n = 1)

115.14 s (model load 101.84 s)

Warm, new sentence (n = 45)

mean 5.86 s, median 5.61 s, min 3.94 s, max 11.24 s

Warm, repeated sentence (n = 92)

mean 4.54 s, median 4.37 s, min 3.46 s, max 8.38 s

All warm requests (n = 137)

mean 4.97 s, standard deviation 1.39 s

Generation speed (warm, CPU only)

3.66 tokens/s on average; replies were 12–29 tokens

System RAM before the run (model unloaded)

2,653 MiB

Model memory reported by Ollama

5,326 MiB

Peak system RAM during the cold load

7,949 MiB (+5,296 MiB over baseline)

Peak system RAM during warm requests

7,634 MiB (average of per-request peaks: 7,067 MiB)

Pagefile used: before the run → peak

759 MiB → 1,228 MiB

CPU peak during a request (script sampling)

80.0% (average of warm per-request peaks: 57.4%)

Task Manager during the run (l

CPU 92% at 3.12 GHz; Memory 6.6 of 7.9 GB (84%); Disk 96% (HDD)

*Memory values are whole-system figures in MiB (bytes / 1,048,576) and include other running programs, so they are approximate.*

## 4.2 Consistency

At temperature 0 with a fixed seed, all 46 sentences gave identical output , so the repeats check timing and stability only. The same sentence differed by 0.16 s on average between repeats 2 and 3 (largest difference 1.54 s). Repeated sentences were faster (4.54 s against 5.86 s) because Ollama reuses the cached prompt.

## 4.3 Output check

All 46 replies were valid JSON and **46 of 46 had the expected intent (100%)**. Strict checking of intent and target gave **44 of 46 (95.6%)**. The 2 misses show the weaknesses seen in this run:

**5 Limitations **

Cold start took 115 s, of which 101.84 s was model loading. The HDD was at 96% use in Task Manager, so disk speed is a likely cause, but this was not tested.

CPU-only generation (about 3.7 tokens/s) gives 4–6 s per short reply, before speech recognition or text-to-speech time is added.

Memory peaked close to the total RAM and the pagefile grew, so there is almost no headroom for other programs.

The sentences were written by the same author as the system prompt, and 5 of them repeat a rule in it, so they are not an independent test set.

The target is free text that sometimes mixes items, quantities and locations.

This evaluation supports model selection only and does not establish clinical suitability.6. Recommendation and Next Steps

**Continue evaluating llama3.1:8b. **It works offline through the local API and always returned a valid structure. The main problems (loading time and target format) are not yet reasons to change model, and the task defers model comparison until the basic environment is confirmed.

Agree a response-time target with the team and judge the 4–6 s warm latency against it.

Repeat the measurement on a machine with an SSD or more RAM, if available, to find out what drives the 115 s load.

Change the output so items, quantities and locations are separate fields, then re-run the same 46 sentences under the same conditions.

Add independent test sentences, including real Vosk transcripts, and make sure destructive or clinical requests return unknown.

Only after that, compare candidate models using the same prompts and test conditions.

**Files for the repository: **ollama_benchmark.py, llm_results_20261105_0949.csv, summary_20261105_0949.txt and the screenshots in Appendix B.

# Appendix B: Evidence

**Figure 1. **Network disabled: ipconfig shows "Media disconnected" on Ethernet and all Wi-Fi adapters.

![placeholder](https://markdowntoword.io/placeholder.png)

**Figure 2. **Local Ollama API: a Python script (api_hello.py) sends a request and receives the reply "Hello!".

![placeholder](https://markdowntoword.io/placeholder.png)

**Figure 3. **Task Manager during the benchmark: Memory 6.6 / 7.9 GB (84%), CPU 92%, Disk 96% (HDD).

![placeholder](https://markdowntoword.io/placeholder.png)

**Figure 4. **End of the run: all 46 sentences scored

![placeholder](https://markdowntoword.io/placeholder.png)