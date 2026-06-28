# RITO Business Kit

Esta pasta reúne os entregáveis finais da RITO Sistemas em formatos prontos para uso comercial e institucional.

## Estrutura

- `editable-docx/`: arquivos editáveis em Word para briefing, proposta, orçamento, contrato, follow-up e materiais operacionais.
- `editable-xlsx/`: planilhas editáveis de apoio comercial e precificação.
- `presentation/`: apresentação institucional em PowerPoint.
- `pdf/`: materiais prontos para distribuição em PDF.

## Arquivos principais

- `editable-docx/rito-contract-template.docx`
- `editable-docx/rito-commercial-proposal-template.docx`
- `editable-docx/rito-estimate-template.docx`
- `editable-docx/rito-client-briefing-form.docx`
- `editable-docx/rito-pricing-guide.docx`
- `editable-xlsx/rito-pricing-calculator.xlsx`
- `pdf/rito-branding-guide.pdf`
- `pdf/rito-software-brand-system.pdf`
- `presentation/rito-company-presentation.pptx`
- `pdf/rito-company-presentation.pdf`
- `pdf/rito-company-onepager.pdf`

## Como regenerar

```bash
python3 scripts/generate_final_business_assets.py
python3 scripts/generate_pricing_calculator_xlsx.py
```

## Observação

Os arquivos desta pasta são gerados a partir da base em `docs/sales/`, `docs/legal/`, `docs/brand/` e dos scripts de geração. Quando os documentos-fonte ou as regras de precificação forem refinados, execute os scripts novamente para atualizar o kit final.

## Observação sobre a planilha de precificação

A planilha `rito-pricing-calculator.xlsx` agora inclui:

- cálculo por horas e por etapa;
- leitura por pacote comercial;
- cenários mínimo, ideal e premium;
- simulação de parcelamento;
- aba `Resumo-Proposta` pronta para exportação em PDF;
- aba `Historico` para acompanhar estimado, vendido e realizado.
