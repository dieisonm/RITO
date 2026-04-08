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

## Fluxo recomendado para atualizacoes

Use uma branch dedicada para a Hostinger, contendo apenas os arquivos publicos do site:

```bash
./scripts/publish_hostinger_branch.sh
```

Esse comando:

- gera `dist/`
- cria uma publicacao limpa
- envia somente os arquivos do site para a branch `hostinger`

Na Hostinger, configure:

- Repositorio: `https://github.com/dieisonm/RITO.git`
- Ramo: `hostinger`
- Diretorio: `public_html`

## Como publicar na Hostinger

1. Gere a pasta `dist/`.
2. No painel da Hostinger, abra o `File Manager` do dominio.
3. Entre na pasta `public_html`.
4. Apague os arquivos padrao que estiverem la.
5. Envie o conteudo inteiro da pasta `dist/` para `public_html`.

Ou:

5. Envie o arquivo `release/ritosistemas-hostinger.zip` e extraia dentro de `public_html`.

## Se for usar Git Deployment na Hostinger

Depois de configurar o repositório uma vez, as proximas atualizacoes ficam assim:

1. Atualize o projeto localmente.
2. Suba a `main` normalmente:

```bash
git add .
git commit -m "Sua mensagem"
git push
```

3. Publique a branch de deploy:

```bash
./scripts/publish_hostinger_branch.sh
```

Se a Hostinger estiver com auto deploy ativado para a branch `hostinger`, ela publica sozinha.

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
