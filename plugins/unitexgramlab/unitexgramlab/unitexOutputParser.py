#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

# Copyright (c) 2017 Adler Neves <adlerosn@gmail.com>
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

__author__ = "Adler Neves"
__email__ = "adlerosn@gmail.com"
__title__ = None
__description__ = None
__license__ = 'MIT'
__copyright__ = 'Copyright 2017 Adler O. S. Neves'
__version__ = '0.0.1'

import re

def unescapeWithChar(string, escapechar):
    unescaped = ''
    escaping = False
    for char in string:
        if not escaping and char == escapechar:
            escaping = True
        else:
            unescaped+=char
            escaping = False
    return unescaped


def parseDelaf(line):
    if line.startswith('/'):
        return None
    etapa = 0
    entrada = ''
    lema = ''
    gramSem = []
    gramSemBuf = ''
    inflx = []
    inflxBuf = ''
    willEscape = False
    for char in line+'::':
        if not willEscape and char == '\\':
            willEscape = True
        elif not willEscape and (
            (etapa==0 and char==',')
            or
            (etapa==1 and char=='.')
            or
            (etapa==2 and char=='+')
            or
            (etapa==2 and char==':')
            or
            (etapa==3 and char==':')
        ):
            if etapa==0 and char==',':
                etapa+=1
            elif etapa==1 and char=='.':
                etapa+=1
                if len(lema) == 0:
                    lema = entrada
            elif etapa==2 and char=='+':
                gramSem.append(gramSemBuf)
                gramSemBuf = ''
            elif etapa==2 and char==':':
                gramSem.append(gramSemBuf)
                gramSemBuf = ''
                etapa+=1
            elif etapa==3 and char==':':
                inflx.append(inflxBuf)
                inflxBuf = ''
            else:
                pass
        else:
            willEscape = False
            if etapa == 0:
                entrada+=char
            elif etapa == 1:
                lema+=char
            elif etapa == 2:
                gramSemBuf+=char
            elif etapa == 3:
                inflxBuf+=char
    gramSem = [x for x in gramSem if len(x)>0]
    inflx = [list(x) for x in inflx if len(x)>0]
    return {
        'texto': entrada,
        'lema':lema,
        'gramSem':gramSem,
        'flex':inflx,
    }

def parseDelas(line):
    if line.startswith('/'):
        return None
    etapa = 0
    entrada = ''
    gramSem = []
    gramSemBuf = ''
    willEscape = False
    for char in line+'++':
        if not willEscape and char == '\\':
            willEscape = True
        elif not willEscape and (
            (etapa==0 and char==',')
            or
            (etapa==1 and char=='+')
        ):
            if etapa==0 and char==',':
                etapa+=1
            elif etapa==1 and char=='+':
                gramSem.append(gramSemBuf)
                gramSemBuf = ''
            else:
                pass
        else:
            willEscape = False
            if etapa == 0:
                entrada+=char
            elif etapa == 1:
                gramSemBuf+=char
    gramSem = [x for x in gramSem if len(x)>0]
    return {
        'texto': entrada,
        'gramSem':gramSem,
    }


def delasToDelaf(delas):
    delaf = dict()
    delaf['texto'] = delas['texto']
    delaf['lema'] = delas['texto']
    delaf['gramSem'] = delas['gramSem'].copy()
    delaf['flex'] = list()
    return delaf

def textToDelas(texto):
    delas = dict()
    delas['texto'] = texto
    delas['gramSem'] = list()
    return delas

def segmentaTfst(tfst):
    segmentos = tfst[1:]
    grafoN = 0
    grafos = []
    grafo = []
    for line in segmentos:
        if line == '$'+str(grafoN+1):
            if grafoN!=0:
                grafos.append(grafo)
                grafo = []
            grafoN+=1
        else:
            grafo.append(line)
    if len(grafo)>0:
        grafos.append(grafo)
    return grafos

def parseTfstSegment(tfst, tokens):
    skiplines = 0
    etapa = 0
    sentenca = ''
    componentes = []
    caixaPosicao = []
    caixas = []
    caractereInicial = 0
    for linha in tfst:
        if skiplines>0:
            skiplines-=1
        elif etapa == 0:
            sentenca = linha
            etapa+=1
        elif etapa == 1:
            componentes = [
                    tokens[int(seg.split('/')[0])]
                    for seg in linha.strip().split(' ')
            ]
            etapa+=1
        elif etapa == 2:
            caractereInicial = int(linha.strip().split('_')[-1])
            etapa+=1
        elif etapa == 3 and linha.startswith(':'):
            x = linha[1:].strip().split(' ')
            caixaPosicao+=([[int(x[k])-1, int(x[k+1])-1] for k in range(0, len(x), 2)])
        elif etapa == 3:
            etapa+=1
            skiplines+=3
        elif etapa == 4 and linha.strip()=='f':
            etapa = -1 #bloqueia grafo finalizado
        elif etapa == 4 and linha.strip()=='.':
            pass
        elif etapa == 4 and linha.strip()=='@STD':
            etapa+=1
        elif etapa == 5 and linha.strip().startswith('@'):
            etapa-=1
            skiplines+=1
            linha = linha[1:]
            node = None
            if linha.startswith('{') and linha.endswith('}'):
                node = parseDelaf(linha[1:-1])
            else:
                node = delasToDelaf(textToDelas(linha))
            caixas.append(node)
        else:
            pass
#            print('Algum caso passou')
    for i in range(len(caixaPosicao)):
        caixaPosicao[i].append(caixas[caixaPosicao[i][0]])
        del caixaPosicao[i][0]
    return {
        'sentenca': sentenca,
        'componentes': componentes,
        'caractereInicial': caractereInicial,
        'grafoLinear': caixaPosicao,
    }

def parseGrf(grf):
    segmenter = re.compile(r'''"(.*)"([0-9 ]*)''')
    for i in range(len(grf)):
        if grf[i] == '#':
            grf = grf[i+2:]
            break
    grf = [segmenter.findall(k) for k in grf]
    grf = [
        {
            'local_id': 0,
            'conteudo': unescapeWithChar(k[0][0],'\\'),
            'arestaPara': list(map(int, k[0][1].strip().split(' '))),
            'inicial': False,
            'final': False,
        }
        for k in grf
    ]
    grf[0]['inicial'] = True
    grf[1]['final'] = True
    for i in range(len(grf)):
        grf[i]['local_id'] = i
    return grf
