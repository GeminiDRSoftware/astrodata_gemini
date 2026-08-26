dragons_conda_channels = [
    "conda-forge",
    "http://astroconda.gemini.edu/public",
]  # fmt: skip

dragons_venv_params = [
    v for channel in dragons_conda_channels for v in ("-c", channel)
]
dragons_venv_params += ["--override-channels"]

dragons_github_url = "https://github.com/GeminiDRSoftware/DRAGONS.git"