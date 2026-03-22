"""
D2 - Secure XML Prompt Builder
Builds structured prompts with strict XML boundaries.
"""

from typing import List, Dict, Any


class PromptBuilder:
    """Build secure XML-structured prompts for LLM."""
    
    def build_compliance_prompt(
        self,
        query: str,
        criterion: str,
        framework: str,
        metric_name: str,
        confidence: Dict[str, Any],
        coverage: Dict[str, Any],
        sanitized_chunks: List[Dict[str, Any]]
    ) -> str:
        """
        Build secure XML prompt for compliance auditing.
        
        Args:
            query: User query
            criterion: Criterion ID
            framework: NAAC or NBA
            metric_name: Full metric name
            confidence: Confidence scores
            coverage: Dimension coverage
            sanitized_chunks: Sanitized evidence chunks
            
        Returns:
            XML-structured prompt string
        """
        # Build system instructions
        system_instructions = self._build_system_instructions()
        
        # Build hypothetical ideal answer
        hypothetical = self._build_hypothetical_ideal(framework, criterion, metric_name)
        
        # Build retrieved context
        context = self._build_retrieved_context(sanitized_chunks)
        
        # Build output schema
        schema = self._build_output_schema()
        
        # Assemble full prompt
        prompt = f"""<SYSTEM_INSTRUCTIONS>
{system_instructions}
</SYSTEM_INSTRUCTIONS>

<USER_QUERY>
{query}
</USER_QUERY>

<CRITERION_INFO>
Framework: {framework}
Criterion: {criterion}
Metric: {metric_name}
Confidence Score: {confidence['confidence_score']:.3f} ({confidence['status']})
Dimensions Covered: {', '.join(coverage['dimensions_covered']) if coverage['dimensions_covered'] else 'None'}
Dimensions Missing: {', '.join(coverage['dimensions_missing']) if coverage['dimensions_missing'] else 'None'}
</CRITERION_INFO>

<HYPOTHETICAL_IDEAL>
{hypothetical}
</HYPOTHETICAL_IDEAL>

<RETRIEVED_CONTEXT>
{context}
</RETRIEVED_CONTEXT>

<OUTPUT_SCHEMA>
{schema}
</OUTPUT_SCHEMA>"""
        
        return prompt
    
    def _build_system_instructions(self) -> str:
        """Build system instructions section."""
        return """You are a compliance auditing expert for educational accreditation with deep knowledge of NAAC/NBA requirements.

PRIMARY TASK: Answer the user's specific question FIRST using the retrieved evidence.

Your responsibilities:
1. FIRST: Directly answer the user's query in the USER_QUERY section
2. THEN: Analyze retrieved evidence chunks
3. Summarize what evidence was found (reference actual numbers from evidence)
4. Identify gaps in the evidence
5. Provide CONCRETE, ACTIONABLE recommendations with REAL examples

CRITICAL: Your recommendations MUST be SPECIFIC and IMPLEMENTABLE:
❌ BAD: "Improve research funding documentation"
✅ GOOD: "Apply for DST-SERB Core Research Grant (₹25-50 Lakhs). Deadline: June 2026. Contact: Dr. [Name], Research Cell"

❌ BAD: "Organize faculty development programs"
✅ GOOD: "Host 5-day FDP on 'AI in Education' (AICTE approved, 50 participants). Budget: ₹2 Lakhs. Partner with IIT/NIT for resource persons"

❌ BAD: "Enhance student activities"
✅ GOOD: "Launch National Tech Fest 'Innovate 2026' (500+ participants, 20+ colleges). Include hackathon, paper presentations, workshops. Budget: ₹5 Lakhs"

Your recommendations should include:
- Specific program/event names
- Target numbers (participants, budget, duration)
- Funding sources or agencies
- Timeline/deadlines
- Responsible departments/persons
- Expected outcomes with metrics

Examples of CONCRETE actions by criterion:
- Research (3.2.1): "Apply for ICSSR Major Research Project (₹15-20 Lakhs). Topic: [relevant to institution]. PI: Dr. [Name]. Deadline: August 2026"
- Teaching (2.4.2): "Launch Certificate Course in 'Data Analytics' (60 hours, 100 students/year). Partner with IBM/Microsoft for curriculum. Fee: ₹15,000"
- Extension (3.4.1): "Adopt 5 villages under Unnat Bharat Abhiyan. Conduct health camps (500 beneficiaries), skill training (200 youth), literacy programs"
- Infrastructure (4.1.2): "Upgrade library with 5000 e-books, 20 e-journals (IEEE, Springer). Budget: ₹10 Lakhs. Complete by Dec 2026"
- Student Support (5.1.3): "Establish Career Guidance Cell. Conduct 50 industry visits, 20 guest lectures, 10 placement drives. Target: 80% placement"

Critical rules:
- PRIORITIZE answering the user's specific question
- Use ONLY the retrieved evidence provided (reference actual data from evidence)
- Do NOT invent or fabricate data about the institution
- Do NOT contradict the confidence score
- Do NOT determine compliance status (already calculated)
- If only templates/guidelines found, state "no institutional evidence found"
- Be precise and factual
- Tailor your response to what the user asked
- Make recommendations ACTIONABLE with real-world examples"""
    
    def _build_hypothetical_ideal(self, framework: str, criterion: str, metric_name: str) -> str:
        """Build hypothetical ideal answer section."""
        return f"""For {framework} {criterion} ({metric_name}), ideal evidence would include:
- Specific institutional data with numbers and dates
- Documented proof from institutional records
- Clear mapping to all required dimensions
- Verifiable sources with page references

The retrieved evidence should demonstrate actual institutional compliance, not just framework guidelines."""
    
    def _build_retrieved_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Build retrieved context section with sanitized chunks."""
        if not chunks:
            return "No evidence chunks retrieved."
        
        context_parts = []
        
        for i, chunk in enumerate(chunks[:5], 1):  # Top 5 chunks
            child_text = chunk.get('child_text', '')[:500]  # Limit length
            source = chunk.get('source', 'Unknown')
            page = chunk.get('page', 'N/A')
            source_type = chunk.get('source_type', 'unknown')
            
            context_parts.append(
                f"""<EVIDENCE_{i}>
