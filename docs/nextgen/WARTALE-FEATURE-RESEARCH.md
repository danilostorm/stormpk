# Wartale e StormPK: levantamento comparativo de recursos (somente fatos observáveis)

Data: 2026-10-21. Uso: especificação técnica de comportamento desejado, não licença para copiar conteúdo de terceiros.

## Escopo e limitações

A análise estática inicial do Wartale considerou somente os dois executáveis visíveis (~46 MB). Um inventário Windows com `-Force` encontrou **32.032 arquivos e 11.390.387.057 bytes**, com seis diretórios marcados como ocultos: `char`, `Effect`, `Field`, `game`, `image`, `wav`. A análise inicial do Ghidra não equivale a ter recuperado o código-fonte do cliente e servidor. Não existe source do servidor Wartale neste laboratório. O cliente StormPK de referência no AEROCOOL tem 32.279 arquivos e 7.120.563.250 bytes; as árvores não são diretamente comparáveis por contagem, pois usam diferentes formas de empacotamento.

Os arquivos `.xpk` do Wartale somam **117 pacotes e 5.129.920.523 bytes**. O tamanho adicional do cliente não comprova a existência de vários idiomas. Não identificamos até esta data diretório explícito de idiomas dentro de `game`; o idioma pode estar embutido em recursos ou ser carregado por outro mecanismo, ainda não verificado. O nome de um arquivo indica uma provável categoria de conteúdo, **não comprova que o recurso está habilitado ou funciona em jogo**.

A lista detalhada de metadados permanece no laboratório privado: `C:\StormPK\Research\Wartale-Asset-Metadata.json` e `/mnt/user/appdata/stormpk-research/reports/Wartale-Asset-Metadata.json`; não publicar conteúdo extraído de pacotes.

## Matriz de observação e objetivo StormPK independente

| Área | Evidência no Wartale | Source StormPK hoje | Implementação original desejada |
|---|---|---|---|
| Montarias | nomes `mounts.xpk`, `mounts1.xpk`, `wav_mounts.xpk` | não localizado módulo de montaria | controle de invocação, montar/desmontar, movimento e animação sincronizados, titularidade e modelos próprios |
| Mascotes | `stable.xpk`, `minions.xpk`, diretório `char/pet` | `CPetSystemHandler`, `CStableWindow`, `StableHandler`; quatro skins SQL, zero pets atribuídos; interface parcialmente comentada | estabilizar fluxo, possuir/invocar/renomear/trocar/guardar companheiros persistentes |
| Clima | `sky.xpk`, `particles.xpk`, `snow.part`, `Thunder.wav` | `RainMaker` é efeito de habilidade, não clima do mundo | chuva/neve/vento/neblina opcionais, qualidade adaptativa e possibilidade de sincronizar por mapa |
| Gráficos | importação `D3D11CreateDevice`, `CreateDXGIFactory2` | `Direct3DCreate9`, cliente Win32 | abstração do renderizador e backend D3D11 opt-in mantendo D3D9 funcional |
| Armas/equipamentos | `weapons.xpk`, `equips.xpk`, `defenses.xpk` | catálogo de itens, stat validation, inventário e modelos atuais | pipeline original de itens, equipamentos, animação, material, balanço, loja e validação anti-dupe |
| Fabricação/profissões | `crafting.xpk`, `professions.xpk`, `recipes.xpk` | `ManufactureHandler` tem receitas específicas | receitas/data model e interface independente com validação de ingredientes server-side |
| Missões/eventos | `quests.xpk`, `events.xpk` | missões existem com compatibilidade histórica sensível | conteúdo e trilhas de eventos versionadas, migrações testadas |
| Áudio | `wav_mounts.xpk`, `wav_weapons.xpk`, `music.xpk` | efeitos e `wav` existentes | recursos sonoros próprios, mixagem ambiental, controle de volumes e streaming quando necessário |
| Idiomas | nenhuma pasta de idioma explicitamente identificada; insuficiente para afirmar suporte | código CSystem já lê idioma Windows; implementação `pt-BR` em NextGen em staging | tradução verdadeira de UI, missões, NPCs e fontes, com seleção automática e manual |
| Login e patch | `launcher.exe` importa APIs de HTTP e URL; comportamento não testado | manifesto RSA, Range, tickets e patches em funcionamento | preservar protocolos/segurança do StormPK e evolução gradual do launcher |

## Regras de comprovação

Classificar cada observação como:

1. `arquivo_observado` — arquivo ou nome existe, funcionalidade **não confirmada**;
2. `binario_estatico` — importação, estrutura ou string detectada por ferramenta, sem inferir fluxo integral;
3. `comportamento_observado` — funcionalidade foi demonstrada com vídeo/teste/documentação adequada e autorização;
4. `implementado_stormpk` — código próprio integrado, compilado e testado no cliente/servidor StormPK;
5. `homologado` — fluxo ponta a ponta em ambiente de teste (e rollback verificado).

**Não registrar como `homologado` recursos somente nomeados em arquivos.**

## Ordem técnica recomendada

1. Compatibilidade/login/clãs atuais estáveis + baseline de performance.
2. PT-BR real, configurações do launcher e sistema de mascotes existente.
3. Chuva, neve e ambientação **cliente-only** opcional primeiro; sincronização de clima depois de negociar capacidades sem quebrar clientes antigos.
4. Montarias e fabricação como novos sistemas, com backend auditável e assets próprios.
5. D3D11 experimental e novos equipamentos, com testes de desempenho e migração de recursos.

Não transferir binários, texturas, shaders, recursos, modelos ou código decompilado do Wartale para o produto público. Testes sobre arquivos originais devem ficar isolados e sem contato com dados de usuários.
