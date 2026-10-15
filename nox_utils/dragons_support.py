"""Settings for creating an environment with DRAGONS installed."""

dragons_conda_channels = [
    "http://astroconda.gemini.edu/public",
    "conda-forge",
]  # fmt: skip

dragons_venv_params = [
    v for channel in dragons_conda_channels for v in ("-c", channel)
]
dragons_venv_params += ["--override-channels"]

dragons_github_url = "https://github.com/GeminiDRSoftware/DRAGONS.git"
