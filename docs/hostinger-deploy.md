# Hostinger Deploy

## Estrutura pronta

O projeto gera uma pasta `dist/` com tudo o que a Hostinger precisa para publicar o site estatico:

- `index.html`
- `pages/`
- `assets/`
- `logos/`
- `robots.txt`
- `sitemap.xml`
- `404.html`

## Como gerar a pasta de deploy

No terminal, dentro da pasta do projeto:

```bash
./scripts/build_dist.sh
```

## Como gerar um .zip pronto para upload

```bash
./scripts/package_hostinger.sh
```

Isso cria:

- `release/ritosistemas-hostinger.zip`

## Como publicar na Hostinger

1. Gere a pasta `dist/`.
2. No painel da Hostinger, abra o `File Manager` do dominio.
3. Entre na pasta `public_html`.
4. Apague os arquivos padrao que estiverem la.
5. Envie o conteudo inteiro da pasta `dist/` para `public_html`.

Ou:

5. Envie o arquivo `release/ritosistemas-hostinger.zip` e extraia dentro de `public_html`.

## Dominio principal

- Dominio principal: `ritosistemas.com`
- Dominio secundario: `ritosistemas.com.br`

## Redirecionamento do .com.br

Na Hostinger, configure um redirecionamento 301 permanente de:

- `https://ritosistemas.com.br`
- para `https://ritosistemas.com`

## Verificacoes apos publicar

1. Abrir `https://ritosistemas.com`
2. Testar as paginas internas:
   - `/pages/solucoes.html`
   - `/pages/como-funciona.html`
   - `/pages/para-quem.html`
   - `/pages/sobre.html`
   - `/pages/contato.html`
3. Confirmar carregamento de logo, favicon e CSS.
4. Confirmar que `https://ritosistemas.com/sitemap.xml` abre corretamente.
5. Confirmar que `https://ritosistemas.com/robots.txt` abre corretamente.
