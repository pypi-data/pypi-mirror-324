from __future__ import annotations
import ostk.core.filesystem
import ostk.core.type
import ostk.io
import typing
__all__ = ['Client', 'Request', 'Response']
class Client:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def fetch(url: ostk.io.URL, directory: ostk.core.filesystem.Directory, follow_count: int = 0) -> ostk.core.filesystem.File:
        ...
    @staticmethod
    def get(arg0: ostk.io.URL) -> Response:
        ...
    @staticmethod
    def list(arg0: ostk.io.URL, arg1: ostk.core.filesystem.File, arg2: bool) -> None:
        ...
    @staticmethod
    def send(arg0: Request) -> Response:
        ...
class Request:
    class Method:
        """
        Members:
        
          Undefined
        
          Get
        
          Head
        
          Post
        
          Put
        
          Delete
        
          Trace
        
          Options
        
          Connect
        
          Patch
        """
        Connect: typing.ClassVar[Request.Method]  # value = <Method.Connect: 8>
        Delete: typing.ClassVar[Request.Method]  # value = <Method.Delete: 5>
        Get: typing.ClassVar[Request.Method]  # value = <Method.Get: 1>
        Head: typing.ClassVar[Request.Method]  # value = <Method.Head: 2>
        Options: typing.ClassVar[Request.Method]  # value = <Method.Options: 7>
        Patch: typing.ClassVar[Request.Method]  # value = <Method.Patch: 9>
        Post: typing.ClassVar[Request.Method]  # value = <Method.Post: 3>
        Put: typing.ClassVar[Request.Method]  # value = <Method.Put: 4>
        Trace: typing.ClassVar[Request.Method]  # value = <Method.Trace: 6>
        Undefined: typing.ClassVar[Request.Method]  # value = <Method.Undefined: 0>
        __members__: typing.ClassVar[dict[str, Request.Method]]  # value = {'Undefined': <Method.Undefined: 0>, 'Get': <Method.Get: 1>, 'Head': <Method.Head: 2>, 'Post': <Method.Post: 3>, 'Put': <Method.Put: 4>, 'Delete': <Method.Delete: 5>, 'Trace': <Method.Trace: 6>, 'Options': <Method.Options: 7>, 'Connect': <Method.Connect: 8>, 'Patch': <Method.Patch: 9>}
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def get(arg0: ostk.io.URL) -> Request:
        ...
    @staticmethod
    def string_from_method(arg0: typing.Any) -> ostk.core.type.String:
        ...
    @staticmethod
    def undefined() -> Request:
        ...
    def __init__(self, arg0: typing.Any, arg1: ostk.io.URL, arg2: ostk.core.type.String) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_body(self) -> ostk.core.type.String:
        ...
    def get_method(self) -> ...:
        ...
    def get_url(self) -> ostk.io.URL:
        ...
    def is_defined(self) -> bool:
        ...
