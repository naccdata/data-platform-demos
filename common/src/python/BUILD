python_sources(name="lib")

python_distribution(
    name="dist",
    dependencies=[":lib"],
    wheel=True,
    sdist=True,
    provides=python_artifact(
        name="nacc-common",
        version="1.0.0",
        description="NACC Data Platform utilities",
        author="NACC",
        author_email="nacchelp@uw.edu",
        url="https://github.com/naccdata/data-platform-demos"),
)
