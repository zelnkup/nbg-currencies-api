import pytest
from unittest.mock import patch
from nbg_currency_api.constants import BASE_URL
from nbg_currency_api.exceptions import CurrencyAPIException
from tests.mocker import MockResponse


@pytest.mark.asyncio
@patch("nbg_currency_api.api.aiohttp.ClientSession.get")
async def test_afetch_success(mock_client_session, currency_api_async):
    resp = MockResponse({"rate": 3.14}, 200)
    mock_client_session.return_value = resp

    expected_url = f"{BASE_URL}/en/json/?currencies=USD&date=2025-01-12"

    result = await currency_api_async.afetch()

    assert result == {"rate": 3.14}
    mock_client_session.assert_called_once_with(expected_url)


@pytest.mark.asyncio
@patch("nbg_currency_api.api.aiohttp.ClientSession.get")
async def test_afetch_failure(mock_client_session, currency_api_async):
    resp = MockResponse("Internal Server Error", 500)
    mock_client_session.return_value = resp

    with pytest.raises(
        CurrencyAPIException, match="Error fetching data: 500 Internal Server Error"
    ):
        await currency_api_async.afetch()
