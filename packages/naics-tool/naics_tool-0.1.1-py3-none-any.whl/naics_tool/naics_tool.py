import json
from typing import Any, Dict, List, Optional, Tuple, Union, Type, Literal
import aiohttp
import requests
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.utils import get_from_dict_or_env
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field, model_validator

class NAICSLookupAPIWrapper(BaseModel):
    base_url: str

    @model_validator(mode='before')
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Get base_url for endpoint and validate that it exists."""
        base_url = get_from_dict_or_env(
            values, "naics_lookup_url", "NAICS_LOOKUP_URL", "http://localhost:8085/naics/"
        )
        values["base_url"] = base_url

        return values

    def results(
        self, 
        code: str
    ) -> Dict:
        """ Lookup NAICS code and return metadata. 
        Args:
            code (str): NAICS code to lookup.
        Returns:
            code (str): NAICS code.
            title (str): Title of NAICS code.
            description (str): Description of NAICS code.
            cross_reference (str): Cross-reference of NAICS code.
        """
        response = requests.get(f"{self.base_url}{code}")
        response.raise_for_status()
        return response.json()

    async def results_async(
        self, 
        code: str
    ) -> Dict:
        async def fetch() -> str:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}{code}") as response:
                    if response.status == 200:
                        data = await response.text()
                        return data
                    else:
                        raise Exception(f"Error {response.status}: {response.reason}")
        results_json_str = await fetch()
        return json.loads(results_json_str)


class NAICSSearchAPIWrapper(BaseModel):
    base_url: str

    @model_validator(mode='before')
    @classmethod
    def validate_environment(cls, values: Dict) -> Any:
        """Get base_url for endpoint and validate that it exists."""
        base_url = get_from_dict_or_env(
            values, "naics_search_url", "NAICS_SEARCH_URL", "http://localhost:8085/search"
        )
        values["base_url"] = base_url

        return values

    def results(
        self, 
        query: str,
        top_k: int = 5
    ) -> Dict:
        """ Retrieve a list of NAICS codes, titles, descriptions, and cross-references based on a query
        matching the descriptions of the NAICS codes.
        Args:
            query (str): The query to search for.
            top_k (int): The number of results to return.
        Returns:
            results: A list of dictionaries containing the results:
                code (str): NAICS code.
                title (str): Title of NAICS code.
                description (str): Description of NAICS code.
                cross_reference (str): Cross-reference of NAICS code.
                score (float): The score of the result.
        """
        response = requests.get(f"{self.base_url}?query={query}&top_k={top_k}")
        response.raise_for_status()
        return response.json()

    async def results_async(
        self, 
        query: str,
        top_k: int = 5
    ) -> Dict:
        async def fetch() -> str:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}?query={query}&top_k={top_k}") as response:
                    if response.status == 200:
                        data = await response.text()
                        return data
                    else:
                        raise Exception(f"Error {response.status}: {response.reason}")
        results_json_str = await fetch()
        return json.loads(results_json_str)

class NAICSLookupInput(BaseModel):
    """Input for the NAICS Lookup tool."""
    code: str = Field(description="The six-digit NAICS code to lookup.")

class NAICSSearchInput(BaseModel):
    """Input for the NAICS Search tool."""
    query: str = Field(description="The query to match against NAICS code descriptions.")
    top_k: Optional[int] = Field(default=5, description="The number of results to return.")

class NAICSLookupResults(BaseTool):
    """Tool that queries the National American Industry Classification System (NAICS) Lookup API and returns back json."""

    name: str = "naics_lookup_results_json"

    description: str = (
        "A tool to lookup National American Industry Classification System (NAICS) codes."
        "Useful for when you need the title, description, or cross-reference information for a given six-digit NAICS code."
        "Input should be a six-digit numeric NAICS code."
    )

    args_schema: Type[BaseModel] = NAICSLookupInput
    """The tool input format."""
    
    api_wrapper: NAICSLookupAPIWrapper = Field(default_factory=NAICSLookupAPIWrapper)  # type: ignore[arg-type]
    response_format: Literal["content"] = "content"
    
    def _run(
        self, 
        code: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[List[Dict[str, str]], str]:
        """Use the tool."""
        # TODO: remove try/except, should be handled by BaseTool
        try:
            results = self.api_wrapper.results(code)
        except Exception as e:
            return repr(e)
        return results

class NAICSSearchResults(BaseTool):
    """Tool that queries the Naitonal American Industry Classification System (NAICS) Search API and returns back json."""

    name: str = "naics_search_results_json"
    description: str = (
        "A tool to search for National American Industry Classification System (NAICS) codes based on a query matching the NAICS code description."
        "Useful for when you need to identify and retrieve metadata about the six-digit NAICS code for a company or organization based on a description of their service, product, or production activity."
        "Input should be a one-sentence (ten to twenty words) query string that describes the service, product, or production activity of the company."
    )

    args_schema: Type[BaseModel] = NAICSSearchInput
    """The tool input format."""
    
    api_wrapper: NAICSSearchAPIWrapper = Field(default_factory=NAICSSearchAPIWrapper)  # type: ignore[arg-type]
    response_format: Literal["content"] = "content"
    
    def _run(
        self, 
        query: str,
        top_k: int = 5,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Union[List[Dict[str, str]], str]:
        """Use the tool."""
        # TODO: remove try/except, should be handled by BaseTool
        try:
            results = self.api_wrapper.results(query, top_k)
        except Exception as e:
            return repr(e)
        return results