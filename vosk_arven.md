ARVEN — Offline Speech Recognition Test (Vosk)

This report documents a test of offline English speech recognition with Vosk on the development laptop, with no internet connection. The model converted 20 hospital-related sentences, spoken into the laptop microphone, into text. The task asks for 2 to 5 sentences; 20 were used to cover both short and long sentences. All 20 returned a transcript. Six were exactly right, and the whole set had 29 word errors in 223 words (13.0%).

**Conclusion: **Vosk works fully offline and turns speech into text, which meets the completion criterion for this stage. The small model still misses some hospital terms (for example “nurse station” and “IV bag”), so 13.0% is a first measurement from one speaker, not a final accuracy figure. No other model was compared, as the task requires.

# 1. Test Environment

**Item**

**Value**

Machine 

Intel Core i5-8265U, 8 GB RAM, HDD

Speech model

vosk-model-small-en-us-0.15 (English, small)

Software

Python packages vosk and sounddevice; Vosk version

Audio input

Laptop built-in microphone, 16 kHz, mono, 16-bit; one speaker, one recording session

Stop rule

Recording stops after about 2 s of silence once speech has been heard, or at 25 s. Short pauses inside a sentence do not stop it

Network

Wi-Fi and Ethernet off. The script exits if it can reach 8.8.8.8 (port 53); the run printed the OFFLINE line 

Test script

vosk_test.py (saves one wav per sentence and a results JSON)

# 2.Procedure

install the packages (pip install vosk sounddevice), download vosk-model-small-en-us-0.15, and record the Vosk version 

Turn off Wi-Fi then run python vosk_test.py --model vosk-model-small-en-us-0.15. The script stops if it can open a connection to 8.8.8.8, so it cannot run online. This run printed offline check (before): OFFLINE (good) 

For each of the 20 sentences the script shows the text, waits for Enter, then records from the microphone until about 2 s of silence (maximum 25 s).

Each recording is saved as a wav file, and the text Vosk returned is printed and stored in the results JSON.

The text is compared with the sentence after lower-casing and removing punctuation. Each wrong, missing or extra word counts as one error (word-level edit distance). A few spellings are treated as equal (wheelchair, bedpan, IV, nurse station, operating theatre). Error rate = word errors ÷ reference words.

**Sentences.**

** **The 20 sentences were written for ARVEN’s hospital scenarios: greetings, calling staff, equipment and supplies, room and bed numbers, and departments. Sentences 1–12 have 5–11 words; sentences 13–20 have 14–18 words. The same sentences and procedure should be reused when other models are compared.

# 3 Results

## 3.1 Summary

**Measurement**

**Result**

Sentences tested

20 (12 short, 5–11 words; 8 long, 14–18 words)

Word errors, all sentences

29 of 223 reference words (13.0%)

Word errors, short sentences (1–12)

14 of 95 words (14.7%)

Word errors, long sentences (13–20)

15 of 128 words (11.7%)

Recording length per sentence

6.81 s to 23.48 s (includes the 2 s silence wai)

Script Errors

none. All 20 sentences returned text. Recognition errors are listed below

## 3.2 Error patterns

**Hospital terms. **“Call the nurse station” became “coughlin or station” (3 errors). “Bring a new IV bag” became “are you new ip back” (4 errors). “Linens” became “winans”, and “operating theatre” became “operation theater”.

**Numbers were mostly correct. **Fourteen, twelve, twenty, fifteen, “four hundred and twelve” and “three hundred and five” were all recognised. The only number error was “two” heard as “to” in sentence 14.

**Small words. **“The” or “this” was heard as “a” in 7 sentences, and “needs” as “need” in 2. In sentence 11, “in room” became “around”, so the word “room” was lost although the number was right.

**First word. **The first word was wrong in 7 of 20 sentences (3, 6, 7, 10, 13, 17, 19). The recording may start just as the speaker begins; this was not tested.

**Length. **Long sentences were not worse per word (11.7%) than short ones (14.7%). The errors depend on the particular words, not on sentence length.

**Effect on ARVEN. **Errors such as “nurse station” or “IV bag” could change the intent that is later parsed from the text. This was not tested here.

# 4. Limitations

One small model, one speaker, one session, one take per sentence. The 13.0% figure describes this run only and is not a benchmark or a model comparison.

The small model misses some hospital words. A larger English model was not tested, as the task defers model comparison.

“Theater” against “theatre” is a US/UK spelling difference that the script counted as an error. Without it the count is 28 of 223 (12.6%).

The output is lower case with no punctuation, so any later intent parser must accept that format.

Sentences were read aloud from the screen into the laptop microphone. Real nurse speech, background noise and other accents were not tested. 

This test does not establish clinical suitability.

# Conclusion and Next Steps

**Completion criterion**

**Status**

Vosk and an English model installed

Done (vosk-model-small-en-us-0.15)

Sentences tested by microphone (2 to 5 required)

Done, 20 sentences

Works with no internet

Done. The script refuses to run online

Speech converted to text

Done

Script and experiment documented

Done (vosk_test.py, results JSON, this report)

Vosk runs offline and converts a spoken sample to text, so the Vosk part of the week’s task is complete. Vosk can be used as the speech-recognition component for the next stage, with the accuracy limits above.

***Next steps***

Send the 20 Vosk transcripts to the Ollama intent parser and check whether the recognition errors change the intent (this is also next step 4 of the Ollama report).

Repeat the test with more speakers and some background noise before relying on the accuracy figure.

Only after the basic environment is confirmed, compare a larger English Vosk model using the same 20 sentences and procedure.

# Appendix : Evidence

**Figure 1. **Vosk installed: output of pip show vosk, showing the version.

*![placeholder](https://markdowntoword.io/placeholder.png)*

*Terminal screenshot after running  pip show vosk  (the Name: vosk and Version: lines must be visible).*

**Figure  **End of the run: total word errors and the saved results file.

![placeholder](https://markdowntoword.io/placeholder.png)