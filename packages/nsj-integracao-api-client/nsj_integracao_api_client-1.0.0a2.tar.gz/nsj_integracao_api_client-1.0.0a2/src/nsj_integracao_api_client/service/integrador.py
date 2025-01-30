import hashlib

import base64

import datetime

from typing import List, Dict

import requests

from nsj_gcf_utils.json_util import convert_to_dumps, json_loads

from nsj_integracao_api_client.infra.injector_factory import InjectorFactory

from nsj_rest_lib.dto.dto_base import DTOBase

#nsj_integracao_api_client

entidades_integracao: List[str] = [
    # --- Dimensoes ---
    'ns.gruposempresariais',
    'ns.empresas',
    'ns.estabelecimentos',
    'ns.configuracoes',
    'financas.bancos',
    #'financas.agencias', 'financas.bancos'
    'persona.faixas',
    #'persona.itensfaixas','persona.faixas'
    'ns.obras',
    'ns.feriados',
    'persona.instituicoes',
    'persona.eventos',
    'persona.tiposdocumentoscolaboradores',
    'persona.tiposhistoricos',
    'persona.tiposanexos',
    'ponto.regras',# ns.empresas
    'persona.processos',
    #'persona.processosrubricas',persona.processos
    'persona.lotacoes',
    'persona.ambientes',
    'persona.condicoesambientestrabalho',
    'persona.departamentos',
    'persona.funcoes',
    'persona.jornadas',
    'persona.horarios',
    'persona.horariosespeciais',
    'persona.sindicatos',
    'persona.cargos',
    'persona.niveiscargos',
    'persona.tiposfuncionarios',
    'persona.trabalhadores',
    'persona.dependentestrabalhadores',
    #'persona.horariosalternativostrabalhadores', persona.trabalhadores
    'persona.escalasfolgastrabalhadores',
    'persona.beneficios',
    'persona.concessionariasvts',
    #'persona.tarifasconcessionariasvts', 'persona.concessionariasvts'
    'persona.tarifasconcessionariasvtstrabalhadores',
    'persona.configuracoesordemcalculomovimentos',
    'persona.configuracoesordemcalculomovimentosponto',
    #'persona.gestorestrabalhadores',persona.trabalhadores
    'persona.historicos',
    'persona.medicos',
    'persona.rubricasponto',
    'persona.rubricasapontamento',
    #Fatos
    #'persona.avisospreviostrabalhadores',persona.trabalhadores
    'persona.compromissostrabalhadores',
    'persona.convocacoestrabalhadores',
    'persona.dispensavalestransportestrabalhadores',
    'persona.emprestimostrabalhadores',
    'persona.historicosadiantamentosavulsos',
    'persona.adiantamentosavulsos',
    'persona.membroscipa',
    #'persona.outrosrecebimentostrabalhadores',persona.trabalhadores
    #'persona.processossuspensoes',persona.processos
    'persona.reajustessindicatos',
    'persona.reajustestrabalhadores',
    'ponto.compensacoeslancamentos',
    'ponto.pagamentoslancamentos',
    #'ponto.pendenciascalculostrabalhadores',persona.trabalhadores
    'persona.admissoespreliminares',
    'persona.avisosferiastrabalhadores',
    'persona.pendenciaspagamentos',
    'persona.documentoscolaboradores',
    'persona.faltastrabalhadores',
    #'persona.intervalosjornadas', persona.jornadas
    'persona.mudancastrabalhadores',
    #'persona.valestransportespersonalizadostrabalhadores',persona.trabalhadores
    'ponto.diascompensacoestrabalhadores',
    'persona.afastamentostrabalhadores',
    #'persona.outrosrendimentostrabalhadores',persona.trabalhadores
    'ponto.atrasosentradascompensaveistrabalhadores',
    'ponto.saidasantecipadascompensaveistrabalhadores',
    'persona.beneficiostrabalhadores',
    'persona.movimentosponto',
    'persona.movimentos',
    'persona.calculostrabalhadores'
]

