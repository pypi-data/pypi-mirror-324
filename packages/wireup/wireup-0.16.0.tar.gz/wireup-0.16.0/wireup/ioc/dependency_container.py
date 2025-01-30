from __future__ import annotations

import asyncio
import functools
import sys
import warnings
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, TypeVar, overload

from wireup.ioc._exit_stack import async_clean_exit_stack, clean_exit_stack
from wireup.ioc.base_container import BaseContainer

if sys.version_info < (3, 9):
    from graphlib2 import TopologicalSorter
else:
    from graphlib import TopologicalSorter

from wireup.errors import (
    InvalidRegistrationTypeError,
    UnknownServiceRequestedError,
    WireupError,
)
from wireup.ioc.service_registry import GENERATOR_FACTORY_TYPES, FactoryType, ServiceRegistry
from wireup.ioc.types import (
    AnyCallable,
    ContainerObjectIdentifier,
    EmptyContainerInjectionRequest,
    Qualifier,
    ServiceLifetime,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from types import AsyncGeneratorType, GeneratorType

    from wireup.ioc.initialization_context import InitializationContext
    from wireup.ioc.parameter import ParameterBag

T = TypeVar("T")


@dataclass(frozen=True)
class _CreationResult:
    instance: Any
    exit_stack: list[GeneratorType[Any, Any, Any] | AsyncGeneratorType[Any, Any]]


@dataclass(frozen=True)
class _InjectionResult:
    kwargs: dict[str, Any]
    exit_stack: list[GeneratorType[Any, Any, Any] | AsyncGeneratorType[Any, Any]]


class DependencyContainer(BaseContainer):
    """Dependency Injection and Service Locator container registry.

    This contains all the necessary information to initialize registered classes.
    Objects instantiated by the container are lazily loaded and initialized only on first use.

    Provides the following decorators: `register`, `abstract` and `autowire`. Use register on factory functions
    and concrete classes which are to be injected from the container.
    Abstract classes are to be used as interfaces and will not be injected directly, rather concrete classes
    which implement them will be injected instead.

    Use the `autowire` decorator on methods where dependency injection must be performed.
    Services will be injected automatically where possible. Parameters will have to be annotated as they cannot
    be located from type alone.
    """

    __slots__ = ("__exit_stack",)

    def __init__(self, parameter_bag: ParameterBag) -> None:
        """:param parameter_bag: ParameterBag instance holding parameter information."""
        super().__init__(registry=ServiceRegistry(), parameters=parameter_bag, overrides={})
        self.__exit_stack: list[GeneratorType[Any, Any, Any] | AsyncGeneratorType[Any, Any]] = []

    def get(self, klass: type[T], qualifier: Qualifier | None = None) -> T:
        """Get an instance of the requested type.

        Use this to locate services by their type but strongly prefer using injection instead.

        :param qualifier: Qualifier for the class if it was registered with one.
        :param klass: Class of the dependency already registered in the container.
        :return: An instance of the requested object. Always returns an existing instance when one is available.
        """
        if res := self._overrides.get((klass, qualifier)):
            return res  # type: ignore[no-any-return]

        if self._registry.is_interface_known(klass):
            klass = self._registry.interface_resolve_impl(klass, qualifier)

        if instance := self._initialized_objects.get((klass, qualifier)):
            return instance  # type: ignore[no-any-return]

        if res := self.__create_instance(klass, qualifier):
            if res.exit_stack:
                msg = "Container.get does not support Transient lifetime service generator factories."
                raise WireupError(msg)

            return res.instance  # type: ignore[no-any-return]

        raise UnknownServiceRequestedError(klass)

    async def aget(self, klass: type[T], qualifier: Qualifier | None = None) -> T:
        """Get an instance of the requested type.

        Use this to locate services by their type but strongly prefer using injection instead.

        :param qualifier: Qualifier for the class if it was registered with one.
        :param klass: Class of the dependency already registered in the container.
        :return: An instance of the requested object. Always returns an existing instance when one is available.
        """
        if res := self._overrides.get((klass, qualifier)):
            return res  # type: ignore[no-any-return]

        if self._registry.is_interface_known(klass):
            klass = self._registry.interface_resolve_impl(klass, qualifier)

        if instance := self._initialized_objects.get((klass, qualifier)):
            return instance  # type: ignore[no-any-return]

        if res := await self.__async_create_instance(klass, qualifier):
            if res.exit_stack:
                msg = "Container.get does not support Transient lifetime service generator factories."
                raise WireupError(msg)

            return res.instance  # type: ignore[no-any-return]

        raise UnknownServiceRequestedError(klass)

    def abstract(self, klass: type[T]) -> type[T]:
        """Register a type as an interface.

        This type cannot be initialized directly and one of the components implementing this will be injected instead.
        """
        self._registry.register_abstract(klass)

        return klass

    @overload
    def register(
        self,
        obj: None = None,
        *,
        qualifier: Qualifier | None = None,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ) -> Callable[[T], T]:
        pass

    @overload
    def register(
        self,
        obj: T,
        *,
        qualifier: Qualifier | None = None,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ) -> T:
        pass

    def register(
        self,
        obj: T | None = None,
        *,
        qualifier: Qualifier | None = None,
        lifetime: ServiceLifetime = ServiceLifetime.SINGLETON,
    ) -> T | Callable[[T], T]:
        """Register a dependency in the container. Dependency must be either a class or a factory function.

        * Use as a decorator without parameters @container.register on a factory function or class to register it.
        * Use as a decorator with parameters to specify qualifier and lifetime, @container.register(qualifier=...).
        * Call it directly with @container.register(some_class_or_factory, qualifier=..., lifetime=...).
        """
        # Allow register to be used either with or without arguments
        if obj is None:

            def decorated(decorated_obj: T) -> T:
                self.register(decorated_obj, qualifier=qualifier, lifetime=lifetime)
                return decorated_obj

            return decorated

        if isinstance(obj, type):
            self._registry.register_service(obj, qualifier, lifetime)
            return obj

        if callable(obj):
            self._registry.register_factory(obj, qualifier=qualifier, lifetime=lifetime)
            return obj

        raise InvalidRegistrationTypeError(obj)

    @property
    def context(self) -> InitializationContext:
        """The initialization context for registered targets. A map between an injection target and its dependencies."""
        warnings.warn(
            "Using the initialization context directly is deprecated. "
            "Register your services using @service/@abstract. "
            "See: https://maldoinc.github.io/wireup/latest/getting_started/",
            DeprecationWarning,
            stacklevel=2,
        )
        return self._registry.context

    @property
    def params(self) -> ParameterBag:
        """Parameter bag associated with this container."""
        return self._params

    def clear_initialized_objects(self) -> None:
        """Drop references to initialized singleton objects.

        Calling this will cause the container to drop references to initialized singletons
        and cause it to create new instances when they are requested to be injected.

        This can be useful in tests in a `unittest.TestCase.setUp` method or pytest autouse=True fixture,
        allowing you to have a fresh copy of the container with no previously initialized instances
        to make test cases independent of each-other.
        """
        warnings.warn(
            "Using clear_initialized_objects is deprecated. "
            "Recreate the container if you want to reset its state. "
            "See: https://maldoinc.github.io/wireup/latest/testing/",
            DeprecationWarning,
            stacklevel=2,
        )
        self._initialized_objects.clear()

    def autowire(self, fn: AnyCallable) -> AnyCallable:
        """Automatically inject resources from the container to the decorated methods.

        Any arguments which the container does not know about will be ignored
        so that another decorator or framework can supply their values.
        This decorator can be used on both async and blocking methods.

        * Classes will be automatically injected.
        * Parameters need to be annotated in order for container to be able to resolve them
        * When injecting an interface for which there are multiple implementations you need to supply a qualifier
          using annotations.
        """
        self._registry.target_init_context(fn)

        if asyncio.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def async_inner(*args: Any, **kwargs: Any) -> Any:
                res = await self.__async_callable_get_params_to_inject(fn)
                try:
                    return await fn(*args, **{**kwargs, **res.kwargs})
                finally:
                    await async_clean_exit_stack(res.exit_stack)

            return async_inner

        @functools.wraps(fn)
        def sync_inner(*args: Any, **kwargs: Any) -> Any:
            res = self.__callable_get_params_to_inject(fn)
            try:
                return fn(*args, **{**kwargs, **res.kwargs})
            finally:
                clean_exit_stack(res.exit_stack)

        return sync_inner

    def warmup(self) -> None:
        """Initialize all singleton dependencies registered in the container.

        This should be executed once all services are registered with the container. Targets of autowire will not
        be affected.
        """
        sorter = TopologicalSorter(self._registry.get_dependency_graph())

        for klass in sorter.static_order():
            for qualifier in self._registry.known_impls[klass]:
                if (klass, qualifier) not in self._initialized_objects:
                    self.get(klass, qualifier)

    def __callable_get_params_to_inject(self, fn: AnyCallable) -> _InjectionResult:
        result: dict[str, Any] = {}
        names_to_remove: set[str] = set()
        exit_stack: list[GeneratorType[Any, Any, Any] | AsyncGeneratorType[Any, Any]] = []

        for name, param in self._registry.context.dependencies[fn].items():
            obj, value_found = self._try_get_existing_value(param)

            if value_found:
                result[name] = obj
            elif param.klass and (creation := self.__create_instance(param.klass, param.qualifier_value)):
                if creation.exit_stack:
                    exit_stack.extend(creation.exit_stack)
                result[name] = creation.instance
            else:
                # Normally the container won't throw if it encounters a type it doesn't know about
                # But if it's explicitly marked as to be injected then we need to throw.
                if param.klass and isinstance(param.annotation, EmptyContainerInjectionRequest):
                    raise UnknownServiceRequestedError(param.klass)

                names_to_remove.add(name)

        # If autowiring, the container is assumed to be final, so unnecessary entries can be removed
        # from the context in order to speed up the autowiring process.
        if names_to_remove:
            self._registry.context.remove_dependencies(fn, names_to_remove)

        return _InjectionResult(kwargs=result, exit_stack=exit_stack)

    async def __async_callable_get_params_to_inject(self, fn: AnyCallable) -> _InjectionResult:
        result: dict[str, Any] = {}
        names_to_remove: set[str] = set()
        exit_stack: list[GeneratorType[Any, Any, Any] | AsyncGeneratorType[Any, Any]] = []

        for name, param in self._registry.context.dependencies[fn].items():
            obj, value_found = self._try_get_existing_value(param)

            if value_found:
                result[name] = obj
            elif param.klass and (creation := await self.__async_create_instance(param.klass, param.qualifier_value)):
                if creation.exit_stack:
                    exit_stack.extend(creation.exit_stack)
                result[name] = creation.instance
            else:
                # Normally the container won't throw if it encounters a type it doesn't know about
                # But if it's explicitly marked as to be injected then we need to throw.
                if param.klass and isinstance(param.annotation, EmptyContainerInjectionRequest):
                    raise UnknownServiceRequestedError(param.klass)

                names_to_remove.add(name)

        # If autowiring, the container is assumed to be final, so unnecessary entries can be removed
        # from the context in order to speed up the autowiring process.
        if names_to_remove:
            self._registry.context.remove_dependencies(fn, names_to_remove)

        return _InjectionResult(kwargs=result, exit_stack=exit_stack)

    def __create_instance(self, klass: type[T], qualifier: Qualifier | None) -> _CreationResult | None:
        ctor_and_type = self._get_ctor(klass=klass, qualifier=qualifier)

        if not ctor_and_type:
            return None

        ctor, resolved_type, factory_type = ctor_and_type

        if factory_type == FactoryType.ASYNC_GENERATOR:
            msg = "Cannot construct async objects fron a non-async context."
            raise WireupError(msg)

        injection_result = self.__callable_get_params_to_inject(ctor)
        instance_or_generator = ctor(**injection_result.kwargs)
        object_identifier = resolved_type, qualifier

        if factory_type == FactoryType.GENERATOR:
            generator = instance_or_generator
            instance = next(instance_or_generator)
        else:
            instance = instance_or_generator
            generator = None

        return self.__wrap_result(
            generator=generator,
            instance=instance,
            object_identifier=object_identifier,
            injection_result=injection_result,
        )

    async def __async_create_instance(self, klass: type[T], qualifier: Qualifier | None) -> _CreationResult | None:
        ctor_and_type = self._get_ctor(klass=klass, qualifier=qualifier)

        if not ctor_and_type:
            return None

        ctor, resolved_type, factory_type = ctor_and_type
        injection_result = await self.__async_callable_get_params_to_inject(ctor)
        instance_or_generator = (
            await ctor(**injection_result.kwargs)
            if factory_type == FactoryType.COROUTINE_FN
            else ctor(**injection_result.kwargs)
        )
        object_identifier = resolved_type, qualifier

        if factory_type in GENERATOR_FACTORY_TYPES:
            generator = instance_or_generator
            instance = (
                next(instance_or_generator)
                if factory_type == FactoryType.GENERATOR
                else await instance_or_generator.__anext__()
            )
        else:
            generator = None
            instance = instance_or_generator

        return self.__wrap_result(
            generator=generator,
            instance=instance,
            object_identifier=object_identifier,
            injection_result=injection_result,
        )

    def __wrap_result(
        self,
        *,
        generator: Any | None,
        instance: Any,
        object_identifier: ContainerObjectIdentifier,
        injection_result: _InjectionResult,
    ) -> _CreationResult:
        is_singleton = self._registry.is_impl_singleton(object_identifier[0])

        if generator:
            if is_singleton:
                self.__exit_stack.append(generator)
                self._initialized_objects[object_identifier] = instance

            return _CreationResult(
                instance=instance,
                exit_stack=injection_result.exit_stack if is_singleton else [*injection_result.exit_stack, generator],
            )

        if is_singleton:
            self._initialized_objects[object_identifier] = instance

        return _CreationResult(instance=instance, exit_stack=injection_result.exit_stack)

    def close(self) -> None:
        """Consume generator factories allowing them to properly release resources."""
        clean_exit_stack(self.__exit_stack)

    async def aclose(self) -> None:
        """Consume generator factories allowing them to properly release resources."""
        await async_clean_exit_stack(self.__exit_stack)
