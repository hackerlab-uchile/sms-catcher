from dotenv import load_dotenv
import subprocess

load_dotenv()

result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE).stdout.decode('utf-8')