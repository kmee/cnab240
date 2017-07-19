
from __future__ import division, print_function, unicode_literals

import os
import codecs
import time
from decimal import Decimal

TESTS_DIRPATH = os.path.abspath(os.path.dirname(__file__))
ARQS_DIRPATH = os.path.join(TESTS_DIRPATH, 'arquivos')

def get_banco_brasil_data_from_dict():
    data = dict()

    header_arquivo = {
        # CONTROLE
        # 01.0
        'controle_banco': 1,
        # 02.0 # Sequencia para o Arquivo
        'controle_lote': 1,
        # 03.0  0- Header do Arquivo
        'controle_registro': 0,
        # 04.0
        # CNAB - Uso Exclusivo FEBRABAN / CNAB

        # EMPRESA
        # 05.0 - 1 - CPF / 2 - CNPJ
        'cedente_inscricao_tipo': 2,
        # 06.0
        'cedente_inscricao_numero': 23130935000198,
        # 07.0
        'cedente_convenio': '8597254075443',
        # 08.0
        'cedente_agencia': 1220,
        # 09.0
        'cedente_agencia_dv': '1',
        # 10.0
        'cedente_conta': 385298,
        # 11.0
        'cedente_conta_dv': '0',
        # 12.0
        'cedente_agencia_conta_dv': '',
        # 13.0
        'cedente_nome': "KMEE INFORMATICA LTDA         ",
        # 14.0
        'nome_banco': "BANCO DO BRASIL S.A.",
        # 15.0
        # CNAB - Uso Exclusivo FEBRABAN / CNAB

        # ARQUIVO
        # 16.0 Codigo Remessa = 1 / Retorno = 2
        'arquivo_codigo': '1',
        # 17.0
        'arquivo_data_de_geracao': '13072017',
        # 18.0
        'arquivo_hora_de_geracao': '062238',
        # 19.0 Numero sequencial de arquivo
        'arquivo_sequencia': 1,
        # 20.0
        'arquivo_layout': 103,
        # 21.0
        'arquivo_densidade': 0,
        # 22.0
        'reservado_banco': '',
        # 23.0
        'reservado_empresa': 'MIL GRAU   ',
        # 24.0
        # CNAB - Uso Exclusivo FEBRABAN / CNAB
    }

    header_lote = {
        # CONTROLE
        # 01.1
        'controle_banco': 1,
        # 02.1  Sequencia para o Arquivo
        'controle_lote': 1,
        # 03.1  0- Header do Arquivo
        'controle_registro': 1,

        # SERVICO
        # 04.1 # Header do lote sempre 'C'
        'servico_operacao': 'C',
        # 05.1 30 - Pagamento de Salarios
        'servico_servico': 30,
        # 06.1
        'servico_forma_lancamento': 1,
        # 07.1
        'servico_layout': 20,
        # 08.1
        # CNAB - Uso Exclusivo da FEBRABAN/CNAB

        # EMPRESA CEDENTE
        # 09.1
        'empresa_inscricao_tipo': 2,
        # 10.1
        'empresa_inscricao_numero': 23130935000198,
        # 11.1
        'cedente_convenio': '8597254075443',
        # 12.1
        'cedente_agencia': 1220,
        # 13.1
        'cedente_agencia_dv': '1',
        # 14.1
        'cedente_conta': 385298,
        # 15.1cd ..for
        'cedente_conta_dv': '0',
        # 16.1
        'cedente_agencia_conta_dv': '',
        # 17.1
        'cedente_nome': "KMEE INFORMATICA LTDA         ",
        # 18.1
        'mensagem1': '',

        # ENDERECO
        # 19.1
        'empresa_logradouro': 'Rua Coronel Reno1275',
        # 20.1
        'empresa_endereco_numero': 00,
        # 21.1
        'empresa_endereco_complemento': 'ANDAR 11',
        # 22.1
        'empresa_endereco_cidade': 'Itajuba ',
        # 23.1
        'empresa_endereco_cep': '37500',
        # 24.1
        'empresa_endereco_cep_complemento': '050',
        # 25.1
        'empresa_endereco_estado': 'MG',

        # 26.1
        'indicativo_forma_pagamento': '',
        # 27.1
        # CNAB - Uso Exclusivo FEBRABAN / CNAB
        # 28.1
        'ocorrencias': '',
    }

    pagamento_1 = {

        # SEGMENTO A
        # CONTROLE
        # 01.3A
        'controle_banco': 1,
        # 02.3A
        'controle_lote': 1,
        # 03.3A -  3-Registros Iniciais do Lote
        'controle_registro': 3,

        # SERVICO
        # 04.3A - Numero Sequencial do Registro - Inicia em 1 em cada novo lote
        'servico_numero_registro': 1,
        # 05.3A
        #   Segmento Codigo de Segmento do Reg.Detalhe
        # 06.3A
        'servico_tipo_movimento': 0,
        # 07.3A 00 - Inclusao de registros
        'servico_codigo_movimento': 00,

        # FAVORECIDO
        # 08.3A - 018-TED 700-DOC
        'favorecido_camara': 0,
        # 09.3A
        'favorecido_banco': 1,
        # 10.3A
        'favorecido_agencia': 3884,
        # 11.3A
        'favorecido_agencia_dv': '6',
        # 12.3A
        'favorecido_conta': 12675,
        # 13.3A
        'favorecido_conta_dv': '0',
        # 14.3A
        'favorecido_dv': '',
        # 15.3A
        'favorecido_nome': 'Ana Claudia Muniz Casagrande  ',

        # CREDITO
        # 16.3A -
        'credito_seu_numero': '167',
        # 17.3A
        'credito_data_pagamento': '13072017',
        # 18.3A
        'credito_moeda_tipo': 'BRL',
        # 19.3A
        'credito_moeda_quantidade': Decimal('0.00000'),
        # 20.3A
        'credito_valor_pagamento': Decimal('7472.91'),
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
        'favorecido_tipo_inscricao': 1,
        # 08.3B
        'favorecido_num_inscricao': 17187459238,
        # 09.3B
        'favorecido_endereco_rua': 'Rua projetada1',
        # 10.3B
        'favorecido_endereco_num': 0,
        # 11.3B
        'favorecido_endereco_complemento': '',
        # 12.3B
        'favorecido_endereco_bairro': 'Projeto 01     ',
        # 13.3B
        'favorecido_endereco_cidade': 'Itajuba ',
        # 14.3B
        # 'favorecido_cep': int(line.partner_id.zip[:5]) or 0,
        'favorecido_cep': 37500,
        # 15.3B
        'favorecido_cep_complemento': '050',
        # 16.3B
        'favorecido_estado': 'MG',

        # DADOS COMPLEMENTARES - PAGAMENTO
        # 17.3B
        'pagamento_vencimento': 0,
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

    pagamento_2 = {
        'aviso_ao_favorecido': 0,
        'codigo_finalidade_complementar': '',
        'codigo_finalidade_ted': '',
        'controle_banco': '001',
        'controle_lote': '0001',
        'controle_registro': '3',
        'credito_data_pagamento': '13072017',
        'credito_moeda_quantidade': Decimal('0.00000'),
        'credito_moeda_tipo': 'BRL',
        'credito_seu_numero': '168                 ',
        'credito_valor_pagamento': Decimal('7472.91'),
        'favorecido_agencia': '13555',
        'favorecido_agencia_dv': '1',
        'favorecido_banco': 1,
        'favorecido_camara': 0,
        'favorecido_conta': '127631273189',
        'favorecido_conta_dv': '1',
        'favorecido_dv': ' ',
        'favorecido_nome': 'Carolina Carvalho do Nasciment',
        'servico_codigo_movimento': '00',
        'servico_numero_registro': '00003',
        'servico_tipo_movimento': '0',
        'favorecido_cep': '00000',
        'favorecido_cep_complemento': '   ',
        'favorecido_endereco_bairro': '               ',
        'favorecido_endereco_cidade': '                    ',
        'favorecido_endereco_complemento': '               ',
        'favorecido_endereco_num': '00000',
        'favorecido_endereco_rua': '                              ',
        'favorecido_estado': '  ',
        'favorecido_num_inscricao': '87674326788',
        'favorecido_tipo_inscricao': '1',
        'pagamento_abatimento': Decimal('0.00'),
        'pagamento_desconto': Decimal('0.00'),
        'pagamento_mora': Decimal('0.00'),
        'pagamento_multa': Decimal('0.00'),
        'pagamento_valor_documento': Decimal('0.00'),
        'pagamento_vencimento': '00000000'
    }

    pagamento_3 = {
        'aviso_ao_favorecido': 0,
        'codigo_finalidade_complementar': '',
        'codigo_finalidade_ted': '',
        'controle_banco': '001',
        'controle_lote': '0001',
        'controle_registro': '3',
        'credito_data_pagamento': '13072017',
        'credito_moeda_quantidade': Decimal('0.00000'),
        'credito_moeda_tipo': 'BRL',
        'credito_seu_numero': '169                 ',
        'credito_valor_pagamento': Decimal('00000030996.82'),
        'favorecido_agencia': '54237',
        'favorecido_agencia_dv': '6',
        'favorecido_banco': 1,
        'favorecido_camara': 0,
        'favorecido_conta': '000001209149',
        'favorecido_conta_dv': '7',
        'favorecido_dv': ' ',
        'favorecido_nome': 'Barbara Ribeiro da Silva Mercu',
        'servico_codigo_movimento': '00',
        'servico_numero_registro': '00005',
        'servico_tipo_movimento': '0',
        'favorecido_cep': '00000',
        'favorecido_cep_complemento': '   ',
        'favorecido_endereco_bairro': '               ',
        'favorecido_endereco_cidade': '                    ',
        'favorecido_endereco_complemento': '               ',
        'favorecido_endereco_num': '00000',
        'favorecido_endereco_rua': '                              ',
        'favorecido_estado': '  ',
        'favorecido_num_inscricao': '87437638438',
        'favorecido_tipo_inscricao': '1',
        'pagamento_abatimento': Decimal('0.00'),
        'pagamento_desconto': Decimal('0.00'),
        'pagamento_mora': Decimal('0.00'),
        'pagamento_multa': Decimal('0.00'),
        'pagamento_valor_documento': Decimal('0.00'),
        'pagamento_vencimento': '00000000',
    }

    pagamento_4 = {
        'aviso_ao_favorecido': 0,
        'codigo_finalidade_complementar': '',
        'codigo_finalidade_ted': '',
        'controle_banco': '001',
        'controle_lote': '0001',
        'controle_registro': '3',
        'credito_data_pagamento': '13072017',
        'credito_moeda_quantidade': Decimal('0.00000'),
        'credito_moeda_tipo': 'BRL',
        'credito_seu_numero': '170                 ',
        'credito_valor_pagamento': Decimal('00000011615.60'),
        'favorecido_agencia': '12370',
        'favorecido_agencia_dv': '5',
        'favorecido_banco': 1,
        'favorecido_camara': 0,
        'favorecido_conta': '000000095738',
        'favorecido_conta_dv': '0',
        'favorecido_dv': ' ',
        'favorecido_nome': 'Carina Malafaia de Oliveira   ',
        'servico_codigo_movimento': '00',
        'servico_numero_registro': '00007',
        'servico_tipo_movimento': '0',
        'favorecido_cep': '00000',
        'favorecido_cep_complemento': '   ',
        'favorecido_endereco_bairro': '               ',
        'favorecido_endereco_cidade': '                    ',
        'favorecido_endereco_complemento': '               ',
        'favorecido_endereco_num': '00000',
        'favorecido_endereco_rua': '                              ',
        'favorecido_estado': '  ',
        'favorecido_num_inscricao': '10217421092',
        'favorecido_tipo_inscricao': '1',
        'pagamento_abatimento': Decimal('0.00'),
        'pagamento_desconto': Decimal('0.00'),
        'pagamento_mora': Decimal('0.00'),
        'pagamento_multa': Decimal('0.00'),
        'pagamento_valor_documento': Decimal('0.00'),
        'pagamento_vencimento': '00000000',
    }

    pagamento_5 = {
        'aviso_ao_favorecido': 0,
        'codigo_finalidade_complementar': '',
        'codigo_finalidade_ted': '',
        'controle_banco': '001',
        'controle_lote': '0001',
        'controle_registro': '3',
        'credito_data_pagamento': '13072017',
        'credito_moeda_quantidade': Decimal('0.00000'),
        'credito_moeda_tipo': 'BRL',
        'credito_seu_numero': '171                 ',
        'credito_valor_pagamento': Decimal('00000011615.60'),
        'favorecido_agencia': '12345',
        'favorecido_agencia_dv': '6',
        'favorecido_banco': 1,
        'favorecido_camara': 0,
        'favorecido_conta': '000002033244',
        'favorecido_conta_dv': '3',
        'favorecido_dv': ' ',
        'favorecido_nome': 'Mariana de Albuquerque de Sa  ',
        'servico_codigo_movimento': '00',
        'servico_numero_registro': '00009',
        'servico_tipo_movimento': '0',
        'favorecido_cep': '00000',
        'favorecido_cep_complemento': '   ',
        'favorecido_endereco_bairro': '               ',
        'favorecido_endereco_cidade': '                    ',
        'favorecido_endereco_complemento': '               ',
        'favorecido_endereco_num': '00000',
        'favorecido_endereco_rua': '                              ',
        'favorecido_estado': '  ',
        'favorecido_num_inscricao': '84327483299',
        'favorecido_tipo_inscricao': '1',
        'pagamento_abatimento': Decimal('0.00'),
        'pagamento_desconto': Decimal('0.00'),
        'pagamento_mora': Decimal('0.00'),
        'pagamento_multa': Decimal('0.00'),
        'pagamento_valor_documento': Decimal('0.00'),
        'pagamento_vencimento': '00000000',
    }

    pagamentos = []
    pagamentos.append(pagamento_1)
    pagamentos.append(pagamento_2)
    pagamentos.append(pagamento_3)
    pagamentos.append(pagamento_4)
    pagamentos.append(pagamento_5)

    data['header'] = header_arquivo
    data['header_lote'] = header_lote
    data['pagamento'] = pagamentos

    return data


def get_banco_brasil_file_remessa():
    arquivo_remessa = codecs.open(
        os.path.join(ARQS_DIRPATH,
                     'pagamento_dict.banco_brasil.rem'), encoding='ascii')
    arquivo_data = arquivo_remessa.read()
    arquivo_remessa.close()
    return arquivo_data
