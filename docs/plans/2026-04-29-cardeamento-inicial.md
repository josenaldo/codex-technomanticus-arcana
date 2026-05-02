# Plano de Cardeamento Inicial — 2026-04-29

## Cabeçalho

- **Data:** 2026-04-29
- **Vault HEAD:** `6a4bf7898bdd93c44dda20b4be7f290ab4241d4c` (refactor workspace)
- **Tipo de run:** First run (`.last-carding` vazio) + atualização de stale
- **Total de notas no escopo:** ~89 (12 stale + 77 novas)
- **Decks afetados:** Codex::Arquitetura, Codex::Fundamentos, Codex::Java, Codex::JavaScript, Codex::IA, Codex::Infraestrutura

### Exclusões confirmadas com o usuário

**Pastas inteiras excluídas (não-conteúdo / fora dos decks):**

- `00-Meta/` (guia, mestres, templates, README)
- `01-Pergaminhos/` (inbox, recursos, brag, cursos)
- `02-Glosas/` (fichamentos derivados)
- `04-Sendas/` (MOCs/trilhas)
- `Go/`, `Python/`, `RPA/`, `Inglês/`, `Ferramentas/`, `Entrevistas/` (sem deck mapeado, decisão do usuário em pular)

**MOCs/índices excluídos:**

- `Java/Java.md`, `Java/Backend/Kafka/Kafka.md`, `Java/Backend/Kafka/Kafka Concepts.md`, `Java/Backend/Kafka/Vídeos.md`
- `JavaScript/JavaScript.md`, `JavaScript/Frontend/TypeScript com React/TypeScript com React.md`
- `IA/IA.md`, `IA/Memória de Agentes/Memória de Agentes.md`
- `Infraestrutura/Infraestrutura.md`
- `Java/Core/Helsinki MOOC - Guia de Revisão.md` (guia, não conteúdo)
- `JavaScript/Full Stack Open - Guia de Revisão.md` (guia)
- `README.md`, `index.md`, `.claude/skills/glosa/SKILL.md` (vazaram do detect)

**Notas duvidosas excluídas:**

- `Java/Core/What should you do to stand out as a Java-Spring Boot Developer.md` (meta-carreira)
- `Infraestrutura/Docker credential helpers.md` (how-to muito específico)

### Comando para retomar detecção (se a sessão morrer)

```bash
python3 ~/.agents/skills/arcana-forge/detect_changes.py \
  ~/repos/personal/codex-technomanticus \
  ~/repos/personal/codex-technomanticus-arcana/.last-carding
```

---

## Auditoria — YAMLs stale (regenerar mantendo IDs)

| # | Nota fonte | YAML alvo | Hash atual → novo |
|---|---|---|---|
| 1 | `IA/Agents.md` | `cards/ia/ia-agents.yaml` | `11ec312d3de2` → `25ebe85d2fc5` |
| 2 | `IA/Inteligência Artificial.md` | `cards/ia/ia-fundamentos.yaml` | `dbdfb9e0dd29` → `1a2e00ac8836` |
| 3 | `IA/LLMs.md` | `cards/ia/ia-llms.yaml` | `85b99d5874fb` → `a8dda46effec` |
| 4 | `IA/MCP.md` | `cards/ia/ia-mcp.yaml` | `4495a420a054` → `7e23b0238ff9` |
| 5 | `IA/Skills e Prompting.md` | `cards/ia/ia-prompting.yaml` | `c99952ab5f13` → `891968d48697` |
| 6 | `IA/RAG e Vector Databases.md` | `cards/ia/ia-rag.yaml` | `e12545dd48dc` → `550b9676deb0` |
| 7 | `Java/Core/Java Fundamentals.md` | `cards/java/java-fundaments.yaml` | `042948ee158d` → `d6c146155418` |
| 8 | `Java/Core/Certificação Java OCP.md` | `cards/java/java-ocp.yaml` | `7896f3125eb2` → `2feafbd73fc8` |
| 9 | `JavaScript/Frontend/HTML e CSS.md` | `cards/javascript/js-htmlcss.yaml` | `4b3f8764c598` → `3c8395dcca7e` |
| 10 | `JavaScript/Backend/Node.js.md` | `cards/javascript/js-nodejs.yaml` | `322e28e86d98` → `e216fbd24471` |
| 11 | `JavaScript/Frontend/React.md` | `cards/javascript/js-react.yaml` | `9c11a182957f` → `514624ba9279` |
| 12 | `JavaScript/Core/TypeScript.md` | `cards/javascript/js-typescript.yaml` | `6ecc9a8229df` → `360e3a98789a` |