TAMANHO_PAGINA: int = 100

_entidades_particionadas_por_grupo = ['ns.empresas', 'ns.configuracoes']

_entidades_particionadas_por_empresa = [
    'ns.configuracoes',
    'persona.movimentosponto',
    'ns.estabelecimentos',
    'persona.trabalhadores',
    'persona.processos',
    'persona.jornadas',
    'persona.ambientes',
    'persona.funcoes',
    'persona.cargos',
    #'persona.beneficios',#'persona.lotacoes'Removido pois existem entidades dependentes que não são são particionadas (persona.beneficiostrabalhadores)
    'persona.configuracoesordemcalculomovimentos',
    'persona.configuracoesordemcalculomovimentosponto',
    'persona.membroscipa',
    'persona.movimentos',
    'persona.rubricasponto',
    'persona.condicoesambientestrabalho',
    'persona.tiposfuncionarios',
    'persona.horarios',
    'persona.admissoespreliminares',
    'persona.eventos',
    #'persona.lotacoes'Removido pois existem entidades dependentes que não são são particionadas (persona.beneficiostrabalhadores)
]

_entidades_particionadas_por_estabelecimento = [
    'ns.configuracoes',
    'ns.obras',
    'persona.movimentosponto',
    'persona.trabalhadores',
    'ns.configuracoes',
    'persona.processos',
    'persona.jornadas',
    'persona.ambientes',
    'persona.funcoes',
    'persona.cargos',
    #'persona.beneficios',#'persona.lotacoes'Removido pois existem entidades dependentes que não são são particionadas (persona.beneficiostrabalhadores)
    'persona.configuracoesordemcalculomovimentos',
    'persona.configuracoesordemcalculomovimentosponto',
    'persona.membroscipa',
    'persona.movimentos',
    'persona.rubricasponto',
    'persona.condicoesambientestrabalho',
    'persona.tiposfuncionarios',
    'persona.horarios',
    'persona.admissoespreliminares',
    'persona.eventos',
    #'persona.lotacoes' Removido pois existem entidades dependentes que não são são particionadas (persona.beneficiostrabalhadores)
]

