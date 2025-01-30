from __future__ import annotations
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Callable, Dict, List, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from ....models.error_response import ErrorResponse
    from ....models.windows import Windows

class WindowsRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /vehicles/{vin}/windows
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, Dict[str, Any]]) -> None:
        """
        Instantiates a new WindowsRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/vehicles/{vin}/windows", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[Windows]:
        """
        Vehicle's Latest Window Status Values
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Windows]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ....models.error_response import ErrorResponse

        error_mapping: Dict[str, type[ParsableFactory]] = {
            "400": ErrorResponse,
            "401": ErrorResponse,
            "403": ErrorResponse,
            "404": ErrorResponse,
            "405": ErrorResponse,
            "409": ErrorResponse,
            "415": ErrorResponse,
            "422": ErrorResponse,
            "500": ErrorResponse,
            "503": ErrorResponse,
            "504": ErrorResponse,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.windows import Windows

        return await self.request_adapter.send_async(request_info, Windows, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Vehicle's Latest Window Status Values
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> WindowsRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WindowsRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return WindowsRequestBuilder(self.request_adapter, raw_url)
    
    @dataclass
    class WindowsRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

