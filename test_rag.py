"""
Test script for RAG integration
Run this to test the GitHub repo Q&A functionality
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8001/api"

def test_rag_query():
    """Test a RAG query about code in a repository"""
    
    test_queries = [
        {
            "query": "What does the main.py file do in Ishan1819/crewai for alice?",
            "expected_agent": "github_rag"
        },
        {
            "query": "Explain the github_agent.py code in alice's Ishan1819/crewai repo",
            "expected_agent": "github_rag"
        },
        {
            "query": "Show me alice's GitHub repositories",
            "expected_agent": "github"
        },
        {
            "query": "What are bob's Linear issues?",
            "expected_agent": "linear"
        }
    ]
    
    print("🧪 Testing RAG Integration\n")
    print("=" * 60)
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n📝 Test {i}: {test['query']}")
        print(f"Expected agent: {test['expected_agent']}")
        print("-" * 60)
        
        try:
            response = requests.post(
                f"{BASE_URL}/query",
                json={"query": test['query']},
                timeout=120  # RAG can take time for first query
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Status: Success")
                print(f"Agent: {data.get('agent')}")
                print(f"User: {data.get('user')}")
                if data.get('repo'):
                    print(f"Repo: {data.get('repo')}")
                print(f"\nResult:\n{data.get('result')}")
                
                # Verify expected agent
                if data.get('agent') == test['expected_agent']:
                    print(f"\n✅ Agent matched expected: {test['expected_agent']}")
                else:
                    print(f"\n⚠️ Agent mismatch! Got: {data.get('agent')}, Expected: {test['expected_agent']}")
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                
        except requests.exceptions.ConnectionError:
            print("❌ Cannot connect to server. Make sure the server is running:")
            print("   python main.py")
            return
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("=" * 60)

if __name__ == "__main__":
    print("\n⚠️  Make sure the FastAPI server is running:")
    print("   python main.py\n")
    input("Press Enter to start tests...")
    test_rag_query()
