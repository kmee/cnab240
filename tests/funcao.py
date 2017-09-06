
from decimal import Decimal

def get_dict_from_line(line, tipo):
    """
    Dado o registro de um segmento do CNAB, retornar o dict para montar 
    os exemplos para teste 
    """

    if tipo == 'A':
        segmento = {
            # SEGMENTO A
            # CONTROLE
            # 01.3A
            'controle_banco': line[0:3],
            # 02.3A
            'controle_lote': line[3:7],
            # 03.3A -  3-Registros Iniciais do Lote
            'controle_registro': line[7],

            # SERVICO
            # 04.3A - Numero Sequencial do Registro -
            # Inicia em 1 em cada novo lote
            'servico_numero_registro': line[8:13],
            # 05.3A
            #   Segmento Codigo de Segmento do Reg.Detalhe line[13]
            # 06.3A
            'servico_tipo_movimento': line[14],
            # 07.3A 00 - Inclusao de registros
            'servico_codigo_movimento': line[15:17],

            # FAVORECIDO
            # 08.3A - 018-TED 700-DOC
            'favorecido_camara': 0,
            # 09.3A
            'favorecido_banco': 1,
            # 10.3A
            'favorecido_agencia': line[23:28],
            # 11.3A
            'favorecido_agencia_dv': line[28],
            # 12.3A
            'favorecido_conta': line[29:41],
            # 13.3A
            'favorecido_conta_dv': line[41],
            # 14.3A
            'favorecido_dv': line[42],
            # 15.3A
            'favorecido_nome': line[43:73],

            # CREDITO
            # 16.3A -
            'credito_seu_numero': line[73:93],
            # 17.3A
            'credito_data_pagamento': line[93:101],
            # 18.3A
            'credito_moeda_tipo': line[101:104],
            # 19.3A
            'credito_moeda_quantidade': Decimal('0.00000'),
            # 20.3A
            'credito_valor_pagamento': line[121:134],
            # 21.3A
            # 'credito_noso_numero': '',
            # 22.3A
            # 'credito_data_real': '',
            # 23.3A
            # 'credito_valor_real': '',

            # INFORMACOES
            # 24.3A
            # 'outras_informacoes': '',
            # 25.3A
            # 'codigo_finalidade_doc': line.codigo_finalidade_doc,
            # 26.3A
            'codigo_finalidade_ted': '',
            # 27.3A
            'codigo_finalidade_complementar': '',
            # 28.3A
            # CNAB - Uso Exclusivo FEBRABAN/CNAB
            # 29.3A
            # 'aviso_ao_favorecido': line.aviso_ao_favorecido,
            'aviso_ao_favorecido': 0,
            # 'ocorrencias': '',
        }

    elif tipo == 'B':
        segmento = {
            # SEGMENTO B
            # Preenchido no segmento A
            # 01.3B
            # 02.3B
            # 03.3B

            # 04.3B
            # 05.3B
            # 06.3B

            # DADOS COMPLEMENTARES - FAVORECIDOS
            # 07.3B
            'favorecido_tipo_inscricao': line[17],
            # 08.3B
            'favorecido_num_inscricao': line[21:32],
            # 09.3B
            'favorecido_endereco_rua': line[32:62],
            # 10.3B
            'favorecido_endereco_num': line[62:67],
            # 11.3B
            'favorecido_endereco_complemento': line[67:82],
            # 12.3B
            'favorecido_endereco_bairro': line[82:97],
            # 13.3B
            'favorecido_endereco_cidade': line[97:117],
            # 14.3B
            # 'favorecido_cep': int(line.partner_id.zip[:5]) or 0,
            'favorecido_cep': line[117:122],
            # 15.3B
            'favorecido_cep_complemento': line[122:125],
            # 16.3B
            'favorecido_estado': line[125:127],

            # DADOS COMPLEMENTARES - PAGAMENTO
            # 17.3B
            'pagamento_vencimento': line[127:135],
            # 18.3B
            'pagamento_valor_documento': Decimal('0.00'),
            # 19.3B
            'pagamento_abatimento': Decimal('0.00'),
            # 20.3B
            'pagamento_desconto': Decimal('0.00'),
            # 21.3B
            'pagamento_mora': Decimal('0.00'),
            # 22.3B
            'pagamento_multa': Decimal('0.00'),
            # 23.3B
            # 'cod_documento_favorecido': '',
            # 24.3B - Informado No SegmentoA
            # 'aviso_ao_favorecido': '0',
            # 25.3B
            # 'codigo_ug_centralizadora': '0',
            # 26.3B
            # 'codigo_ispb': '0',
        }

    else:
        return {}

    return segmento