class Response:
    class StatusCode:
        """
        Members:
        
          Undefined
        
          Continue
        
          SwitchingProtocols
        
          Processing
        
          EarlyHints
        
          Ok
        
          Created
        
          Accepted
        
          NonAuthoritativeInformation
        
          NoContent
        
          ResetContent
        
          PartialContent
        
          MultiStatus
        
          AlreadyReported
        
          IMUsed
        
          MultipleChoices
        
          MovedPermanently
        
          Found
        
          SeeOther
        
          NotModified
        
          UseProxy
        
          SwitchProxy
        
          TemporaryRedirect
        
          PermanentRedirect
        
          BadRequest
        
          Unauthorized
        
          PaymentRequired
        
          Forbidden
        
          NotFound
        
          MethodNotAllowed
        
          NotAcceptable
        
          ProxyAuthenticationRequired
        
          RequestTimeout
        
          Conflict
        
          Gone
        
          LengthRequired
        
          PreconditionFailed
        
          PayloadTooLarge
        
          URITooLong
        
          UnsupportedMediaType
        
          RangeNotSatisfiable
        
          ExpectationFailed
        
          ImATeapot
        
          MisdirectedRequest
        
          UnprocessableEntity
        
          Locked
        
          FailedDependency
        
          UpgradeRequired
        
          PreconditionRequired
        
          TooManyRequests
        
          RequestHeaderFieldsTooLarge
        
          UnavailableForLegalReasons
        
          InternalServerError
        
          NotImplemented
        
          BadGateway
        
          ServiceUnavailable
        
          GatewayTimeout
        
          HTTPVersionNotSupported
        
          VariantAlsoNegotiates
        
          InsufficientStorage
        
          LoopDetected
        
          NotExtended
        
          NetworkAuthenticationRequire
        """
        Accepted: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Accepted: 202>
        AlreadyReported: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.AlreadyReported: 208>
        BadGateway: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.BadGateway: 502>
        BadRequest: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.BadRequest: 400>
        Conflict: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Conflict: 409>
        Continue: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Continue: 100>
        Created: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Created: 201>
        EarlyHints: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.EarlyHints: 103>
        ExpectationFailed: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.ExpectationFailed: 417>
        FailedDependency: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.FailedDependency: 424>
        Forbidden: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Forbidden: 403>
        Found: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Found: 302>
        GatewayTimeout: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.GatewayTimeout: 504>
        Gone: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Gone: 410>
        HTTPVersionNotSupported: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.HTTPVersionNotSupported: 505>
        IMUsed: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.IMUsed: 226>
        ImATeapot: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.ImATeapot: 418>
        InsufficientStorage: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.InsufficientStorage: 507>
        InternalServerError: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.InternalServerError: 500>
        LengthRequired: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.LengthRequired: 411>
        Locked: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Locked: 423>
        LoopDetected: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.LoopDetected: 508>
        MethodNotAllowed: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.MethodNotAllowed: 405>
        MisdirectedRequest: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.MisdirectedRequest: 421>
        MovedPermanently: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.MovedPermanently: 301>
        MultiStatus: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.MultiStatus: 207>
        MultipleChoices: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.MultipleChoices: 300>
        NetworkAuthenticationRequire: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.NetworkAuthenticationRequire: 511>
        NoContent: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.NoContent: 204>
        NonAuthoritativeInformation: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.NonAuthoritativeInformation: 203>
        NotAcceptable: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.NotAcceptable: 406>
        NotExtended: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.NotExtended: 510>
        NotFound: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.NotFound: 404>
        NotImplemented: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.NotImplemented: 501>
        NotModified: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.NotModified: 304>
        Ok: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Ok: 200>
        PartialContent: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.PartialContent: 206>
        PayloadTooLarge: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.PayloadTooLarge: 413>
        PaymentRequired: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.PaymentRequired: 402>
        PermanentRedirect: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.PermanentRedirect: 308>
        PreconditionFailed: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.PreconditionFailed: 412>
        PreconditionRequired: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.PreconditionRequired: 428>
        Processing: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Processing: 102>
        ProxyAuthenticationRequired: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.ProxyAuthenticationRequired: 407>
        RangeNotSatisfiable: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.RangeNotSatisfiable: 416>
        RequestHeaderFieldsTooLarge: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.RequestHeaderFieldsTooLarge: 431>
        RequestTimeout: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.RequestTimeout: 408>
        ResetContent: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.ResetContent: 205>
        SeeOther: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.SeeOther: 303>
        ServiceUnavailable: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.ServiceUnavailable: 503>
        SwitchProxy: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.SwitchProxy: 306>
        SwitchingProtocols: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.SwitchingProtocols: 101>
        TemporaryRedirect: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.TemporaryRedirect: 307>
        TooManyRequests: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.TooManyRequests: 429>
        URITooLong: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.URITooLong: 414>
        Unauthorized: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Unauthorized: 401>
        UnavailableForLegalReasons: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.UnavailableForLegalReasons: 451>
        Undefined: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.Undefined: 0>
        UnprocessableEntity: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.UnprocessableEntity: 422>
        UnsupportedMediaType: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.UnsupportedMediaType: 415>
        UpgradeRequired: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.UpgradeRequired: 426>
        UseProxy: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.UseProxy: 305>
        VariantAlsoNegotiates: typing.ClassVar[Response.StatusCode]  # value = <StatusCode.VariantAlsoNegotiates: 506>
        __members__: typing.ClassVar[dict[str, Response.StatusCode]]  # value = {'Undefined': <StatusCode.Undefined: 0>, 'Continue': <StatusCode.Continue: 100>, 'SwitchingProtocols': <StatusCode.SwitchingProtocols: 101>, 'Processing': <StatusCode.Processing: 102>, 'EarlyHints': <StatusCode.EarlyHints: 103>, 'Ok': <StatusCode.Ok: 200>, 'Created': <StatusCode.Created: 201>, 'Accepted': <StatusCode.Accepted: 202>, 'NonAuthoritativeInformation': <StatusCode.NonAuthoritativeInformation: 203>, 'NoContent': <StatusCode.NoContent: 204>, 'ResetContent': <StatusCode.ResetContent: 205>, 'PartialContent': <StatusCode.PartialContent: 206>, 'MultiStatus': <StatusCode.MultiStatus: 207>, 'AlreadyReported': <StatusCode.AlreadyReported: 208>, 'IMUsed': <StatusCode.IMUsed: 226>, 'MultipleChoices': <StatusCode.MultipleChoices: 300>, 'MovedPermanently': <StatusCode.MovedPermanently: 301>, 'Found': <StatusCode.Found: 302>, 'SeeOther': <StatusCode.SeeOther: 303>, 'NotModified': <StatusCode.NotModified: 304>, 'UseProxy': <StatusCode.UseProxy: 305>, 'SwitchProxy': <StatusCode.SwitchProxy: 306>, 'TemporaryRedirect': <StatusCode.TemporaryRedirect: 307>, 'PermanentRedirect': <StatusCode.PermanentRedirect: 308>, 'BadRequest': <StatusCode.BadRequest: 400>, 'Unauthorized': <StatusCode.Unauthorized: 401>, 'PaymentRequired': <StatusCode.PaymentRequired: 402>, 'Forbidden': <StatusCode.Forbidden: 403>, 'NotFound': <StatusCode.NotFound: 404>, 'MethodNotAllowed': <StatusCode.MethodNotAllowed: 405>, 'NotAcceptable': <StatusCode.NotAcceptable: 406>, 'ProxyAuthenticationRequired': <StatusCode.ProxyAuthenticationRequired: 407>, 'RequestTimeout': <StatusCode.RequestTimeout: 408>, 'Conflict': <StatusCode.Conflict: 409>, 'Gone': <StatusCode.Gone: 410>, 'LengthRequired': <StatusCode.LengthRequired: 411>, 'PreconditionFailed': <StatusCode.PreconditionFailed: 412>, 'PayloadTooLarge': <StatusCode.PayloadTooLarge: 413>, 'URITooLong': <StatusCode.URITooLong: 414>, 'UnsupportedMediaType': <StatusCode.UnsupportedMediaType: 415>, 'RangeNotSatisfiable': <StatusCode.RangeNotSatisfiable: 416>, 'ExpectationFailed': <StatusCode.ExpectationFailed: 417>, 'ImATeapot': <StatusCode.ImATeapot: 418>, 'MisdirectedRequest': <StatusCode.MisdirectedRequest: 421>, 'UnprocessableEntity': <StatusCode.UnprocessableEntity: 422>, 'Locked': <StatusCode.Locked: 423>, 'FailedDependency': <StatusCode.FailedDependency: 424>, 'UpgradeRequired': <StatusCode.UpgradeRequired: 426>, 'PreconditionRequired': <StatusCode.PreconditionRequired: 428>, 'TooManyRequests': <StatusCode.TooManyRequests: 429>, 'RequestHeaderFieldsTooLarge': <StatusCode.RequestHeaderFieldsTooLarge: 431>, 'UnavailableForLegalReasons': <StatusCode.UnavailableForLegalReasons: 451>, 'InternalServerError': <StatusCode.InternalServerError: 500>, 'NotImplemented': <StatusCode.NotImplemented: 501>, 'BadGateway': <StatusCode.BadGateway: 502>, 'ServiceUnavailable': <StatusCode.ServiceUnavailable: 503>, 'GatewayTimeout': <StatusCode.GatewayTimeout: 504>, 'HTTPVersionNotSupported': <StatusCode.HTTPVersionNotSupported: 505>, 'VariantAlsoNegotiates': <StatusCode.VariantAlsoNegotiates: 506>, 'InsufficientStorage': <StatusCode.InsufficientStorage: 507>, 'LoopDetected': <StatusCode.LoopDetected: 508>, 'NotExtended': <StatusCode.NotExtended: 510>, 'NetworkAuthenticationRequire': <StatusCode.NetworkAuthenticationRequire: 511>}
        @staticmethod
        def _pybind11_conduit_v1_(*args, **kwargs):
            ...
        def __eq__(self, other: typing.Any) -> bool:
            ...
        def __getstate__(self) -> int:
            ...
        def __hash__(self) -> int:
            ...
        def __index__(self) -> int:
            ...
        def __init__(self, value: int) -> None:
            ...
        def __int__(self) -> int:
            ...
        def __ne__(self, other: typing.Any) -> bool:
            ...
        def __repr__(self) -> str:
            ...
        def __setstate__(self, state: int) -> None:
            ...
        def __str__(self) -> str:
            ...
        @property
        def name(self) -> str:
            ...
        @property
        def value(self) -> int:
            ...
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @staticmethod
    def string_from_status_code(arg0: typing.Any) -> ostk.core.type.String:
        ...
    @staticmethod
    def undefined() -> Response:
        ...
    def __init__(self, arg0: typing.Any, arg1: ostk.core.type.String) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
    def get_body(self) -> ostk.core.type.String:
        ...
    def get_status_code(self) -> ...:
        ...
    def is_defined(self) -> bool:
        ...
    def is_ok(self) -> bool:
        ...
