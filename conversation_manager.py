from datetime import datetime
from typing import List, Dict, Any
from openai import OpenAI
from config import Config

client = OpenAI(api_key=Config.GROQ_API_KEY, base_url=Config.GROQ_BASE_URL)

# =============================================================================
# TASK 1: CONVERSATION MANAGEMENT WITH SUMMARIZATION
# =============================================================================

  class ConversationManager:
    """
    Manages conversation history with intelligent summarization and truncation.
    """
    
    def __init__(self, max_turns: int = 10, max_chars: int = 4000, 
                 summarize_every: int = 3):
        self.conversation_history: List[Dict[str, str]] = []
        self.max_turns = max_turns
        self.max_chars = max_chars
        self.summarize_every = summarize_every
        self.turn_count = 0
        self.summary = ""
        
    def add_message(self, role: str, content: str):
        """Add a new message to conversation history"""
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(message)
        self.turn_count += 1
        
        # Check if we need to summarize
        if self.turn_count % self.summarize_every == 0:
            self._periodic_summarization()
        
        # Apply truncation if needed
        self._apply_truncation()
    
    def _periodic_summarization(self):
        """Perform periodic summarization of conversation history"""
        if len(self.conversation_history) < 2:
            return
            
        try:
            # Prepare conversation text for summarization
            conversation_text = self._format_conversation_for_summary()
            
            response = client.chat.completions.create(
                model=Config.MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "Summarize the following conversation concisely, capturing key points and context. Keep it under 200 words."
                    },
                    {
                        "role": "user", 
                        "content": f"Conversation to summarize:\n{conversation_text}"
                    }
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            new_summary = response.choices[0].message.content.strip()
            
            # Update summary and compress history
            if self.summary:
                self.summary = f"{self.summary}\n\nRecent conversation: {new_summary}"
            else:
                self.summary = new_summary
            
            # Keep only the last few messages and replace older ones with summary
            self.conversation_history = self.conversation_history[-2:]
            
            print(f"✅ Summarization completed after {self.turn_count} turns")
            
        except Exception as e:
            print(f"❌ Summarization failed: {str(e)}")
    
    def _format_conversation_for_summary(self) -> str:
        """Format conversation history for summarization"""
        formatted = []
        for msg in self.conversation_history:
            role = msg["role"].upper()
            content = msg["content"]
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)
    
    def _apply_truncation(self):
        """Apply truncation based on turns and character limits"""
        # Truncate by number of turns
        if len(self.conversation_history) > self.max_turns:
            self.conversation_history = self.conversation_history[-self.max_turns:]
        
        # Truncate by character count
        total_chars = sum(len(msg["content"]) for msg in self.conversation_history)
        while total_chars > self.max_chars and len(self.conversation_history) > 1:
            removed = self.conversation_history.pop(0)
            total_chars -= len(removed["content"])
    
    def get_conversation_context(self) -> str:
        """Get the complete conversation context including summary"""
        context_parts = []
        
        if self.summary:
            context_parts.append(f"Previous conversation summary:\n{self.summary}\n")
        
        context_parts.append("Current conversation:")
        for msg in self.conversation_history:
            role = msg["role"].upper()
            content = msg["content"]
            context_parts.append(f"{role}: {content}")
        
        return "\n".join(context_parts)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get conversation statistics"""
        total_chars = sum(len(msg["content"]) for msg in self.conversation_history)
        return {
            "total_turns": self.turn_count,
            "current_messages": len(self.conversation_history),
            "total_characters": total_chars,
            "has_summary": bool(self.summary),
            "summary_length": len(self.summary) if self.summary else 0
        }

