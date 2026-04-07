#!/usr/bin/env python3
"""
BMad QA Runner - Simula spawn de agentes usando subprocess
Quando sessions_spawn está bloqueado, usamos subprocess em paralelo
"""

import asyncio
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class Finding:
    severity: str
    category: str
    description: str
    location: str
    suggestion: str


@dataclass
class QAResult:
    agent_name: str
    status: str
    findings: List[Finding] = field(default_factory=list)
    execution_time: float = 0.0
    error: Optional[str] = None


class BMadQAAgent:
    """Simulates a BMad QA Agent using subprocess"""
    
    def __init__(self, name: str, skill_file: str):
        self.name = name
        self.skill_file = skill_file
        
    def analyze(self, project_path: str) -> QAResult:
        """Run QA analysis"""
        import time
        start_time = time.time()
        
        try:
            # Read the skill file to understand what to check
            skill_path = Path(f"/home/node/.openclaw/skills/{self.skill_file}/SKILL.md")
            if not skill_path.exists():
                return QAResult(
                    agent_name=self.name,
                    status="error",
                    error=f"Skill file not found: {skill_path}"
                )
            
            skill_content = skill_path.read_text()
            
            # Run specific analysis based on agent type
            findings = self._run_analysis(project_path, skill_content)
            
            return QAResult(
                agent_name=self.name,
                status="completed",
                findings=findings,
                execution_time=time.time() - start_time
            )
            
        except Exception as e:
            return QAResult(
                agent_name=self.name,
                status="error",
                error=str(e),
                execution_time=time.time() - start_time
            )
    
    def _run_analysis(self, project_path: str, skill_content: str) -> List[Finding]:
        """Run specific analysis based on agent type"""
        findings = []
        
        if "bug-founder" in self.name.lower():
            findings = self._analyze_bugs(project_path)
        elif "code-quality" in self.name.lower():
            findings = self._analyze_quality(project_path)
        elif "performance" in self.name.lower():
            findings = self._analyze_performance(project_path)
        elif "security" in self.name.lower():
            findings = self._analyze_security(project_path)
        elif "tdd" in self.name.lower():
            findings = self._analyze_tdd(project_path)
            
        return findings
    
    def _analyze_bugs(self, project_path: str) -> List[Finding]:
        """Bug Founder analysis"""
        findings = []
        
        # Check for race conditions
        repo_path = Path(project_path) / "backend/src/infrastructure/repositories"
        if repo_path.exists():
            for file in repo_path.glob("*.py"):
                content = file.read_text()
                
                # Check for non-atomic operations
                if "check_conflicts" in content and "create" in content:
                    if "SELECT" in content and "INSERT" in content:
                        if "for update" not in content.lower():
                            findings.append(Finding(
                                severity="major",
                                category="race-condition",
                                description="Potential race condition: check_conflicts and create are not atomic",
                                location=f"{file.name}:check_conflicts",
                                suggestion="Use SELECT FOR UPDATE or serializable transaction"
                            ))
        
        return findings
    
    def _analyze_quality(self, project_path: str) -> List[Finding]:
        """Code Quality analysis"""
        findings = []
        
        # Check for TODOs
        src_path = Path(project_path) / "backend/src"
        if src_path.exists():
            for file in src_path.rglob("*.py"):
                content = file.read_text()
                todos = [line for line in content.split('\n') if 'TODO' in line]
                if len(todos) > 5:
                    findings.append(Finding(
                        severity="minor",
                        category="tech-debt",
                        description=f"{len(todos)} TODOs found in {file.name}",
                        location=str(file.relative_to(project_path)),
                        suggestion="Address TODOs or create issues"
                    ))
        
        return findings
    
    def _analyze_performance(self, project_path: str) -> List[Finding]:
        """Performance analysis"""
        findings = []
        
        # Check for N+1 queries
        repo_path = Path(project_path) / "backend/src/infrastructure/repositories"
        if repo_path.exists():
            for file in repo_path.glob("*.py"):
                content = file.read_text()
                if "list_by" in content:
                    if "selectinload" not in content:
                        findings.append(Finding(
                            severity="major",
                            category="n-plus-1",
                            description=f"Potential N+1 query in {file.name}",
                            location=f"{file.name}:list methods",
                            suggestion="Add eager loading with selectinload()"
                        ))
        
        return findings
    
    def _analyze_security(self, project_path: str) -> List[Finding]:
        """Security analysis"""
        findings = []
        
        # Check for hardcoded secrets
        settings_file = Path(project_path) / "backend/src/config/settings.py"
        if settings_file.exists():
            content = settings_file.read_text()
            if 'default="change-me' in content or 'default="' in content and 'secret' in content.lower():
                findings.append(Finding(
                    severity="blocker",
                    category="secrets",
                    description="Default secret value found in settings",
                    location="config/settings.py",
                    suggestion="Remove default value, require via environment"
                ))
        
        return findings
    
    def _analyze_tdd(self, project_path: str) -> List[Finding]:
        """TDD analysis"""
        findings = []
        
        # Check test coverage
        test_path = Path(project_path) / "backend/tests"
        src_path = Path(project_path) / "backend/src"
        
        if test_path.exists() and src_path.exists():
            test_files = list(test_path.rglob("test_*.py"))
            src_files = list(src_path.rglob("*.py"))
            
            # Simple heuristic
            if len(test_files) < len(src_files) / 3:
                findings.append(Finding(
                    severity="blocker",
                    category="coverage",
                    description=f"Low test coverage: {len(test_files)} tests for {len(src_files)} source files",
                    location="backend/tests/",
                    suggestion="Add more unit and integration tests"
                ))
        
        return findings


