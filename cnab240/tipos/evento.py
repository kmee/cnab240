# -*- coding: utf-8 -*-

from __future__ import division, print_function, unicode_literals


class Evento(object):

    def __init__(self, banco, codigo_evento):
        self._segmentos = []
        self.banco = banco
        self.codigo_evento = codigo_evento
        self._codigo_lote = None

    def adicionar_segmento(self, segmento):
        self._segmentos.append(segmento)
        for segmento in self._segmentos:
            segmento.servico_codigo_movimento = self.codigo_evento

    @property
    def segmentos(self):
        return self._segmentos

    def __getattribute__(self, name):
        for segmento in object.__getattribute__(self, '_segmentos'):
            if hasattr(segmento, name):
                return getattr(segmento, name)
        return object.__getattribute__(self, name)

    def __unicode__(self):
        return u'\r\n'.join(unicode(seg) for seg in self._segmentos)

    def __len__(self):
        return len(self._segmentos)

    @property
    def codigo_lote(self):
        return self._codigo_lote

    @codigo_lote.setter
    def codigo_lote(self, valor):
        self._codigo_lote = valor
        for segmento in self._segmentos:
            segmento.controle_lote = valor

    def atualizar_codigo_registros(self, last_id):
        current_id = last_id
        for segmento in self._segmentos:
            current_id += 1
            segmento.servico_numero_registro = current_id
        return current_id
