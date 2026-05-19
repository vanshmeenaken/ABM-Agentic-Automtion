import subprocess

claude_path = r'C:\Users\Vansh\AppData\Roaming\npm\claude.cmd'
prompt = 'List 3 K-12 CFO pain points on teacher retention in JSON format.'

result = subprocess.run(
    [claude_path, '-p', prompt, '--model', 'haiku'],
    capture_output=True,
    text=True,
    timeout=30
)

print('Return code:', result.returncode)
print('Stdout length:', len(result.stdout))
print('Stdout:', result.stdout[:300])
print('Stderr:', result.stderr[:200])
