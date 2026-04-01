# babel-tcc-translations

Repositorio de tabelas de traducao para o projeto [babel-tcc](https://github.com/NFAsylum/babel-tcc).

## Estrutura

```
programming-languages/
  csharp/
    keywords-base.json       # 89 keywords C# com IDs numericos

natural-languages/
  pt-br/
    csharp.json              # Traducoes PT-BR para C#
  en-us/
    csharp.json              # Traducoes EN-US para C#
  ...
  template.json              # Template para novos idiomas

schema/
  keyword-table.schema.json  # JSON Schema para keywords-base
  translation.schema.json    # JSON Schema para traducoes
```

## Formato

### keywords-base.json

Mapeia keywords da linguagem de programacao para IDs numericos unicos:

```json
{
  "keywords": {
    "class": 10,
    "if": 30,
    "return": 52
  }
}
```

### Traducao (ex: pt-br/csharp.json)

Mapeia IDs numericos para traducoes no idioma natural:

```json
{
  "version": "1.0.0",
  "languageCode": "pt-br",
  "languageName": "Português (Brasil)",
  "programmingLanguage": "CSharp",
  "translations": {
    "10": "classe",
    "30": "se",
    "52": "retornar"
  }
}
```

## Convencoes para tabelas de traducao

### Metadata

| Campo | Padrao | Exemplo |
|-------|--------|---------|
| `languageCode` | [BCP 47](https://www.rfc-editor.org/info/bcp47) — `idioma-pais` (ISO 639-1 + ISO 3166-1 alpha-2) | `pt-br`, `en-us`, `ja-jp` |
| `languageName` | [CLDR](https://cldr.unicode.org/) — nome nativo do idioma com pais entre parenteses | `Português (Brasil)`, `Español (España)` |
| `programmingLanguage` | PascalCase, deve corresponder a um diretorio em `programming-languages/` | `CSharp` |
| `version` | [SemVer](https://semver.org/) | `1.0.0` |

Variantes de um mesmo idioma usam sufixo no `languageCode` e qualificador no `languageName`:
- `pt-br` — `Português (Brasil)`
- `pt-br-acentuado` — `Português (Brasil, Acentuado)`

### Valores de traducao

- **Caracteres nativos da lingua**: traducoes devem usar os caracteres proprios do idioma, incluindo acentos, cedilhas, CJK, arabico, etc. O engine babel-tcc suporta UTF-8 completo.
- **Minusculas**: todos os valores em letras minusculas (para idiomas que possuem distincao de caixa).
- **Sem espacos**: palavras compostas devem ser concatenadas sem espacos (ex: `paracada`, `somenteleitura`, `espaconome`).
- **Completude**: todos os IDs do `keywords-base.json` devem ter uma traducao correspondente.
- **Unicidade**: nao pode haver duas keywords traduzidas para a mesma palavra dentro do mesmo arquivo.
- **Lookup reverso**: o engine babel-tcc usa comparacao case-insensitive mas accent-sensitive (`OrdinalIgnoreCase`). O usuario deve digitar os caracteres exatamente como definidos na tabela.

### Variantes simplificadas

Variantes ASCII (sem acentos/diacriticos) ou romanizadas (romaji, pinyin) podem ser oferecidas como alternativas para facilitar a digitacao. Usar sufixo apropriado no `languageCode`:

| Tipo | Exemplo de code | Descricao |
|------|----------------|-----------|
| Nativo (padrao) | `pt-br-acentuado` | Usa caracteres corretos: `padrão`, `senão` |
| ASCII simplificado | `pt-br` | Remove acentos: `padrao`, `senao` |
| Romanizado | `ja-jp` | Usa romaji: `kurikaeshi`, `kurasu` |

### Diretorio

Cada idioma deve ter seu proprio diretorio dentro de `natural-languages/`, nomeado com o `languageCode`:

```
natural-languages/{languageCode}/csharp.json
```

## Validacao automatica

Todas as PRs para `main` sao validadas automaticamente via GitHub Actions. O CI verifica:
- Sintaxe JSON valida
- Conformidade com os schemas
- Completude (todos os IDs do keywords-base cobertos)
- Unicidade (sem traducoes duplicadas)

## Adicionar novo idioma

1. Copiar `natural-languages/template.json` para `natural-languages/<language-code>/csharp.json`
2. Preencher `languageCode` (BCP 47), `languageName` (CLDR) e todas as traducoes
3. Usar caracteres nativos do idioma nos valores de traducao
4. Abrir PR — o CI valida automaticamente

## Idiomas disponiveis

| Codigo | Idioma | Linguagens |
|--------|--------|------------|
| pt-br | Português (Brasil) | C# |
| pt-br-acentuado | Português (Brasil, Acentuado) | C# |
| en-us | English (United States) | C# |
| es-es | Español (España) | C# |
| fr-fr | Français (France) | C# |
| de-de | Deutsch (Deutschland) | C# |
| it-it | Italiano (Italia) | C# |
| ja-jp | Nihongo (Nihon, Romaji) | C# |