---

## Lotes

> **Convenção:** marque `- [x]` ao concluir um item. Ordem dentro de um lote é livre. Lotes podem rodar em paralelo (waves).

### Lote 1 — Arquitetura novas (2 notas) — `Codex::Arquitetura`

- [ ] `Arquitetura/Event Storming/Exemplos.md` → `cards/arquitetura/event-storming-exemplos.yaml` (novo)
- [ ] `Arquitetura/Gateway de Pagamento.md` → `cards/arquitetura/gateway-de-pagamento.yaml` (novo)

### Lote 2 — Java núcleo (6 notas) — `Codex::Java`

**Stale (regenerar preservando IDs):**

- [ ] `Java/Core/Java Fundamentals.md` → `cards/java/java-fundaments.yaml`
- [ ] `Java/Core/Certificação Java OCP.md` → `cards/java/java-ocp.yaml`

**Novas:**

- [ ] `Java/Backend/Kafka/Otimizando Kafka consumers.md` → `cards/java/java-kafka-tuning.yaml`
- [ ] `Java/Backend/Kafka/Setting Up Kafka.md` → `cards/java/java-kafka-setup.yaml`
- [ ] `Java/Backend/gRPC e Go.md` → `cards/java/java-grpc.yaml`
- [ ] `Java/Frontend/JavaFX.md` → `cards/java/java-javafx.yaml`

### Lote 3 — Kafka Concepts parte 1 (10 notas, 1–10) — `Codex::Java`

- [ ] `Java/Backend/Kafka/Kafka Concepts/1. Introdução ao Apache Kafka.md` → `cards/java/java-kafka-01-intro.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/2. Kafka Cluster.md` → `cards/java/java-kafka-02-cluster.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/3. Broker no Apache Kafka- Funções e Interações.md` → `cards/java/java-kafka-03-broker.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/4. Apache Zookeeper e o Apache Kafka- Uma Era em Transição.md` → `cards/java/java-kafka-04-zookeeper.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/5. Kafka Raft Metadata.md` → `cards/java/java-kafka-05-kraft.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/6. Topics.md` → `cards/java/java-kafka-06-topics.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/7. Partitions.md` → `cards/java/java-kafka-07-partitions.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/8. Topic Replication.md` → `cards/java/java-kafka-08-replication.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/9. Producers.md` → `cards/java/java-kafka-09-producers.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/10. Consumers.md` → `cards/java/java-kafka-10-consumers.yaml`

### Lote 4 — Kafka Concepts parte 2 (9 notas, 11–19) — `Codex::Java`

- [ ] `Java/Backend/Kafka/Kafka Concepts/11. Consumer Groups.md` → `cards/java/java-kafka-11-consumer-groups.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/12. Consumer Offsets.md` → `cards/java/java-kafka-12-consumer-offsets.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/13. Keys.md` → `cards/java/java-kafka-13-keys.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/14- Messages.md` → `cards/java/java-kafka-14-messages.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/15. Partições e Fator de Replicação.md` → `cards/java/java-kafka-15-replication-factor.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/16. Offsets e Compacção de Log.md` → `cards/java/java-kafka-16-log-compaction.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/17. Kafka Connect.md` → `cards/java/java-kafka-17-connect.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/18. Kafka Streams.md` → `cards/java/java-kafka-18-streams.yaml`
- [ ] `Java/Backend/Kafka/Kafka Concepts/19. Segurança no Apache Kafka.md` → `cards/java/java-kafka-19-security.yaml`

### Lote 5 — JavaScript núcleo (8 notas) — `Codex::JavaScript`

**Stale (regenerar preservando IDs):**

- [ ] `JavaScript/Frontend/HTML e CSS.md` → `cards/javascript/js-htmlcss.yaml`
- [ ] `JavaScript/Backend/Node.js.md` → `cards/javascript/js-nodejs.yaml`
- [ ] `JavaScript/Frontend/React.md` → `cards/javascript/js-react.yaml`
- [ ] `JavaScript/Core/TypeScript.md` → `cards/javascript/js-typescript.yaml`

**Novas:**

- [ ] `JavaScript/Frontend/Bootstrap.md` → `cards/javascript/js-bootstrap.yaml`
- [ ] `JavaScript/Frontend/Mantine.md` → `cards/javascript/js-mantine.yaml`
- [ ] `JavaScript/Frontend/Material UI.md` → `cards/javascript/js-mui.yaml`
- [ ] `JavaScript/Frontend/React Red Flag Manual.md` → `cards/javascript/js-react-red-flags.yaml`

### Lote 6 — TypeScript com React (15 notas, série completa) — `Codex::JavaScript`

