# Wartale client → StormPK server: estudo de compatibilidade inicial

Data: 2026-10-21. Estado **NÃO CONECTADO / NÃO HOMOLOGADO**. Nenhum binário do Wartale foi modificado, executado na VM Windows ou publicado no launcher. Nenhuma porta do servidor público foi alterada.

## Ponto de partida

- A pasta `C:\Users\danil\Downloads\Wartale` contém **32.032 arquivos / 11.390.387.057 bytes**. `game.exe` e `launcher.exe` são PE Windows x64. O cliente StormPK existente é Win32, com componente `Game.exe` + `game.dll`. Essa diferença de arquitetura não impede interoperação via rede, mas impede acoplar as DLLs do StormPK ao processo x64 do Wartale.
- O pacote base StormPK atualmente é C/C++ em `shared/packets.h`: cabeçalho de **8 bytes**, `u16 tamanho`, `u8 índice da chave`, `u8 flag encriptação`, `u32 opcode` no formato little-endian. O login usa `PKTHDR_LoginUser=0x48480001`, `GAME_VERSION=1309`, estrutura `PacketLoginUser` contendo nome, digest de senha, informações de máquina e outras propriedades, e os primeiros 12 bytes `dwUnk[3]` levam o ticket temporário de uso único do nosso launcher. O servidor valida `sizeof(PacketLoginUser)`, versão, ticket e autenticidade da conta; **não remover essas validações**.
- Uma varredura estática do binário Wartale não encontrou a sequência literal little-endian `01 00 48 48` correspondente ao opcode de login StormPK. Isso **não prova incompatibilidade**, pois a constante pode ser calculada ou codificada dinamicamente. Não localizamos source pública/licença de redistribuição do cliente Wartale no material inspecionado.
- O cabeçalho dos pacotes Wartale `game/assets/*.xpk` começa com variantes `07 58 50 4B` / `08 58 50 4B`. O loader de assets do StormPK não oferece integração XPK documentada. O fato de ambos os clientes terem pastas `char`, `Field` e `Effect` não é prova de formatos de armazenamento nem protocolos iguais.
- O site oficial Wartale oferece um cliente para download, mas isso, isoladamente, não é publicação de código aberto. Antes de **modificar e redistribuir** o cliente Wartale, localizar a licença e repositório de origem ou obter autorização. As regras públicas do projeto também desaconselham modificar o cliente e jogar em VM; este estudo permanece estático até esclarecer permissões.

## Idiomas — achados concretos

Há strings embutidas no `game.exe` do Wartale: `Language`, `language_combobox`, `The language of text in the Game`, `Portuguese`, `English`, `Spanish`, `Korean`, `French` e `InstalledLocales`. **Conclusão limitada:** há suporte de UI para escolha de idioma no cliente. Não se pode concluir que todas as traduções estejam no cliente; textos de missões, NPCs, eventos e economia podem vir do servidor. Não foi encontrado diretório explícito de localização em `game/`, e os nove `.db` da árvore são `Thumbs.db` de caches do Windows, não catálogos de idioma conhecidos.

## Estratégia para tornar interoperável sem quebrar o protocolo atual

1. **Fonte/licença:** obter referência pública do código do cliente Wartale e licença. Se o código não estiver disponível/autorizado, limitar a análise estática e implementar funcionalidade equivalente em nossa própria base.
2. **Lab isolado:** configurar um servidor de staging com cópia anonimizada dos dados e contas de teste. Nunca apontar um executável de origem incerta para a produção. Não executar cliente Wartale em VM contra as regras do distribuidor sem autorização.
3. **Fingerprint mínimo:** usar uma porta loopback de teste, ler no máximo os oito bytes do primeiro pacote e comparar com o framing StormPK. O utilitário `tools/interoperability/wire_probe.py` nunca recebe senha, token, payload completo ou nome de conta. Não intercepta tráfego nem acessa o servidor público.
4. **Mapa de protocolo:** quando houver uma amostra legitimamente executada contra endpoint próprio, documentar handshake, modos de criptografia, autenticação, escolha de servidor/personagem, mundo, itens, combate, NPCs, habilidades, clãs e atualização de mapas. Definir mapeamento dos estados, formatos, códigos de erro, limites de tamanho e versões. O adaptador será uma implementação independente e com testes, não alteração às cegas de um IP.
5. **Login com segurança:** o adaptador/protocol gateway autenticará usuários por fluxo aprovado; preservar a exigência de ticket do launcher e as verificações server-side. Não aceitar credenciais em texto, não redirecionar logins acidentalmente para terceiros, não alterar a política em produção.
6. **Mundo e recursos:** depois de login e lista de personagens, implementar serialização do mundo/entidades com autorização e limite de banda. Assets e montarias de outra distribuição exigem direitos de uso específicos para distribuição.
7. **Idiomas:** testar com contas de laboratório, alternar Português/English no cliente e registrar diferenças entre textos estáticos e mensagens enviadas pelo servidor, sem expor credenciais. Isso será um teste de caixa-preta em ambiente autorizado.

## Trabalho efetuado

- Inventário de conteúdo e arquivos XPK; análise de headers PE, imports e strings de UI/locale.
- Comparação documentada com `shared/packets.h`, `GameCore.cpp` e `packetserver.cpp` da source StormPK.
- Utilitário de fingerprint do cabeçalho de protocolo **desenvolvido**, com testes sintéticos. Não há captura real do cliente Wartale e nenhum gateway funcional neste momento.

### Teste local do utilitário

`python3 -m unittest discover -s tests/interoperability -v`

`python3 tools/interoperability/wire_probe.py --decode 'e801000001004848'`

**Critério de êxito real para o futuro:** abrir um cliente autorizado numa estação compatível, autenticar com conta de staging, listar personagens, entrar em Pillai e permanecer conectado; verificar os dados no servidor. Nada disso foi concluído nesta fase.
