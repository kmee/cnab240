# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals

from ..evento import Evento


class Pagamento(Evento):

    _name = 'pagamento'

    @staticmethod
    def carrega_segmento(banco, linha):
        codigo_segmento = linha[13]
        abertura = False

        if codigo_segmento == 'A':
            segmento = banco.registros.SegmentoA()
            abertura = True
        elif codigo_segmento == 'B':
            segmento = banco.registros.SegmentoB()
        elif codigo_segmento == 'C':
            segmento = banco.registros.SegmentoC()
        else:
            raise NotImplementedError

        segmento.carregar(linha)
        return segmento, abertura


class Titulos(Evento):

    _name = 'pagamento_titulos'

    @staticmethod
    def carrega_segmento(banco, linha):

        raise NotImplementedError

        codigo_segmento = linha[13]
        abertura = False
        if codigo_segmento == 'J':
            segmento = banco.registros.SegmentoJ(**args)

        segmento.carregar(linha)
        return segmento, abertura


class Tributos(Evento):

    _name = 'pagamento_tributos'

    @staticmethod
    def carrega_segmento(banco, linha):
        raise NotImplementedError

        codigo_segmento = linha[13]
        abertura = False
        if codigo_segmento == 'O':
            segmento = banco.registros.SegmentoO(**args)

        segmento.carregar(linha)
        return segmento, abertura
