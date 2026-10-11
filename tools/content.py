"""Conteúdo estruturado do guia aula a aula (nível iniciante).

Fonte única: gera os .md de plano/iniciante/aulas/ e o PDF do guia.
"""

# --------------------------------------------------------------------------- vídeos
# id -> (título, quem, credencial curta, url)
V = {
    "shadow101": ("How to Shadow Box 101", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=fWfsbL2ulj8"),
    "basics_tj": ("Basics of Boxing — Training for Beginners at Home", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=kKDHdsVN0b8"),
    "stance_wrong": ("Your Boxing Stance is Wrong", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=e2S6-gwR0es"),
    "roach_basics": ("Freddie Roach teaching boxing basics", "Freddie Roach", "Hall of Fame, treinador de Pacquiao", "https://www.youtube.com/watch?v=uUTWcGol3CY"),
    "footwork1": ("#1 Boxing Footwork Drill for Beginners", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=v0y86288Wt0"),
    "roach_shadow": ("Boxing Drill Notes #1 — Shadow Boxing and Footwork", "Freddie Roach", "Hall of Fame", "https://www.youtube.com/watch?v=15G47Yp1e1I"),
    "pivot": ("How To Pivot in Boxing 101", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=72M0E5LM92M"),
    "olympic_fw": ("Olympic Boxing Footwork Drills", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=gvdWLS-Y-2M"),
    "jab_tj": ("How to throw a jab", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=odM78vAS86M"),
    "jab_atlas": ("Teddy Atlas on How to Improve Your Jab", "Teddy Atlas", "treinou Tyson (amador) e Moorer (campeão)", "https://www.youtube.com/watch?v=geagJaTewsY"),
    "jab_roach": ("Freddie Roach — The Jab (TITLE Boxing)", "Freddie Roach", "Hall of Fame", "https://www.youtube.com/watch?v=HU8LxzWzTac"),
    "jab_lewis": ("Lennox Lewis on the Jab", "Lennox Lewis", "ouro olímpico 1988, campeão indiscutível", "https://www.youtube.com/watch?v=3jbTmHRHhC8"),
    "cross_tj": ("How to Throw the Perfect Cross", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=sK-6Ujp3KYY"),
    "cross_roach": ("Mitt Work Notes #15 — Throwing the Right Hand", "Freddie Roach", "Hall of Fame", "https://www.youtube.com/watch?v=j3YJyXe57_0"),
    "onetwo": ("How to Throw a 1-2", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=vyTaKpylOcU"),
    "hook_tj": ("How to throw a hook punch", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=UFVDcNDnpoU"),
    "hook_roach": ("Heavy Bag Notes #5 — Left Hook", "Freddie Roach", "Hall of Fame", "https://www.youtube.com/watch?v=cHkUm_XMntM"),
    "upper_tj": ("The Correct Way to Throw Uppercut", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=eBxn21FtqPg"),
    "upper_roach": ("Uppercuts — Freddie Roach (TITLE)", "Freddie Roach", "Hall of Fame", "https://www.youtube.com/watch?v=8uwaPQFraqg"),
    "body_tj": ("Master the Jab to the Body", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=Xy54UGeUDyM"),
    "body_hatton": ("How to Throw a Bodyshot", "Ricky Hatton", "campeão mundial em 2 categorias", "https://www.youtube.com/watch?v=xmdzcfwQApU"),
    "defend_best": ("Olympic Boxer Reveals the Best Way to Defend a Punch", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=a07NnmSmJqU"),
    "defend_any": ("How to Defend Any Punch in Boxing", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=ReD58z0jFJM"),
    "slip_atlas": ("Slip the Jab — Teddy Atlas", "Teddy Atlas", "treinador de campeão mundial", "https://www.youtube.com/watch?v=FHEv5EF91CY"),
    "slip_roach": ("Defense Notes #3 — Slip / Under", "Freddie Roach", "Hall of Fame", "https://www.youtube.com/watch?v=-Qdn-BjKGxo"),
    "block_roach": ("Defense Notes #2 — Blocking Counter Punches", "Freddie Roach", "Hall of Fame", "https://www.youtube.com/watch?v=YJIxOai5MOo"),
    "catch_atlas": ("Catch and Pitch", "Teddy Atlas", "treinador de campeão mundial", "https://www.youtube.com/watch?v=ayTCI-SG_uc"),
    "def_roach": ("Boxing Defense Techniques (TITLE)", "Freddie Roach", "Hall of Fame", "https://www.youtube.com/watch?v=wOX3UHc_Pd0"),
    "combos_tj": ("First Combinations You Should Learn", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=9oN2RCx5peY"),
    "combos_atlas": ("Throwing Combination Punches", "Teddy Atlas", "treinador de campeão mundial", "https://www.youtube.com/watch?v=jkDbe2ujzRw"),
    "angles": ("Footwork: create angles with the shift drill", "Precision Striking", "apoio (sem currículo de elite)", "https://www.youtube.com/watch?v=inm9XaTwlRc"),
    "rope_tj": ("How to Jump Rope (Beginner to Expert)", "Tony Jeffries", "bronze olímpico 2008", "https://www.youtube.com/watch?v=wqN5bRkZPK0"),
    "rope_roach": ("Training Notes #1 — jump rope", "Freddie Roach", "Hall of Fame", "https://www.youtube.com/watch?v=ZQE0uq40A-g"),
    "weldon1": ("Becoming a Better Boxer vol. 1 (completo)", "Kenny Weldon", "corner de 18 lutas de título mundial", "https://www.youtube.com/watch?v=vwkjHfR6VPs"),
    "bs_amateur": ("Strength and Conditioning for Amateur Boxing", "Boxing Science", "ciência do esporte, England Boxing", "https://www.youtube.com/watch?v=y-tlaxJvUGk"),
    "bs_power": ("Top 5 Exercises to Improve Punch Power", "Boxing Science", "ciência do esporte", "https://www.youtube.com/watch?v=oAEFPwRYnyc"),
    "fight_loma": ("Lomachenko vs Rigondeaux (2017) — busca", "luta de estudo", "footwork e ângulos", "https://www.youtube.com/results?search_query=Lomachenko+vs+Rigondeaux+2017"),
    "fight_chavez": ("Chávez vs Rosario (1987) — busca", "luta de estudo", "pressão e corpo", "https://www.youtube.com/results?search_query=Julio+Cesar+Chavez+vs+Edwin+Rosario+1987"),
    "fight_whitaker": ("Whitaker vs Chávez (1993) — busca", "luta de estudo", "defesa e contra", "https://www.youtube.com/results?search_query=Pernell+Whitaker+vs+Julio+Cesar+Chavez+1993"),
    "fight_hearns": ("Thomas Hearns — jab e distância (busca)", "luta de estudo", "modelo para atleta alto e magro", "https://www.youtube.com/results?search_query=Thomas+Hearns+jab+highlights"),
    "fight_inoue": ("Inoue vs Fulton (2023) — busca", "luta de estudo", "jab e distância", "https://www.youtube.com/results?search_query=Inoue+vs+Fulton+2023"),
    "fight_ali": ("Ali vs Cleveland Williams (1966) — busca", "luta de estudo", "Ali no auge", "https://www.youtube.com/results?search_query=Muhammad+Ali+vs+Cleveland+Williams+1966"),
}

# --------------------------------------------------------------------------- blocos padrão
WARMUP = {
    1: ["Corda: 3 × 2 min (30 s de descanso). Pulo básico com os dois pés, baixo e leve, na planta dos pés.",
        "Protocolo de ombro (~4 min): rotação externa deitado de lado 2×12 por braço · Y-T-W 1×8 de cada letra · flexão escapular 1×12 · alongamento de peitoral menor no batente 2×20 s por lado · círculos de braço.",
        "Mobilidade (2 min): rotação de quadril, tornozelo, agachamento profundo segurando 30 s, rotação torácica de quatro apoios."],
    2: ["Corda: 3 × 2 min. Alterne os pés (\"boxer skip\") e faça 2 pulos rápidos a cada 30 s.",
        "Protocolo de ombro (~4 min), igual ao da fase 1.",
        "Mobilidade (1 min) + 1 round de 2 min de shadowboxing leve, só jab e footwork (revisão da fase 1)."],
    3: ["Corda: 3 × 2 min. Boxer skip, com 10 s de velocidade máxima a cada 40 s.",
        "Protocolo de ombro (~4 min).",
        "1 round de 2 min de shadowboxing leve e livre."],
}

STRENGTH = {
    1: ("Fase 1: aprender os movimentos (2 voltas, 45–60 s entre exercícios)",
        ["Agachamento goblet com halter: 10", "Flexão de braço (inclinada se precisar), cotovelos a ~45°: 8–12",
         "Remada unilateral com halter: 10 por lado (+1 série extra no braço esquerdo)", "Prancha: 30 s",
         "Isometria de pescoço com a mão (frente, trás, lados): 10 s cada"]),
    2: ("Fase 2: força (3 voltas)",
        ["Afundo reverso com halteres: 8 por lado", "Flexão de braço: 8 (desenvolvimento unilateral leve só se o ombro esquerdo estiver com 0 de dor)",
         "Remada unilateral: 10 por lado (+1 série no esquerdo)", "Dead bug: 10", "Farmer walk com halteres pesados: 40 s"]),
    3: ("Fase 3: potência e condicionamento",
        ["3 voltas: 3 saltos verticais máximos + goblet 8 + flexão explosiva 6 (flexão normal se o ombro reclamar). Descanso de 60 s.",
         "Depois, 2 voltas de: 40 s burpee / 20 s descanso / 40 s mountain climber / 20 s descanso."]),
}

COOLDOWN = "Volta à calma (3 min): respiração lenta, alongamento leve, notas do ombro no diário (antes/depois) e 1 erro visto no vídeo."

# --------------------------------------------------------------------------- sessões
# drill: (nome, minutos, [como fazer], [pontos-chave], diagrama|None, [vídeos])
S = []


def add(**k):
    S.append(k)


# ============================== FASE 1 ==============================
add(id="01A", week=1, phase=1, title="Base e guarda",
    goal="Montar a base ortodoxa e a guarda corretas, de forma automática, e dar os primeiros passos sem desmontá-las.",
    pre=["shadow101", "basics_tj", "stance_wrong"],
    tech=[
        ("Montagem da base no espelho", 5,
         ["Fique em pé, com os pés juntos e relaxado.", "Em 1 segundo, monte a base e a guarda.", "Confira o checklist no espelho, relaxe e repita. Faça 20 repetições."],
         ["pé E à frente, um pé em cada \"trilho\"", "calcanhar D levantado", "mão D colada na bochecha", "queixo baixo, cotovelos fechados"], "base", []),
        ("Fita no chão e olhos fechados", 5,
         ["Monte a base e marque a posição dos dois pés com fita crepe.", "Saia da posição, feche os olhos e monte a base de novo.", "Abra os olhos e veja se os pés caíram nas marcas. Faça 10 repetições."],
         ["o corpo precisa \"sentir\" a base certa sem olhar"], None, []),
        ("Step-drag: frente e trás", 5,
         ["Faça 1 passo por vez: o pé da frente sai, o de trás acompanha.", "Pare, confira a base e só então dê o próximo passo.", "Faça 4 × 1 min, alternando frente e trás."],
         ["passos de 10–20 cm", "pés raspando o chão", "a cabeça não sobe nem desce"], "step-drag", ["footwork1"]),
        ("Step-drag: esquerda e direita", 5,
         ["Para a esquerda, o pé E sai primeiro. Para a direita, o pé D sai primeiro.", "Faça 4 × 1 min."],
         ["nunca cruzar os pés", "nunca juntar os pés"], None, []),
    ],
    shadow=("4 rounds de 2 min (1 min de descanso)", [
        "R1: só movimentação nas 4 direções, guarda perfeita, olhar fixo num ponto à frente.",
        "R2: igual ao R1, mas os pés só podem andar dentro de um quadrado de 2 × 2 m.",
        "R3: movimentar → parar → 1 jab devagar → movimentar.",
        "R4: igual ao R3. Grave este round no celular."]),
    focus="A base nunca desmonta: os pés nunca ficam na mesma linha.")

add(id="01B", week=1, phase=1, title="Jab parado",
    goal="Construir o jab com a mecânica certa: sem telegrafar, com volta rápida e com a guarda protegendo.",
    pre=["jab_tj", "roach_basics"],
    tech=[
        ("Revisão da base", 5, ["Faça 10 montagens de base no espelho.", "Faça 2 min de step-drag nas 4 direções."], ["o checklist da sessão 01A"], "base", []),
        ("Jab parado, um detalhe por round", 15,
         ["Faça 5 rounds de 2 min (30 s de descanso), com 1 jab a cada 3–4 s, a 50–70% da velocidade.",
          "Em cada round, foque em um item: (1) sem recuar a mão antes, (2) mão D colada no queixo, (3) volta mais rápido do que vai, (4) ombro E sobe e protege o queixo, (5) expire (\"tss\") em cada jab."],
         ["punho gira no fim", "não travar o cotovelo (ombro E!)", "a mão volta pelo mesmo caminho"], "trajetorias", ["jab_tj"]),
    ],
    shadow=("4 rounds de 2 min", [
        "R1: drill da caixa com a fita no chão (frente → direita → trás → esquerda).",
        "R2: jab parado + 1 passo para trás.",
        "R3: jab duplo (1-1) parado.",
        "R4: livre, com jab e footwork. Grave."]),
    focus="A mão de trás fica colada no rosto o tempo todo.", diagrams_extra=["caixa"])

add(id="02A", week=2, phase=1, title="Jab em movimento",
    goal="Coordenar o pé e a mão: jab entrando e jab saindo.",
    pre=["jab_atlas", "jab_roach", "jab_lewis"],
    tech=[
        ("Step-drag duplo", 5, ["Dê 2 passos seguidos em cada direção e confira a base no fim.", "Faça 5 min no total."], ["a base não muda de formato"], "step-drag", []),
        ("Jab entrando", 7, ["O pé da frente e o punho chegam juntos ao alvo; o pé de trás acompanha.", "Faça 3 × 2 min."], ["o peso não passa do joelho da frente", "volte à guarda antes do próximo"], None, []),
        ("Jab saindo", 8, ["Jab parado e, logo depois, 1 passo para trás (o pé D sai primeiro).", "Faça 3 × 2 min."], ["saia com a guarda alta", "não incline o tronco para trás"], None, []),
    ],
    shadow=("5 rounds de 2 min", [
        "R1: jab entrando.", "R2: jab saindo.", "R3: 1-1 entrando, depois passo para trás.",
        "R4: jab + passo lateral (esquerda ou direita).", "R5: livre, com jab e footwork. Grave."]),
    focus="O jab volta mais rápido do que vai.")

add(id="02B", week=2, phase=1, title="Direto (2) e 1-2",
    goal="Aprender o direto com o giro do pé de trás e do quadril, e juntá-lo ao jab.",
    pre=["cross_tj", "cross_roach"],
    tech=[
        ("Direto lento, um detalhe por round", 10,
         ["Faça 5 rounds de 1:30 a 50% da velocidade.", "Itens, um por round: giro do calcanhar D para fora · quadril gira · mão E fica no rosto · cabeça não passa do joelho da frente · volta pela mesma linha."],
         ["o soco começa no chão"], "cadeia-cinetica", ["cross_tj"]),
        ("1-2 parado", 10, ["Primeiro lento, depois médio. Faça 4 × 2 min."], ["o 1 \"abre\" e o 2 \"fecha\"", "as duas mãos voltam à guarda"], "trajetorias", ["onetwo"]),
    ],
    shadow=("5 rounds de 2 min", [
        "R1–R2: 1-2 parado, lento.", "R3: 1 entrando, 2 parado.", "R4: 1-2 e passo para trás.", "R5: livre com jab, direto e footwork."]),
    focus="Direto com o giro do pé de trás e a mão esquerda no rosto.")

add(id="03A", week=3, phase=1, title="Potência do 2 e velocidade do 1-2",
    goal="Fazer a força vir do chão e treinar o 1-2 em três velocidades sem perder a técnica.",
    pre=["onetwo", "roach_shadow"],
    tech=[
        ("\"Esmagar a barata\"", 5, ["Gire o pé de trás sem socar, 20 vezes.", "Depois faça 20 diretos com o mesmo giro."], ["o calcanhar D gira para fora", "o quadril vai junto"], "cadeia-cinetica", []),
        ("1-2 em 3 velocidades", 15, ["2 min lento, 2 min médio e 1 min rápido. Repita o ciclo 3 vezes."], ["se a técnica quebrar no rápido, volte para o médio"], None, []),
    ],
    shadow=("5 rounds de 2 min", [
        "R1: 1-2 parado.", "R2: 1-2 entrando e saída para trás.", "R3: 1-1-2.",
        "R4: introdução ao 2 no corpo, abaixando com as pernas.", "R5: livre. Grave e compare com o vídeo da semana 1."]),
    focus="Respire em cada golpe.")

add(id="03B", week=3, phase=1, title="Pivô",
    goal="Aprender a mudar de ângulo sem desmontar a base.",
    pre=["pivot", "footwork1"],
    tech=[
        ("Pivô no pé da frente", 10, ["Faça 4 × 2 min, devagar, alternando o sentido A e o sentido B.", "Depois de cada pivô, confira a base no espelho."], ["o pé E gira na planta", "o pé D descreve um arco", "a guarda não cai"], "pivo", ["pivot"]),
        ("1-2 + pivô", 10, ["Faça o 1-2 e em seguida o pivô. 4 × 2 min."], ["termine o pivô já na base, pronto para golpear de novo"], None, []),
    ],
    shadow=("5 rounds de 2 min", [
        "R1: footwork completo (4 direções e diagonais).", "R2: 1-2 + pivô.", "R3: 1-1-2 + passo lateral.",
        "R4: round \"chamada\": grave um áudio com \"1\", \"1-1\", \"1-2\", \"1-1-2\", \"passo\", \"pivô\" em intervalos aleatórios e reaja.", "R5: livre."]),
    focus="Pergunte ao professor qual sentido de pivô ele quer que você priorize.")

add(id="04A", week=4, phase=1, title="Consolidação da fase 1",
    goal="Qualidade total em tudo o que foi aprendido.",
    pre=["olympic_fw", "shadow101", "weldon1"],
    tech=[
        ("Revisão em circuito", 20, ["Base 2 min · step-drag 3 min · jab parado, entrando e saindo 5 min · direto 5 min · 1-2 + pivô 5 min."], ["filme 1 minuto de cada bloco"], None, []),
    ],
    shadow=("5 rounds de 2 min", ["R1: jab.", "R2: direto.", "R3: footwork.", "R4: pivô.", "R5: livre."]),
    focus="Peça ao professor: \"qual é o meu maior erro hoje?\"")

add(id="04B", week=4, phase=1, title="AVALIAÇÃO 1",
    goal="Medir objetivamente a fase 1 e decidir se você avança ou repete.",
    pre=[],
    tech=[
        ("Avaliação filmada", 30, ["Faça os itens 1 a 8 de avaliacoes/avaliacao-iniciante.md, filmando de frente e de lado.", "Dê nota 0, 1 ou 2 a cada item."], ["meta: 12 ou mais, sem nenhum 0"], None, []),
        ("Correção", 15, ["Use o resto do tempo para corrigir o item com a pior nota."], [], None, []),
    ],
    shadow=None, strength_override="Sem bloco D. Refaça os testes físicos da semana 0 e anote.",
    focus="Mande ao coach as notas e 3 observações.")

# ============================== FASE 2 ==============================
add(id="05A", week=5, phase=2, title="Gancho de esquerda (3)",
    goal="Gancho curto e potente, com a força vindo do giro do pé da frente.",
    pre=["hook_tj", "hook_roach"],
    tech=[
        ("Giro do pé da frente", 5, ["Gire o calcanhar E para fora, sem soco, 20 vezes devagar."], ["o quadril acompanha o pé"], None, []),
        ("Gancho parado, um detalhe por round", 10, ["Faça 5 × 1:30. Itens, um por round: cotovelo na altura do punho · giro do pé · curto · mão D no rosto · expirar."], ["o braço é um \"gancho\" rígido de ~90°", "posição do punho: siga o seu professor"], "trajetorias", []),
        ("2-3", 5, ["O direto gira o quadril e \"carrega\" o gancho. Faça 2 × 2 min."], [], None, []),
    ],
    shadow=("5 rounds de 2:30", ["R1: 1-2 (revisão).", "R2: 1-2-3 lento.", "R3: 1-2-3 e passo para trás.", "R4: 1-1-2-3.", "R5: livre com 1, 2 e 3."]),
    focus="Gancho curto, girando o pé da frente.")

add(id="05B", week=5, phase=2, title="Bloqueio e parry",
    goal="As primeiras camadas de defesa: absorver e desviar.",
    pre=["defend_best", "block_roach", "catch_atlas"],
    tech=[
        ("Bloqueios na chamada", 10, ["Diga o golpe em voz alta e bloqueie: jab (5×), direto (5×), gancho E e D (5× cada), corpo (5×). Faça 4 rounds de 2 min."], ["a luva fica colada, não vai \"buscar\" o golpe", "contra gancho: luva na têmpora, cotovelo alto"], None, []),
        ("Parry do jab", 10, ["Toque curto de 5–10 cm com a mão D e volta imediata. Faça 3 × 2 min."], ["sem \"abanar\" a mão"], None, []),
    ],
    shadow=("5 rounds de 2:30", ["R1: 1-2-3.", "R2: bloqueio + 1-2.", "R3: parry + 2.", "R4: 1-2-3 + bloqueio do gancho dele.", "R5: livre."]),
    focus="Depois de defender: golpeie ou saia.")

add(id="06A", week=6, phase=2, title="Corpo, gancho de direita e uppercuts",
    goal="Completar o arsenal: golpes no corpo, o 4, o 5 e o 6.",
    pre=["upper_tj", "upper_roach", "body_tj", "body_hatton"],
    tech=[
        ("Abaixar com as pernas: 2b e 3b", 7, ["Faça 3 × 2 min, descendo pelos joelhos e não dobrando a coluna."], ["olhos à frente, nunca no chão", "suba já protegido"], None, []),
        ("Uppercuts 5 e 6", 8, ["Faça 4 × 1:30. São curtos, saem da flexão do joelho do mesmo lado."], ["não baixar a mão antes", "cotovelo a ~90°"], "trajetorias", []),
        ("Gancho de direita (4)", 5, ["Curto, no corpo e na cabeça. Faça 2 × 2 min."], [], None, []),
    ],
    shadow=("5 rounds de 2:30", ["R1: 1-2-3.", "R2: 1-2-3b.", "R3: 3b-3 (corpo e cabeça com a mesma mão).", "R4: 1-6-3-2 lento.", "R5: livre com todos os golpes."]),
    focus="Abaixe com as pernas para os golpes no corpo.")

add(id="06B", week=6, phase=2, title="Slip e roll",
    goal="Movimento de cabeça e tronco para sair da linha do golpe.",
    pre=["slip_atlas", "slip_roach", "defend_any"],
    tech=[
        ("Slip sem soco", 5, ["Slip do jab (cabeça para a sua direita) e slip do direto (cabeça para a sua esquerda), no espelho."], ["só 10–15 cm", "o joelho do mesmo lado dobra", "olhos no alvo"], "slip", []),
        ("Slip + resposta", 5, ["Slip do jab e devolve um 2; slip do direto e devolve um 3."], [], None, []),
        ("Roll na corda", 10, ["Estique uma corda na altura dos ombros e atravesse por baixo dela de um lado para o outro. Faça 4 × 2 min."], ["desça pelos joelhos, em \"U\"", "a guarda fica colada"], "bob-weave", []),
    ],
    shadow=("5 rounds de 2:30", ["R1: slip, slip, 1-2.", "R2: roll + 3 ao subir.", "R3: 1-2 + slip + 2.", "R4: na corda, roll por baixo + 1-2 do outro lado.", "R5: livre."]),
    focus="Slip com os olhos no adversário.")

add(id="07A", week=7, phase=2, title="Defesa integrada (rounds de 3 min)",
    goal="Ataque e defesa como um fluxo contínuo.",
    pre=["def_roach", "defend_any"],
    tech=[
        ("Defesa e ataque", 10, ["O adversário imaginário lança 1-2; você bloqueia ou faz slip e responde com 2-3. Faça 5 × 2 min."], [], None, []),
        ("Ataque e defesa", 10, ["Você lança 1-2-3, ele responde com um gancho, você faz roll e sai em pivô. Faça 5 × 2 min."], ["todo combo termina com defesa ou saída"], None, []),
    ],
    shadow=("4 rounds de 3 min", ["R1: ataque e defesa.", "R2: defesa e ataque.", "R3: corpo e cabeça.", "R4: livre. Grave."]),
    focus="Todo combo termina com defesa ou saída.")

add(id="07B", week=7, phase=2, title="Combinações de 4 golpes + chamada",
    goal="Fluidez nas combinações longas e reação a comandos.",
    pre=["combos_tj", "combos_atlas"],
    tech=[
        ("1-2-3-2 e 1-6-3-2", 10, ["Faça em 3 velocidades (lento, médio e rápido)."], ["o quadril alterna o giro a cada golpe"], None, []),
        ("Chamada com defesas", 10, ["Grave um áudio: \"1-2… slip… roll… 3b-3… bloqueia…\" e reaja."], [], None, []),
    ],
    shadow=("4 rounds de 3 min", ["R1: só defesa, nenhum soco.", "R2: chamada.", "R3: pressão, você avança.", "R4: livre."]),
    focus="Mantenha a guarda nos últimos 30 s de cada round.")

add(id="08A", week=8, phase=2, title="Consolidação da fase 2",
    goal="Revisar e polir o arsenal completo.",
    pre=["combos_tj"],
    tech=[("Revisão", 20, ["Todos os golpes e defesas, 2 min cada, com foco no item mais fraco da avaliação 1."], [], None, [])],
    shadow=("4 rounds de 3 min", ["R1: ataque.", "R2: defesa.", "R3: corpo.", "R4: livre."]),
    focus="Pergunte ao professor quando você pode começar o sparring técnico leve.")

add(id="08B", week=8, phase=2, title="AVALIAÇÃO 2",
    goal="Medir a fase 2.",
    pre=[],
    tech=[("Avaliação filmada", 30, ["Itens 1 a 16 de avaliacoes/avaliacao-iniciante.md."], ["meta: itens 9–16 com 11 ou mais e a fase 1 com 13 ou mais"], None, []),
          ("Correção", 15, ["Corrija o pior item."], [], None, [])],
    shadow=None, strength_override="Sem bloco D. Refaça os testes físicos.",
    focus="Mande os resultados ao coach.")

# ============================== FASE 3 ==============================
add(id="09A", week=9, phase=3, title="Ângulos",
    goal="Nunca terminar uma combinação parado na frente do adversário.",
    pre=["angles", "fight_loma", "fight_hearns"],
    tech=[
        ("Saídas em ângulo", 10, ["1-2 e passo lateral · 1-2-3 e pivô · 1-2 e diagonal para trás. Faça 5 × 2 min."], [], None, []),
        ("Drill do X", 10, ["Combine no centro do X de fita, saia em diagonal por um dos braços e volte."], ["recuar em linha reta é proibido"], "x-drill", []),
    ],
    shadow=("4 rounds de 3 min", ["R1: combina e sai em ângulo.", "R2: ele pressiona, você recua em ângulo e contra-ataca.", "R3: corpo e cabeça + ângulo.", "R4: livre. Grave."]),
    focus="Mude de ângulo depois de combinar.")

add(id="09B", week=9, phase=3, title="Ritmo e fintas",
    goal="Tornar-se imprevisível.",
    pre=["shadow101"],
    tech=[("Fintas e mudança de ritmo", 20, ["Finta de jab (com o ombro) e 2 · finta de 2 e 3 · jab no corpo e jab na cabeça. Use pausas e mudanças de velocidade. Faça 6 × 2 min."], ["a finta precisa parecer o golpe de verdade"], None, [])],
    shadow=("4 rounds de 3 min", ["R1: fintas.", "R2: chamada.", "R3: contra-ataque (só responde depois de defender).", "R4: livre."]),
    focus="Respire e solte os ombros.")

add(id="10A", week=10, phase=3, title="Pressão",
    goal="Cortar o ringue e entrar com defesa, no estilo de Chávez, Frazier e Tyson.",
    pre=["fight_chavez"],
    tech=[
        ("Cortar o ringue", 10, ["Dê passos laterais acompanhando o adversário imaginário e mantenha-o contra a parede, usando o jab para fechar a saída."], ["vá para onde ele vai, não para onde ele está"], "cortar-ringue", []),
        ("Entrar com defesa", 10, ["Roll e 3b-3 · slip e 6-3-2."], [], None, []),
    ],
    shadow=("4 rounds de 3 min", ["Todos os rounds são de pressão, alternando cabeça e corpo."]),
    focus="Se o professor liberar, faça o primeiro sparring técnico leve (20–30% de força).")

add(id="10B", week=10, phase=3, title="Contra-ataque",
    goal="Defender e responder, no estilo de Whitaker, Mayweather e Márquez.",
    pre=["fight_whitaker"],
    tech=[("Os 4 contras clássicos", 20, ["Parry do jab e 2 · slip do jab e 2 · slip do direto e 3 · roll do gancho e 3 · bloqueio do 2 e 1-2. Faça 4 blocos de 5 min."], [], "slip", [])],
    shadow=("4 rounds de 3 min", ["Todos os rounds são de contra-ataque, recuando em ângulo."]),
    focus="Como você é alto (1,80 m a 70 kg), seu jogo natural é de distância: jab e contra.")

add(id="11A", week=11, phase=3, title="Técnica sob cansaço",
    goal="Manter a técnica intacta quando o gás acaba.",
    pre=["bs_amateur"],
    tech=[("Drill de exaustão técnica", 20, ["30 s de burpee ou mountain climber e, imediatamente, 1 min de 1-2-3-slip-2 perfeito, filmado. Faça 6 ciclos."], ["confira no vídeo: queixo, mão de trás e base"], None, [])],
    shadow=("4 rounds de 3 min", ["Os últimos 30 s de cada round são em intensidade máxima, sem perder a guarda."]),
    focus="Mantenha a forma no último round, com o queixo baixo mesmo cansado.")

add(id="11B", week=11, phase=3, title="Simulação de luta amadora",
    goal="Viver o formato de 3 × 3 min.",
    pre=["fight_inoue"],
    tech=[("Revisão dos 3 piores itens", 20, ["Use a avaliação 2 para escolher os itens."], [], None, [])],
    shadow=("4 rounds de 3 min", ["R1: estudo e jab.", "R2: pressão.", "R3: tudo.", "R4: livre e leve."]),
    focus="Sparring técnico, se o professor liberar.")

add(id="12A", week=12, phase=3, title="Polimento",
    goal="Chegar descansado à avaliação final.",
    pre=["fight_ali"],
    tech=[("Revisão leve", 30, ["Revise tudo a 70%, priorizando a qualidade."], [], None, [])],
    shadow=("3 rounds de 3 min", ["Qualidade máxima."]),
    strength_override="Sem bloco D pesado: só mobilidade.",
    focus="Peça ao professor uma avaliação honesta: você está pronto para o sparring técnico regular?")

add(id="12B", week=12, phase=3, title="AVALIAÇÃO FINAL DO INICIANTE",
    goal="Decidir a passagem para o bloco pré-competitivo (semanas 13–26).",
    pre=[],
    tech=[("Avaliação completa filmada", 45, ["Todos os itens de avaliacoes/avaliacao-iniciante.md e os testes físicos."], ["meta: 36 ou mais de 44, nenhum 0, e o OK do professor"], None, [])],
    shadow=None, strength_override="Sem bloco D.",
    focus="Mande tudo ao coach: notas, vídeos e o que o professor disse.")
