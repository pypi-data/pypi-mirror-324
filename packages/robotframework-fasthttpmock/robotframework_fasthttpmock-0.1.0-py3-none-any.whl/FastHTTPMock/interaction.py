from typing import Dict, Any, Optional
from pydantic import BaseModel

class Interaction(BaseModel):
    """Model for HTTP mock interactions."""
    id: str
    request: Dict[str, Any]
    response: Dict[str, Any]
    call_count: int = 0
    expected_calls: Optional[int] = None
    
    class Config:
        arbitrary_types_allowed = True

    def increment_calls(self):
        """Increment the call count for this interaction."""
        self.call_count += 1

    def verify_calls(self) -> bool:
        """Verify if the interaction was called the expected number of times."""
        if self.expected_calls is None:
            return True
        return self.call_count == self.expected_calls 