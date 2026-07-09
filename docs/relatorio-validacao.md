# Relatório de validação · dataset completo (bncc.dev, protótipo)

EF 1304 + EM 183 + EI 93 = **1580 aprendizagens** · 10 competências gerais · 105 específicas · 885 contextos de organização

## Contratos

- ✅ 1. Gramática: todos os códigos decodificam
- ✅ 2. EF: 1.304 habilidades
- ✅ 2. EF: contagem por componente
- ✅ 2. EM: 183 = LGG 28 + LP 54 + MAT 43 + CNT 26 + CHS 32
- ✅ 2. EI: 93 objetivos (EO 20, CG 15, TS 9, EF 27, ET 22)
- ✅ 2. Competências: 10 gerais + 105 específicas (84 EF + 21 EM)
- ✅ 3. Integridade referencial (organização, objetos, competências)
- ✅ 3. Organização por layout: LP=campo_pratica, LI=eixo, demais=unidade_tematica
- ✅ 4. EM área: competência coerente com o dígito do código
- ✅ 4. EM LP: 1..n competências da planilha
- ✅ 4. Agrupamento: área/componente atribuídos = decodificação do código
- ✅ 4. Competência de componente só em área multi-componente
- ✅ 5. Sem duplicatas
- ✅ 6. Alinhamentos EI: 32; incompletos só onde o quadro oficial tem célula vazia
- ✅ 7. Verificação PDF: 1.576/1.580 ok; 4 divergências conhecidas e documentadas
- ✅ 8. Vigência coerente
- ✅ 9. Completude: nenhum código do PDF fora do dataset
- ✅ 9. Completude: nenhum código do dataset fora do PDF

## Verificação contra o PDF homologado

- `{'ok': 1576, 'divergente': 4}` · 1576/1580 com página registrada em `fonte.localizador_pdf`
- Fila de divergências conhecidas (4):
  - **EM13LP35**: planilha omite "de" ("a quantidade [de] texto e imagem") · PDF prevalece
  - **EF03MA05**: planilha omite ", inclusive os convencionais," · PDF prevalece
  - **EF02MA06**: camada de texto do PDF perde glifos na pág. 285 (dígitos e trecho final) · planilha prevalece, conferência visual feita
  - **EF07MA33**: glifo π ausente da camada de texto do PDF · planilha prevalece

## Completude (varredura de códigos no PDF inteiro)

- Códigos no PDF: 1580 · extraídos: 1580 · faltando: nenhum · sobrando: nenhum

## Diff Profy PEI (EF + EM completos)

- Faltam no PEI: ['EF35LP16']
- Extras no PEI: nenhum
- Textos divergentes: 0

## As 14 consultas do caso âncora

- **C1: componentes disponíveis para aluno do 6º ano** → 9: AR, CI, EF, ER, GE, HI, LI, LP, MA
- **C2: habilidades de LP dos anos 3º–6º (flexibilização PEI)** → 238 habilidades
- **C3: agrupadas por prática de linguagem** → Análise linguística/semiótica (Ortografização): 49 · Leitura/escuta (compartilhada e autônoma): 37 · Leitura: 37 · Oralidade: 34 · Análise linguística/semiótica: 32 · Produção de textos (escrita compartilhada e autônoma): 23 · Produção de textos: 21 · Oralidade *Considerar todas as habilidades dos eixos leitura e produção que se referem a textos ou produções orais, em áudio ou vídeo: 3 · Escrita (compartilhada e autônoma): 2
- **C4: registro completo de EF67LP08** → anos [6, 7], campos ['Campo jornalístico/midiático'], prática Leitura, 1 objetos, fonte: Base-Nacional-Comum-Curricular-BNCC.pdf, página PDF 167
- **C5: decodificar código colado ("em13lgg103")** → {"codigo": "EM13LGG103", "etapa": "EM", "seriacao": null, "area": "LGG", "area_nome": "Linguagens e suas Tecnologias", "competencia_especifica": 1, "sequencia": 3}
- **C6: busca textual "frações" em Matemática** → 9: EF04MA09, EF04MA26, EF05MA03, EF05MA04, EF06MA07, EF06MA09, EF07MA08, EF07MA09…
- **C7: progressão de EF06MA07 via objetos em anos anteriores** → nenhuma por igualdade de slug · dedução exige curadoria (decisão nº 2 do schema)
- **C8: progressão EI entre faixas (campo TS)** → EI01TS01 → EI02TS01 → EI03TS01
- **C9: EM com competência (área e LP)** → LGG103 → ['em-area-lgg-ce-01']; LP02 → ['em-area-lgg-ce-01']
- **C10: EJA segmento → recorte** → eja-1→EF anos iniciais · eja-2→EF anos finais · eja-3→EM
- **C11: cobertura · habilidades de MA do 4º ano** → 28 habilidades
- **C12: fonte oficial citável** → 1483/1487 com página do PDF homologado
- **C13: filtro de vigência** → 1487 vigentes; filtro operacional (nenhuma revogada no dado atual)
- **C14: sugerir adaptação da habilidade** → fora do dado de referência (inteligência do produto) · por desenho

## Decisões de interpretação

Consolidadas em `saida/DECISOES.md` (8 entradas) + `decisoes-extracao.json` (3 da extração).
