#\!/usr/bin/env python3
"""
Fabric Fast-Track AI Assistant Router
Multi-provider LLM router with cost tracking
"""

import os
import sqlite3
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import openai
import anthropic

class LLMRouter:
    def __init__(self, db_path: str = "cost_log.sqlite"):
        self.db_path = db_path
        self.setup_database()
        self.offline_mode = os.getenv('LLM_OFFLINE', 'False').lower() == 'true'
        
    def setup_database(self):
        """Initialize cost tracking database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS llm_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                provider TEXT,
                model TEXT,
                prompt_tokens INTEGER,
                completion_tokens INTEGER,
                total_tokens INTEGER,
                cost_usd REAL,
                feature TEXT
            )
        ''')
        conn.commit()
        conn.close()
        
    def route_request(self, prompt: str, provider: str = "openai", feature: str = "general") -> str:
        """Route request to appropriate LLM provider"""
        
        if self.offline_mode:
            return self._offline_response(prompt, feature)
            
        try:
            if provider == "openai":
                return self._call_openai(prompt, feature)
            elif provider == "claude":
                return self._call_claude(prompt, feature)
            elif provider == "local":
                return self._call_local(prompt, feature)
            else:
                raise ValueError(f"Unknown provider: {provider}")
                
        except Exception as e:
            logging.error(f"LLM call failed: {e}")
            return self._offline_response(prompt, feature)
    
    def _call_openai(self, prompt: str, feature: str) -> str:
        """Call OpenAI API"""
        client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )
        
        # Log usage
        self._log_usage(
            provider="openai",
            model="gpt-4o-mini", 
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            total_tokens=response.usage.total_tokens,
            cost_usd=self._calculate_openai_cost(response.usage),
            feature=feature
        )
        
        return response.choices[0].message.content
    
    def _call_claude(self, prompt: str, feature: str) -> str:
        """Call Anthropic Claude API"""
        client = anthropic.Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Log usage (simplified - actual token counting needed)
        self._log_usage(
            provider="claude",
            model="claude-3-haiku",
            prompt_tokens=len(prompt.split()) * 1.3,  # Rough estimate
            completion_tokens=len(response.content[0].text.split()) * 1.3,
            total_tokens=0,
            cost_usd=0.01,  # Placeholder
            feature=feature
        )
        
        return response.content[0].text
    
    def _call_local(self, prompt: str, feature: str) -> str:
        """Call local Ollama instance"""
        # Placeholder for local LLM integration
        return f"[LOCAL] Processed request for {feature}: {prompt[:50]}...";
    
    def _offline_response(self, prompt: str, feature: str) -> str:
        """Return deterministic offline response"""
        responses = {
            "dax_genie": "-- Generated DAX measure\nSample Measure = SUM(Table[Column])",
            "source_mapper": "# Generated source mapping\nsource: sample_table\ndestination: bronze/sample",
            "qa_buddy": "✅ No issues detected in logs",
            "release_scribe": "## Release Notes\n- Updated core functionality"
        }
        return responses.get(feature, "Offline mode - limited functionality")
    
    def _calculate_openai_cost(self, usage) -> float:
        """Calculate OpenAI API cost"""
        # GPT-4o-mini pricing (as of 2024)
        input_cost = usage.prompt_tokens * 0.00015 / 1000
        output_cost = usage.completion_tokens * 0.0006 / 1000
        return input_cost + output_cost
    
    def _log_usage(self, **kwargs):
        """Log API usage to database"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            INSERT INTO llm_usage 
            (timestamp, provider, model, prompt_tokens, completion_tokens, total_tokens, cost_usd, feature)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            datetime.now().isoformat(),
            kwargs['provider'],
            kwargs['model'],
            kwargs['prompt_tokens'],
            kwargs['completion_tokens'], 
            kwargs['total_tokens'],
            kwargs['cost_usd'],
            kwargs['feature']
        ))
        conn.commit()
        conn.close()

if __name__ == "__main__":
    router = LLMRouter()
    print(router.route_request("Generate a DAX measure for total sales", "openai", "dax_genie"))
