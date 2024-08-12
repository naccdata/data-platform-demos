"""Example script for querying pipeline dataviews on NACC Data Platform."""
import logging
import os
import sys

from flywheel import Client

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
log = logging.getLogger('__main__')


def main():
    """Queries the pipeline dataviews available on the NACC Data Platform.

    Uses Flywheel instance determined by the API key value set in
    FW_API_KEY.
    """

    # 1. The Flywheel SDK uses a Client object to interact with Flywheel.
    #    First get the API key from the environment variable FW_API_KEY
    if 'FW_API_KEY' not in os.environ:
        log.error("environment variable FW_API_KEY not found")
        sys.exit(1)

    # 2. Create the Client object using the API key.
    #    The key determines which instance you are using.
    client = Client(os.environ['FW_API_KEY'])
    if not client:
        log.error("not connected to Flywheel")
        sys.exit(1)

    # 3. NACC has published dataviews for center use in the nacc/metadata
    #    project. Get the project to start.
    metadata_project = client.lookup("nacc/metadata")

    # 4. Print the list of available dataviews
    for view in client.get_views(metadata_project.id):
        print(f"label: {view.label} description:\t{view.description}")


if __name__ == "__main__":
    main()