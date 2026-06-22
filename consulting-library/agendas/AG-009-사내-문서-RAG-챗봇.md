---
id: AG-009
domain: ai-ml
status: done
title: "사내 문서 RAG 챗봇"
skills: [chroma, fastmcp, hermes-agent, evaluating-llms-harness]
---

# AG-009 · 사내 문서 RAG 챗봇

> 라벨: `agenda` · `domain/ai-ml` · `status/done`  ·  적립 절차: [SOP-002](../sop/SOP-002-agenda-knowledge-capture.md)

## 도메인 / 아젠다
주: AI/ML 엔지니어링 & 에이전트 · 참조 카탈로그 아젠다: 「사내 문서 RAG 챗봇」

## 핵심 스킬
- `chroma` — 온프레미스 벡터 저장/검색
- `fastmcp` — 검색 도구를 MCP로 노출
- `hermes-agent` — 대화 오케스트레이션
- `evaluating-llms-harness` — 정확도 평가

## 산출물
- RAG 파이프라인, 검색 MCP 서버, 챗봇, 평가 리포트

## 재사용 포인트
온프레미스 RAG 스택(chroma+fastmcp+hermes-agent)은 사내검색 의뢰에 그대로 재사용.

## 기획문서
[playbooks/ai-ml-rag-chatbot.md](../playbooks/ai-ml-rag-chatbot.md)
