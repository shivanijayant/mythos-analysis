import json, os, requests, urllib3
from e2b import Sandbox
urllib3.disable_warnings()
os.environ["E2B_API_KEY"] = E2B_API_KEY
AK = ANTHROPIC_API_KEY
MODEL = "claude-opus-4-7"
def run_pipeline():
    print("[*] Step 1: Provisioning SDK Sandbox...")
    with Sandbox.create() as sb:
        print(f"[SUCCESS] Active: {sb.sandbox_id}")
        sb.commands.run("mkdir -p ./target")
        sb.commands.run("echo \"#include <stdio.h>\" > ./target/main.c")
        sb.commands.run("echo \"#include <string.h>\" >> ./target/main.c")
        sb.commands.run("echo \"int main(int c, char *v[]) {\" >> ./target/main.c")
        sb.commands.run("echo \"  char buf[32];\" >> ./target/main.c")
        sb.commands.run("echo \"  if (c < 2) return 1;\" >> ./target/main.c")
        sb.commands.run("echo \"  strcpy(buf, v[1]);\" >> ./target/main.c")
        sb.commands.run("echo \"  return 0;\" >> ./target/main.c")
        sb.commands.run("echo \"}\" >> ./target/main.c")
        src = sb.commands.run("cat ./target/main.c").stdout
        print("[*] Step 3: Compiling Target...")
        sb.commands.run("gcc ./target/main.c -o ./target/bin -fno-stack-protector")
        print("[*] Step 4: Running Test Matrix...")
        logs = []
        for sz in [16, 64, 128]:
            print(f"    -> Size: {sz} bytes")
            arg = "A" * sz
            try:
                res = sb.commands.run(f"./target/bin {arg}")
                ec = res.exit_code
                st = "PASS" if ec == 0 else "FAIL"
            except Exception as err:
                ec = getattr(err, "exit_code", -1)
                st = "CRASH"
            logs.append({"size": sz, "status": st, "exit_code": ec})
        print("[*] Step 5: Requesting Synthesis...")
        fmt_tel = json.dumps(logs, indent=2)
        p1 = "You are a reliability engineer. Analyze these logs.\n\n"
        p2 = f"SOURCE CODE:\n{src}\n\nTELEMETRY:\n{fmt_tel}\n\n"
        p3 = "Provide a report identifying boundaries and a clean fix."
        prompt = p1 + p2 + p3
        hdrs = {"x-api-key": AK, "anthropic-version": "2023-06-01", "content-type": "application/json"}
        payload = {"model": MODEL, "max_tokens": 2048, "messages": [{"role": "user", "content": prompt}]}
        ar = requests.post("https://api.anthropic.com/v1/messages", headers=hdrs, json=payload, verify=False, timeout=60)
        md = ar.json()["content"][0]["text"]
        with open("mythos_report.md", "w") as f: f.write(md)
        print("[SUCCESS] Real report generated!")
if __name__ == "__main__":
    run_pipeline()
