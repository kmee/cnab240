# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from ..evento import Evento


class Cobranca(Evento):

    _name = 'cobranca'

    @staticmethod
    def carrega_segmento(banco, linha):

        codigo_segmento = linha[13]
        abertura = False

        if codigo_segmento == 'P':
            abertura = True
            segmento = banco.registros.SegmentoO()
        elif codigo_segmento == 'Q':
            segmento = banco.registros.SegmentoQ()
        elif codigo_segmento == 'R':
            segmento = banco.registros.SegmentoR()
        #
        # Retorno de cobrança
        #
        elif codigo_segmento == 'T':
            abertura = True
            segmento = banco.registros.SegmentoT()
        elif codigo_segmento == 'U':
            segmento = banco.registros.SegmentoU()
        else:
            raise NotImplementedError

        segmento.carregar(linha)
        return segmento, abertura
