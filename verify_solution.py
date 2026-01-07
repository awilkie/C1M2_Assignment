import sys
from unittest.mock import MagicMock

# Mock imports
sys.modules["dotenv"] = MagicMock()
sys.modules["aisuite"] = MagicMock()
sys.modules["unittests"] = MagicMock()
sys.modules["utils"] = MagicMock() # Mock utils if used

# Import the module to test
# We need to handle the fact that it runs code on import (the unittests calls)
# But since we mocked unittests, those calls should just do nothing.
import C1M2_Assignment

def test_solution():
    print("Testing generate_draft...")
    topic = "AI Safety"
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "Generated Draft Content"
    C1M2_Assignment.CLIENT.chat.completions.create.return_value = mock_response
    
    draft = C1M2_Assignment.generate_draft(topic)
    assert draft == "Generated Draft Content"
    
    call_args = C1M2_Assignment.CLIENT.chat.completions.create.call_args
    prompt_sent = call_args.kwargs['messages'][0]['content']
    model_used = call_args.kwargs['model']
    print(f"Prompt sent: {prompt_sent}")
    print(f"Model used: {model_used}")
    assert f"topic: {topic}" in prompt_sent
    assert model_used == "openai:gemini-2.0-flash"
    print("generate_draft PASSED")

    print("\nTesting reflect_on_draft...")
    draft_content = "Generated Draft Content"
    mock_response.choices[0].message.content = "Reflection Feedback"
    # Reset mock
    C1M2_Assignment.CLIENT.chat.completions.create.reset_mock()
    C1M2_Assignment.CLIENT.chat.completions.create.return_value = mock_response

    feedback = C1M2_Assignment.reflect_on_draft(draft_content)
    assert feedback == "Reflection Feedback"
    
    call_args = C1M2_Assignment.CLIENT.chat.completions.create.call_args
    prompt_sent = call_args.kwargs['messages'][0]['content']
    model_used = call_args.kwargs['model']
    print(f"Prompt sent: {prompt_sent}")
    print(f"Model used: {model_used}")
    assert draft_content in prompt_sent
    assert model_used == "openai:gemini-2.0-flash"
    print("reflect_on_draft PASSED")

    print("\nTesting revise_draft...")
    reflection = "Reflection Feedback"
    mock_response.choices[0].message.content = "Revised Essay"
    # Reset mock
    C1M2_Assignment.CLIENT.chat.completions.create.reset_mock()
    C1M2_Assignment.CLIENT.chat.completions.create.return_value = mock_response

    revised = C1M2_Assignment.revise_draft(draft_content, reflection)
    assert revised == "Revised Essay"
    
    call_args = C1M2_Assignment.CLIENT.chat.completions.create.call_args
    prompt_sent = call_args.kwargs['messages'][0]['content']
    model_used = call_args.kwargs['model']
    print(f"Prompt sent: {prompt_sent}")
    print(f"Model used: {model_used}")
    assert draft_content in prompt_sent
    assert reflection in prompt_sent
    assert model_used == "google:gemini-1.5-flash"
    print("revise_draft PASSED")

if __name__ == "__main__":
    try:
        test_solution()
        print("\nAll tests PASSED")
    except Exception as e:
        print(f"\nTests FAILED: {e}")
        sys.exit(1)