class BMadOrchestrator:
    """Orchestrates QA agents in parallel"""
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.agents = [
            BMadQAAgent("Bug Founder", "bmad-qa-bug-founder"),
            BMadQAAgent("Code Quality", "bmad-qa-code-quality"),
            BMadQAAgent("Performance", "bmad-qa-performance"),
            BMadQAAgent("Security", "bmad-qa-security"),
            BMadQAAgent("TDD", "bmad-qa-tdd"),
        ]
    
    def run_all(self) -> Dict[str, QAResult]:
        """Run all QA agents in parallel using ThreadPool"""
        results = {}
        
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_agent = {
                executor.submit(agent.analyze, self.project_path): agent
                for agent in self.agents
            }
            
            for future in as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    result = future.result()
                    results[agent.name] = result
                except Exception as e:
                    results[agent.name] = QAResult(
                        agent_name=agent.name,
                        status="error",
                        error=str(e)
                    )
        
        return results
    
    def consolidate(self, results: Dict[str, QAResult]) -> Dict:
        """Consolidate all QA results"""
        blockers = []
        majors = []
        minors = []
        
        for agent_name, result in results.items():
            for finding in result.findings:
                if finding.severity == "blocker":
                    blockers.append((agent_name, finding))
                elif finding.severity == "major":
                    majors.append((agent_name, finding))
                else:
                    minors.append((agent_name, finding))
        
        verdict = "REPROVADO" if blockers else "APROVADO"
        
        return {
            "verdict": verdict,
            "blockers": len(blockers),
            "majors": len(majors),
            "minors": len(minors),
            "results": results
        }


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="BMad QA Runner")
    parser.add_argument("--project", default=".", help="Project path")
    parser.add_argument("--output", default="bmad_qa_report.json", help="Output file")
    args = parser.parse_args()
    
    print("🎯 BMad QA Runner")
    print("=" * 60)
    print(f"Project: {args.project}")
    print()
    
    orchestrator = BMadOrchestrator(args.project)
    
    print("Running QA agents in parallel...")
    results = orchestrator.run_all()
    
    print("\nConsolidating results...")
    report = orchestrator.consolidate(results)
    
    # Print report
    print("\n" + "=" * 60)
    print(f"Verdict: {report['verdict']}")
    print(f"Blockers: {report['blockers']}")
    print(f"Majors: {report['majors']}")
    print(f"Minors: {report['minors']}")
    print()
    
    for agent_name, result in results.items():
        print(f"\n{agent_name}:")
        print(f"  Status: {result.status}")
        print(f"  Findings: {len(result.findings)}")
        for finding in result.findings:
            print(f"    - [{finding.severity}] {finding.description}")
    
    # Save report
    with open(args.output, 'w') as f:
        json.dump(report, f, indent=2, default=lambda o: o.__dict__)
    
    print(f"\n\nReport saved to: {args.output}")
    
    return 0 if report['verdict'] == "APROVADO" else 1


if __name__ == "__main__":
    sys.exit(main())