from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from wireup.ioc.types import Qualifier


class WireupError(Exception):
    """Base type for all exceptions raised by wrireup."""


class DuplicateServiceRegistrationError(WireupError):
    """Raised when attempting to register a service with the same qualifier twice."""

    def __init__(self, klass: type[Any], qualifier: Qualifier | None) -> None:
        self.klass = klass
        self.qualifier = qualifier

        msg = f"Cannot register type {klass} with qualifier '{qualifier}' as it already exists."
        super().__init__(msg)


class DuplicateQualifierForInterfaceError(WireupError):
    """Raised when registering an impl for an interface using a qualifier that is already known."""

    def __init__(self, klass: type[Any], qualifier: Qualifier | None) -> None:
        super().__init__(
            f"Cannot register implementation class {klass} for {klass.__base__} "
            f"with qualifier '{qualifier}' as it already exists",
        )


class UnknownParameterError(WireupError):
    """Raised when requesting a parameter by name which does not exist."""

    def __init__(self, parameter_name: str) -> None:
        self.parameter_name = parameter_name
        super().__init__(f"Unknown parameter requested: {parameter_name}")


class FactoryReturnTypeIsEmptyError(WireupError):
    """Raised when a factory function has no return type defined."""

    def __init__(self) -> None:
        super().__init__("Factory functions must specify a return type denoting the type of dependency it can create.")


class FactoryDuplicateServiceRegistrationError(WireupError):
    """Raised when a factory function declares that it produces a type which is already known."""

    def __init__(self, return_type: type[Any], qualifier: Qualifier | None = None) -> None:
        self.return_type = return_type
        super().__init__(
            f"A function is already registered as a factory for dependency type {return_type} "
            f"with qualifier {qualifier}."
        )


class UnknownQualifiedServiceRequestedError(WireupError):
    """Raised when requesting a type which exists but using an unknown qualifier."""

    def __init__(
        self,
        klass: type[Any],
        qualifier: Qualifier | None,
        available_qualifiers: set[Qualifier | None],
    ) -> None:
        self.klass = klass
        self.qualifier = qualifier
        qualifiers_str = ", ".join(sorted(f"'{q}'" for q in available_qualifiers))

        super().__init__(
            f"Cannot instantiate concrete class for {klass} as qualifier '{qualifier}' is unknown. "
            f"Available qualifiers: [{qualifiers_str}].",
        )


class UnknownServiceRequestedError(WireupError):
    """Raised when requesting an unknown type."""

    def __init__(self, klass: type[Any]) -> None:
        super().__init__(
            f"Cannot wire unknown class {klass}. Use '@service' or '@abstract' to enable autowiring.",
        )


class UsageOfQualifierOnUnknownObjectError(WireupError):
    """Raised when using a qualifier on an unknown type that is not managed by the container."""

    def __init__(self, qualifier_value: Qualifier | None) -> None:
        super().__init__(f"Cannot use qualifier {qualifier_value} on a type that is not managed by the container.")


class InvalidRegistrationTypeError(WireupError):
    """Raised when attempting to call @container.register with an invalid argument."""

    def __init__(self, attempted: Any) -> None:
        super().__init__(f"Cannot register {attempted} with the container. Allowed types are callables and types")


class UnknownOverrideRequestedError(WireupError):
    """Raised when attempting to override a service which does not exist."""

    def __init__(self, klass: type, qualifier: Qualifier | None) -> None:
        super().__init__(f"Cannot override unknown {klass} with qualifier '{qualifier}'.")


class ContainerCloseError(WireupError):
    """Contains a list of exceptions raised while closing the container."""

    def __init__(self, errors: list[Exception]) -> None:
        self.errors = errors
        super().__init__(f"The following exceptions were raised while closing the container: {errors}")
