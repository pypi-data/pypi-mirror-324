import subprocess

def pre_build():
    print("Running `make babel` before building...")
    subprocess.run(["make", "babel"], check=True)

if __name__ == "__main__":
    pre_build()