Source: {source}
Page: {page}
Type: {source_type}
Text: {child_text}...
</EVIDENCE_{i}>"""
            )
        
        return '\n\n'.join(context_parts)
    
    def _build_output_schema(self) -> str:
        """Build output schema specification."""
        return """Return ONLY valid JSON with these exact fields:

{
  "evidence_summary": "Brief summary of what evidence was found with SPECIFIC NUMBERS from the evidence (2-3 sentences). Example: 'Found 15 research projects totaling ₹45 Lakhs from DST and SERB during 2019-2023'",
  "gaps": ["List of missing information with specifics. Example: 'No evidence of funding from industry partners', 'Missing year-wise breakdown for 2022-23'"],
  "recommendation": "CONCRETE, ACTIONABLE next steps with REAL examples. Include: (1) Specific programs/events to launch, (2) Target numbers (budget, participants, timeline), (3) Funding sources, (4) Responsible departments. Example: 'Apply for DST-SERB Core Research Grant (₹25-50 Lakhs, Deadline: June 2026). Launch National Conference on AI (300 participants, Budget: ₹8 Lakhs). Establish Industry Collaboration Cell - target 5 MoUs with IT companies for funded projects (₹10-15 Lakhs each)'"
}

CRITICAL: Make recommendations SPECIFIC and IMPLEMENTABLE:
- Include actual program names, not generic advice
- Provide budget estimates and timelines
- Mention specific funding agencies (DST, SERB, ICSSR, DBT, AICTE, UGC, Industry)
- Give target numbers (participants, beneficiaries, duration)
- Suggest partnerships (IITs, NITs, Industry, NGOs)

Do NOT include:
- confidence_score (already calculated)
- compliance_status (already calculated)
- coverage_ratio (already calculated)

Return ONLY the JSON object, no markdown, no additional text."""
