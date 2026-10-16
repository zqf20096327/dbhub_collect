# TiDB + SCaiLE Learning Workshop

**Learn distributed databases by building a real e-commerce platform.**

## 🎯 What You'll Learn

- **TiDB 기본**: CRUD, 트랜잭션, 분산 시스템 개념
- **SCaiLE 스케일링**: 데이터 샤딩 및 분산 전략
- **프로덕션 운영**: Docker 배포, 모니터링, 성능 튜닝
- **실전 경험**: 완전한 전자상거래 플랫폼 구축

## ⏱️ Duration

- **총 기간**: 2주
- **시간 투자**: 16-24시간
- **모듈**: 8개의 점진적 Lab
- **최종 결과물**: 배포 가능한 애플리케이션

## 🚀 Quick Start

### 1. 사전 요구사항 확인

```bash
python --version          # Python 3.9+
docker --version          # Docker 4.10+
docker-compose --version  # Docker Compose 2.0+
```

### 2. 저장소 클론

```bash
git clone <repo-url>
cd tidb-scale-workshop
```

### 3. 환경 시작

```bash
# 환경 변수 설정 (선택사항, 기본값 사용 가능)
cp .env.example .env

# TiDB 및 모니터링 환경 시작
docker-compose up -d

# 상태 확인
docker-compose ps
```

### 4. Lab 01 시작

```bash
cd labs/lab-01-setup
python starter/app.py
```

## 📚 Lab 목록

| # | 주제 | 학습 목표 | 시간 |
|---|------|---------|------|
| 01 | 환경 설정 | TiDB 연결, Python 기초 | 1-2h |
| 02 | CRUD 작업 | 상품 관리 | 2-3h |
| 03 | 트랜잭션 | 주문-결제 원자성 | 2-3h |
| 04 | 데이터 분산 | SCaiLE 샤딩 | 3-4h |
| 05 | 성능 최적화 | 인덱싱, 쿼리 최적화 | 3-4h |
| 06 | 프로덕션 배포 | Docker, 마이그레이션 | 3-4h |
| 07 | 모니터링 | Prometheus, Grafana | 3-4h |
| 08 | 아키텍처 설계 | 완성된 플랫폼 | 4-5h |

## 📖 문서

- [아키텍처 개요](docs/architecture-overview.md)
- [프로젝트 스코핑](docs/scoping.md) (ERD, API 명세)
- [용어집](docs/glossary.md)
- [Pro Tips](docs/pro-tips.md)
- [FAQ](docs/faq.md)
- [사전 요구사항](PREREQUISITES.md)

## 🛠️ 기술 스택

- **언어**: Python 3.9+
- **데이터베이스**: TiDB + SCaiLE
- **프레임워크**: FastAPI
- **ORM**: SQLAlchemy
- **테스트**: Pytest
- **컨테이너**: Docker + Docker Compose
- **모니터링**: Prometheus + Grafana

## 🤝 기여

[CONTRIBUTING.md](CONTRIBUTING.md)를 읽고 기여해주세요.

## 📄 라이선스

MIT License - [LICENSE](LICENSE) 참고

## 🆘 도움말

- [FAQ](docs/faq.md)
- [Troubleshooting](docs/pro-tips.md)
- GitHub Issues로 질문 또는 버그 리포트

---

**행운을 빕니다!** 🎉

Built with ❤️ for the TiDB Community
