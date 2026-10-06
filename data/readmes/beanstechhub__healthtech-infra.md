# healthtech-infra — BeansTech na Alibaba Cloud

Infra-as-code dos portais healthtech (dodr.ai, exame.tech, prontuario.tech, drogaria.tech, beanshealth.com.br,
portaldodentista.ai, drhealth.tech, petiq.tech). **Sem segredos**: tudo vem do KMS 3.0 em tempo de deploy.

- [ALIBABA-HEALTHTECH-2026-09.md](ALIBABA-HEALTHTECH-2026-09.md) — arquitetura, decisões, preços, backup
- [deploy/README.md](deploy/README.md) — runbook (build ACR → deploy ECS → DNS → backup)
- [shared/evidence-chain](shared/evidence-chain) — cadeia anti-alucinação (5 camadas) usada pelos portais
- [RAGMED-PORTAIS-DATASETS-FLUXOS.md](RAGMED-PORTAIS-DATASETS-FLUXOS.md) — produto DoDr/RagMed

O código dos apps vive em repositórios próprios (ex.: `beanstechhub/beanshealth`).
