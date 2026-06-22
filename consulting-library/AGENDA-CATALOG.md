# 아젠다 카탈로그 (Agenda Catalog)

> hermes-agent 프로젝트(170개 스킬 / 8개 도메인)를 분석해, 휴먼 컨설턴트가
> 의뢰를 받았을 때 출발점으로 삼을 **대표 아젠다**를 도메인별로 정리한 문서입니다.
> 각 아젠다는 「대표 의뢰 → 핵심 역량(스킬) → 산출물」 구조입니다.
>
> 실제 스킬의 전체 목록·설명·키워드는 [`index/skills-index.md`](./index/skills-index.md) 참고.
> 새 아젠다가 완료되면 GitHub `agenda` 이슈로 적립하여 검색 자산으로 누적합니다.

## 도메인 한눈에 보기

| 도메인 | 스킬 수 | 컨설팅에서의 쓰임 |
|--------|:------:|-------------------|
| [리서치 & 인텔리전스](#1-리서치--인텔리전스) | 17 | 시장·기술·경쟁사 조사, 문헌/특허 리뷰, OSINT |
| [콘텐츠 & 크리에이티브 제작](#2-콘텐츠--크리에이티브-제작) | 30 | 디자인·영상·인포그래픽·카피, 브랜드 자산 |
| [생산성 & 업무 자동화](#3-생산성--업무-자동화) | 25 | 문서/메일/캘린더/회의 자동화, 사내 워크플로우 |
| [소프트웨어 엔지니어링 & DevOps](#4-소프트웨어-엔지니어링--devops) | 29 | 코드베이스 진단, 기능 개발, CI/리뷰, 컨테이너 |
| [AI/ML 엔지니어링 & 에이전트](#5-aiml-엔지니어링--에이전트) | 48 | 모델 파인튜닝·서빙·평가, RAG/벡터DB, 에이전트 |
| [데이터·금융·Web3](#6-데이터금융web3) | 11 | 재무모델링, 밸류에이션, 온체인/자산 분석 |
| [보안 & 거버넌스](#7-보안--거버넌스) | 5 | 펜테스트, OSINT 포렌식, 시크릿 관리 |
| [스마트 라이프](#8-스마트-라이프-홈헬스게임) | 5 | 스마트홈, 헬스/피트니스, 게임 서버 |

각 아젠다 항목의 `핵심 스킬`은 인덱스의 스킬명과 일치합니다. ✅=기본 활성, ⬇️=선택 설치.

---

## 1. 리서치 & 인텔리전스

| 아젠다 | 대표 의뢰 | 핵심 스킬 | 산출물 |
|--------|-----------|-----------|--------|
| **시장·기술 조사** | "이 시장/기술 동향을 정리해줘" | `duckduckgo-search`, `searxng-search`, `scrapling`, `blogwatcher` | 리서치 리포트, 출처 목록 |
| **학술/특허 리뷰** | "관련 논문 핵심만 추려줘" | `arxiv`, `research-paper-writing`, `llm-wiki` | 문헌 리뷰, 요약 노트 |
| **경쟁사/대상 OSINT** | "이 회사/도메인을 조사해줘" | `osint-investigation`, `domain-intel`, `polymarket` | 인텔리전스 브리프 |
| **데이터 탐색** | "이 데이터셋에서 인사이트 뽑아줘" | `jupyter-live-kernel`, `parallel-cli`, `qmd` | 분석 노트북, 시각화 |

## 2. 콘텐츠 & 크리에이티브 제작

| 아젠다 | 대표 의뢰 | 핵심 스킬 | 산출물 |
|--------|-----------|-----------|--------|
| **인포그래픽/도식화** | "개념/구조를 한 장으로 보여줘" | `baoyu-infographic`, `concept-diagrams`, `architecture-diagram`, `excalidraw` | SVG/PNG 다이어그램 |
| **영상·모션** | "설명 영상/모션을 만들어줘" | `manim-video`, `ascii-video`, `youtube-content`, `kanban-video-orchestrator` | 영상 클립, 스토리보드 |
| **웹/UI 디자인** | "랜딩/UI 시안을 잡아줘" | `claude-design`, `popular-web-designs`, `design-md`, `p5js` | 디자인 시안, 프로토타입 |
| **카피·브랜딩** | "톤을 다듬고 카피를 써줘" | `humanizer`, `pretext`, `ideation`, `meme-generation` | 카피, 브랜드 메시지 |
| **음악·오디오** | "BGM/사운드를 만들어줘" | `songwriting-and-ai-music`, `heartmula`, `songsee` | 음원, 가사 |

## 3. 생산성 & 업무 자동화

| 아젠다 | 대표 의뢰 | 핵심 스킬 | 산출물 |
|--------|-----------|-----------|--------|
| **문서 파이프라인** | "PDF/문서를 처리·생성해줘" | `ocr-and-documents`, `nano-pdf`, `powerpoint`, `notion` | 정리된 문서, 슬라이드 |
| **메일·캘린더 자동화** | "메일/일정 운영을 자동화해줘" | `google-workspace`, `himalaya`, `agentmail` | 자동화 워크플로우 |
| **회의 운영** | "회의록·후속작업을 정리해줘" | `teams-meeting-pipeline`, `obsidian`, `one-three-one-rule` | 회의록, 액션 아이템 |
| **노코드 운영DB** | "운영 데이터를 표로 관리해줘" | `airtable`, `notion`, `shopify` | 운영 베이스/대시보드 |

## 4. 소프트웨어 엔지니어링 & DevOps

| 아젠다 | 대표 의뢰 | 핵심 스킬 | 산출물 |
|--------|-----------|-----------|--------|
| **코드베이스 진단** | "이 레포 구조/리스크를 파악해줘" | `codebase-inspection`, `code-wiki`, `gitnexus-explorer` | 아키텍처 노트, 진단 리포트 |
| **기능 개발(계획→구현)** | "이 기능을 설계하고 만들어줘" | `plan`, `spike`, `test-driven-development`, `subagent-driven-development` | 설계서, 구현 PR |
| **코드 리뷰·품질** | "PR을 리뷰/정리해줘" | `github-code-review`, `requesting-code-review`, `simplify-code` | 리뷰 코멘트, 리팩터링 |
| **디버깅** | "이 버그를 추적해줘" | `systematic-debugging`, `python-debugpy`, `node-inspect-debugger`, `rest-graphql-debug` | 원인 분석, 수정안 |
| **배포·운영** | "컨테이너/배포를 정리해줘" | `docker-management`, `hermes-s6-container-supervision`, `pinggy-tunnel` | 배포 구성, 운영 가이드 |

## 5. AI/ML 엔지니어링 & 에이전트

| 아젠다 | 대표 의뢰 | 핵심 스킬 | 산출물 |
|--------|-----------|-----------|--------|
| **모델 파인튜닝** | "우리 데이터로 모델을 학습시켜줘" | `fine-tuning-with-trl`, `unsloth`, `peft-fine-tuning`, `axolotl` | 학습 파이프라인, 체크포인트 |
| **추론 서빙** | "모델을 효율적으로 서빙해줘" | `serving-llms-vllm`, `llama-cpp`, `tensorrt-llm`, `modal-serverless-gpu` | 서빙 엔드포인트, 벤치 |
| **RAG / 벡터검색** | "사내 지식 검색을 붙여줘" | `chroma`, `qdrant-vector-search`, `pinecone`, `faiss` | RAG 파이프라인 |
| **평가·관측** | "모델 품질을 측정해줘" | `evaluating-llms-harness`, `weights-and-biases`, `dspy` | 평가 리포트, 대시보드 |
| **에이전트 구축** | "에이전트/MCP를 만들어줘" | `hermes-agent`, `fastmcp`, `claude-code`, `instructor`, `outlines` | 에이전트, MCP 서버 |
| **이미지/오디오 생성** | "이미지/음성 생성을 붙여줘" | `stable-diffusion-image-generation`, `whisper`, `audiocraft-audio-generation` | 생성 파이프라인 |

## 6. 데이터·금융·Web3

| 아젠다 | 대표 의뢰 | 핵심 스킬 | 산출물 |
|--------|-----------|-----------|--------|
| **재무 모델링** | "재무모델을 만들어줘" | `3-statement-model`, `dcf-model`, `lbo-model`, `merger-model` | Excel 재무모델 |
| **밸류에이션·비교** | "기업 가치를 평가해줘" | `comps-analysis`, `dcf-model`, `excel-author` | 밸류에이션 덱 |
| **시장·자산 분석** | "주식/온체인을 분석해줘" | `stocks`, `hyperliquid`, `evm`, `solana` | 분석 리포트 |

## 7. 보안 & 거버넌스

| 아젠다 | 대표 의뢰 | 핵심 스킬 | 산출물 |
|--------|-----------|-----------|--------|
| **웹 펜테스트** | "우리 서비스 취약점을 점검해줘" | `web-pentest`, `godmode` | 취약점 리포트 |
| **OSINT·포렌식** | "흔적/계정을 추적해줘" | `sherlock`, `oss-forensics` | 조사 보고서 |
| **시크릿 관리** | "자격증명을 안전하게 관리해줘" | `1password` | 시크릿 운영 가이드 |

> ⚠️ 보안 아젠다는 **인가된 대상에 한해** 진행합니다. 의뢰서에 범위·권한 근거를 명시하세요.

## 8. 스마트 라이프 (홈·헬스·게임)

| 아젠다 | 대표 의뢰 | 핵심 스킬 | 산출물 |
|--------|-----------|-----------|--------|
| **스마트홈 자동화** | "조명/기기를 자동화해줘" | `openhue` | 자동화 시나리오 |
| **헬스·피트니스** | "운동/영양 계획을 짜줘" | `fitness-nutrition` | 플랜, 트래킹 |
| **게임 서버 운영** | "게임 서버를 세팅해줘" | `minecraft-modpack-server`, `pokemon-player` | 서버 구성 |
