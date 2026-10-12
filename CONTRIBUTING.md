# Contribuir para o babel-tcc-translations

Obrigado pelo interesse em contribuir com tabelas de traducao! Este repositorio nao tem codigo executavel — apenas arquivos JSON com mapeamentos de keywords. **Nao e necessario saber programar** para contribuir.

## Como contribuir

### Adicionar um novo idioma

1. Fork este repositorio
2. Escolha um codigo de idioma no formato BCP 47 (ex: `de-at` para Alemao da Austria)
3. Crie a pasta `natural-languages/<seu-codigo>/`
4. Para cada linguagem de programacao suportada (`csharp`, `python`, `javascript`, `visualg`, `portugolstudio`), crie um arquivo JSON copiando como base uma traducao existente (ex: `natural-languages/pt-br/python.json`)
5. Atualize `version`, `languageCode`, `languageName` e todas as `translations`
6. Valide localmente: `python3 scripts/validate.py`
7. Abra Pull Request

### Adicionar uma nova linguagem de programacao

1. Crie `programming-languages/<nome>/keywords-base.json` com mapeamento `keyword -> id_numerico`
2. Para cada idioma natural existente, crie a traducao correspondente em `natural-languages/<idioma>/<nome>.json`
3. Valide com `python3 scripts/validate.py`
4. Abra Pull Request

Nota: adicionar nova linguagem de programacao tambem requer mudancas no repositorio [babel-tcc](https://github.com/NFAsylum/babel-tcc) (criar o adapter C#). Coordene os dois PRs.

## Convencoes (resumo)

Detalhes completos no [README.md](README.md). Resumo:

- **Diretorio**: `natural-languages/<languageCode>/<programmingLanguage>.json`
- **Metadata obrigatoria**: `version`, `languageCode` (BCP 47), `languageName` (CLDR), `programmingLanguage` (PascalCase, deve corresponder ao nome do diretorio em `programming-languages/`)
- **Valores de traducao**:
  - Usar caracteres nativos do idioma (UTF-8 suportado)
  - Tudo minusculas em idiomas com distincao de caixa
  - Sem espacos (palavras compostas concatenadas: `paracada`, `espaconome`)
  - Todos os IDs do `keywords-base.json` devem ter traducao
  - Sem duplicatas (case-insensitive)

## Validacao automatica

Todas as PRs para `main` sao validadas via GitHub Actions:

- Sintaxe JSON valida
- Conformidade com os JSON Schemas em `schema/`
- Completude (todos os IDs cobertos)
- Unicidade (sem traducoes duplicadas dentro do mesmo arquivo)

PRs que falham qualquer dessas validacoes nao podem ser merged. Rode `python3 scripts/validate.py` antes de abrir o PR para acelerar o ciclo.

## Reportar bugs ou inconsistencias

Abra uma [issue](https://github.com/NFAsylum/babel-tcc-translations/issues) descrevendo:

- Qual arquivo (`natural-languages/.../*.json`)
- Qual traducao parece errada e por que
- Sugestao alternativa, se tiver

Falantes nativos do idioma sao a melhor fonte para esse tipo de feedback.

## Processo de review

- PRs devem ter descricao curta do que mudou (ex: "feat: adicionar traducao Alemao Austriaco para C#")
- Indique se voce e falante nativo, fluente ou estudante do idioma
- Indique nivel de completude (% das keywords traduzidas)
- Mudancas em arquivos existentes devem justificar por que a traducao anterior estava errada

## Licenca

Este projeto e licenciado sob a [MIT License](LICENSE). Ao contribuir, voce concorda que suas contribuicoes serao distribuidas sob a mesma licenca.
