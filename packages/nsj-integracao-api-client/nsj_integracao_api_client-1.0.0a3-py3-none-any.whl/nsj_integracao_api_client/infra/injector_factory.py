import os
import importlib
import inspect
import sqlalchemy

from nsj_rest_lib.injector_factory_base import NsjInjectorFactoryBase
from nsj_rest_lib.dao.dao_base import DAOBase
from nsj_rest_lib.dto.dto_base import DTOBase, DTOFieldFilter
from nsj_rest_lib.descriptor.dto_field import DTOField
from nsj_rest_lib.descriptor.filter_operator import FilterOperator
from nsj_rest_lib.service.service_base import ServiceBase

from nsj_integracao_api_entidades.entity_registry import EntityRegistry

db_pool = None

class InjectorFactory(NsjInjectorFactoryBase):

    # _dtos: dict = {}
    # _entities: dict = {}
    _entity_registry = EntityRegistry()

    def __enter__(self):

        if db_pool is not None:
            pool = db_pool
        else:
            assert os.getenv("bd_user") and os.getenv("bd_senha") and \
                   os.getenv("bd_host") and os.getenv("bd_porta") and \
                   os.getenv("bd_nome"), "Variáveis de conexão não informadas"

            pool = sqlalchemy.create_engine(
                sqlalchemy.engine.URL.create(
                    "postgresql+pg8000",
                    username=os.getenv("bd_user"),
                    password=os.getenv("bd_senha", None),
                    host=os.getenv("bd_host", None),
                    port=os.getenv("bd_porta", None),
                    database=os.getenv("bd_nome", None)
                ),
                poolclass=sqlalchemy.pool.NullPool,
            )

        self._db_connection = pool.connect()

        return self

    def db_adapter(self):
        from nsj_gcf_utils.db_adapter2 import DBAdapter2

        return DBAdapter2(self._db_connection)

    def generic_dao(self, entity_class)-> DAOBase:
        return DAOBase(self.db_adapter(), entity_class)

    #treta de hoje - auto register
    def entity_for(self, entity_name: str):

        return self._entity_registry.entity_for(entity_name)

    def dto_for(self, entity_name: str, adiciona_filtros_data: bool = False):

        _classe : DTOBase = self._entity_registry.dto_for(entity_name)
        if _classe is None:
            raise KeyError(f"Não existe um DTO correpondente a tabela {entity_name}")

        if adiciona_filtros_data:
            # Adicionando campos de filtro no DTO
            _classe.field_filters_map['created_at'] = DTOFieldFilter('created_at', FilterOperator.GREATER_THAN)
            _classe.field_filters_map['created_at'].set_field_name('created_at')
            _classe.field_filters_map['lastupdate'] = DTOFieldFilter('lastupdate', FilterOperator.GREATER_THAN)
            _classe.field_filters_map['lastupdate'].set_field_name('lastupdate')

            if not 'created_at' in _classe.fields_map.keys():
                _classe.fields_map['created_at'] = DTOField()

            if not 'lastupdate' in _classe.fields_map.keys():
                _classe.fields_map['lastupdate'] = DTOField()

        return _classe

    def service_for(self, entity_name: str, adiciona_filtros_data: bool = False) -> ServiceBase:
        _entity_class = self.entity_for(entity_name)
        _dto_class = self.dto_for(entity_name, adiciona_filtros_data)
        _dto_response_class = _dto_class

        return ServiceBase(
            self,
            DAOBase(self.db_adapter(), _entity_class),
            _dto_class,
            _entity_class,
            _dto_response_class
        )

    # Customs
    def integracao_dao(self):
        from nsj_integracao_api_client.dao.integracao import IntegracaoDAO
        return IntegracaoDAO(self.db_adapter())
