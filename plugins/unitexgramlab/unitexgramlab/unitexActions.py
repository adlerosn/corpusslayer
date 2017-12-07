#!/usr/bin/env python3
#  -*- encoding: utf-8 -*-

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
import os
import json
import time
import errno
import shutil
import traceback

pluginName = os.path.abspath(__file__).split(os.path.sep)[-3]

exec('import '+('.'.join(['plugins',pluginName,'unitexgramlab','unitexwrapper']))+' as unitexwrapper')
exec('from '+('.'.join(['plugins',pluginName,'unitexgramlab','commandlineLogger']))+' import CommandLogger')
exec('import '+('.'.join(['plugins',pluginName,'unitexgramlab','unitexOutputParser']))+' as uniparser')

class UnitexActions(object):
    unitex = None
    logger = None
    workspace = "work"
    lang = None

    _executionPlan = list()

    corpus_content = ""
    corpus_diskname = "corpus"
    corpus_directory = ''
    corpus_file = ''
    corpus_sentences =''
    corpus_wdir = ''
    volume_id = 0

    langNameFs = {
        'ar':  'Arabic',
        'en':  'English',
        'fi':  'Finnish',
        'fr':  'French',
        'ka':  'Georgian (Ancient)',
        'de':  'German',
        'ela': 'Greek (Ancient)',
        'el':  'Greek (Modern)',
        'it':  'Italian',
        'ko':  'Korean',
        'la':  'Latin',
        'mg':  'Malagasy',
        'nb':  'Norwegian (Bokmal)',
        'nn':  'Norwegian (Nynorsk)',
        'po':  'Polish',
        'ptb': 'Portuguese (Brazil)',
        'pt':  'Portuguese (Portugal)',
        'ru':  'Russian',
        'src': 'Serbian-Cyrillic',
        'sr':  'Serbian-Latin',
        'es':  'Spanish',
        'th':  'Thai',
    }

    assets = {
        'snt_grf':      '/Graphs/Preprocessing/Sentence/Sentence.grf',
        'snt_fst2':     '/Graphs/Preprocessing/Sentence/Sentence.fst2',# autoderived from above
        'norm_txt':     '/Norm.txt',
        'norm_grf':     '/Graphs/Normalization/Norm.grf',
        'norm_fst2':    '/Graphs/Normalization/Norm.fst2',# autoderived from above
        'replace_grf':  '/Graphs/Preprocessing/Replace/Replace.grf',
        'replace_fst2': '/Graphs/Preprocessing/Replace/Replace.fst2', # autoderived from above
        'alp_txt':      '/Alphabet.txt',
        'alp_sort_txt': '/Alphabet_sort.txt',
        'aec_grf':      '/Graphs/auto-ex-corpus.grf', #output
        #'regexp_txt':   '/regexp.txt', # user input
        #'regexp_grf':   '/regexp.grf', # autoderived from above
        #'regexp_fst2':  '/regexp.fst2', # autoderived from above
        'tagger_bin':   '/Dela/tagger_data_cat.bin',
        'tagger_inf':   '/Dela/tagger_data_cat.inf',
        'tagger_def':   '/Elag/tagset.def',
        'dela_bin_dics':[],
    }

    reopening = False

    @property
    def id(self):
        return self.volume_id

    def __init__(self,
            corpus_content = None,
            lang = None,
            volume_id = None,
            workspace = None,
            custom_assets = None,
            dumbMode = False
        ):
        if workspace is not None:
            self.workspace = workspace
        if volume_id is not None:
            self.volume_id = volume_id
        else:
            self.volume_id = self._nextVolumeId
        self.lang = lang
        del workspace
        del volume_id
        del lang

        if not dumbMode:
            self.__assert_existance()

        if not dumbMode:
            self.__create_unitex_instance()
            self.__setup_working_directory()
        self.__update_supported_languages()
        if not dumbMode:
            self.__provide_default_linguistic_resources()
            self.__update_asset_definitions()
            self.__setup_corpus_filenames()
            self.__write_corpus_file(corpus_content)
            self.__install_custom_assets(custom_assets)

    def __assert_existance(self):
        if self.lang is None and not os.path.exists(self._workspace_volume(self.volume_id)):
            raise FileNotFoundError(
                errno.ENOENT,
                os.strerror(errno.ENOENT),
                os.path.abspath(self._workspace_volume(self.volume_id))
            )

    def __install_custom_assets(self, custom_assets):
        if custom_assets is not None:
            for custom_asset in custom_assets:
                pass

    def __update_supported_languages(self):
        pass

    def __update_asset_definitions(self):
        self.__update_dela_dics_list()

    def __write_corpus_file(self,corpus_content):
        if corpus_content is None and not os.path.exists(self.corpus_file):
            corpus_content = ''
        if corpus_content is not None:
            with open(self.corpus_file, 'w') as f:
                f.writelines(re.split(r'(\r\n|\r|\n)', corpus_content))

    def __setup_corpus_filenames(self):
        self.corpus_file = self.corpus_directory+self.corpus_diskname+".txt"
        self.corpus_sentences = self.corpus_directory+self.corpus_diskname+".snt"

        self.corpus_wdir = self.corpus_directory+self.corpus_diskname+"_snt"+os.path.sep
        if not os.path.exists(self.corpus_wdir):
            os.makedirs(self.corpus_wdir)

    def __provide_default_linguistic_resources(self):
        if not os.path.exists(self.corpus_workspace):
            shutil.copytree(self.langWorkspaceSource, self.corpus_workspace)

    def __update_dela_dics_list(self):
        self.assets['dela_bin_dics'] = [
            f for f in
            [
                    os.path.abspath(self.corpus_workspace+'/Dela/'+file)
                    for file in os.listdir(os.path.abspath(self.corpus_workspace+'/Dela'))
            ]
            if os.path.isfile(f) and f.lower().endswith('.bin')
        ]

    def __setup_working_directory(self):
        self.corpus_directory = (
            self._workspaces_container +
            str(self.volume_id) +
            os.path.sep
        )

        if not os.path.exists(self.corpus_directory):
            os.makedirs(self.corpus_directory)
        else:
            self.reopening = True

        self.langWorkspaceSource = (
            self.__context_dir +
            os.path.sep +
            'lang' +
            os.path.sep +
            self.langNameFs.get(self.lang,self.langNameFs['en'])
        )

        self.langWorkspaceSource = os.path.abspath(self.langWorkspaceSource)

        self.corpus_workspace = (
            self.corpus_directory +
            "workspace" +
            os.path.sep
        )

        self.__configure_logger()

    def __configure_logger(self):
        self.logger = CommandLogger(
            self.corpus_directory+"log",
            dontTouchPid = self.reopening
        )


    def __create_unitex_instance(self):
        self.unitex = unitexwrapper.Unitex(
            os.path.join(
                self.__context_dir,
                'UnitexTool'
            )
        )

    @property
    def __context_dir(self):
        return os.path.dirname(os.path.abspath(__file__))

    @property
    def _workspaces_container(self):
        return (
            self.__context_dir +
            os.path.sep +
            str(self.workspace) +
            os.path.sep
        )

    def _workspace_volume(self, num):
        return self._workspaces_container+str(num)

    @property
    def _nextVolumeId(self):
        i = 1
        while os.path.exists(self._workspace_volume(i)):
            i+=1
        return i

    def _preprocess(self):
        # Preprocessing

        log = self.logger.task("preprocessing_normalize_input")
        log.began = True
        log.result = self.unitex.Normalize(
            self.corpus_file,
            '-r'+os.path.abspath(self.corpus_workspace+self.assets['norm_txt']),
            '--output_offsets='+self.corpus_wdir+'normalize.out.offsets',
            '-qutf8-no-bom'
        )

        log = self.logger.task("preprocessing_converting_graph")
        log.began = True
        log.result = self.unitex.Grf2Fst2(
            os.path.abspath(self.corpus_workspace+self.assets['snt_grf']),
            '-y',
            '--alphabet='+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
            '-qutf8-no-bom'
        )

        log = self.logger.task("preprocessing_flattening_graph")
        log.began = True
        log.result = self.unitex.Flatten(
            os.path.abspath(self.corpus_workspace+self.assets['snt_fst2']),
            '--rtn',
            '-d5',
            '-qutf8-no-bom'
        )

        log = self.logger.task("preprocessing_plainifying_graph")
        log.began = True
        log.result = self.unitex.Fst2Txt(
            '-t'+self.corpus_sentences,
            os.path.abspath(self.corpus_workspace+self.assets['snt_fst2']),
            '-a'+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
            '-M',
            '--input_offsets='+self.corpus_wdir+'normalize.out.offsets',
            '--output_offsets='+self.corpus_wdir+'normalize.out.offsets',
            '-qutf8-no-bom'
        )

        log = self.logger.task("preprocessing_converting_graph_again")
        log.began = True
        log.result = self.unitex.Grf2Fst2(
            os.path.abspath(self.corpus_workspace+self.assets['replace_grf']),
            '-y',
            '--alphabet='+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
            '-qutf8-no-bom'
        )

        log = self.logger.task("preprocessing_flattening_graph_again")
        log.began = True
        log.result = self.unitex.Fst2Txt(
            '-t'+self.corpus_sentences,
            os.path.abspath(self.corpus_workspace+self.assets['replace_fst2']),
            '-a'+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
            '-R',
            '--input_offsets='+self.corpus_wdir+'normalize.out.offsets',
            '--output_offsets='+self.corpus_wdir+'normalize.out.offsets',
            '-qutf8-no-bom'
        )

        log = self.logger.task("preprocessing_extracting_tokens")
        log.began = True
        log.result = self.unitex.Tokenize(
            self.corpus_sentences,
            '-a'+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
            '--input_offsets='+self.corpus_wdir+'normalize.out.offsets',
            '--output_offsets='+self.corpus_wdir+'tokenize.out.offsets',
            '-qutf8-no-bom'
        )


        if len(self.assets['dela_bin_dics'])>0:
            log = self.logger.task("preprocessing_using_dictionary")
            log.began = True
            log.result = self.unitex.Dico(*[
                '-t'+self.corpus_sentences,
                '-a'+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
                ]+self.assets['dela_bin_dics']+[
                '-qutf8-no-bom'
            ])

            log = self.logger.task("preprocessing_sorting_text_simple")
            log.began = True
            log.result = self.unitex.SortTxt(
                self.corpus_wdir+'dlf',
                '-l'+self.corpus_wdir+'dlf.n',
                '-o'+os.path.abspath(self.corpus_workspace+self.assets['alp_sort_txt']),
                '-qutf8-no-bom'
            )

            log = self.logger.task("preprocessing_sorting_text_compound")
            log.began = True
            log.result = self.unitex.SortTxt(
                self.corpus_wdir+'dlc',
                '-l'+self.corpus_wdir+'dlc.n',
                '-o'+os.path.abspath(self.corpus_workspace+self.assets['alp_sort_txt']),
                '-qutf8-no-bom'
            )

            log = self.logger.task("preprocessing_sorting_text_unknown")
            log.began = True
            log.result = self.unitex.SortTxt(
                self.corpus_wdir+'err',
                '-l'+self.corpus_wdir+'err.n',
                '-o'+os.path.abspath(self.corpus_workspace+self.assets['alp_sort_txt']),
                '-qutf8-no-bom'
            )

            log = self.logger.task("preprocessing_sorting_text_unknown_unique")
            log.began = True
            log.result = self.unitex.SortTxt(
                self.corpus_wdir+'tags_err',
                '-l'+self.corpus_wdir+'tags_err.n',
                '-o'+os.path.abspath(self.corpus_workspace+self.assets['alp_sort_txt']),
                '-qutf8-no-bom'
            )

            log = self.logger.task("preprocessing_wordlist_parsing")
            log.began = True
            with open(self.corpus_wdir+'dlf') as fdlf:
                with open(self.corpus_wdir+'dlc') as fdlc:
                    with open(self.corpus_wdir+'err') as ferr:
                        dlf = fdlf.read().strip().splitlines()
                        dlc = fdlc.read().strip().splitlines()
                        err = ferr.read().strip().splitlines()
                        dlf = [uniparser.parseDelaf(k) for k in dlf]
                        dlc = [uniparser.parseDelaf(k) for k in dlc]
                        with open(self.corpus_directory+'wordlist.json','w') as fw:
                            fw.write(
                                json.dumps(
                                    {
                                        'simples':        dlf,
                                        'composto':       dlc,
                                        'naoReconhecido': err,
                                    }
                                )
                            )
            log.completed = True
        else:
            log = self.logger.task("preprocessing_wordlist_parsing")
            log.began = True
            with open(self.corpus_wdir+'tokens.txt') as fr:
                with open(self.corpus_directory+'wordlist.json','w') as fw:
                    fw.write(
                        json.dumps(
                            {
                                'simples':        [],
                                'composto':       [],
                                'naoReconhecido': sorted(fr.read().splitlines()[1:]),
                            }
                        )
                    )
            log.completed = True

        log = self.logger.task("preprocessing_wordfreq_parsing")
        log.began = True
        with open(self.corpus_wdir+'tok_by_freq.txt') as fr:
            keyPair = [line.split('\t') for line in fr.read().splitlines() if '\t' in line]
            with open(self.corpus_directory+'wordfreq.json','w') as fw:
                fw.write(
                    json.dumps(
                        {
                            word: int(freq)
                            for freq,word in keyPair
                        }
                    )
                )
        log.completed = True

        log = self.logger.task("preprocessing_sentences_parsing")
        log.began = True
        #sentenceCount = 0
        with open(self.corpus_sentences) as fr:
            sentences = [sentence.replace('\n',' ').replace('\r','') for sentence in fr.read().split('{S}')]
            #sentenceCount = len(sentences)
            with open(self.corpus_directory+'sentences.json','w') as fw:
                fw.write(json.dumps(sentences))
        log.completed = True

    def _fstText(self):
        # FST text

        log = self.logger.task("converting_fst_graph")
        log.result = self.unitex.Grf2Fst2(
            os.path.abspath(self.corpus_workspace+self.assets['norm_grf']),
            '-y',
            '--alphabet='+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
            '-qutf8-no-bom'
        )

        log = self.logger.task("building_fst_text")
        log.result = self.unitex.Txt2Tfst(
            self.corpus_sentences,
            '-a'+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
            '--clean',
            '-n'+os.path.abspath(self.corpus_workspace+self.assets['norm_fst2']),
            '-qutf8-no-bom'
        )

        log = self.logger.task("parsing_fst_text")
        log.began = True
        with open(self.corpus_wdir+'tokens.txt') as fr2:
            tokens = fr2.read().splitlines()[1:]
            with open(self.corpus_wdir+'text.tfst') as fr:
                tfst = fr.read().splitlines()
                grafos = uniparser.segmentaTfst(tfst)
                grafosParsed = [uniparser.parseTfstSegment(grafo, tokens) for grafo in grafos]
                with open(self.corpus_directory+'fsttext.json','w') as fw:
                    fw.write(json.dumps(grafosParsed))
        log.completed = True

        log = self.logger.task("parsing_fst_tagfreq")
        log.began = True
        with open(self.corpus_wdir+'tfst_tags_by_freq.txt') as fr:
            tagfreq = [[x.split('\t')[-1],float(x.split('\t')[0])] for x in fr.read().splitlines()]
            for tag in tagfreq:
                if tag[0].startswith('{') and tag[0].endswith('}'):
                    tag[0] = uniparser.parseDelaf(tag[0][1:-1])
                else:
                    tag[0] = uniparser.delasToDelaf(uniparser.textToDelas(tag[0]))
            with open(self.corpus_directory+'tagfreq.json','w') as fw:
                fw.write(json.dumps(tagfreq))
        log.completed = True

        log = self.logger.task("tagging_fst_text")
        log.result = self.unitex.Tagger(
            os.path.abspath(self.corpus_wdir+'text.tfst'),
            '-d'+os.path.abspath(self.corpus_workspace+self.assets['tagger_bin']),
            '-t'+os.path.abspath(self.corpus_workspace+self.assets['tagger_def']),
            '-a'+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
            '-qutf8-no-bom'
        )

        taggingFailed = log.errored

        log = self.logger.task("parsing_fst_text_tagged")
        log.began = True
        with open(self.corpus_wdir+'tokens.txt') as fr2:
            tokens = fr2.read().splitlines()[1:]
            with open(self.corpus_wdir+'text.tfst') as fr:
                grafosParsed = None
                if not taggingFailed:
                    tfst = fr.read().splitlines()
                    grafos = uniparser.segmentaTfst(tfst)
                    grafosParsed = [uniparser.parseTfstSegment(grafo, tokens) for grafo in grafos]
                with open(self.corpus_directory+'fsttexttagged.json','w') as fw:
                    fw.write(json.dumps(grafosParsed))
        log.completed = True

        log = self.logger.task("parsing_fst_taggedfreq")
        log.began = True
        with open(self.corpus_wdir+'tfst_tags_by_freq.txt') as fr:
            tagfreq = None
            if not taggingFailed:
                tagfreq = [[x.split('\t')[-1],float(x.split('\t')[0])] for x in fr.read().splitlines()]
                for tag in tagfreq:
                    if tag[0].startswith('{') and tag[0].endswith('}'):
                        tag[0] = uniparser.parseDelaf(tag[0][1:-1])
                    else:
                        tag[0] = uniparser.delasToDelaf(uniparser.textToDelas(tag[0]))
            with open(self.corpus_directory+'taggedfreq.json','w') as fw:
                fw.write(json.dumps(tagfreq))
        log.completed = True

    def _sequenceAutomata(self):
        # Automato de sequencias
        log = self.logger.task("seq_auto_process")
        log.result = self.unitex.Seq2Grf(
            self.corpus_file,
            '-o'+os.path.abspath(self.corpus_workspace+self.assets['aec_grf']),
            '-a'+os.path.abspath(self.corpus_workspace+self.assets['alp_txt']),
            '--b',
            '-qutf8-no-bom'
        )

        log = self.logger.task("seq_auto_parsing")
        log.began = True
        with open(self.corpus_workspace+self.assets['aec_grf']) as fr:
            with open(self.corpus_directory+'aec.json','w') as fw:
                fw.write(json.dumps(uniparser.parseGrf(fr.read().splitlines())))
        log.completed = True

        self.logger.done = True

    def planPreprocessing(self):
        self.logger.planTasks(10)
        if len(self.assets['dela_bin_dics'])>0:
            self.logger.planTasks(5)
        self._executionPlan.append(self._preprocess)

    def planFstText(self):
        self.logger.planTasks(7)
        self._executionPlan.append(self._fstText)

    def planSequenceAutomata(self):
        self.logger.planTasks(2)
        self._executionPlan.append(self._sequenceAutomata)

    def planAll_shortcut(self):
        self.planPreprocessing()
        self.planFstText()
        self.planSequenceAutomata()

    def executePlanning(self):
        try:
            while len(self._executionPlan)>0:
                call = self._executionPlan[0]
                del self._executionPlan[0]
                call()
        except:
            traceback.print_exc()
        self.logger.done = True

    @staticmethod
    def get_dumb_one():
        return UnitexActions(dumbMode = True)

    @staticmethod
    def get_languages():
        return UnitexActions.get_dumb_one().langNameFs

    @staticmethod
    def _get_volumes():
        d = UnitexActions.get_dumb_one()
        c = d._workspaces_container
        return [v for v in os.listdir(c) if os.path.isdir(c+v)]

    @staticmethod
    def reopen(proj_id):
        return UnitexActions(volume_id=proj_id, lang=None)

    @staticmethod
    def reopen_all():
        return [UnitexActions.reopen(v) for v in UnitexActions._get_volumes()]

    @staticmethod
    def reopen_list():
        return [v for v in UnitexActions._get_volumes()]

    @property
    def status(self):
        s = dict()
        s['logs'] = self.logger._jsonable
        return s

    @property
    def _jsonable(self):
        j = dict()
        j['status'] = self.status
        j['results'] = {
            'aec': None,
            'fsttext': None,
            'fsttexttagged': None,
            'sentences': None,
            'wordfreq': None,
            'wordlist': None,
            'tagfreq': None,
            'taggedfreq': None,
        }
        for key in j['results'].keys():
            try:
                with open(self.corpus_directory+key+'.json') as f:
                    j['results'][key] = json.loads(f.read())
            except:
                pass
        j['id'] = self.id
        j['age'] = self.newestAge
        return j

    @property
    def _fileList(self):
        return [
            os.path.join(dirname, filename)
            for dirname, dirnames, filenames in os.walk(self.corpus_directory)
            for filename in filenames
            if not os.path.join(dirname, filename).startswith(self.corpus_workspace)
        ]

    @property
    def oldestFile(self):
        return min(self._fileList, key=lambda fn: os.stat(fn).st_mtime)

    @property
    def newestFile(self):
        return max(self._fileList, key=lambda fn: os.stat(fn).st_mtime)

    @property
    def oldestAge(self):
        return time.time()-os.stat(self.oldestFile).st_mtime

    @property
    def newestAge(self):
        return time.time()-os.stat(self.newestFile).st_mtime

    def delete(self):
        shutil.rmtree(os.path.abspath(self._workspace_volume(self.volume_id)))

    def __repr__(self):
        return json.dumps(self._jsonable)

    def __str__(self):
        return os.path.abspath(self._workspaces_container)
