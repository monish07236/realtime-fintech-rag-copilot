# Let's create additional important files for the repository

# 1. GitHub Actions CI/CD Pipeline
github_ci = """name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, "3.10", "3.11"]

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Cache dependencies
      uses: actions/cache@v3
      with:
        path: ~/.cache/pip
        key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install pytest pytest-cov black flake8 mypy
    
    - name: Lint with flake8
      run: |
        flake8 src/ tests/ --count --select=E9,F63,F7,F82 --show-source --statistics
        flake8 src/ tests/ --count --exit-zero --max-complexity=10 --max-line-length=88 --statistics
    
    - name: Format check with black
      run: black --check src/ tests/
    
    - name: Type check with mypy
      run: mypy src/ --ignore-missing-imports
    
    - name: Test with pytest
      run: |
        pytest tests/ -v --cov=src --cov-report=xml
    
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
        fail_ci_if_error: true

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run Trivy vulnerability scanner
      uses: aquasecurity/trivy-action@master
      with:
        scan-type: 'fs'
        scan-ref: '.'
        format: 'sarif'
        output: 'trivy-results.sarif'
    
    - name: Upload Trivy scan results to GitHub Security tab
      uses: github/codeql-action/upload-sarif@v2
      with:
        sarif_file: 'trivy-results.sarif'

  build:
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to DockerHub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKERHUB_USERNAME }}
        password: ${{ secrets.DOCKERHUB_TOKEN }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v3
      with:
        context: .
        push: true
        tags: |
          yourusername/fintech-rag:latest
          yourusername/fintech-rag:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    environment: production
    
    steps:
    - name: Deploy to production
      run: |
        echo "Deployment would happen here"
        # Add actual deployment steps
"""

# 2. Sample test file
sample_test = '''"""
Test suite for the real-time fintech RAG pipeline.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

from src.fintech_rag.core.pipeline import RealtimeFintechPipeline
from src.fintech_rag.agents.trading_copilot import TradingCopilotAgent


class TestRealtimeFintechPipeline:
    """Test suite for the main pipeline."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for testing."""
        return {
            'pathway': {'license_key': 'test-key'},
            'llm': {
                'model': 'gpt-3.5-turbo',
                'temperature': 0.1,
                'max_tokens': 1000,
                'embedding_model': 'text-embedding-ada-002'
            },
            'data_sources': {
                'documents': {
                    'enabled': True,
                    'watch_directories': ['./test_data']
                },
                'market_data': {'enabled': False},
                'news_feeds': {'enabled': False},
                'sanctions': {'enabled': False}
            },
            'app': {'host': '0.0.0.0', 'port': 8000}
        }
    
    def test_pipeline_initialization(self, mock_config):
        """Test pipeline initializes correctly."""
        with patch('pathway.set_license_key'):
            pipeline = RealtimeFintechPipeline(mock_config)
            assert pipeline.config == mock_config
    
    @patch('pathway.io.fs.read')
    def test_create_data_sources(self, mock_fs_read, mock_config):
        """Test data source creation."""
        with patch('pathway.set_license_key'):
            pipeline = RealtimeFintechPipeline(mock_config)
            sources = pipeline.create_data_sources()
            
            # Should create one source for documents
            assert len(sources) == 1
            mock_fs_read.assert_called_once()


class TestTradingCopilotAgent:
    """Test suite for the trading copilot agent."""
    
    @pytest.fixture
    def mock_config(self):
        """Mock configuration for agent testing."""
        return {
            'agents': {
                'trading_copilot': {
                    'risk_threshold': 0.8,
                    'portfolio_monitoring': True
                }
            }
        }
    
    @pytest.fixture
    def trading_agent(self, mock_config):
        """Create trading agent for testing."""
        with patch('src.fintech_rag.core.retrieval.DocumentRetriever'), \\
             patch('src.fintech_rag.core.llm_interface.LLMInterface'), \\
             patch('src.fintech_rag.data_sources.market_data.MarketDataConnector'):
            return TradingCopilotAgent(mock_config)
    
    @pytest.mark.asyncio
    async def test_analyze_portfolio_success(self, trading_agent):
        """Test successful portfolio analysis."""
        # Mock portfolio data
        portfolio = {
            'holdings': [
                {'symbol': 'AAPL', 'quantity': 100},
                {'symbol': 'GOOGL', 'quantity': 50}
            ]
        }
        
        # Mock dependencies
        trading_agent._get_portfolio_data = AsyncMock(return_value=[
            {'symbol': 'AAPL', 'quantity': 100, 'current_price': 150.0, 'price_change': 2.5},
            {'symbol': 'GOOGL', 'quantity': 50, 'current_price': 2500.0, 'price_change': -10.0}
        ])
        
        trading_agent.retriever.get_relevant_documents = AsyncMock(return_value=[
            {'title': 'Market Analysis', 'summary': 'Positive outlook for tech stocks'}
        ])
        
        trading_agent.llm.generate_response = AsyncMock(return_value="Portfolio shows strong performance")
        
        result = await trading_agent.analyze_portfolio(portfolio)
        
        # Verify result structure
        assert 'portfolio_value' in result
        assert 'daily_change' in result
        assert 'risk_score' in result
        assert 'analysis' in result
        assert 'timestamp' in result
    
    @pytest.mark.asyncio
    async def test_analyze_portfolio_error_handling(self, trading_agent):
        """Test portfolio analysis error handling."""
        portfolio = {'holdings': []}
        
        # Mock an exception
        trading_agent._get_portfolio_data = AsyncMock(side_effect=Exception("API Error"))
        
        result = await trading_agent.analyze_portfolio(portfolio)
        
        # Should return error information
        assert 'error' in result
        assert 'API Error' in result['error']
    
    @pytest.mark.asyncio
    async def test_answer_trading_question(self, trading_agent):
        """Test trading question answering."""
        question = "What is the outlook for AAPL stock?"
        
        trading_agent.retriever.get_relevant_documents = AsyncMock(return_value=[
            {'content': 'AAPL stock analysis shows positive momentum'}
        ])
        
        trading_agent._get_relevant_market_data = AsyncMock(return_value={
            'AAPL': {'price': 150.0, 'change': 2.5}
        })
        
        trading_agent.llm.generate_response = AsyncMock(return_value="AAPL shows strong growth potential")
        
        response = await trading_agent.answer_trading_question(question)
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    def test_risk_threshold_configuration(self, trading_agent):
        """Test risk threshold is properly configured."""
        assert trading_agent.risk_threshold == 0.8


@pytest.mark.integration
class TestEndToEndFlow:
    """Integration tests for the complete system."""
    
    @pytest.mark.asyncio
    async def test_data_ingestion_to_query_flow(self):
        """Test complete flow from data ingestion to query response."""
        # This would test the entire pipeline end-to-end
        # Mock file system changes, verify they are picked up,
        # indexed, and reflected in query responses
        pass
    
    def test_real_time_update_detection(self):
        """Test that system detects and processes updates in real-time."""
        # Add a file to watched directory
        # Verify it gets processed within expected timeframe
        pass


class TestDataSources:
    """Test data source connectors."""
    
    def test_market_data_connector(self):
        """Test market data API connections."""
        pass
    
    def test_news_feed_connector(self):
        """Test news feed processing.""" 
        pass
    
    def test_sanctions_monitor(self):
        """Test sanctions list monitoring."""
        pass


class TestAPI:
    """Test API endpoints."""
    
    def test_health_endpoint(self):
        """Test health check endpoint."""
        pass
    
    def test_chat_endpoint(self):
        """Test chat interface."""
        pass
    
    def test_portfolio_analysis_endpoint(self):
        """Test portfolio analysis API."""
        pass


if __name__ == '__main__':
    pytest.main(['-v', __file__])
'''

