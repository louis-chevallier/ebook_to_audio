from html.parser import HTMLParser
from kokoro import KPipeline
from IPython.display import display, Audio
import soundfile as sf
import torch
from utillc import *
import numpy as np
import ebooklib
from ebooklib import epub
from pydub import AudioSegment

pipeline = KPipeline(lang_code='f',device="cuda")

fr_text = """J’y ai trouvé je crois l’occasion d’une réconciliation avec mes amours de jeunesse, Holmes, Lupin, Poirot, Maigret.
Cette formule est d’ailleurs imprécise.
Ce n’est pas comme si j’avais cessé de les fréquenter.
Ils n’ont au contraire jamais cessé de m’accompagner.
Eux, d’ailleurs, et non pas l’intrigue policière prise en elle-même.
Ce sont des héros que j’ai aimé suivre, plus que des intrigues que j’ai aimé résoudre.
Suivre comme on peut suivre Phileas Fogg ou Montecristo.
On aime Phileas Fogg parce qu’il nous apprend à voyager sans se perdre ; Montécristo, parce qu’il venge les offenses qui nous ont été faites.
La question qui se pose alors c’est de savoir pourquoi j’ai voulu créer un héros pour le suivre, un héros à aimer  ?
Simplement parce que la vie tout entière, comme dans l’épître de Paul, m’est toujours apparue « comme en miroir, en énigme », et que j’ai plaisir à me faire aider d’un personnage de fiction pour m’en approcher.
Un personnage que son talent, sa complexion, sa vocation précisément de déchiffreur d’énigmes rendent agréable à suivre.
L’essentiel, ce n’est pas le crime, c’est la vérité des caractères.
"""
fr_text = "On aime Phileas Fogg parce qu’il nous apprend à voyager sans se perdre ; Montécristo, parce qu’il venge les offenses qui nous ont été faites. "

fr_text = """
Il est difficile de rester empereur en présence d'un médecin, et difficile aussi de garder sa qualité d'homme.
L'œil du praticien ne voyait en moi qu'un monceau d'humeurs, triste amalgame de lymphe et de sang.
Ce matin, l'idée m'est venue pour la première fois que mon corps, ce fidèle compagnon, cet ami plus sûr, mieux connu de moi que mon âme, n'est qu'un monstre sournois qui finira par dévorer son maître.
"""


fr_text = """
Paul était remonté de l’étable un peu plus tôt, se réjouissant de n’avoir plus d’herbe fauchée ni de récoltes d’aucune sorte à la merci des aléas météorologiques ; il avait allumé le plafonnier et raconté les folies de Lola, la chienne, que tout orage, si modeste fût-il, poussait à d’étranges extrémités ; elle était pour l’heure en bas, réfugiée et réduite à sa plus mince expression, pliée en mille sous l’évier dans le placard des produits de ménage qu’elle avait dévasté sans vergogne pour s’introduire en son tréfonds. On avait ri et mangé distraitement en comptant les éclairs, tandis que Paul racontait comment les oncles, quand ils étaient jeunes, avaient vu le trait de feu de la foudre traverser de part en part la grande salle, de la porte à la fenêtre du fond dont les montants vermoulus avaient été arrachés. Les oncles, les deux, parlaient avec les mêmes mots empesés d’une révérence sourde de cet orage du trait de feu qui leur avait tué trois bêtes jeunes dans le pré du haut. Un peu avant huit heures, le vacarme s’exaspérant, la lumière, après quelques intermittences prémonitoires, s’éteignit, et Paul, impérial, alluma les trois bougies qu’il avait, au moment de passer à table, extraites du tiroir des réserves. Éric s’inquiétait de Lola, on le devinait aux aguets, désemparé par cette brutale défection de la chienne. Dès le premier jour ils s’étaient entendus ; dès le premier soir Éric avait pu prendre Lola dans les bras au grand dam de Nicole, la sœur de Paul, qui s’était étonnée à bas bruit derrière sa frange raide, de voir ainsi conquise, éprise et embrassée, cette bête rétive que l’on avait eu toutes les peines du monde à dresser et qu’il ne faudrait pas déranger en lui faisant trop de manières maintenant qu’elle commençait à aller aux vaches comme il faut et à se rendre utile, ce qui était le rôle des bêtes dans une ferme ; le gamin devrait le comprendre, à la campagne les bêtes travaillaient on les nourrissait pour ça et pas pour rien ou seulement pour la compagnie comme en ville où on avait les moyens peut-être. 
"""

text = '''
[Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.
'''
voice = "af_heart"
voice = "ff_siwis"

book_name, file_in = "le grand troupeau", "/mnt/NUC/download/Le Grand troupeau -- Giono Jean [Giono Jean] -- 1972 -- Gallimard -- 5716ff776f50d54d8e3fc54a820dc84a -- Anna’s Archive.epub"
book = epub.read_epub(file_in)

words_per_block = 1000

class HTMLFilter(HTMLParser):
    """
    Source: https://stackoverflow.com/a/55825140/1209004
    """
    i = 0
    words = []
    def handle_data(self, data):
        save_path = 'out/output.wav'
        self.words += data.split()
        #EKOX(len(self.words))
        while len(self.words) > words_per_block :
            EKOX(self.i)
            #EKOX(data)
            #EKOX(" ".join(self.words[0:words_per_block]))
            self.gen()
            self.words = self.words[words_per_block: ]
            content = ""
    def end(self) :
        EKOX(len(self.words))

    def gen(self) :
        EKOX(len(self.words))
        txt = " ".join(self.words)
        generator = pipeline(txt, voice=voice, speed=0.8, split_pattern=r'\n+')        
        a = np.hstack([ audio for i, (gs, ps, audio) in enumerate(generator)])
        sf.write("out.wav", a, 24000)
        AudioSegment.from_wav("out.wav").export("%s_%03d.mp3" % (book_name, self.i), format="mp3")
        self.i += 1

f = HTMLFilter()

for item in book.get_items():
    if item.get_type() == ebooklib.ITEM_DOCUMENT:
        #EKO()
        bodyContent = item.get_body_content().decode()
        f.feed(bodyContent)
EKO()
f.end()
EKO()



EKOX(a.shape)


