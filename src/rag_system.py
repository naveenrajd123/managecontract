"""
RAG System - Retrieval Augmented Generation
This is the brain of our contract analysis system!

What is RAG?
- RAG = Retrieval + Augmented + Generation
- We break contracts into chunks, store them in a vector database
- When asked a question, we find relevant chunks and send them to the AI
- The AI generates answers based on actual contract content
"""

import google.generativeai as genai
from typing import List, Dict, Any
import os
from datetime import datetime
from src.config import settings

# Initialize Google Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)


class ContractRAGSystem:
    """
    The RAG system that handles contract analysis using Google Gemini.
    Note: Simplified version without ChromaDB for Python 3.14 compatibility.
    """
    
    def __init__(self):
        """Initialize the RAG system with Gemini."""
        
        # Create uploads directory if it doesn't exist
        os.makedirs(settings.UPLOAD_DIRECTORY, exist_ok=True)
        
        # Initialize Google Gemini model (using gemini-2.5-flash, the latest stable model)
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        
        # Simple in-memory storage for contracts (replaces ChromaDB temporarily)
        self.contracts_storage = {}
    
    def chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Why chunking?
        - Contracts can be very long (100+ pages)
        - AI models have token limits
        - Smaller chunks = more precise retrieval
        
        Args:
            text: The contract text to split
            chunk_size: Characters per chunk
            overlap: Characters to overlap between chunks (maintains context)
        
        Returns:
            List of text chunks
        """
        chunks = []
        start = 0
        text_length = len(text)
        
        while start < text_length:
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += (chunk_size - overlap)
        
        return chunks
    
    async def add_contract_to_vectordb(
        self,
        contract_id: int,
        contract_text: str,
        contract_metadata: Dict[str, Any]
    ):
        """
        Add a contract to storage for search.
        Chunks the contract for better retrieval.
        
        Args:
            contract_id: Unique contract ID
            contract_text: Full contract text
            contract_metadata: Additional info (name, parties, dates, etc.)
        """
        # Chunk the contract text for better retrieval
        chunks = self.chunk_text(contract_text, chunk_size=3000, overlap=500)
        
        # Store contract with chunks
        self.contracts_storage[contract_id] = {
            "text": contract_text,
            "chunks": chunks,
            "metadata": contract_metadata
        }
        
        print(f"[INFO] Added contract ID {contract_id} to RAG storage. Total contracts: {len(self.contracts_storage)}")
    
    async def load_contract_from_file(
        self,
        contract_id: int,
        file_path: str,
        contract_metadata: Dict[str, Any]
    ):
        """
        Load an existing contract from file into the RAG system.
        Used during startup to reload contracts from database.
        
        Args:
            contract_id: Unique contract ID
            file_path: Path to the contract file
            contract_metadata: Contract metadata (name, parties, etc.)
        """
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"[WARNING] Contract file not found: {file_path}")
                return
            
            # Read contract text based on file type
            file_extension = os.path.splitext(file_path)[1].lower()
            contract_text = ""
            
            if file_extension == ".txt":
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    contract_text = f.read()
            elif file_extension == ".pdf":
                try:
                    from PyPDF2 import PdfReader
                    reader = PdfReader(file_path)
                    for page in reader.pages:
                        contract_text += page.extract_text()
                except Exception as e:
                    print(f"[ERROR] Failed to read PDF {file_path}: {e}")
                    return
            
            # Add to RAG system if we got content
            if contract_text and len(contract_text) > 100:
                await self.add_contract_to_vectordb(
                    contract_id=contract_id,
                    contract_text=contract_text,
                    contract_metadata=contract_metadata
                )
                print(f"[INFO] Loaded contract {contract_metadata.get('number', contract_id)} into RAG system")
            else:
                print(f"[WARNING] Contract file is empty or too short: {file_path}")
                
        except Exception as e:
            print(f"[ERROR] Failed to load contract {contract_id}: {e}")
    
    def search_contracts(
        self,
        query: str,
        n_results: int = 5,
        contract_id: int = None
    ) -> Dict[str, Any]:
        """
        Search across contracts using enhanced keyword matching on chunks.
        Now includes semantic keyword expansion for better results.
        
        Args:
            query: Search question
            n_results: Number of results to return
            contract_id: Optional - search only in specific contract
        
        Returns:
            Dictionary with relevant text chunks
        """
        documents = []
        query_lower = query.lower()
        
        # Enhanced keyword extraction with semantic mappings
        keywords = [word for word in query_lower.split() if len(word) > 3]
        
        # Semantic keyword expansion for better matching
        semantic_expansions = {
            'date': ['date', 'effective', 'execution', 'commence', 'start', 'end', 'termination', 'expiration', 'expire', 'term', 'period', 'duration', 'until', 'from', 'renewal'],
            'payment': ['payment', 'fee', 'cost', 'price', 'invoice', 'compensation', 'amount', 'value', 'quarterly', 'monthly', 'annual'],
            'termination': ['termination', 'terminate', 'cancel', 'cancellation', 'end', 'expiration', 'expire', 'notice', 'breach'],
            'party': ['party', 'parties', 'vendor', 'client', 'company', 'provider', 'supplier', 'customer'],
            'liability': ['liability', 'liable', 'damages', 'limitation', 'indemnify', 'indemnification', 'responsible'],
            'confidential': ['confidential', 'confidentiality', 'non-disclosure', 'proprietary', 'secret'],
            'renewal': ['renewal', 'renew', 'extend', 'extension', 'auto-renew', 'automatic'],
            'obligation': ['obligation', 'duty', 'responsibility', 'requirement', 'must', 'shall'],
            'penalty': ['penalty', 'penalties', 'damages', 'liquidated', 'fine', 'breach'],
            'risk': ['risk', 'risks', 'liability', 'exposure', 'assessment'],
        }
        
        # Expand keywords based on semantic mappings
        expanded_keywords = set(keywords)
        for keyword in keywords:
            for key, values in semantic_expansions.items():
                if keyword in values or keyword == key:
                    expanded_keywords.update(values)
        
        # Convert back to list
        expanded_keywords = list(expanded_keywords)
        
        if contract_id and contract_id in self.contracts_storage:
            # Search specific contract chunks
            contract_data = self.contracts_storage[contract_id]
            chunks = contract_data.get("chunks", [contract_data["text"]])
            
            # Score chunks based on keyword matches with expanded keywords
            chunk_scores = []
            for idx, chunk in enumerate(chunks):
                chunk_lower = chunk.lower()
                
                # Calculate score with original keywords (higher weight)
                original_score = sum(chunk_lower.count(keyword) * 3 for keyword in keywords)
                
                # Calculate score with expanded keywords (lower weight)
                expanded_score = sum(chunk_lower.count(keyword) for keyword in expanded_keywords)
                
                # Bonus for chunks at the beginning (often contain key info)
                position_bonus = max(0, 10 - idx)
                
                total_score = original_score + expanded_score + position_bonus
                
                if total_score > 0:
                    chunk_scores.append((total_score, chunk))
            
            # Sort by score and get top chunks
            chunk_scores.sort(reverse=True, key=lambda x: x[0])
            documents = [chunk for score, chunk in chunk_scores[:n_results]]
            
            # If no keyword matches, return first few chunks (likely contains intro/key info)
            if not documents:
                documents = chunks[:min(3, len(chunks))]
                
        elif not contract_id:
            # Search all contracts
            for cid, data in list(self.contracts_storage.items())[:n_results]:
                chunks = data.get("chunks", [data["text"][:3000]])
                # Get first chunk of each contract
                if chunks:
                    documents.append(chunks[0])
        
        return {"documents": [documents] if documents else [[]]}
    
    async def generate_contract_summary(self, contract_text: str) -> str:
        """
        Generate a concise summary of the contract using Gemini.
        
        Args:
            contract_text: Full or partial contract text
        
        Returns:
            AI-generated summary
        """
        # Truncate if too long (Gemini has token limits)
        max_chars = 30000
        if len(contract_text) > max_chars:
            contract_text = contract_text[:max_chars] + "..."
        
        prompt = f"""
        You are a legal contract analyst. Analyze the following contract and provide a structured summary with MAIN SECTIONS and SUB-SECTIONS.
        
        CRITICAL FORMATTING RULES:
        1. Use **BOLD CAPS** for main section headers (e.g., **MAIN PARTIES**, **KEY OBLIGATIONS**)
        2. Use **Bold Title Case** for subsection headers (e.g., **Vendor Obligations:**, **Payment Structure:**)
        3. Use bullet points (- or *) for individual items under subsections
        4. Bold important values: party names, dates, amounts, percentages, penalties
        5. Create clear hierarchy with indentation using spaces
        6. Keep each bullet point SHORT and scannable
        
        REQUIRED STRUCTURE:
        
        **MAIN PARTIES**
        - **Party A (Client/Company):** [Name and location]
        - **Party B (Vendor/Provider):** [Name and location]
        
        **KEY OBLIGATIONS**
          **Vendor Obligations:**
          - [obligation 1]
          - [obligation 2]
          - [obligation 3]
          
          **Client Obligations:**
          - [obligation 1]
          - [obligation 2]
          
          **Mutual Obligations:**
          - [if any mutual obligations]
        
        **DURATION & TERMINATION**
          **Contract Period:**
          - **Start Date:** [date]
          - **End Date:** [date]
          - **Initial Term:** [duration]
          
          **Renewal Terms:**
          - [auto-renewal or manual renewal terms]
          
          **Termination Rights:**
          - [termination for convenience]
          - [termination for cause]
          - [notice periods]
        
        **FINANCIAL TERMS**
          **Payment Structure:**
          - **Total Contract Value:** [amount]
          - **Payment Frequency:** [monthly/quarterly/annual]
          - **Payment Terms:** [Net X days]
          
          **Penalties & Fees:**
          - **Early Termination:** [penalty amount]
          - **SLA Breach:** [penalty per incident]
          - **Late Payment:** [interest rate]
          - **Other Penalties:** [if any]
          
          **Expenses & Taxes:**
          - [expense reimbursement policy]
          - [tax responsibility]
        
        **RISK & COMPLIANCE** (if applicable)
        - **Risk Level:** [assessment]
        - **Insurance Requirements:** [coverage amounts]
        - **Compliance Standards:** [GDPR, SOC2, etc.]
        
        Contract:
        {contract_text}
        
        Structured Summary (with main sections and subsections):
        """
        
        response = self.model.generate_content(prompt)
        return response.text
    
    async def extract_key_clauses(self, contract_text: str) -> Dict[str, str]:
        """
        Extract important clauses from the contract.
        
        Args:
            contract_text: Full contract text
        
        Returns:
            Dictionary of clause types and their content
        """
        max_chars = 30000
        if len(contract_text) > max_chars:
            contract_text = contract_text[:max_chars] + "..."
        
        prompt = f"""
        You are a legal contract analyst. Extract and identify the following key clauses from this contract.
        Provide your response in a structured format.
        
        Please identify:
        - Payment Terms
        - Termination Clause
        - Renewal Terms
        - Liability Limitations
        - Confidentiality Obligations
        - Dispute Resolution
        - Penalties/Damages
        
        Contract:
        {contract_text}
        
        Format your response as:
        **Payment Terms:** [content]
        **Termination Clause:** [content]
        ... etc
        """
        
        response = self.model.generate_content(prompt)
        return {"extracted_clauses": response.text}
    
    async def extract_contract_metadata(self, contract_text: str) -> Dict[str, Any]:
        """
        Extract structured metadata from contract using AI.
        
        Extracts: contract name, number, parties, dates, value, etc.
        """
        max_chars = 15000  # Use first part of contract
        if len(contract_text) > max_chars:
            contract_text = contract_text[:max_chars]
        
        prompt = f"""
        You are a contract metadata extractor. Analyze this contract and extract key information.
        
        Return ONLY a valid JSON object with these exact fields (use null if not found):
        {{
            "contract_name": "type of agreement (e.g., Software License Agreement)",
            "contract_number": "contract number or ID",
            "party_a": "first party name",
            "party_b": "second party name", 
            "start_date": "YYYY-MM-DD format",
            "end_date": "YYYY-MM-DD format",
            "contract_value": numeric value or null,
            "currency": "USD or other currency code"
        }}
        
        IMPORTANT: Return ONLY the JSON object, no explanations or markdown.
        
        Contract Text:
        {contract_text}
        """
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            print(f"[DEBUG] AI Response: {result_text[:200]}...")  # Debug output
            
            # Extract JSON from response (handle various formats)
            import json
            import re
            
            # Remove markdown code blocks if present
            if "```json" in result_text:
                result_text = result_text.split("```json")[1].split("```")[0].strip()
            elif "```" in result_text:
                result_text = result_text.split("```")[1].split("```")[0].strip()
            
            # Try to find JSON object using regex
            json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', result_text, re.DOTALL)
            if json_match:
                result_text = json_match.group(0)
            
            # Clean up the text
            result_text = result_text.strip()
            
            # Parse JSON
            metadata = json.loads(result_text)
            
            # Validate required fields
            required_fields = ["contract_name", "contract_number", "party_a", "party_b", "start_date", "end_date", "contract_value", "currency"]
            for field in required_fields:
                if field not in metadata:
                    metadata[field] = None if field == "contract_value" else "Unknown"
            
            return metadata
            
        except Exception as e:
            print(f"[ERROR] Error extracting metadata: {e}")
            print(f"[ERROR] AI Response was: {response.text if 'response' in locals() else 'No response'}")
            
            # Return defaults
            return {
                "contract_name": "Untitled Contract",
                "contract_number": f"AUTO-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "party_a": "Unknown",
                "party_b": "Unknown",
                "start_date": None,
                "end_date": None,
                "contract_value": None,
                "currency": "USD"
            }
    
    async def assess_risk_level(self, contract_text: str) -> Dict[str, Any]:
        """
        Analyze contract for potential risks.
        
        Returns risk level and identified risks.
        """
        max_chars = 30000
        if len(contract_text) > max_chars:
            contract_text = contract_text[:max_chars] + "..."
        
        prompt = f"""
        You are a risk assessment specialist for legal contracts.
        Analyze this contract and identify potential risks.
        
        Assess:
        1. Financial risks (penalties, payment terms, contract value)
        2. Compliance risks (regulatory obligations)
        3. Operational risks (delivery timelines, SLA failures)
        4. Legal risks (ambiguous terms, termination conditions)
        
        Provide your response in this EXACT format:
        
        RISK LEVEL: [LOW/MEDIUM/HIGH/CRITICAL]
        
        PRIMARY REASON: [One sentence explaining the main reason for this risk level - focus on the most significant risk factor]
        
        KEY RISKS:
        - [Risk 1]
        - [Risk 2]
        - [Risk 3]
        
        Contract:
        {contract_text}
        
        Risk Assessment:
        """
        
        response = self.model.generate_content(prompt)
        risk_text = response.text
        
        # Parse risk level from response
        risk_level_lower = risk_text.lower()
        if "critical" in risk_level_lower:
            risk_level = "critical"
        elif "high" in risk_level_lower:
            risk_level = "high"
        elif "medium" in risk_level_lower:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Extract primary reason (one-liner)
        import re
        reason_match = re.search(r'PRIMARY REASON:\s*(.+?)(?:\n|$)', risk_text, re.IGNORECASE)
        if reason_match:
            risk_reason = reason_match.group(1).strip()
        else:
            # Fallback: extract first line after risk level
            lines = [line.strip() for line in risk_text.split('\n') if line.strip()]
            risk_reason = lines[1] if len(lines) > 1 else "Risk level determined by contract analysis"
        
        # Limit reason to 150 characters for display
        if len(risk_reason) > 150:
            risk_reason = risk_reason[:147] + "..."
        
        return {
            "risk_level": risk_level,
            "risk_reason": risk_reason,
            "risk_analysis": response.text
        }
    
    async def answer_question(
        self,
        question: str,
        contract_id: int = None
    ) -> str:
        """
        Answer questions about contracts using RAG.
        
        This is the core RAG functionality:
        1. Search for relevant contract chunks (Retrieval)
        2. Send chunks + question to AI (Augmentation)
        3. Get AI-generated answer (Generation)
        
        Args:
            question: User's question
            contract_id: Optional - limit to specific contract
        
        Returns:
            AI-generated answer based on contract content
        """
        # Step 1: Retrieve relevant chunks
        search_results = self.search_contracts(
            query=question,
            n_results=5,
            contract_id=contract_id
        )
        
        # Extract the relevant text chunks
        relevant_chunks = search_results.get('documents', [[]])[0]
        
        if not relevant_chunks:
            return "I couldn't find relevant information in the contracts to answer this question."
        
        # Combine chunks for context
        context = "\n\n---\n\n".join(relevant_chunks)
        
        # Detect question type for better prompting
        question_lower = question.lower()
        
        # Determine if this is a date-related question
        is_date_question = any(word in question_lower for word in ['date', 'when', 'deadline', 'expir', 'start', 'end', 'term'])
        
        # Determine if this is a payment-related question
        is_payment_question = any(word in question_lower for word in ['pay', 'cost', 'fee', 'price', 'amount', 'value'])
        
        # Determine if this is a parties question
        is_parties_question = any(word in question_lower for word in ['who', 'party', 'parties', 'vendor', 'client'])
        
        # Build specialized instructions based on question type
        special_instructions = ""
        if is_date_question:
            special_instructions = """
            IMPORTANT: The user is asking about dates. Please:
            1. Look for and list ALL relevant dates in the contract excerpts
            2. Include: Effective Date, Execution Date, Start Date, End Date, Termination Date, Renewal Date
            3. Format dates clearly (e.g., "Effective Date: June 08, 2024")
            4. If you find dates in different formats, normalize them for clarity
            5. Explain what each date means in the context of the contract
            """
        elif is_payment_question:
            special_instructions = """
            IMPORTANT: The user is asking about payments. Please:
            1. Identify total contract value and payment amounts
            2. Specify payment frequency (monthly, quarterly, annual)
            3. Note payment terms (e.g., Net 30 days)
            4. Mention any penalties or late fees
            """
        elif is_parties_question:
            special_instructions = """
            IMPORTANT: The user is asking about parties. Please:
            1. Clearly identify Party A and Party B
            2. Include company names and locations if available
            3. Note their roles (Client, Vendor, Provider, etc.)
            """
        
        # Step 2 & 3: Generate answer using context
        prompt = f"""
        You are a helpful contract management assistant with expertise in contract analysis.
        
        Based on the following contract excerpts, please answer the user's question accurately and comprehensively.
        {special_instructions}
        
        IMPORTANT GUIDELINES:
        - Extract ALL relevant information from the provided excerpts
        - Use bullet points for clarity when listing multiple items
        - Quote exact text from the contract when appropriate
        - If the information is not in the provided context, say so clearly
        - Be specific and precise with dates, amounts, and names
        
        Contract Excerpts:
        {context}
        
        User Question: {question}
        
        Answer (be thorough and extract all relevant information):
        """
        
        response = self.model.generate_content(prompt)
        return response.text


# Create a global instance
rag_system = ContractRAGSystem()
