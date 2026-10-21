# StormPK EU — estado da implantação (2026-10-21)

## Servidor

- Host: Unraid AEROCOOL, VM libvirt `StormPK`, Windows 11 Pro, 8 vCPUs, 12 GB RAM, disco 100 GB, TPM 2.0 e autostart.
- IP na LAN de teste: `192.168.30.89`. **Não há lançamento público nem autorização para expor o SQL Server na internet.**
- Windows runtime: `C:\StormPK\Runtime\Server\login-server` e `C:\StormPK\Runtime\Server\game-server`.
- SQL: instância local SQL Server Express 2022 `.\SQLEXPRESS`, driver ODBC 17 **x86**.
- Bancos restaurados dos backups originais: `ClanDB`, `EventDB`, `GameDB`, `ItemDB`, `LogDB`, `ServerDB`, `SkillDBNew`, `UserDB`.
- Login Server TCP `10009`, Game Server TCP `10007`. Confirmado que ambos escutam no Windows e aceitam conexões da LAN.
- Tarefa agendada `StormPK Servers` como SYSTEM, trigger AtStartup, arquivo `C:\StormPK\Deploy\start-servers.ps1`. Executada manualmente com sucesso após verificar SQL Express.
- Logs de inicialização: `C:\StormPK\Deploy\startup.log`.

## Dados e cliente

- Pacote original mantido: `/mnt/user/Games/install/StormPK/Files.7z`.
- Diretório extraído: `/mnt/user/Games/install/StormPK/Files/`.
- Um instalador LAN foi preparado no Unraid: `/mnt/user/Games/install/StormPK/Instalar-StormPK.cmd`, também acessível via compartilhamento SMB `\\AEROCOOL\Games\install\StormPK` (requer 7-Zip no PC Windows).
- O instalador extrai `Files/Game` para a pasta local de usuário `Games\StormPK\Files\Game` e aplica `StormPK-Client-Patch.zip`.
- O patch altera **somente a cópia** da string de IP em `game.dll`: `15.204.184.155` -> `192.168.30.89`; arquivo original preservado. O cliente **ainda não foi testado em uma estação Windows com GPU**.

## Pendências que impedem declarar o projeto jogável

1. Após a restauração, o schema histórico de `GameDB.QuestList` não tinha oito campos do código EU. Migração SQL aplicada e validada com 187 missões; o script versionado está em `database/migrations/001-eu-quest-schema.sql`.
2. **A consulta complexa de missões ainda gera `Invalid column name 'ASMQuestBit'` no log**, embora a coluna exista e seja consultável isoladamente via ODBC x86. Investigar a consulta completa e possíveis dependências de schema, sem inserir dados ou criar colunas às cegas. As mensagens `Quest not found...` refletem conteúdo de missão ausente no backup de origem.
3. O Login Server reporta erro na limpeza de registros antigos do `LogDB` por conversão de texto em data.
4. Ainda não existe conta de teste `danilostorm` na nova base `UserDB`; as 77 contas restauradas pertencem ao backup original. **Não usar senhas recuperadas dos backups.** O cliente EU calcula SHA-256 em maiúsculas do texto `UPPER(nome) + ':' + senha` para enviar ao servidor; código-fonte em `game/game/GameCore.cpp`. Criar conta teste com autorização, hash compatível e senha temporária que será alterada.
5. Testar a abertura do cliente, login, seleção/criação de personagem e entrada em Ricarten no PC do usuário. Não afirmar sucesso antes dessa validação.
6. Para acesso público futuro, rever autenticação, atualização de DLLs, segurança de credenciais e firewall.

## Histórico/segurança

A implementação antiga Etervale/StormPK e o container Docker antigo foram removidos. A branch principal foi substituída pela base nativa C++ de `dwSize-PE/PristonTale-EU-main`. As releases antigas foram apagadas. Não copiar backups proprietários, bancos, senhas ou arquivos de jogo ao GitHub.
