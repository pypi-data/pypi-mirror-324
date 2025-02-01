from pathlib import Path


def config_file_path():
    return Path.home() / ".reasoner"


def read_config_file():
    reasoner_dir = config_file_path()
    reasoner_dir.mkdir(exist_ok=True)
    config_file = reasoner_dir / "config"

    config_data = {}
    if config_file.exists():
        with open(config_file) as f:
            for line in f:
                if "=" in line:
                    key, value = line.strip().split("=", 1)
                    config_data[key] = value

    return config_data


def write_config_file(config_data):
    reasoner_dir = config_file_path()
    reasoner_dir.mkdir(exist_ok=True)
    config_file = reasoner_dir / "config"

    with open(config_file, "w") as f:
        for key, value in config_data.items():
            f.write(f"{key}={value}\n")


def clear_config_file():
    config_file = config_file_path() / "config"
    if config_file.exists():
        config_file.unlink()
