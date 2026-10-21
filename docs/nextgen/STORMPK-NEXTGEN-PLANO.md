# StormPK NextGen — evolução funcional inspirada no nível de recursos do Wartale

**Status:** desenvolvimento isolado, não publicado no jogo. **Objetivo:** um Priston Tale StormPK com funcionalidades equivalentes em experiência a clientes modernos, mas com código próprio, assets licenciados e compatibilidade com nossas contas, dados e infraestrutura.

**Princípio arquitetural:** não substituir `Game.exe`, `game.dll` ou `server.dll` do StormPK por binários do Wartale. São clientes e protocolos distintos (Wartale `game.exe`/`launcher.exe`: PE x64; StormPK: cliente/servidor x86). Não importar ou redistribuir gráficos, modelos, sons, mapas, textos e código proprietários do Wartale sem licença. Engenharia reversa somente para compreender interoperabilidade, comportamento e requisitos, e implementar componentes independentes.

## Constatações do código e banco atual

1. **Mascotes já existem em parte.** `Server/server/CPetSystemHandler.cpp`, `game/game/CStableWindow.cpp`, `game/game/StableHandler.cpp`, `shared/packets.h` implementam estruturas, interface e pacotes de mascotes. `GameDB.dbo.PetSystem` existe e tem **0 linhas**; `GameDB.dbo.PetSystemSkin` existe com **4 linhas** em 21/10/2026. A seleção de mascotes está parcialmente comentada em `CPetSystemHandler::HandlePacket`. Portanto não ativar até restaurar sincronização, validar models, DB, titularidade, permissões e casos de desconexão. Há falhas de nulidade/nomes de colunas sendo corrigidas em branch de homologação.
2. **Gráficos:** `game/game/DXGraphicEngine.cpp` usa `Direct3DCreate9`; Wartale `game.exe` importa `D3D11CreateDevice` e `CreateDXGIFactory2`. A transição D3D9→D3D11 exige abstração de renderizador, gestão de dispositivos, shaders, materiais, texturas, UI, iluminação e testes; não basta mudar importações de DLL.
3. **Clima:** não foi encontrado no cliente/servidor atual um subsistema global de chuva sincronizada por mapa. `ShamanHandler` contém efeito de partículas chamado *Rain Maker*, que não é clima do mundo. Chuva/neve dinâmicas exigem condições/flags por mapa, estado de mundo, partículas e áudio no cliente, sincronização somente se o clima for compartilhado entre jogadores.
4. **Idioma:** `shared/CSystem.cpp` usa idioma do Windows para cinco opções não brasileiras; adicionamos identificação de `pt-BR` em branch de desenvolvimento. Isso **não** traduz automaticamente UI/NPCs/itens: requer catálogo multilíngue, fontes compatíveis, strings do cliente, dados dinâmicos do servidor e fallback. Não misturar encoding UTF-8 em buffers antigos de tamanho fixo sem auditoria.
5. **Novas armas e equipamentos:** ampliar catálogo de IDs, requisitos de classe/nível, características, raridade, modelos, animações, ícones, inventário, trade, drop, loja e tabelas SQL. Servidor deve ser autoridade e preservar anti-dupe/anti-cheat. Sem importar os itens/artes do Wartale.
6. **Launcher:** StormPK já possui manifesto RSA assinado, atualização incremental, retomada por Range, autoatualização do launcher, atualização de patches e configurações gráficas. Evoluir preservando provas de acesso, logs e rollback.

## Entregas organizadas por fases

### Fase 0 — compatibilidade e infraestrutura de testes

- Branch/worktree separada: `feature/stormpk-nextgen-20261021`; não aplicar arquivos na VM de produção sem homologação.
- Inventário de structs/pacotes x86, bancos SQL e configurações do cliente; testes de build Win32 no GitHub Actions; pacote de homologação isolado.
- Feature flags do lado servidor para novos pacotes, migrações versionadas, snapshots dos bancos e mecanismos de reversão.
- Manter suporte à versão atual do cliente durante a implantação gradativa. Aguardar confirmação de estabilidade dos sistemas de login, mundo e clãs existentes.

### Fase 1 — localização PT-BR real

- Idioma padrão determinado pelo Windows UI locale (`pt-BR` -> PT-BR; outro -> EN até inclusão da tradução correspondente); suporte a preferência explícita sem limitar a uma conta.
- Catálogo JSON/CSV para tradutores, compilação ou conversão para formato cliente, controle de codificação, textos em NPC/quests/chat/UI, validação de truncamento e fallback por chave.
- Adicionar opção de idioma ao launcher e aplicar ao processo Game.exe sem modificar o protocolo de rede.
- Critérios de aceite: login, gameplay, menus, missões e novo conteúdo sem caracteres corrompidos ou quebra de alinhamento; alternância de idioma persistente.

### Fase 2 — mascotes (estábulo) já parcialmente implementados

- Auditar e completar `CPetSystemHandler`, `CStableWindow`, `StableHandler` e suas mensagens, retirando caminhos de código comentados quando houver equivalência cliente-servidor.
- Validar permissões, titularidade por personagem, renomeação, spawn em mapa, teleporte, respawn, limites de entidades e modelo/escala de cada skin.
- Testes de SQL por transação, concorrência e desconexão sem perder mascote, além de um pacote de quatro skins originais existentes antes de novas artes.
- Critérios de aceite: jogador convoca, troca e guarda mascote; os outros jogadores o veem e ninguém invoca pets de outro personagem.

### Fase 3 — clima e ambientação

- Implementar serviço `WeatherState` e adaptador para mapa (tempo, chuva e neve), com valores de intensidade, transições e comandos de GM auditados.
- Cliente renderiza partículas e efeitos de solo/visibilidade e reproduz áudio; opcional por mapa para não sobrecarregar GPUs antigas.
- Critérios de aceite: efeitos consistentes, limitações por mapa e opção de qualidade reduzida/sem clima.

### Fase 4 — motor gráfico modernizado

- Criar interface de renderização comum antes da versão D3D11; manter backend D3D9 em fallback e ativar DX11 inicialmente como beta opt-in.
- Substituir gradualmente materiais, shaders, transparências, iluminação, anti-aliasing, apresentação de quadros, UI e gerenciamento de recursos.
- Critérios de aceite: cliente loga, exibe todos os mapas e efeitos, carrega equipamento, responde à perda de dispositivo e usa desempenho/memória medidos em GPUs representativas; compatibilidade com o `Game.exe`/`game.dll` e instalador.

### Fase 5 — armas, itens e outros recursos

- Pipeline de assets **originais/licenciados**, definições server/client versionadas, novos itens com validação de stats, efeitos, sons, drops e commerce.
- Pacotes compatíveis, migrações idempotentes e administração via API do Game Server (não apenas escrita SQL em personagens online).
- Critérios de aceite: aquisição, equipar, remover, vender, dropar, trade, relog e rollback de dados sem duplicação.

## Condições obrigatórias antes de produção

- Build de cliente e servidor verificado; DLLs em staging e testes manuais com jogador.
- Backups de UserDB/GameDB/ItemDB/ClanDB e restauração simulada; trilha de auditoria e rollout por recurso.
- Nenhum patch do Wartale incorporado aos downloads do StormPK. Nenhuma alteração de protocolo sem controle de versões.
- Correções de segurança e estabilidade antigas continuam prioridade sobre recursos cosméticos caso impactem jogadores.

**Situação em 21/10/2026:** a branch NextGen contém apenas a primeira detecção `pt-BR` + medidas defensivas de mascotes. Não existe DX11, sistema de chuva ou pacote de armas novos entregue no StormPK neste momento.