- [ ] `01 - A tripla inferência - props, state, hooks.md` → `cards/javascript/js-tsr-01-tripla-inferencia.yaml`
- [ ] `02 - Inferir vs anotar - quando deixar o TS trabalhar.md` → `cards/javascript/js-tsr-02-inferir-vs-anotar.yaml`
- [ ] `03 - Por que React.FC saiu de moda.md` → `cards/javascript/js-tsr-03-react-fc.yaml`
- [ ] `04 - interface vs type vs satisfies para props.md` → `cards/javascript/js-tsr-04-interface-type-satisfies.yaml`
- [ ] `05 - Tipando state e refs.md` → `cards/javascript/js-tsr-05-state-refs.yaml`
- [ ] `06 - Tipando event handlers.md` → `cards/javascript/js-tsr-06-event-handlers.yaml`
- [ ] `07 - Tipando hooks customizados.md` → `cards/javascript/js-tsr-07-hooks-customizados.yaml`
- [ ] `08 - Tipando Context API.md` → `cards/javascript/js-tsr-08-context-api.yaml`
- [ ] `09 - Tipando reducers e state machines.md` → `cards/javascript/js-tsr-09-reducers.yaml`
- [ ] `10 - Tipando formulários.md` → `cards/javascript/js-tsr-10-formularios.yaml`
- [ ] `11 - Tipando data fetching.md` → `cards/javascript/js-tsr-11-data-fetching.yaml`
- [ ] `12 - Generic components.md` → `cards/javascript/js-tsr-12-generic-components.yaml`
- [ ] `13 - Polymorphic components com as prop.md` → `cards/javascript/js-tsr-13-polymorphic.yaml`
- [ ] `14 - Compound components, slots, render props.md` → `cards/javascript/js-tsr-14-compound.yaml`
- [ ] `15 - Armadilhas, tsconfig, ferramentas.md` → `cards/javascript/js-tsr-15-armadilhas.yaml`

> Path raiz: `JavaScript/Frontend/TypeScript com React/`

### Lote 7 — IA stale (6 notas, regenerar) — `Codex::IA`

- [ ] `IA/Agents.md` → `cards/ia/ia-agents.yaml`
- [ ] `IA/Inteligência Artificial.md` → `cards/ia/ia-fundamentos.yaml`
- [ ] `IA/LLMs.md` → `cards/ia/ia-llms.yaml`
- [ ] `IA/MCP.md` → `cards/ia/ia-mcp.yaml`
- [ ] `IA/Skills e Prompting.md` → `cards/ia/ia-prompting.yaml`
- [ ] `IA/RAG e Vector Databases.md` → `cards/ia/ia-rag.yaml`

### Lote 8 — Ferramentas de IA (5 notas) — `Codex::IA`

- [ ] `IA/Ferramentas de IA/Claude.md` → `cards/ia/ia-tool-claude.yaml`
- [ ] `IA/Ferramentas de IA/Codex.md` → `cards/ia/ia-tool-codex.yaml`
- [ ] `IA/Ferramentas de IA/Comparativo de LLMs.md` → `cards/ia/ia-tool-comparativo.yaml`
- [ ] `IA/Ferramentas de IA/Gemini.md` → `cards/ia/ia-tool-gemini.yaml`
- [ ] `IA/Ferramentas de IA/GitHub Copilot.md` → `cards/ia/ia-tool-copilot.yaml`

### Lote 9 — Memória de Agentes parte 1 (12 notas, 01–12) — `Codex::IA`

- [ ] `01 - O que é memória em IA.md` → `cards/ia/ia-mem-01-o-que-e.yaml`
- [ ] `02 - O problema das janelas de contexto.md` → `cards/ia/ia-mem-02-context-windows.yaml`
- [ ] `03 - Taxonomia da memória (episódica, semântica, procedural).md` → `cards/ia/ia-mem-03-taxonomia.yaml`
- [ ] `04 - RAG vs memória de longo prazo.md` → `cards/ia/ia-mem-04-rag-vs-longo-prazo.yaml`
- [ ] `05 - Beyond RAG - quando RAG não basta.md` → `cards/ia/ia-mem-05-beyond-rag.yaml`
- [ ] `06 - O LLM Wiki Pattern (gist do Karpathy).md` → `cards/ia/ia-mem-06-wiki-pattern.yaml`
- [ ] `07 - Por que Obsidian e markdown como substrato.md` → `cards/ia/ia-mem-07-obsidian-substrato.yaml`
- [ ] `08 - Arquitetura de um sistema de memória.md` → `cards/ia/ia-mem-08-arquitetura.yaml`
- [ ] `09 - Panorama de implementações (abril 2026).md` → `cards/ia/ia-mem-09-panorama.yaml`
- [ ] `10 - LLM-knowledge-base (Wendel) — direto do gist.md` → `cards/ia/ia-mem-10-llm-kb.yaml`
- [ ] `11 - graphify — knowledge graph de raw.md` → `cards/ia/ia-mem-11-graphify.yaml`
- [ ] `12 - basic-memory — MCP nativo Obsidian.md` → `cards/ia/ia-mem-12-basic-memory.yaml`

