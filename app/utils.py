import pickle
import yaml
import subprocess




def unsafe_deserialize(data_bytes):
# insecure: using pickle.loads on untrusted data
return pickle.loads(data_bytes)




def unsafe_yaml_load(stream):
# insecure: using yaml.load (not safe_load)
return yaml.load(stream)




def run_shell_command(cmd):
# insecure: passing user input directly to shell
return subprocess.check_output(cmd, shell=True)