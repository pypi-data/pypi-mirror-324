from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar

from wireup.errors import (
    UnknownQualifiedServiceRequestedError,
    UsageOfQualifierOnUnknownObjectError,
)
from wireup.ioc.override_manager import OverrideManager
from wireup.ioc.service_registry import FactoryType
from wireup.ioc.types import (
    AnnotatedParameter,
    ParameterWrapper,
    Qualifier,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from wireup import ParameterBag
    from wireup.ioc.service_registry import ServiceRegistry
    from wireup.ioc.types import ContainerObjectIdentifier, Qualifier

T = TypeVar("T")


class BaseContainer:
    """Base Container class providing core functionality."""

    __slots__ = ("_initialized_objects", "_override_mgr", "_overrides", "_params", "_registry")

    def __init__(
        self,
        registry: ServiceRegistry,
        parameters: ParameterBag,
        overrides: dict[ContainerObjectIdentifier, Any],
    ) -> None:
        self._registry = registry
        self._params = parameters
        self._overrides = overrides
        self._override_mgr = OverrideManager(overrides, self._registry.is_type_with_qualifier_known)
        self._initialized_objects: dict[ContainerObjectIdentifier, Any] = {}

    def is_type_known(self, klass: type) -> bool:
        """Given a class type return True if's registered in the container as a service or interface."""
        return self._registry.is_impl_known(klass) or self._registry.is_interface_known(klass)

    @property
    def override(self) -> OverrideManager:
        """Override registered container services with new values."""
        return self._override_mgr

    def _get_ctor(
        self, klass: type[T], qualifier: Qualifier | None
    ) -> tuple[Callable[..., Any], type[T], FactoryType] | None:
        if ctor := self._registry.factory_functions.get((klass, qualifier)):
            return ctor.factory, klass, ctor.factory_type

        if self._registry.is_interface_known(klass):
            concrete_class = self._registry.interface_resolve_impl(klass, qualifier)
            return self._get_ctor(concrete_class, qualifier)

        if self._registry.is_impl_known(klass):
            if not self._registry.is_impl_with_qualifier_known(klass, qualifier):
                raise UnknownQualifiedServiceRequestedError(
                    klass,
                    qualifier,
                    self._registry.known_impls[klass],
                )

            return klass, klass, FactoryType.REGULAR

        # Throw if a qualifier is being used on an unknown type.
        if qualifier:
            raise UsageOfQualifierOnUnknownObjectError(qualifier)

        return None

    def _try_get_existing_value(self, param: AnnotatedParameter) -> tuple[Any, bool]:
        if param.klass:
            obj_id = param.klass, param.qualifier_value

            if res := self._overrides.get(obj_id):
                return res, True

            if self._registry.is_interface_known(param.klass):
                resolved_type = self._registry.interface_resolve_impl(param.klass, param.qualifier_value)
                obj_id = resolved_type, param.qualifier_value

            if res := self._initialized_objects.get(obj_id):
                return res, True

        if isinstance(param.annotation, ParameterWrapper):
            return self._params.get(param.annotation.param), True

        return None, False
