#!/usr/bin/env python3
"""
BMad Orchestrator - Simula o fluxo completo de QA
Substitui a orquestração por subagentes quando sessions_spawn está bloqueado
"""

import asyncio
import subprocess
import sys
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict
import json


class Severity(Enum):
    BLOCKER = "blocker"
    MAJOR = "major"
    MINOR = "minor"


class Status(Enum):
    PENDING = "pending"
    RUNNING = "running"
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class Finding:
    severity: Severity
    description: str
    location: str
    suggestion: str


@dataclass
class QAResult:
    agent_name: str
    status: Status
    findings: List[Finding] = field(default_factory=list)
    execution_time: float = 0.0


class BMadOrchestrator:
    """Orchestrates QA agents in parallel (simulated)"""
    
    def __init__(self, feature_id: str, max_retries: int = 3):
        self.feature_id = feature_id
        self.max_retries = max_retries
        self.results: Dict[str, QAResult] = {}
        
    async def run_qa_agent(self, agent_name: str, check_command: List[str]) -> QAResult:
        """Run a QA agent and return results"""
        print(f"🔍 Starting {agent_name}...")
        
        result = QAResult(agent_name=agent_name, status=Status.RUNNING)
        
        try:
            # Run the check command
            process = await asyncio.create_subprocess_exec(
                *check_command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                result.status = Status.PASSED
                print(f"✅ {agent_name} PASSED")
            else:
                result.status = Status.FAILED
                # Parse findings from output
                result.findings = self._parse_findings(stderr.decode())
                print(f"❌ {agent_name} FAILED")
                
        except Exception as e:
            result.status = Status.FAILED
            result.findings.append(Finding(
                severity=Severity.MAJOR,
                description=f"Agent execution failed: {str(e)}",
                location=agent_name,
                suggestion="Check agent configuration"
            ))
            print(f"💥 {agent_name} ERROR: {e}")
            
        return result
    
    def _parse_findings(self, output: str) -> List[Finding]:
        """Parse findings from agent output"""
        findings = []
        # Simple parsing - can be enhanced
        for line in output.split('\n'):
            if 'error' in line.lower() or 'warning' in line.lower():
                findings.append(Finding(
                    severity=Severity.MAJOR if 'error' in line.lower() else Severity.MINOR,
                    description=line,
                    location="unknown",
                    suggestion="Review code"
                ))
        return findings
    
    async def run_all_agents(self) -> Dict[str, QAResult]:
        """Run all QA agents in parallel"""
        
        agents = [
            ("Bug Founder", ["python", "-m", "scripts.qa_bug_founder"]),
            ("Code Quality", ["python", "-m", "scripts.qa_code_quality"]),
            ("Performance", ["python", "-m", "scripts.qa_performance"]),
            ("Security", ["python", "-m", "scripts.qa_security"]),
            ("TDD", ["python", "-m", "scripts.qa_tdd"]),
        ]
        
        # Run all agents concurrently
        tasks = [
            self.run_qa_agent(name, cmd)
            for name, cmd in agents
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                print(f"💥 Agent crashed: {result}")
            else:
                self.results[result.agent_name] = result
                
        return self.results
    
    def consolidate(self) -> Dict:
        """Consolidate all QA results into final verdict"""
        
        print("\n" + "="*60)
        print("🎯 BMad QA Consolidator")
        print("="*60)
        
        blockers = []
        majors = []
        minors = []
        
        for agent_name, result in self.results.items():
            for finding in result.findings:
                if finding.severity == Severity.BLOCKER:
                    blockers.append((agent_name, finding))
                elif finding.severity == Severity.MAJOR:
                    majors.append((agent_name, finding))
                else:
                    minors.append((agent_name, finding))
        
        # Determine verdict
        if blockers:
            verdict = "REPROVADO"
            retry_eligible = True
        elif len(majors) > 3:
            verdict = "REPROVADO"
            retry_eligible = True
        else:
            verdict = "APROVADO"
            retry_eligible = False
            
        # Print report
        print(f"\nFeature: {self.feature_id}")
        print(f"Verdict: {'✅' if verdict == 'APROVADO' else '❌'} {verdict}")
        print(f"Retry Eligible: {'Sim' if retry_eligible else 'Não'}")
        
        print(f"\n🚫 Blockers ({len(blockers)}):")
        for agent, finding in blockers:
            print(f"  [{agent}] {finding.description}")
            
        print(f"\n⚠️ Majors ({len(majors)}):")
        for agent, finding in majors[:5]:  # Limit output
            print(f"  [{agent}] {finding.description}")
            
        print(f"\nℹ️ Minors ({len(minors)}):")
        print(f"  ... ({len(minors)} minor issues)")
        
        print("\n📊 Per-QA Summary:")
        for agent_name, result in self.results.items():
            status_icon = "✅" if result.status == Status.PASSED else "❌"
            print(f"  {status_icon} {agent_name}: {len(result.findings)} findings")
        
        return {
            "feature_id": self.feature_id,
            "verdict": verdict,
            "blockers": len(blockers),
            "majors": len(majors),
            "minors": len(minors),
            "retry_eligible": retry_eligible,
            "results": {
                name: {
                    "status": r.status.value,
                    "findings": len(r.findings)
                }
                for name, r in self.results.items()
            }
        }


class BMadRetryLoop:
    """Implements retry logic for BMad"""
    
    def __init__(self, orchestrator: BMadOrchestrator, max_retries: int = 3):
        self.orchestrator = orchestrator
        self.max_retries = max_retries
        self.current_attempt = 0
        
    async def run_with_retry(self) -> Dict:
        """Run QA with automatic retry"""
        
        while self.current_attempt < self.max_retries:
            self.current_attempt += 1
            print(f"\n🔄 Attempt {self.current_attempt}/{self.max_retries}")
            print("="*60)
            
            # Run all agents
            await self.orchestrator.run_all_agents()
            
            # Consolidate results
            result = self.orchestrator.consolidate()
            
            # Check if we should retry
            if result["verdict"] == "APROVADO":
                print("\n✅ QA Passed! No retry needed.")
                return result
                
            if not result["retry_eligible"]:
                print("\n❌ QA Failed. Not eligible for retry.")
                return result
                
            if self.current_attempt >= self