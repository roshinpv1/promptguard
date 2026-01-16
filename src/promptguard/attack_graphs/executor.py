from __future__ import annotations

from typing import Any, Dict, List

from promptguard.models import AttackGraph, AttackGraphResult, AttackNode, ProbeResult, Severity
from promptguard.probes.base import ProbeExecutor


class AttackGraphExecutor:
    """Executor for attack graphs (multi-step adversarial flows)."""

    def __init__(self, probe_executor: ProbeExecutor, probe_registry: Dict[str, Any]):
        """
        Initialize attack graph executor.
        
        Args:
            probe_executor: Executor for individual probes
            probe_registry: Registry mapping probe_id to Probe objects
        """
        self.probe_executor = probe_executor
        self.probe_registry = probe_registry

    def execute(
        self, graph: AttackGraph, context: Dict[str, Any]
    ) -> AttackGraphResult:
        """
        Execute an attack graph.
        
        Args:
            graph: The attack graph to execute
            context: Execution context
        
        Returns:
            AttackGraphResult with all node results
        """
        node_results: Dict[str, ProbeResult] = {}
        executed_nodes: set[str] = set()
        
        # Find entry nodes (nodes with no incoming edges)
        entry_nodes = self._find_entry_nodes(graph)
        
        # Execute graph using topological order
        for node in self._topological_sort(graph, entry_nodes):
            if node.node_id in executed_nodes:
                continue
            
            # Check condition
            if node.condition and not self._evaluate_condition(
                node.condition, node_results, context
            ):
                continue
            
            # Get probe
            probe = self.probe_registry.get(node.probe_id)
            if not probe:
                continue
            
            # Execute probe
            result = self.probe_executor.execute(probe, context)
            node_results[node.node_id] = result
            executed_nodes.add(node.node_id)
            
            # Update context with result for next nodes
            context[f"node_{node.node_id}_result"] = result
        
        # Compute overall risk
        overall_risk = self._compute_overall_risk(node_results)
        severity = self._risk_to_severity(overall_risk)
        evidence = self._build_evidence(node_results)
        
        return AttackGraphResult(
            graph_id=graph.graph_id,
            node_results=node_results,
            overall_risk_score=overall_risk,
            severity=severity,
            evidence=evidence,
            metadata={"executed_nodes": list(executed_nodes)},
        )
    
    def _find_entry_nodes(self, graph: AttackGraph) -> List[AttackNode]:
        """Find nodes with no incoming edges."""
        incoming: set[str] = {edge[1] for edge in graph.edges}
        return [node for node in graph.nodes if node.node_id not in incoming]
    
    def _topological_sort(
        self, graph: AttackGraph, entry_nodes: List[AttackNode]
    ) -> List[AttackNode]:
        """Topological sort of graph nodes."""
        # Simple implementation - execute in order
        # Can be enhanced with proper topological sort
        visited: set[str] = set()
        result: List[AttackNode] = []
        
        def visit(node: AttackNode):
            if node.node_id in visited:
                return
            visited.add(node.node_id)
            # Visit dependencies first
            for from_id, to_id in graph.edges:
                if to_id == node.node_id:
                    dep_node = next((n for n in graph.nodes if n.node_id == from_id), None)
                    if dep_node:
                        visit(dep_node)
            result.append(node)
        
        for entry in entry_nodes:
            visit(entry)
        
        # Add any remaining nodes
        for node in graph.nodes:
            if node.node_id not in visited:
                result.append(node)
        
        return result
    
    def _evaluate_condition(
        self, condition: str, node_results: Dict[str, ProbeResult], context: Dict[str, Any]
    ) -> bool:
        """Evaluate condition for node execution."""
        # Simple condition evaluation
        # Supports: "previous.success", "previous.failure", etc.
        if condition == "previous.success":
            # Check if previous node succeeded (risk > 0)
            if node_results:
                last_result = list(node_results.values())[-1]
                return last_result.risk_score > 0
            return True
        elif condition == "previous.failure":
            if node_results:
                last_result = list(node_results.values())[-1]
                return last_result.risk_score == 0
            return True
        # Default: always execute
        return True
    
    def _compute_overall_risk(self, node_results: Dict[str, ProbeResult]) -> float:
        """Compute overall risk score from node results."""
        if not node_results:
            return 0.0
        # Use maximum risk across all nodes
        return max(result.risk_score for result in node_results.values())
    
    def _risk_to_severity(self, risk_score: float) -> Severity:
        """Convert risk score to severity."""
        if risk_score >= 3.0:
            return Severity.CRITICAL
        elif risk_score >= 2.0:
            return Severity.HIGH
        elif risk_score >= 1.0:
            return Severity.MEDIUM
        elif risk_score > 0.0:
            return Severity.LOW
        return Severity.INFO
    
    def _build_evidence(self, node_results: Dict[str, ProbeResult]) -> List[str]:
        """Build evidence from node results."""
        evidence = []
        for node_id, result in node_results.items():
            if result.risk_score > 0:
                evidence.append(f"Node {node_id}: {', '.join(result.evidence)}")
        return evidence