class IntegradorService():
    _injector : InjectorFactory
    _api_key: str = None
    _tenant: int = None
    _dao_intg: 'IntegracaoDAO'
    _filtros_particionamento: list = None


    def __init__(self, injector: InjectorFactory, log):
        self._injector = injector
        self._log = log
        self._dao_intg = None


    def _fields_to_load(self, dto_class) -> dict:

        fields = {}
        fields.setdefault("root", set(dto_class.fields_map.keys()))

        for _related_entity, _related_list_fields in dto_class.list_fields_map.items():
            fields["root"].add(_related_entity)
            fields.setdefault(_related_entity, set())
            _related_fields = _related_list_fields.dto_type.fields_map.keys()
            for _related_field in _related_fields:
                fields["root"].add(f"{_related_entity}.{_related_field}")
                fields[_related_entity].add(_related_field)

        return fields


    def _integracao_dao(self):
        if self._dao_intg is None:
            self._dao_intg = self._injector.integracao_dao()
        return self._dao_intg


    def _url_base(self) -> str:
        return "http://localhost:5000/integracao-pessoas-api/66"


    def _url_diretorio(self) -> str:
        return "https://dir.nasajon.dev"


    def _decode_token(self, token):
        data = token.split('.')[1]
        padding = '=' * (4 - len(data) % 4)
        str_token = base64.b64decode(data + padding).decode('utf-8')
        return  json_loads(str_token)


    @property
    def api_key(self):

        if self._api_key is None:
            self._api_key = self._integracao_dao().recuperar_token()

        return self._api_key


    @property
    def tenant(self):

        if self._tenant is None:
            decoded_token = self._decode_token(self.api_key)
            self._tenant = decoded_token["tenant_id"]

        return self._tenant


    def _enviar_dados(self, dict_data, acao):
        """
        """
        s = requests.Session()
        s.headers.update({'Content-Type':'application/json','X-api-key': self.api_key})
        response = s.put(f'{self._url_base()}/{acao}?upsert=true', json=convert_to_dumps(dict_data))

        if response.status_code < 200 or response.status_code > 299:
            if 'application/json' in response.headers.get('Content-Type', ''):
                _json_response = response.json()
                _message = _json_response[0]['message'] if 'message' in _json_response[0] else ''
            else:
                _message = response.text
            raise Exception(f"""Erro ao enviar dados ao servidor:
            Endpoint: {response.url}
            Status: {response.status_code} - {response.reason}
            Mensagem: {_message}""",convert_to_dumps(dict_data))


    def _apagar_dados(self, dict_data, acao):
        """
        """
        s = requests.Session()
        s.headers.update({'Content-Type':'application/json','X-api-key': self.api_key})
        response = s.delete(f'{self._url_base()}/{acao}?tenant={self.tenant}', json=convert_to_dumps(dict_data))

        if response.status_code < 200 or response.status_code > 299:
            if 'application/json' in response.headers.get('Content-Type', ''):
                _json_response = response.json()
                _message = _json_response[0]['message'] if 'message' in _json_response[0] else ''
            else:
                _message = response.text
            raise Exception(f"""Erro ao apagar dados ao servidor:
            Endpoint: {response.url}
            Status: {response.status_code} - {response.reason}
            Mensagem: {_message}""")


    def _gerar_token_tenant(self, chave_ativacao: str) -> str:
        s = requests.Session()
        s.headers.update({'Content-Type':'application/x-www-form-urlencoded'})
        response = s.post(
            f'{self._url_diretorio()}/v2/api/gerar_token_ativacao_sincronia/',
            data={"codigo_ativacao": chave_ativacao})

        if response.status_code == 200:
            return response.json()["apikey"]

        if response.status_code < 200 or response.status_code > 299:
            if 'application/json' in response.headers.get('Content-Type', ''):
                _json_response = response.json()
                _message = _json_response['message'] if 'message' in _json_response else ''
            else:
                _message = response.text
            raise Exception(f"""Erro ao enviar dados ao servidor:
            Endpoint: {response.url}
            Status: {response.status_code} - {response.reason}
            Mensagem: {_message}""")


    def consultar_integridade_de(self, acao: str, filtros: dict, detalhar_diferencas: bool):

        filtros_str = None
        if filtros:
            filtros_str = ("&".join(
                [ f"{_chave}={filtros[_chave]}" for _chave in filtros.keys() ]
            ))

        s = requests.Session()
        s.headers.update({'Content-Type':'application/json','X-api-key': self.api_key})
        _url = (
            f'{self._url_base()}/{acao}/verificacao-integridade?tenant={self.tenant}&source={detalhar_diferencas}'
            f'{"&" + filtros_str if filtros_str else ""}'
        )
        response = s.get(_url)
        response_content = response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.text

        if response.status_code < 200 or response.status_code > 299:
            if isinstance(response_content, dict):
                _message = response_content.get('message', '')
            else:
                _message = response_content
            raise Exception(f"""Erro ao consultar a integridade no servidor:
            Endpoint: {response.url}
            Status: {response.status_code} - {response.reason}
            Mensagem: {_message}""")
        return response_content


    def _integracao_foi_configurada(self):
        return self._integracao_dao().integracao_configurada()


    def _validar_grupos_empresariais(self, grupos) -> List[Dict[str, str]]:

        grupos_cadastrados = self._integracao_dao().listar_grupos_empresariais(grupos)
        _cods = [grupo['codigo'] for grupo in grupos_cadastrados]
        _grupos_faltantes = [grupo for grupo in grupos if grupo not in _cods]
        assert len(_grupos_faltantes)==0, f"Grupo(s) '{','.join(_grupos_faltantes)}' não encontrado(s)."
        return grupos_cadastrados


    def executar_instalacao(self, chave_ativacao: str, grupos: List[str]):

        assert chave_ativacao, "Chave de ativação não pode ser vazia."
        self._log.mensagem(f"Executando instalação com a chave de ativação: {chave_ativacao}")

        assert not self._integracao_foi_configurada(), "Integração já instalada anteriormente."
        _token: str = self._gerar_token_tenant(chave_ativacao)

        decoded_token = json_loads(base64.b64decode(_token.split('.')[1]).decode('utf-8'))

        if grupos:
            grupos_cadastrados = self._validar_grupos_empresariais(grupos)
        else:
            grupos_cadastrados = self._integracao_dao().listar_grupos_empresariais()

        _ids  = [str(grupo['grupoempresarial']) for grupo in grupos_cadastrados]

        self._integracao_dao().registrar_grupos_empresariais(_ids)

        self._integracao_dao().registra_token_tenant(_token)

        self._log.mensagem(f"Instalação efetuada com sucesso para o tenant '{decoded_token['tenant_id']}'.")


    def ativar_grupos_empresariais(self, grupos: List[str]):

        assert self._integracao_foi_configurada(), "Integração não configurada!"
        assert grupos, "Grupos não podem ser vazios!"

        if grupos:
            grupos_cadastrados = self._validar_grupos_empresariais(grupos)
        else:
            grupos_cadastrados = self._integracao_dao().listar_grupos_empresariais()

        _ids  = [grupo['grupoempresarial'] for grupo in grupos_cadastrados]

        self._integracao_dao().registrar_grupos_empresariais(_ids)

        self._log.mensagem(f"Grupos empresariais ativados: '{','.join(grupos)}'.")


    def desativar_grupos_empresariais(self, grupos: List[str]):

        assert self._integracao_foi_configurada(), "Integração não configurada!"
        assert grupos, "Grupos não podem ser vazios!"

        grupos_cadastrados = self._validar_grupos_empresariais(grupos)

        _ids  = [grupo['grupoempresarial'] for grupo in grupos_cadastrados]

        self._integracao_dao().desativar_grupos_empresariais(_ids)

        self._log.mensagem(f"Grupos empresariais desativados: '{','.join(grupos)}'.")


    def _filtro_particionamento_de(self, entidade: str):

        if self._filtros_particionamento is None:
            _dados_part = self._integracao_dao().listar_dados_particionamento()

            self._filtros_particionamento = [
                {'grupoempresarial' : ",".join(list(map(lambda i: str(i["grupoempresarial"]), _dados_part)))},
                {'empresa' : ",".join(list(map(lambda i: str(i["empresa"]), _dados_part)))},
                {'estabelecimento' : ",".join(list(map(lambda i: str(i["estabelecimento"]), _dados_part)))}
            ]

        if entidade in _entidades_particionadas_por_grupo:
            return  self._filtros_particionamento[0]

        if entidade in _entidades_particionadas_por_empresa:
            return self._filtros_particionamento[1]

        if entidade in _entidades_particionadas_por_estabelecimento:
            return self._filtros_particionamento[2]


    def _dto_to_api(
        self,
        campos: Dict[str, List[str]],
        data: List[DTOBase]
    ) -> List[dict]:
        # Converte os objetos DTO para dicionários e adiciona o tenant
        transformed_data = []
        for dto in data:
            dto.tenant = self.tenant
            dto_dict = dto.convert_to_dict(campos)
            if "created_by" in dto_dict and not dto_dict["created_by"] is None:
                dto_dict["created_by"] = {"id": dto_dict["created_by"]}
            transformed_data.append(dto_dict)

        return transformed_data


    def executar_carga_inicial(self):

        assert self._integracao_foi_configurada(), "Integração não configurada!"

        _dao = self._integracao_dao()

        self._log.mensagem(f"{len(entidades_integracao)} entidades para processar.")

        for entidade in entidades_integracao:

            _idx = entidades_integracao.index(entidade) + 1
            self._log.mensagem(f"Integrando {entidade}, {_idx} de {len(entidades_integracao)}.")

            # Carregar dados paginados para integrar
            service = self._injector.service_for(entidade, True)
            current_after = None
            fields = self._fields_to_load(service._dto_class)
            filters = self._filtro_particionamento_de(entidade)
            search_query = None

            while True:
                data = service.list(
                        current_after,
                        TAMANHO_PAGINA,
                        fields,
                        None,
                        filters,
                        search_query=search_query,
                    )

                if len(data)==0:
                    if current_after is None:
                        self._log.mensagem("Sem dados para transferir, indo adiante...")
                    else:
                        self._log.mensagem("Entidade integrada com sucesso.")
                    break

                dict_data = self._dto_to_api(fields, data)

                # Mandar a bagatela por apis
                _acao = entidade.split('.')[1]

                # Mandar a bagatela por apis
                self._enviar_dados(dict_data, entidade.split('.')[1])

                # Aponta a leitura para a próxima página
                _last = data[-1]
                current_after = getattr(_last, _last.pk_field)

            _dao.atualiza_ultima_integracao(entidade)


    def executar_integracao(self):

        assert self._integracao_foi_configurada(), "Integração não configurada!"

        _dao = self._integracao_dao()

        entidades_pendentes = _dao.listar_entidades_pendentes_integracao()

        entidades_pendentes = {entidade: entidades_pendentes[entidade] for entidade in entidades_integracao if entidade in entidades_pendentes.keys()}

        self._log.mensagem(f"{len(entidades_pendentes)} entidades para processar." if entidades_pendentes else "Nenhuma entidade para processar.")

        for entidade, data_ultima_integracao in entidades_pendentes.items():

            _idx = list(entidades_pendentes.keys()).index(entidade) + 1
            self._log.mensagem(f"Integrando {entidade}, {_idx} de {len(entidades_pendentes)}.")

            # Carregar dados paginados para integrar
            service = self._injector.service_for(entidade, True)
            current_after = None
            fields = self._fields_to_load(service._dto_class) #tornar publico
            filters = self._filtro_particionamento_de(entidade)
            search_query = None
            _acao = entidade.split('.')[1]

            # Dados criados apos data_ultima_integracao
            filtro_criacao = filters.copy() if filters else {}
            filtro_criacao['created_at'] = data_ultima_integracao
            while True:

                data = service.list(
                        current_after,
                        TAMANHO_PAGINA,
                        fields,
                        None,
                        filtro_criacao,
                        search_query=search_query,
                    )

                if len(data)==0:
                    self._log.mensagem("Sem dados para transferir, indo adiante...")
                    break

                # Convertendo para o formato de dicionário (permitindo omitir campos do DTO) e add tenant
                dict_data = self._dto_to_api(fields, data)

                # Mandar a bagatela por apis
                self._enviar_dados(dict_data, _acao)

                # Aponta a leitura para a próxima página
                _last = data[-1]
                current_after = getattr(_last, _last.pk_field)

            # Dados alterados apos data_ultima_integracao
            filtro_atualizacao = filters.copy() if filters else {}
            filtro_atualizacao['atualizado_apos'] = data_ultima_integracao
            while True:

                data = service.list(
                        current_after,
                        TAMANHO_PAGINA,
                        fields,
                        None,
                        filtro_atualizacao,
                        search_query=search_query,
                    )

                if len(data)==0:
                    self._log.mensagem("Sem dados para transferir, indo adiante...")
                    break

                # Convertendo para o formato de dicionário (permitindo omitir campos do DTO) e add tenant
                dict_data = self._dto_to_api(fields, data)

                # Mandar a bagatela por apis
                self._enviar_dados(dict_data, _acao)

                # Aponta a leitura para a próxima página
                _last = data[-1]
                current_after = getattr(_last, _last.pk_field)

            # Dados excluidos apos data_ultima_integracao
            _coluna_id = service._dto_class.fields_map[service._dto_class.pk_field].entity_field
            para_apagar = _dao.listar_dados_exclusao(_coluna_id, entidade, data_ultima_integracao)
            if para_apagar:
                print("Excluindo dados")
                self._apagar_dados(para_apagar, _acao)

            _dao.atualiza_ultima_integracao(entidade)


    def integrity_fields(self, dto) -> dict:
        fields = {}
        fields["root"] = {field for field in dto.fields_map.keys() if not field in ["tenant", "lastupdate"]}

        for _related_entity, _related_list_fields in dto.list_fields_map.items():
            fields["root"].add(_related_entity)
            fields.setdefault(_related_entity, set())
            _related_fields = _related_list_fields.dto_type.fields_map.keys()
            for _related_field in _related_fields:
                if not _related_field in ["tenant", "lastupdate"]:
                    fields["root"].add(f"{_related_entity}.{_related_field}")
                    fields[_related_entity].add(_related_field)

        return fields

    def tratar_campos_comparacao(self, dados: dict, campos_ignorados: list):

        keys_to_delete = []
        for chave, valor in dados.items():

            # Remove timezone para comparação
            if isinstance(valor, (datetime.datetime, datetime.date)):
                dados[chave] = valor.replace(microsecond=0, tzinfo=None)

            # Ignora campos não úteis
            if chave in campos_ignorados:
                keys_to_delete.append(chave)

            # Aplica regras em sublistas
            if isinstance(valor, list):
                for item in valor:
                    self.tratar_campos_comparacao(item, campos_ignorados)

        for chave in keys_to_delete:
            del dados[chave]


    def converte_dados_para_hash(self, dto, integrity_fields):

        data = dto.convert_to_dict(integrity_fields)

        self.tratar_campos_comparacao(data, ["tenant", "lastupdate"])

        concatenated_valors = ''.join(
            str(data[chave]) for chave in sorted(data.keys())
        )

        data['tenant'] = self.tenant

        return {
            'id': str(data[dto.pk_field]),
            'hash': hashlib.sha256(concatenated_valors.encode('utf-8')).hexdigest(),
            '_source': data,
            '_source_hash': concatenated_valors
        }


    def comparar_dados(self, dados_referencia, dados_comparacao):

        if dados_referencia['campos']['_'] != dados_comparacao['campos']['_']:
            print(f"\033[91mExistem diferenças entre os campos comparados:\r\n\r\nLocal: {dados_referencia['campos']['_']}\r\n\r\nWeb  : {dados_comparacao['campos']['_']}\033[0m")

        if dados_referencia['registros'] != dados_comparacao['registros']:
            print(f"\033[91mExistem diferenças nas quantidades de dados:\r\n\r\nLocal: {dados_referencia['registros']}\r\n\r\nWeb  : {dados_comparacao['registros']}\033[0m")

        # Índices para facilitar busca por ID
        idx_referencia = {item['id']: item for item in dados_referencia['dados']}
        idx_comparacao = {item['id']: item for item in dados_comparacao['dados']}

        # Inicializar listas de mudanças
        _criar = []
        _atualizar = []
        _excluir = []
        _diff = {}

        # Verificar itens nos dados de referência
        for item_id, item_ref in idx_referencia.items():
            if item_id not in idx_comparacao:
                # Criar se não existe nos dados de comparação
                _criar.append(item_ref['_source'])
            elif item_ref['hash'] != idx_comparacao[item_id]['hash']:
                # Atualizar se o hash é diferente
                _atualizar.append(item_ref['_source'])
                # Adiciona para exibir os dados pueros se disponível
                if '_source' in idx_comparacao[item_id]:
                    _diff[item_ref['_source_hash']] = idx_comparacao[item_id]['_source']

        # Verificar itens nos dados de comparação
        for item_id in idx_comparacao.keys():
            if item_id not in idx_referencia:
                # Excluir se não existe em A
                _excluir.append(idx_comparacao[item_id]['id'])

        return _criar, _atualizar, _excluir, _diff


    def executar_verificacao_integridade(
        self,
        parar_caso_diferencas : bool = False,
        detalhar_diferencas: bool = False,
        corrigir_auto: bool = False,
        tenant: int = 0
    ):

        assert self._integracao_foi_configurada(), "Integração não configurada!"
        if corrigir_auto:
            assert self.tenant==tenant, "Tenant informado para correção não é igual ao configurado"

        _dao = self._integracao_dao()

        self._log.mensagem(f"{len(entidades_integracao)} entidades para verificar integridade.")

        _diferencas = False
        _idx = 0
        for entidade in reversed(entidades_integracao):

            _idx += 1
            self._log.mensagem(f"Verificando integridade {entidade}, {_idx} de {len(entidades_integracao)}.")

            # Carregar dados paginados para integrar
            service = self._injector.service_for(entidade, False)

            _count = 0
            current_after = None
            fields = self._fields_to_load(service._dto_class)
            filters = self._filtro_particionamento_de(entidade)
            search_query = None
            _integrity_fields = self.integrity_fields(service._dto_class)
            _dados_locais = []

            while True:

                _data = service.list(
                        current_after,
                        TAMANHO_PAGINA,
                        fields,
                        None,
                        filters,
                        search_query=search_query,
                    )

                _count = _count + len(_data)

                if len(_data)==0:
                    break

                # Aponta a leitura para a próxima página
                _last = _data[-1]
                current_after = getattr(_last, _last.pk_field)

                # Convertendo para o formato de dicionário (permitindo omitir campos do DTO) e add tenant
                while _data:
                    dto = _data.pop(0)
                    _dados_locais.append(self.converte_dados_para_hash(dto, _integrity_fields))


            _dados_locais = {
                'registros' : _count,
                'campos': {
                    "_": ",".join(sorted(_integrity_fields['root'])),
                },
                'dados': _dados_locais
            }

            # captura os dados de integridade da entidade
            _acao = entidade.split('.')[1]
            _dados_remotos = self.consultar_integridade_de(_acao, filters, detalhar_diferencas)

            # Compara os dados e obtem o que se deve fazer
            para_criar, para_atualizar, para_apagar, _diff = self.comparar_dados(_dados_locais, _dados_remotos)

            if para_criar:
                print(f"\r\nPara criar -> {len(para_criar)}\r\n")
                if corrigir_auto:
                    print(f"\r\nCriando dados em {entidade}.\r\n")
                    self._enviar_dados(para_criar, _acao)

            if para_atualizar:
                print(f"\r\nPara atualizar -> {len(para_atualizar)}\r\n")
                if _diff:
                    for _chave, _valor in _diff.items():
                        print(f"\r\n{_chave}<=>{_valor}\r\n")
                if corrigir_auto:
                    print(f"\r\nAtualizando dados em {entidade}.\r\n")
                    self._enviar_dados(para_atualizar, _acao)

            if para_apagar:
                print(f"\r\nPara apagar -> {len(para_apagar)}\r\n")
                if corrigir_auto:
                    print(f"\r\nRemovendo dados em {entidade}.\r\n")
                    self._apagar_dados(para_apagar, _acao)

            if not _diferencas:
                _diferencas = para_criar or para_atualizar or para_apagar

            if parar_caso_diferencas and (para_criar or para_atualizar or para_apagar) and not corrigir_auto:
                break

        if _diferencas:
            print("\033[93mOcorreram diferenças na checagem da integridade, verifique a saída.\033[0m")

        if not _diferencas:
            print("\033[92mVerificação finalizada sem diferenças!\033[0m")


