import asyncio
import logging
import os

import pytest
from dotenv import load_dotenv

from linkedin_influencer_mcp import send_linkedin_connection_requests
from linkedin_influencer_mcp.models import ConnectionRequest

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")
TEST_SEARCH_QUERY = "AI Engineer"
TEST_MAX_CONNECTIONS = 2
TEST_CUSTOM_NOTE = False
TEST_USER_PROFILE_ID = os.getenv("USER_LINKEDIN_PROFILE_ID")
TEST_LOCATION = "Toronto, ON"


@pytest.mark.asyncio
async def test_send_linkedin_connection_requests():
    """Test sending LinkedIn connection requests with real browser."""
    logger.info("Starting LinkedIn connection requests test")
    try:
        results = await send_linkedin_connection_requests(
            connection=ConnectionRequest(
                search_query=TEST_SEARCH_QUERY,
                max_connections=TEST_MAX_CONNECTIONS,
                custom_note=TEST_CUSTOM_NOTE,
                user_profile_id=TEST_USER_PROFILE_ID,
                location=TEST_LOCATION,
            )
        )

        logger.info(f"Received results: {results}")

        # Verify the results structure based on the return type
        assert isinstance(
            results, (tuple, list)
        ), "Results should be either a tuple or list"

        if isinstance(results, tuple):
            connection_results, stats = results
            assert isinstance(
                connection_results, list
            ), "First element should be a list"
            assert isinstance(stats, dict), "Second element should be a dict"
            assert (
                len(connection_results) <= TEST_MAX_CONNECTIONS
            ), "Should not exceed max connections"
        else:
            assert isinstance(results, list), "Results should be a list of strings"
            assert (
                len(results) <= TEST_MAX_CONNECTIONS
            ), "Should not exceed max connections"

    except Exception as e:
        logger.error(f"Test failed with exception: {str(e)}", exc_info=True)
        pytest.fail(f"Test failed with exception: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_send_linkedin_connection_requests())
