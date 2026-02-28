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
  "languageName": "Portugues Brasileiro",
  "programmingLanguage": "CSharp",
  "translations": {
    "10": "classe",
    "30": "se",
    "52": "retornar"
  }
}
```

## Validacao automatica

Todas as PRs para `main` sao validadas automaticamente via GitHub Actions. O CI verifica:
- Sintaxe JSON valida
- Conformidade com os schemas
- Completude (todos os IDs do keywords-base cobertos)
- Unicidade (sem traducoes duplicadas)

## Adicionar novo idioma

1. Copiar `natural-languages/template.json` para `natural-languages/<codigo-idioma>/csharp.json`
2. Preencher `languageCode`, `languageName` e todas as traducoes
3. Abrir PR — o CI valida automaticamente

## Idiomas disponiveis

| Codigo | Idioma | Linguagens |
|--------|--------|------------|
| pt-br | Portugues Brasileiro | C# |
