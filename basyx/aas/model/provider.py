# Copyright (c) 2020 the Eclipse BaSyx Authors
#
# This program and the accompanying materials are made available under the terms of the MIT License, available in
# the LICENSE file of this project.
#
# SPDX-License-Identifier: MIT
"""
This module implements Registries for the AAS, in order to enable resolving global
identifier; and mapping
identifier to :class:`~basyx.aas.model.types.Identifiable` objects.
"""

import abc
from typing import MutableSet, Iterator, Generic, TypeVar, Dict, List, Optional, Iterable

from .types import Identifiable, Environment, AssetAdministrationShell, Submodel, ConceptDescription


class AbstractObjectProvider(metaclass=abc.ABCMeta):
    """
    Abstract baseclass for all objects, that allow to retrieve :class:`~basyx.aas.model.types.Identifiable` objects
    (resp. proxy objects for remote :class:`~basyx.aas.model.types.Identifiable` objects) by their
    Identifier.

    This includes local object stores, database clients and AAS API clients.
    """
    @abc.abstractmethod
    def get_identifiable(self, identifier: str) -> Identifiable:
        """
        Find an :class:`~basyx.aas.model.types.Identifiable` by its Identifier

        This may include looking up the object's endpoint in a registry and fetching it from an HTTP server or a
        database.

        :param identifier: Identifier of the object to return
        :return: The :class:`~basyx.aas.model.types.Identifiable` object (or a proxy object for a remote
                 :class:`~basyx.aas.model.types.Identifiable` object)
        :raises KeyError: If no such :class:`~.basyx.aas.model.types.Identifiable` can be found
        """
        pass

    def get(self, identifier: str, default: Optional[Identifiable] = None) -> Optional[Identifiable]:
        """
        Find an object in this set by its identifier, with fallback parameter

        :param identifier: Identifier of the object to return
        :param default: An object to be returned, if no object with the given
                        identifier is found
        :return: The :class:`~basyx.aas.model.types.Identifiable` object with the given
                 identifier in the provider. Otherwise the ``default`` object
                 or None, if none is given.
        """
        try:
            return self.get_identifiable(identifier)
        except KeyError:
            return default


_IT = TypeVar('_IT', bound=Identifiable)


class AbstractObjectStore(AbstractObjectProvider, MutableSet[_IT], Generic[_IT], metaclass=abc.ABCMeta):
    """
    Abstract baseclass of for container-like objects for storage of :class:`~basyx.aas.model.types.Identifiable` objects.

    ObjectStores are special ObjectProvides that – in addition to retrieving objects by
    Identifier – allow to add and delete objects (i.e. behave like a Python set).
    This includes local object stores (like :class:`~.DictObjectStore`) and database
    :class:`Backends <basyx.aas.backend.backends.Backend>`.

    The AbstractObjectStore inherits from the :class:`~collections.abc.MutableSet` abstract collections class and
    therefore implements all the functions of this class.
    """
    @abc.abstractmethod
    def __init__(self):
        pass

    def update(self, other: Iterable[_IT]) -> None:
        for x in other:
            self.add(x)

    @abc.abstractmethod
    def as_environment(self) -> Environment:
        pass


class DictObjectStore(AbstractObjectStore[_IT], Generic[_IT]):
    """
    A local in-memory object store for :class:`~basyx.aas.model.types.Identifiable` objects, backed by a dict, mapping
    Identifier → :class:`~basyx.aas.model.types.Identifiable`
    """
    def __init__(self, objects: Iterable[_IT] = ()) -> None:
        super().__init__()
        self._backend: Dict[str, _IT] = {}
        for x in objects:
            self.add(x)

    def get_identifiable(self, identifier: str) -> _IT:
        return self._backend[identifier]

    def as_environment(self) -> Environment:
        asset_administration_shells: List[AssetAdministrationShell] = []
        submodels: List[Submodel] = []
        concept_descriptions: List[ConceptDescription] = []
        for obj in self._backend.values():
            if isinstance(obj, AssetAdministrationShell):
                asset_administration_shells.append(obj)
            elif isinstance(obj, Submodel):
                submodels.append(obj)
            elif isinstance(obj, ConceptDescription):
                concept_descriptions.append(obj)

        environment = Environment(
            asset_administration_shells, submodels, concept_descriptions
        )
        return environment


    def add(self, x: _IT) -> None:
        if x.id in self._backend and self._backend.get(x.id) is not x:
            raise KeyError("Identifiable object with same id {} is already stored in this store"
                           .format(x.id))
        self._backend[x.id] = x

    def discard(self, x: _IT) -> None:
        if self._backend.get(x.id) is x:
            del self._backend[x.id]

    def __contains__(self, x: object) -> bool:
        if isinstance(x, str):
            return x in self._backend
        if not isinstance(x, Identifiable):
            return False
        return self._backend.get(x.id) is x

    def __len__(self) -> int:
        return len(self._backend)

    def __iter__(self) -> Iterator[_IT]:
        return iter(self._backend.values())


class ObjectProviderMultiplexer(AbstractObjectProvider):
    """
    A multiplexer for Providers of :class:`~basyx.aas.model.types.Identifiable` objects.

    This class combines multiple registries of :class:`~basyx.aas.model.types.Identifiable` objects into a single one
    to allow retrieving :class:`~basyx.aas.model.types.Identifiable` objects from different sources.
    It implements the :class:`~.AbstractObjectProvider` interface to be used as registry itself.

    :ivar registries: A list of :class:`AbstractObjectProviders <.AbstractObjectProvider>` to query when looking up an
                      object
    """
    def __init__(self, registries: Optional[List[AbstractObjectProvider]] = None):
        self.providers: List[AbstractObjectProvider] = registries if registries is not None else []

    def get_identifiable(self, identifier: str) -> Identifiable:
        for provider in self.providers:
            try:
                return provider.get_identifiable(identifier)
            except KeyError:
                pass
        raise KeyError("Identifier could not be found in any of the {} consulted registries."
                       .format(len(self.providers)))
