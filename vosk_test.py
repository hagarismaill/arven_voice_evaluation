import argparse, json, queue, re, socket, time, wave, os
from datetime import datetime
from pathlib import Path
from vosk import KaldiRecognizer, Model, SetLogLevel

SetLogLevel(-1)

SENTENCES = [
    "Hello, how are you today?",
    "Please check the patient's blood pressure.",
    "Call the nurse station immediately.",
    "The patient needs medication now.",
    "Where is the nearest defibrillator?",
    "Call the doctor to the emergency room.",
    "Bring a new IV bag to bed number nine.",
    "Bring a wheelchair and an oxygen mask to room fourteen.",
    "Take me to the radiology department on the third floor.",
    "The patient in bed twelve needs fresh linens and a basin.",
    "Take me to the patient in room four hundred and twelve.",
    "Please take the patient's temperature and write it on the chart.",
    "The doctor asked me to bring the blood test results to the intensive care unit.",
    "I need three pillows, two blankets, and one bedpan for the patient in bed twelve in ward B.",
    "Tell the surgeon that the patient in room twenty is ready for the operating theatre.",
    "Please bring clean towels and a pair of gloves to the pharmacy on the second floor.",
    "The patient in bed seven is feeling dizzy and needs a nurse right away.",
    "Take this sample to the laboratory and ask them to call me when the results are ready.",
    "Move the patient from the emergency room to room three hundred and five on the third floor.",
    "Please remind the doctor that the patient in bed fifteen needs a new prescription before tonight.",
]

# Spelling variants that Vosk splits/merges differently (applied to expected AND heard)
NORMALIZE = [
    (r"\bbed pan\b", "bedpan"), (r"\bwheel chair\b", "wheelchair"),
    (r"\bi v\b", "iv"), (r"\bnurses station\b", "nurse station"),
    (r"\boperating theater\b", "operating theatre"),
]


def internet_available(timeout=2.0):
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=timeout).close()
        return True
    except OSError:
        return False


def words(text):
    t = re.sub(r"[^a-z0-9' ]+", " ", text.lower())
    t = " ".join(t.split())
    for pat, rep in NORMALIZE:
        t = re.sub(pat, rep, t)
    return t.split()


def word_errors(expected, heard):
    ref, hyp = words(expected), words(heard)
    n, m = len(ref), len(hyp)
    dp = list(range(m + 1))
    for i in range(1, n + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, m + 1):
            cur = dp[j]
            dp[j] = prev if ref[i - 1] == hyp[j - 1] else 1 + min(prev, dp[j], dp[j - 1])
            prev = cur
    return dp[m], n


def record_until_silence(model, max_seconds=25, silence_seconds=2.0, rate=16000):
    """Records until the speaker stays silent for `silence_seconds` after speaking."""
    import sounddevice as sd
    q = queue.Queue()

    def cb(indata, frames, t, status):
        q.put(bytes(indata))

    rec = KaldiRecognizer(model, rate)
    raw_bytes, segments = bytearray(), []
    last_partial, last_change, spoke = "", time.perf_counter(), False

    print("🎤 Listening... (speak now; stops after a 2-second pause)")
    start = time.perf_counter()
    with sd.RawInputStream(samplerate=rate, blocksize=4000, dtype="int16",
                           channels=1, callback=cb):
        while time.perf_counter() - start < max_seconds:
            data = q.get()
            raw_bytes.extend(data)
            if rec.AcceptWaveform(data):
                # Short pause inside the sentence: keep the text, KEEP listening
                seg = json.loads(rec.Result()).get("text", "")
                if seg:
                    segments.append(seg)
                    spoke, last_change = True, time.perf_counter()
                last_partial = ""
            else:
                part = json.loads(rec.PartialResult()).get("partial", "")
                if part != last_partial:
                    last_partial, last_change = part, time.perf_counter()
                    if part:
                        spoke = True
            if spoke and time.perf_counter() - last_change > silence_seconds:
                break

    tail = json.loads(rec.FinalResult()).get("text", "")
    if tail:
        segments.append(tail)
    return " ".join(segments).strip(), time.perf_counter() - start, bytes(raw_bytes)


def save_wav(path, raw, rate=16000):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(raw)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True)
    ap.add_argument("--n", type=int, default=len(SENTENCES), help="number of sentences to test")
    args = ap.parse_args()

    if internet_available():
        raise SystemExit("CRITICAL: Network is ON. Turn it off!")
    print("offline check (before): OFFLINE (good)")

    model_path = args.model
    if os.path.isdir(model_path):
        subdirs = [d for d in os.listdir(model_path) if os.path.isdir(os.path.join(model_path, d))]
        if len(subdirs) == 1 and subdirs[0].startswith("vosk-model"):
            model_path = os.path.join(model_path, subdirs[0])
            print(f"Auto-fixed model path to: {model_path}")

    stamp = time.strftime("%Y%m%d_%H%M")
    out_path = Path(f"vosk_results_{stamp}.json")
    wavdir = Path(f"vosk_wavs_{stamp}"); wavdir.mkdir(exist_ok=True)

    model = Model(model_path)
    sentences = SENTENCES[:args.n]
    total = len(sentences)
    results, total_err, total_ref = [], 0, 0

    for n, expected in enumerate(sentences, 1):
        print(f"\n[{n}/{total}] Say exactly: {expected}")
        input("Press Enter, wait a second, then speak...")
        heard, rec_time, raw = record_until_silence(model)
        save_wav(wavdir / f"sent_{n:02d}.wav", raw)

        err, ref_n = word_errors(expected, heard)
        total_err += err; total_ref += ref_n
        results.append({"expected": expected, "text": heard, "word_errors": err,
                        "ref_words": ref_n, "record_seconds": round(rec_time, 2)})
        print(f"-> Vosk heard: '{heard}'")
        print(f"-> Errors: {err}/{ref_n} words")

    wer = round(100 * total_err / total_ref, 1) if total_ref else None
    report = {"date": datetime.now().isoformat(timespec="seconds"), "model": model_path,
              "word_errors": total_err, "ref_words": total_ref, "WER_percent": wer,
              "results": results}
    out_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n=== FINISHED ===")
    print(f"Total word errors: {total_err}/{total_ref}  (WER {wer}%)")
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
