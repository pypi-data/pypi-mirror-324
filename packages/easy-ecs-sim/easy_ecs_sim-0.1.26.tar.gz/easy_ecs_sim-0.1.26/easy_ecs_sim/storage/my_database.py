from functools import cache
from typing import Type, override, TypeVar

from easy_ecs_sim.component import Component
from easy_ecs_sim.signature import Signature
from easy_ecs_sim.storage.database import Database
from easy_ecs_sim.storage.demography import Demography
from easy_ecs_sim.storage.id_generator import IdGenerator
from easy_ecs_sim.storage.index import Index
from easy_ecs_sim.utils import ComponentSet, flatten_components

EID_GEN = IdGenerator()

T = TypeVar('T')


class MyDatabase(Database):
    def __init__(self):
        self._entities: set[int] = set()
        self.tables: dict[Type[Component | Signature], Index] = {}
        self.dirty: Demography = Demography()

    @override
    def find_any[T: Component](self, what: Type[T], having: list[Type[Component]] = None) -> T:
        table = self.get_table(what)
        eids = table.entities
        for _ in having or []:
            eids.intersection_update(self.get_table(_).entities)

        if eids:
            eid = next(iter(eids))
            return table.read(eid)

    @override
    def entity_ids(self):
        return self._entities

    @override
    def create_all(self, items: list[ComponentSet]):
        items = list(map(flatten_components, items))
        for components in items:
            eid = EID_GEN.new_id()
            for _ in components:
                _.eid = eid

        self.dirty.with_birth(items)

    @override
    def destroy_all(self, items: Component | Signature | list[Component | Signature]):
        self.dirty.with_death(items)

    @override
    @cache
    def get_table[T:Component | Signature](self, ttype: Type[T]) -> Index[T]:
        if ttype not in self.tables:
            self.tables[ttype] = Index(ttype=ttype)
        return self.tables[ttype]

    # -----------------------------------------------------------------------------

    def update_demography(self, status: Demography):
        death = status.death

        self._entities.difference_update(death)
        for table in self.tables.values():
            table.destroy_all(death)

        birth = filter(None, status.birth)
        for components in birth:
            self._entities.add(components[0].eid)
            for c in components:
                if c is None:
                    continue
                c.db = self
                ctype = c.type_id
                self.get_table(ctype).create(c)
