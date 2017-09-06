# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

import codecs
from datetime import datetime

from evento import Evento
from lote import Lote
from .. import errors
from ..constantes import (
    TIPO_REGISTRO_HEADER_ARQUIVO,
    TIPO_REGISTRO_HEADER_LOTE,
    TIPO_REGISTRO_REGISTROS_INICIAIS_LOTE,
    TIPO_REGISTRO_DETALHE,
    TIPO_REGISTRO_TRAILER_LOTE,
    TIPO_REGISTRO_REGISTROS_FINAIS_LOTE,
    TIPO_REGISTRO_TRAILER_ARQUIVO,

    TIPO_OPERACAO_ARQUIVO_RETORNO,
    TIPO_OPERACAO_LANCAMENTO_CREDITO,
)


class Arquivo(object):

    def __init__(self, banco, **kwargs):
        """Arquivo Cnab240."""

        self._lotes = []
        self.banco = banco
        self.arquivo_remessa_retorno = None

        self.lote_aberto = None
        self.evento_aberto = None

        arquivo = kwargs.get('arquivo')
        if isinstance(arquivo, (file, codecs.StreamReaderWriter)):
            self.lote_aberto = None
            self.evento_aberto = None
            return self.carregar_arquivo(arquivo)

        self.header = self.banco.registros.HeaderArquivo(**kwargs)
        self.trailer = self.banco.registros.TrailerArquivo(**kwargs)
        self.trailer.totais_quantidade_lotes = 0
        self.trailer.totais_quantidade_registros = 2

        if self.header.arquivo_data_de_geracao is None:
            now = datetime.now()
            self.header.arquivo_data_de_geracao = int(now.strftime("%d%m%Y"))

        # necessario pois o santander nao tem hora de geracao
        try:
            if self.header.arquivo_hora_de_geracao is None:
                if now is None:
                    now = datetime.now()
                self.header.arquivo_hora_de_geracao = int(
                    now.strftime("%H%M%S"))
        except AttributeError:
            pass

    def _carrega_header_arquivo(self, linha):
        self.arquivo_remessa_retorno = linha[142]
        self.header = self.banco.registros.HeaderArquivo()
        self.header.carregar(linha)

        if __debug__ and self.header:
            #
            # Utilizando a saida do print, podemos debugar com facilidade
            # e também utilizar a saída para criar novos testes, quando
            # simulamos a importação de arquivos de clientes.
            #
            from pprint import pprint
            pprint("header_arquivo = ")
            pprint(self.header.todict())

    def _carrega_header_lote(self, linha):
        # self.lote_aberto = None
        self.lote_aberto = Lote(self.banco, linha=linha)
        self._lotes.append(self.lote_aberto)

        if __debug__ and self.lote_aberto:

            from pprint import pprint
            pprint("header_lote_{0} = ".format(
                self.lote_aberto.header.controle_lote
            ))
            pprint(self.lote_aberto.header.todict())

    def _carrega_registros_iniciais_lote(self):
        raise NotImplementedError

    def _carrega_registro_detalhe(self, linha):
        # codigo_evento = linha[9:13]
        codigo_evento = linha[15:17]
        Evento = self.lote_aberto.classe_evento
        segmento, abertura = Evento.carrega_segmento(self.banco, linha)

        if abertura:
            if __debug__ and self.evento_aberto:

                from pprint import pprint
                # TODO: Substituir este for por alguma função built-in dentro
                # de evento, para que o evento sempre mostre os campos de
                # todos os seus segmentos
                registro_debug = dict()
                for seg in self.evento_aberto._segmentos:
                    registro_debug.update(seg.todict())
                pprint("{0}_{1} = ".format(
                    self.evento_aberto._name,
                    self.evento_aberto.servico_numero_registro,

                ))
                pprint(registro_debug)

            self.evento_aberto = Evento(self.banco, int(codigo_evento))
            self.lote_aberto._eventos.append(self.evento_aberto)

        self.evento_aberto._segmentos.append(segmento)
        # self.lote_aberto.adicionar_evento(self.evento_aberto)
        # self.evento_aberto.adicionar_segmento(segmento)

    def _carrega_regitros_finais_lote(self):
        raise NotImplementedError

    def _carrega_trailer_lote(self, linha):
        # TODO: Verificar oque fazer com um arquivo com mais de um lote
        self.lote_aberto.trailer.carregar(linha)

        if __debug__ and self.lote_aberto:
            from pprint import pprint
            pprint("trailer_lote_{0} = ".format(
                self.lote_aberto.trailer.controle_lote
            ))
            pprint(self.lote_aberto.trailer.todict())

    def _carega_trailer_arquivo(self, linha):
        self.trailer = self.banco.registros.TrailerArquivo()
        self.trailer.carregar(linha)

        if __debug__ and self.trailer:
            from pprint import pprint
            pprint("trailer_arquivo = ")
            pprint(self.lote_aberto.trailer.todict())

    def carregar_arquivo(self, arquivo):

        for linha in arquivo:
            tipo_registro = linha[7]

            if tipo_registro == TIPO_REGISTRO_HEADER_ARQUIVO:
                self._carrega_header_arquivo(linha)
            elif tipo_registro == TIPO_REGISTRO_HEADER_LOTE:
                self._carrega_header_lote(linha)
            elif tipo_registro == TIPO_REGISTRO_REGISTROS_INICIAIS_LOTE:
                self._carrega_registros_iniciais_lote(linha)
            elif tipo_registro == TIPO_REGISTRO_DETALHE:
                self._carrega_registro_detalhe(linha)
            elif tipo_registro == TIPO_REGISTRO_REGISTROS_FINAIS_LOTE:
                self._carrega_regitros_finais_lote(linha)
            elif tipo_registro == TIPO_REGISTRO_TRAILER_LOTE:
                self._carrega_trailer_lote(linha)
            elif tipo_registro == TIPO_REGISTRO_TRAILER_ARQUIVO:
                self._carega_trailer_arquivo(linha)

    @property
    def lotes(self):
        return self._lotes

    def incluir_cobranca(self, **kwargs):
        # 1 eh o codigo de cobranca
        codigo_evento = 1
        evento = Evento(self.banco, codigo_evento)

        seg_p = self.banco.registros.SegmentoP(**kwargs)
        evento.adicionar_segmento(seg_p)

        seg_q = self.banco.registros.SegmentoQ(**kwargs)
        evento.adicionar_segmento(seg_q)

        seg_r = self.banco.registros.SegmentoR(**kwargs)
        if seg_r.necessario():
            evento.adicionar_segmento(seg_r)

        lote_cobranca = self.encontrar_lote(codigo_evento)

        if lote_cobranca is None:
            header = self.banco.registros.HeaderLoteCobranca(
                **self.header.todict()
            )
            trailer = self.banco.registros.TrailerLoteCobranca()
            lote_cobranca = Lote(self.banco, header, trailer)

            self.adicionar_lote(lote_cobranca)

            if header.controlecob_numero is None:
                header.controlecob_numero = int('{0}{1:02}'.format(
                    self.header.arquivo_sequencia,
                    lote_cobranca.codigo))

            if header.controlecob_data_gravacao is None:
                header.controlecob_data_gravacao = \
                    self.header.arquivo_data_de_geracao

        lote_cobranca.adicionar_evento(evento)
        # Incrementar numero de registros no trailer do arquivo
        self.trailer.totais_quantidade_registros += len(evento)

    def incluir_debito_pagamento(
            self, tipo_lote=30, seg_a=False, seg_b=False, **kwargs):
        # Codigo do movimento da remessa
        codigo_evento = kwargs.get('servico_codigo_movimento')
        evento = Evento(self.banco, codigo_evento)

        if not seg_a:
            seg_a = self.banco.registros.SegmentoA(**kwargs)
        evento.adicionar_segmento(seg_a)

        if not seg_b:
            seg_b = self.banco.registros.SegmentoB(**kwargs)
        evento.adicionar_segmento(seg_b)

        # seg_c = self.banco.registros.SegmentoC(**kwargs)
        # if seg_c.necessario():
        #     evento.adicionar_segmento(seg_c)

        lote_pagamento = self.encontrar_lote(tipo_lote)

        if lote_pagamento is None:
            header = self.banco.registros.HeaderLotePagamento(
                **self.header.todict()
            )
            trailer = self.banco.registros.TrailerLotePagamento()
            trailer.somatoria_valores = kwargs.get('credito_valor_pagamento')
            trailer.somatoria_quantidade_moedas = kwargs.get(
                'credito_moeda_quantidade')
            lote_pagamento = Lote(self.banco, header, trailer)

            self.adicionar_lote(lote_pagamento)
        else:
            # Lote ja existe mas esta vazio
            if not lote_pagamento.trailer.somatoria_valores:
                lote_pagamento.trailer.somatoria_valores = \
                    kwargs.get('credito_valor_pagamento')
                lote_pagamento.trailer.somatoria_quantidade_moedas = \
                    kwargs.get('credito_moeda_quantidade')
            else:
                lote_pagamento.trailer.somatoria_valores += \
                    kwargs.get('credito_valor_pagamento')
                lote_pagamento.trailer.somatoria_quantidade_moedas += \
                    kwargs.get('credito_moeda_quantidade')

        lote_pagamento.adicionar_evento(evento)
        # Incrementar numero de registros no trailer do arquivo
        self.trailer.totais_quantidade_registros += len(evento)

    def encontrar_lote(self, codigo_tipo_lote):
        for lote in self.lotes:
            if lote.header.servico_servico == codigo_tipo_lote:
                return lote

    def adicionar_lote(self, lote):
        if not isinstance(lote, Lote):
            raise TypeError('Objeto deve ser instancia de "Lote"')

        self._lotes.append(lote)
        lote.codigo = len(self._lotes)

        # Incrementar numero de lotes no trailer do arquivo
        self.trailer.totais_quantidade_lotes += 1

        # Incrementar numero de registros no trailer do arquivo
        self.trailer.totais_quantidade_registros += len(lote)

    def escrever(self, file_):
        file_.write(unicode(self).encode('ascii'))

    def __unicode__(self):
        if not self._lotes:
            raise errors.ArquivoVazioError()

        result = []
        result.append(unicode(self.header))
        result.extend(unicode(lote) for lote in self._lotes)
        result.append(unicode(self.trailer))
        # Adicionar elemento vazio para arquivo terminar com \r\n
        result.append(u'')
        return u'\r\n'.join(result)
