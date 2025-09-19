# Contributing to RealTime Fintech RAG Copilot

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
source venv/bin/activate  # On Windows: venv\Scripts\activate

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
    """Analyze portfolio performance and provide insights.

    Args:
        portfolio: Dictionary containing portfolio holdings and metadata.

    Returns:
        Dictionary with analysis results including risk score and recommendations.

    Raises:
        ValueError: If portfolio data is invalid.
    """
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
