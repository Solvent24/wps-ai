import uuid
import time
import google.generativeai as genai
from typing import Dict, Any, Optional
from datetime import datetime
from database.database import Database
from models.models import AIRequest, AIResponse, AIAction
import os
from dotenv import load_dotenv

load_dotenv()

class AIService:
    def __init__(self):
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
            # Initialize Gemini model
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None
            print("Warning: GEMINI_API_KEY not found. AI features will use fallback methods.")
    
    def process_ai_request(self, request: AIRequest, user_id: str) -> AIResponse:
        """Process AI request using Gemini API"""
        start_time = time.time()
        
        try:
            if request.action == AIAction.SUMMARIZE:
                output = self._summarize_text(request.text_content or "")
            elif request.action == AIAction.GRAMMAR_CHECK:
                output = self._check_grammar(request.text_content or "")
            elif request.action == AIAction.TRANSLATE:
                output = self._translate_text(request.text_content or "", request.parameters or {})
            elif request.action == AIAction.ANALYZE_DATA:
                output = self._analyze_data(request.parameters or {})
            elif request.action == AIAction.FORMAT:
                output = self._format_content(request.text_content or "", request.parameters or {})
            elif request.action == AIAction.GENERATE_CONTENT:
                output = self._generate_content(request.parameters or {})
            else:
                output = {"error": "Unsupported AI action"}
            
            processing_time = int((time.time() - start_time) * 1000)
            
            # Save to history
            ai_history_id = self._save_ai_history(
                request, user_id, output, processing_time
            )
            
            return AIResponse(
                id=ai_history_id,
                action=request.action,
                input_data={
                    "text_content": request.text_content,
                    "parameters": request.parameters
                },
                output_data=output,
                processing_time_ms=processing_time,
                created_at=datetime.now()
            )
            
        except Exception as e:
            processing_time = int((time.time() - start_time) * 1000)
            output = {"error": str(e)}
            
            ai_history_id = self._save_ai_history(
                request, user_id, output, processing_time
            )
            
            return AIResponse(
                id=ai_history_id,
                action=request.action,
                input_data={
                    "text_content": request.text_content,
                    "parameters": request.parameters
                },
                output_data=output,
                processing_time_ms=processing_time,
                created_at=datetime.now()
            )
    
    def _summarize_text(self, text: str) -> Dict[str, Any]:
        """Summarize text using Gemini AI"""
        if not self.model:
            return {"summary": self._fallback_summarize(text), "type": "fallback"}
        
        try:
            prompt = f"Please provide a concise summary of the following text. Focus on the main points and key information:\n\n{text}"
            
            response = self.model.generate_content(prompt)
            summary = response.text.strip()
            
            return {"summary": summary, "type": "ai_generated"}
            
        except Exception as e:
            return {"summary": self._fallback_summarize(text), "type": "fallback", "error": str(e)}
    
    def _check_grammar(self, text: str) -> Dict[str, Any]:
        """Check grammar using Gemini AI"""
        if not self.model:
            return {"corrections": [], "type": "fallback"}
        
        try:
            prompt = f"Please correct any grammar, spelling, or punctuation errors in the following text. Return only the corrected version:\n\n{text}"
            
            response = self.model.generate_content(prompt)
            corrected_text = response.text.strip()
            
            return {
                "original": text,
                "corrected": corrected_text,
                "type": "ai_generated"
            }
            
        except Exception as e:
            return {"corrections": [], "type": "fallback", "error": str(e)}
    
    def _translate_text(self, text: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Translate text using Gemini AI"""
        target_language = parameters.get('target_language', 'English')
        
        if not self.model:
            return {"translated": text, "type": "fallback"}
        
        try:
            prompt = f"Translate the following text to {target_language}. Maintain the original meaning and tone:\n\n{text}"
            
            response = self.model.generate_content(prompt)
            translated_text = response.text.strip()
            
            return {
                "original": text,
                "translated": translated_text,
                "target_language": target_language,
                "type": "ai_generated"
            }
            
        except Exception as e:
            return {"translated": text, "type": "fallback", "error": str(e)}
    
    def _analyze_data(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data using Gemini AI"""
        data = parameters.get('data', [])
        analysis_type = parameters.get('analysis_type', 'general')
        
        if not self.model:
            return self._fallback_analyze_data(data, analysis_type)
        
        try:
            if isinstance(data, list) and len(data) > 0:
                # Convert data to readable format
                data_str = self._format_data_for_analysis(data)
                
                prompt = f"""
                Analyze the following data and provide insights. Data type: {analysis_type}
                
                Data:
                {data_str}
                
                Please provide:
                1. Key observations
                2. Patterns or trends
                3. Recommendations or insights
                """
                
                response = self.model.generate_content(prompt)
                analysis = response.text.strip()
                
                return {
                    "analysis": analysis,
                    "data_summary": {
                        "row_count": len(data),
                        "column_count": len(data[0]) if data and isinstance(data[0], list) else 1
                    },
                    "type": "ai_generated"
                }
            else:
                return {
                    "analysis": "No data provided for analysis",
                    "type": "fallback"
                }
                
        except Exception as e:
            return self._fallback_analyze_data(data, analysis_type)
    
    def _format_content(self, text: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Format content using Gemini AI"""
        format_type = parameters.get('format_type', 'professional')
        
        if not self.model:
            return {"formatted": text, "type": "fallback"}
        
        try:
            prompt = f"""
            Please reformat the following text to make it more {format_type} and well-structured:
            
            {text}
            
            Focus on:
            - Improving readability
            - Proper paragraph structure
            - Clear organization
            - Appropriate tone for {format_type} context
            """
            
            response = self.model.generate_content(prompt)
            formatted_text = response.text.strip()
            
            return {
                "original": text,
                "formatted": formatted_text,
                "format_type": format_type,
                "type": "ai_generated"
            }
            
        except Exception as e:
            return {"formatted": text, "type": "fallback", "error": str(e)}
    
    def _generate_content(self, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Generate content using Gemini AI"""
        content_type = parameters.get('content_type', 'text')
        topic = parameters.get('topic', 'general topic')
        length = parameters.get('length', 'short')
        tone = parameters.get('tone', 'professional')
        
        if not self.model:
            return {"content": f"Sample {content_type} about {topic}", "type": "fallback"}
        
        try:
            prompt = f"""
            Generate a {length} {content_type} about {topic} with a {tone} tone.
            
            Requirements:
            - Content type: {content_type}
            - Topic: {topic}
            - Length: {length}
            - Tone: {tone}
            
            Please create engaging and well-structured content.
            """
            
            response = self.model.generate_content(prompt)
            generated_content = response.text.strip()
            
            return {
                "content": generated_content,
                "content_type": content_type,
                "topic": topic,
                "length": length,
                "tone": tone,
                "type": "ai_generated"
            }
            
        except Exception as e:
            return {"content": f"Sample {content_type} about {topic}", "type": "fallback", "error": str(e)}
    
    def _format_data_for_analysis(self, data: list) -> str:
        """Format data for AI analysis"""
        if not data:
            return "No data"
        
        if isinstance(data[0], list):
            # Tabular data
            result = []
            for i, row in enumerate(data):
                result.append(f"Row {i+1}: {', '.join(map(str, row))}")
            return '\n'.join(result)
        else:
            # Simple list
            return '\n'.join([f"Item {i+1}: {item}" for i, item in enumerate(data)])
    
    def _fallback_summarize(self, text: str) -> str:
        """Fallback summarization when AI is not available"""
        sentences = text.split('.')
        if len(sentences) > 3:
            return '.'.join(sentences[:3]) + '.'
        return text
    
    def _fallback_analyze_data(self, data: list, analysis_type: str) -> Dict[str, Any]:
        """Fallback data analysis"""
        if isinstance(data, list) and len(data) > 0:
            if all(isinstance(row, list) and len(row) > 0 for row in data):
                return {
                    "row_count": len(data),
                    "column_count": len(data[0]) if data else 0,
                    "analysis": f"Basic {analysis_type} analysis: Data has {len(data)} rows and {len(data[0])} columns",
                    "type": "fallback"
                }
        
        return {
            "analysis": f"No specific {analysis_type} analysis performed (AI not available)",
            "type": "fallback"
        }
    
    def _save_ai_history(self, request: AIRequest, user_id: str, output: Dict[str, Any], processing_time: int) -> str:
        """Save AI processing history"""
        ai_history_id = str(uuid.uuid4())
        
        input_json = {
            "text_content": request.text_content,
            "parameters": request.parameters
        }
        
        Database.execute_query(
            """
            INSERT INTO ai_processing_history (id, document_id, user_id, ai_action, input_data, output_data, processing_time_ms)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (ai_history_id, request.document_id, user_id, request.action, 
             str(input_json), str(output), processing_time)
        )
        
        return ai_history_id
    
    def get_ai_history(self, user_id: str, limit: int = 10) -> list:
        """Get AI processing history for user"""
        history = Database.execute_query(
            """
            SELECT * FROM ai_processing_history 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s
            """,
            (user_id, limit),
            fetch=True
        )
        
        return history
    
    def chat_with_document(self, document_content: str, question: str, user_id: str) -> Dict[str, Any]:
        """Chat with document content using Gemini AI"""
        if not self.model:
            return {"answer": "AI service not available", "type": "fallback"}
        
        try:
            prompt = f"""
            Based on the following document content, please answer the user's question.
            
            DOCUMENT CONTENT:
            {document_content}
            
            USER QUESTION:
            {question}
            
            Please provide a helpful and accurate answer based solely on the document content.
            """
            
            response = self.model.generate_content(prompt)
            answer = response.text.strip()
            
            # Save to history
            chat_request = AIRequest(
                action=AIAction.GENERATE_CONTENT,
                document_id="chat",
                parameters={"question": question, "document_length": len(document_content)},
                text_content=document_content
            )
            
            self._save_ai_history(
                chat_request, 
                user_id, 
                {"answer": answer, "question": question}, 
                1000  # Estimated processing time
            )
            
            return {
                "answer": answer,
                "question": question,
                "type": "ai_generated"
            }
            
        except Exception as e:
            return {"answer": f"Error processing request: {str(e)}", "type": "error"}