# tidbit-data

[Tidbit](https://github.com/louis-lemon/tidbit) 크롬 익스텐션이 읽는 **공개 피드 데이터**.

이 저장소는 코드가 아니라 데이터를 담는다. 코드는 별도 비공개 저장소에 있다.
설계 정본은 그쪽의 `docs/spec.md`와 `docs/plans/PLAN-R1-zero-cost.md`다.

**public인 이유는 둘이다** — GitHub Actions가 공개 저장소에서 분 수 제한 없이 무료이고,
jsDelivr가 공개 저장소만 서빙한다. 여기 있는 데이터는 어차피 익스텐션에 공개되는 피드다.

## 파일 소유자 — 이 표가 이 저장소의 척추다

세 주체가 같은 저장소에 커밋한다. **각자 쓰는 파일이 완전히 갈려 있으면 git 충돌이
구조적으로 발생하지 않는다.** 이 분리가 깨지는 순간 세 주체가 서로의 커밋을 밀어내기 시작한다.

| 파일 | **쓰는 주체(유일)** | 읽는 주체 |
| --- | --- | --- |
| `v1/index.json`, `v1/feed/*.json` | GitHub Actions 수집기 | 익스텐션, 모니터 |
| `v1/metrics.jsonl` | GitHub Actions 수집기 | 사람 |
| `v1/summaries.json` | PC 요약 워커 | 수집기 |
| `admin/overrides.json` | PC 어드민 | 수집기 |

발행 순서: 수집기가 카드를 만들고 → `summaries.json`과 `overrides.json`을 **읽어서 병합** →
`feed/*.json`에 쓴다. 워커와 어드민은 자기 파일만 쓰고 피드를 건드리지 않는다.

**각 JSON은 첫 키로 `_owner`를 갖는다.** JSON에 주석을 달 수 없어서 쓰는 방식이다.
그 파일을 고치기 전에 자기가 그 주체가 맞는지 확인한다.

## 서빙

```
https://cdn.jsdelivr.net/gh/louis-lemon/tidbit-data@main/v1/index.json
```

jsDelivr는 브라우저용으로 설계돼 `access-control-allow-origin: *`를 준다.
`@main`의 캐시 반영 지연은 실측으로 확정한다(PLAN-R1 R1-T2).

## 아직 없는 것

`v1/index.json`과 `v1/feed/*.json`은 **첫 수집 run이 만든다.** 여기 미리 두지 않는다 —
`index.json`은 카테고리 1개 이상을 요구하고(`IndexSchema`), index가 가리키는 피드는 항상
이미 존재해야 한다. 빈 껍데기를 두면 그 규칙이 처음부터 깨진 채로 시작한다.