# 3. Contributing guidelines
contributing_md = """# Contributing to RealTime Fintech RAG Copilot

Thank you for your interest in contributing! This document provides guidelines for contributing to this hackathon project.

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Git
- OpenAI API key
- Pathway license key

### Development Setup
1. **Fork and clone the repository**
```bash
git clone https://github.com/yourusername/realtime-fintech-rag-copilot.git
cd realtime-fintech-rag-copilot
```

2. **Set up development environment**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
pip install -e .

# Copy environment template
cp .env.example .env
# Edit .env with your API keys
```

3. **Install development tools**
```bash
pip install pre-commit black flake8 mypy pytest pytest-cov
pre-commit install
```

## 📝 Development Guidelines

### Code Style
- **Formatting**: Use `black` for code formatting
- **Linting**: Use `flake8` for linting
- **Type hints**: Use type hints for all functions and classes
- **Docstrings**: Use Google-style docstrings

```python
def analyze_portfolio(portfolio: Dict[str, Any]) -> Dict[str, Any]:
    \"\"\"Analyze portfolio performance and provide insights.
    
    Args:
        portfolio: Dictionary containing portfolio holdings and metadata.
        
    Returns:
        Dictionary with analysis results including risk score and recommendations.
        
    Raises:
        ValueError: If portfolio data is invalid.
    \"\"\"
    pass
```

### Testing
- **Unit tests**: Test individual components in isolation
- **Integration tests**: Test component interactions
- **End-to-end tests**: Test complete user workflows
- **Coverage**: Maintain >80% test coverage

```bash
# Run tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test types
pytest tests/unit/ -v
pytest tests/integration/ -v -m integration
```

### Commit Messages
Use conventional commit format:
```
feat: add sanctions monitoring agent
fix: resolve websocket connection issue
docs: update API documentation
test: add unit tests for trading agent
refactor: improve pipeline error handling
```

## 🏗️ Project Structure

### Adding New Features
1. **Agents**: Add new AI agents in `src/fintech_rag/agents/`
2. **Data Sources**: Add connectors in `src/fintech_rag/data_sources/`
3. **API Endpoints**: Add routes in `src/fintech_rag/api/routes/`
4. **Utils**: Add shared utilities in `src/fintech_rag/utils/`

### Configuration
- **App config**: Update `config/app.yaml`
- **Environment**: Update `.env.example`
- **Dependencies**: Update `requirements.txt`

## 🐛 Bug Reports

### Before Submitting
1. Check existing issues for duplicates
2. Test with the latest version
3. Verify the bug with minimal reproduction steps

### Bug Report Template
```markdown
**Bug Description**
Clear description of the bug.

**Steps to Reproduce**
1. Start the system with `docker-compose up`
2. Navigate to...
3. Click on...

**Expected Behavior**
What should happen.

**Actual Behavior**
What actually happens.

**Environment**
- OS: [e.g., Ubuntu 20.04]
- Python version: [e.g., 3.9.7]
- Docker version: [e.g., 20.10.8]

**Logs**
Paste relevant log output here.
```

## 💡 Feature Requests

### Feature Request Template
```markdown
**Problem Statement**
Describe the problem this feature would solve.

**Proposed Solution**
Describe your proposed solution.

**Alternatives Considered**
Other solutions you've considered.

**Implementation Notes**
Technical considerations or suggestions.
```

## 🔧 Development Workflow

### Feature Development
1. **Create feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Implement feature**
   - Write code following style guidelines
   - Add comprehensive tests
   - Update documentation
   - Test locally

3. **Pre-commit checks**
```bash
# Format code
black src/ tests/

# Lint
flake8 src/ tests/

# Type check
mypy src/

# Run tests
pytest tests/ -v
```

4. **Submit pull request**
   - Use descriptive title and description
   - Reference related issues
   - Include screenshots/videos if relevant

### Pull Request Guidelines
- **Title**: Use conventional commit format
- **Description**: Explain what and why
- **Testing**: Describe how you tested the changes
- **Documentation**: Update relevant documentation
- **Breaking changes**: Clearly mark any breaking changes

## 🚀 Hackathon Context

This project is built for the **Pathway Gen AI Hackathon 2025**. Key considerations:

### Hackathon Requirements
- ✅ Use Pathway framework for real-time data processing
- ✅ Implement dynamic RAG with no rebuilds
- ✅ Provide live interface reflecting instant updates
- ✅ Include demo video showing real-time functionality

### Time Constraints
- Focus on core functionality first
- Document thoroughly for judges
- Prioritize demo-able features
- Ensure reproducible setup

## 📖 Documentation

### Required Documentation
- **README**: Keep main README up to date
- **API Docs**: Document all endpoints
- **Architecture**: Update architecture diagrams
- **Examples**: Add usage examples

### Documentation Standards
- Use clear, concise language
- Include code examples
- Provide setup instructions
- Add troubleshooting guides

## ⚡ Performance Considerations

### Optimization Guidelines
- **Response Time**: API responses should be <500ms
- **Memory Usage**: Monitor memory consumption
- **Scalability**: Consider multi-instance deployment
- **Caching**: Implement appropriate caching strategies

### Monitoring
- Add logging for key operations
- Monitor Pathway pipeline performance
- Track API response times
- Monitor vector store size and query performance

## 🔒 Security

### Security Guidelines
- **Input Validation**: Validate all user inputs
- **API Security**: Use rate limiting and authentication
- **Secrets**: Never commit API keys or secrets
- **Dependencies**: Keep dependencies updated

### Security Checklist
- [ ] Input validation implemented
- [ ] API rate limiting configured  
- [ ] Secrets properly managed
- [ ] Dependencies scanned for vulnerabilities

## 📞 Getting Help

### Resources
- **Documentation**: Check `docs/` directory
- **Issues**: Search existing GitHub issues
- **Discussions**: Use GitHub Discussions for questions

### Contact
- **Project Lead**: [Your Name] (your.email@example.com)
- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For general questions and ideas

## 🏆 Recognition

Contributors will be recognized in:
- Project README
- Hackathon presentation
- Future presentations and publications

Thank you for contributing to this hackathon project! 🚀
"""

print("ADDITIONAL REPOSITORY FILES CREATED:")
print("=" * 60)
print("\n🔄 GitHub Actions CI/CD (.github/workflows/ci.yml):")
print("-" * 50)
print(github_ci[:1500] + "..." if len(github_ci) > 1500 else github_ci[:1500])

print("\n🧪 Sample Test File (tests/test_main.py) - First 1000 chars:")
print("-" * 50)
print(sample_test[:1000] + "..." if len(sample_test) > 1000 else sample_test[:1000])

print("\n📝 Contributing Guidelines (CONTRIBUTING.md) - First 1000 chars:")
print("-" * 50)
print(contributing_md[:1000] + "..." if len(contributing_md) > 1000 else contributing_md[:1000])

# Save all files
with open('github_ci.yml', 'w') as f:
    f.write(github_ci)
    
with open('test_main.py', 'w') as f:
    f.write(sample_test)
    
with open('CONTRIBUTING.md', 'w') as f:
    f.write(contributing_md)

print(f"\n✅ Files created:")
print(f"   - github_ci.yml ({len(github_ci)} chars)")
print(f"   - test_main.py ({len(sample_test)} chars)")
print(f"   - CONTRIBUTING.md ({len(contributing_md)} chars)")