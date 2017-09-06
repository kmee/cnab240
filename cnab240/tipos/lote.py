# -*- encoding: utf8 -*-

from evento import Evento
from eventos import (
    cobranca,
    pagamento,
)
from .. import errors
from ..constantes import (

    TIPO_OPERACAO_LANCAMENTO_CREDITO,
    TIPO_OPERACAO_LANCAMENTO_DEBITO,
    TIPO_OPERACAO_EXTRATO_CONCILIACAO,
    TIPO_OPERACAO_GESTAO_DE_CAIXA,
    TIPO_OPERACAO_INFORMACOES_TITULOS_CAPTURADOS_PROPRIO_BANCO,
    TIPO_OPERACAO_ARQUIVO_REMESSA,
    TIPO_OPERACAO_ARQUIVO_RETORNO,
    TIPO_SERVICO_PAGAMENTO_SALARIOS,
    TIPO_SERVICO_COBRANCA,
)


class Lote(object):

    def __init__(self, banco, header=None, trailer=None, linha=None):

        self.banco = banco
        self.header = header
        self.trailer = trailer
        self._codigo = None
        self.classe_evento = None
        if linha:
            tipo_registro = linha[7]
            if not tipo_registro == '1':
                raise NotImplementedError
            self.carrega_lote(linha)

        self.trailer.quantidade_registros = 2
        self._eventos = []

    def carrega_lote(self, linha):

        tipo_operacao = linha[8]
        tipo_servico = linha[9:11]
        if tipo_operacao == TIPO_OPERACAO_LANCAMENTO_CREDITO:
            self.header = self.banco.registros.HeaderLotePagamento()
            self.header.carregar(linha)
            self.trailer = self.banco.registros.TrailerLotePagamento()
            if tipo_servico in (
                    TIPO_SERVICO_PAGAMENTO_SALARIOS,
            ):
                self.classe_evento = pagamento.Pagamento
            elif tipo_servico in ():
                self.classe_evento = pagamento.Titulos
            elif tipo_servico in ():
                self.classe_evento = pagamento.Tributos
            else:
                raise NotImplementedError
        elif tipo_operacao == TIPO_OPERACAO_LANCAMENTO_DEBITO:
            raise NotImplementedError
        elif tipo_operacao == TIPO_OPERACAO_EXTRATO_CONCILIACAO:
            raise NotImplementedError
        elif tipo_operacao == TIPO_OPERACAO_GESTAO_DE_CAIXA:
            raise NotImplementedError
        elif tipo_operacao == \
                TIPO_OPERACAO_INFORMACOES_TITULOS_CAPTURADOS_PROPRIO_BANCO:
            raise NotImplementedError
        elif tipo_operacao == TIPO_OPERACAO_ARQUIVO_REMESSA:
            raise NotImplementedError
        elif tipo_operacao == TIPO_OPERACAO_ARQUIVO_RETORNO:

            self.header = self.banco.registros.HeaderLoteCobranca()
            self.header.carregar(linha)
            self.trailer = self.banco.registros.TrailerLoteCobranca()

            if tipo_servico == TIPO_SERVICO_COBRANCA:
                self.classe_evento = cobranca.Cobranca
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError

    @property
    def codigo(self):
        return self._codigo

    @codigo.setter
    def codigo(self, valor):
        self._codigo = valor
        if self.header is not None:
            self.header.controle_lote = valor
        if self.trailer is not None:
            self.trailer.controle_lote = valor
        self.atualizar_codigo_eventos()

    def atualizar_codigo_eventos(self):
        for evento in self._eventos:
            evento.codigo_lote = self._codigo

    def atualizar_codigo_registros(self):
        last_id = 0
        for evento in self._eventos:
            last_id = evento.atualizar_codigo_registros(last_id)

    @property
    def eventos(self):
        return self._eventos

    def adicionar_evento(self, evento):
        if not isinstance(evento, Evento):
            raise TypeError

        self._eventos.append(evento)
        if self.trailer is not None and \
                hasattr(self.trailer, 'quantidade_registros'):

            self.trailer.quantidade_registros += len(evento)
        self.atualizar_codigo_registros()

        if self._codigo:
            self.atualizar_codigo_eventos()

    def __unicode__(self):
        if not self._eventos:
            raise errors.NenhumEventoError()

        result = []
        if self.header is not None:
            result.append(unicode(self.header))
        result.extend(unicode(evento) for evento in self._eventos)
        if self.trailer is not None:
            result.append(unicode(self.trailer))
        return '\r\n'.join(result)

    def __len__(self):
        if self.trailer is not None and \
                hasattr(self.trailer, 'quantidade_registros'):
            return self.trailer.quantidade_registros
        else:
            return len(self._eventos)
