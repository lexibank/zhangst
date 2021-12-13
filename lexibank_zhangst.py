from pathlib import Path
import lingpy as lp

from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank.util import getEvoBibAsBibtex
from pylexibank import progressbar
from pylexibank import Concept, Language, Lexeme
import attr

@attr.s
class CustomConcept(Concept):
    Number = attr.ib(default=None)


@attr.s 
class CustomLanguage(Language):
    Number = attr.ib(default=None)
    Subgrouping = attr.ib(default=None)
    GroupID = attr.ib(default=None)
    SubgroupingName = attr.ib(default=None)
    SubGroup = attr.ib(default=None)


@attr.s
class CustomLexeme(Lexeme):
    STEDTID = attr.ib(default=None)
    GlossInSource = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'zhangst'
    concept_class = CustomConcept
    language_class = CustomLanguage
    lexeme_class = CustomLexeme

    def cmd_download(self, args):

        self.raw_dir.xlsx2csv("Table S1. Sino-Tibetan Language Information and root-meanings.xlsx")
        

    def cmd_makecldf(self, args):
    
        concepts = {}

        for concept in self.concepts:
            idx = '{0}_{1}'.format(concept["NUMBER"], slug(concept["ENGLISH"]))
            args.writer.add_concept(
                    ID=idx,
                    Number=concept["NUMBER"],
                    Name=concept["ENGLISH"],
                    #Concepticon_ID=concept.concepticon_id,
                    #Concepticon_Gloss=concept.concepticon_gloss,
                    )
            concepts[concept["ENGLISH"]] = idx
        
        
        languages = args.writer.add_languages(
                lookup_factory="Name", id_factory=lambda x: slug(x['Name']))
        
        args.writer.add_sources()

        data = self.raw_dir.read_csv(
                "Table S1. Sino-Tibetan Language Information and root-meanings.LexicalData.csv",
                dicts=False)
        meanings = data[1][9:]
        roots = data[3][9:]
        cogids = data[0][9:]

        for row in data[7:]:
            language = row[1]
            for i, val in enumerate(row[9:]):
                concept = meanings[i]
                root = roots[i]
                cogid = cogids[i]
                if val == "1":
                    lexeme = args.writer.add_form(
                            Language_ID=languages[language],
                            Parameter_ID=concepts[concept],
                            Value=root,
                            Form=root,
                            Source="Zhang2019",
                            Cognacy=cogid,
                            )
                    args.writer.add_cognate(
                            lexeme=lexeme,
                            Cognateset_ID=cogid,
                            Cognate_Detection_Method="expert",
                            Source="Matisoff2015"
                            )
       
