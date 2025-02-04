# PanelOfAgents

A flexible and powerful framework for orchestrating multiple AI agents in domain-specific applications, with support for any LLM backend.

## Introduction

This framework enables seamless orchestration of multiple AI agents for domain-specific applications. Inspired by OpenAI's swarm framework but addressing its limitations, our solution offers greater flexibility in agent interactions without being tied to specific LLM implementations.

### Purpose

- Create a simple yet powerful multi-agent orchestration framework
- Enable flexible task handoffs between agents in single-domain applications
- Provide a production-ready alternative to experimental frameworks
- Support integration with various LLM implementations

### Why This Framework?

Unlike OpenAI's swarm framework, which is limited to GPT models and requires predefined handoffs, this framework offers:
- Model-agnostic implementation
- Dynamic agent interactions
- Production-ready architecture
- Flexible integration options

## Features

- **🚀 Flexible Multi-agent Orchestration** - Dynamic task distribution and collaboration between agents
- **⚡️ Real-time Communication** - Token-by-token streaming with minimal latency
- **🔄 Rich Context Sharing** - Comprehensive context including conversation history, action results, and artifacts
- **🔌 Universal LLM Support** - Compatible with any LangChain BaseChatModel implementation
- **🎯 Targeted Agent Usage** - Smart agent selection based on capabilities rather than predefined rules
- **⚙️ Developer-First Design** - Flexible state management and easy service integration