> Path raiz: `IA/Memória de Agentes/`

### Lote 10 — Memória de Agentes parte 2 (11 notas, 13–23) — `Codex::IA`

- [ ] `13 - Letta (ex-MemGPT).md` → `cards/ia/ia-mem-13-letta.yaml`
- [ ] `14 - Mem0 — vetorial + grafo.md` → `cards/ia/ia-mem-14-mem0.yaml`
- [ ] `15 - Zep e Graphiti — knowledge graph temporal.md` → `cards/ia/ia-mem-15-zep-graphiti.yaml`
- [ ] `16 - MemPalace (Milla Jovovich).md` → `cards/ia/ia-mem-16-mempalace.yaml`
- [ ] `17 - Generative Agents (Park, Stanford 2023).md` → `cards/ia/ia-mem-17-generative-agents.yaml`
- [ ] `18 - A-MEM — Zettelkasten dinâmico.md` → `cards/ia/ia-mem-18-a-mem.yaml`
- [ ] `19 - Surveys e estado da arte 2026.md` → `cards/ia/ia-mem-19-surveys.yaml`
- [ ] `20 - Comparativo crítico (LongMemEval).md` → `cards/ia/ia-mem-20-longmemeval.yaml`
- [ ] `21 - Críticas, limitações e armadilhas.md` → `cards/ia/ia-mem-21-criticas.yaml`
- [ ] `22 - Guia de implementação do zero.md` → `cards/ia/ia-mem-22-implementacao.yaml`
- [ ] `23 - Aplicações comerciais e modelo de negócio.md` → `cards/ia/ia-mem-23-aplicacoes.yaml`

> Path raiz: `IA/Memória de Agentes/`

### Lote 11 — Infraestrutura novas (5 notas) — `Codex::Infraestrutura`

- [ ] `Infraestrutura/Comandos Docker e WSL.md` → `cards/infraestrutura/infra-docker-wsl.yaml`
- [ ] `Infraestrutura/Configurando Ambiente Linux no WSL.md` → `cards/infraestrutura/infra-config-linux-wsl.yaml`
- [ ] `Infraestrutura/Digital Ocean.md` → `cards/infraestrutura/infra-digital-ocean.yaml`
- [ ] `Infraestrutura/Terminal.md` → `cards/infraestrutura/infra-terminal.yaml`
- [ ] `Infraestrutura/WSL, Docker e Kubernetes.md` → `cards/infraestrutura/infra-wsl-docker-k8s.yaml`

---

## Plano de execução em waves

Cada wave dispara até 5 subagentes em paralelo. Esperar todos retornarem antes da próxima wave.

### Wave 1 (5 lotes paralelos)

- [ ] Lote 1 — Arquitetura novas (2)
- [ ] Lote 2 — Java núcleo (6)
- [ ] Lote 5 — JS núcleo (8)
- [ ] Lote 8 — IA Ferramentas (5)
- [ ] Lote 11 — Infraestrutura novas (5)

### Wave 2 (5 lotes paralelos)

- [ ] Lote 3 — Kafka Concepts 1–10 (10)
- [ ] Lote 4 — Kafka Concepts 11–19 (9)
- [ ] Lote 7 — IA stale (6)
- [ ] Lote 6 — TypeScript com React (15)
- [ ] Lote 9 — Memória de Agentes 1–12 (12)

### Wave 3 (1 lote restante)

- [ ] Lote 10 — Memória de Agentes 13–23 (11)

---

## Pós-execução

- [ ] Validar todos os YAMLs: `cd ~/repos/personal/codex-technomanticus-arcana && .venv/bin/python -m scripts.validate_cards`
- [ ] Atualizar `.last-carding`: `echo "6a4bf7898bdd93c44dda20b4be7f290ab4241d4c" > ~/repos/personal/codex-technomanticus-arcana/.last-carding`
- [ ] Build do deck: `cd ~/repos/personal/codex-technomanticus-arcana && .venv/bin/python -m scripts.build_deck`
- [ ] Commit no repo arcana com mensagem descritiva
