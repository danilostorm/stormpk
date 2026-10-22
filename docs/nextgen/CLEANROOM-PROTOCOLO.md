# StormPK NextGen — protocolo de desenvolvimento independente (clean-room)

## Importante

"Clean-room" é um processo de separação de evidências e implementação, **não um título obtido automaticamente por instalar Ghidra/REA ou descompilar executáveis**. Se a mesma pessoa lê o código decompilado e reproduz trechos dele, não há isolamento estrito. A validade jurídica depende dos direitos/licenças aplicáveis e não é garantida por este procedimento.

## Papéis separados

**Equipe de análise** (laboratório privado, Ghidra/REA): documenta comportamentos verificáveis, estados, entradas/saídas, restrições de formatos públicos/legítimos e resultados de testes. Pode usar nomes genéricos de categorias de recursos (ex.: montaria, mascote, neve). Não entrega assembly, pseudocódigo decompilado, offsets proprietários, shaders, arquivos de recurso extraídos nem trechos de implementação do Wartale.

**Equipe de implementação** (branch NextGen): lê a especificação funcional, código-fonte próprio do StormPK e bibliotecas com licenças compatíveis. Cria novo código, assets próprios e testes de caixa-preta independentes. Não consulta disassembly nem se baseia em trechos privados do Wartale. Quando a mesma pessoa/ferramenta desempenha ambos os papéis, registrar ausência de independência e submeter a revisão externa antes de descrever o resultado como clean-room estrito.

**Equipe de validação:** compara comportamentos observáveis e métricas. Não confunde igualdade de funcionalidades com igualdade de código, interfaces protegidas ou arquivos artísticos. Exige teste de rollback e compatibilidade de protocolo.

## Barreiras práticas

- Original Wartale permanece no Windows e suas cópias de análise em `C:\StormPK\Research\Samples\Wartale`, leitura/estudo isolados. Não importar nada desses diretórios para `Game`, `Server`, patches, launcher ou repositórios públicos.
- Metadados extensos e resultados do decompilador não são subidos ao GitHub. Documentos de requisitos compartilhados contêm somente observações de alto nível e testes comportamentais.
- Cada recurso recebe ID, evidência (com classificação e data), descrição funcional sem código de terceiros, critérios de aceite e autor da implementação.
- Recursos sujeitos a direitos de terceiros (modelos, sons, sprites, texto, ícones) exigem criação original ou licença compatível antes de qualquer distribuição.
- Alterações que introduzem pacotes precisam de versão/capability handshake, fallback para cliente antigo, limite de tamanho, parsing defensivo e instruções de rollback. Nada de pacotes novos interpretados por clientes antigos sem negociação.
- Não aplicar alterações no servidor de produção apenas porque passaram por descompilação. Usar branch de desenvolvimento + build CI + VM staging + jogador de teste + backups e rollback.

## Critérios de encerramento de uma fase

`especificado` → `implementado` → `compilado` → `testado em staging` → `testado ponta a ponta` → `aprovado para patch assinado`.

A atividade atual comprova `especificado` para vários recursos, `implementado em staging` para parte do locale e validações defensivas de mascotes, mas **não** comprova que o StormPK já ofereça montarias, clima global, novos equipamentos nem DirectX 11.
