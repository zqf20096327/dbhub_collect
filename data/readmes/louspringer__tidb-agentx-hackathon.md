# OpenFlow Playground

A comprehensive, model-driven development environment with security-first architecture, multi-agent testing, and healthcare CDC compliance.

## 🚀 Features

### **Model-Driven Development**
- **Project Model Registry**: Single source of truth for domain detection, tool selection, and requirements traceability
- **MDC Generator**: Python-based component for modeling and generating `.mdc` rule files
- **Deterministic Editing**: Enforced through specialized tools and validation

### **Security-First Architecture**
- **Credential Management**: Environment variables and secure storage
- **HTTPS Enforcement**: SSL/TLS validation and redirect enforcement
- **Rate Limiting**: Redis-based rate limiting for API protection
- **CSRF Protection**: Token-based CSRF protection for web forms
- **Audit Logging**: Immutable audit trails for compliance

### **Multi-Agent Testing**
- **Blind Spot Detection**: AI agents identify overlooked issues
- **Diversity Testing**: Multiple perspectives for comprehensive coverage
- **Automated Validation**: Continuous testing and validation

### **Healthcare CDC Compliance**
- **HIPAA Compliance**: PHI detection and validation
- **Data Encryption**: Healthcare data encryption at rest and in transit
- **Access Control**: Role-based access control for clinical data
- **Audit Logging**: Immutable audit trails for regulatory compliance

### **Package Management**
- **UV Integration**: Modern Python package management with UV
- **Lock File Enforcement**: Reproducible builds with `uv.lock`
- **Security Scanning**: Automated vulnerability detection

## 🛠️ Quick Start

### **Installation**
```bash
# Clone the repository
git clone https://github.com/louspringer/OpenFlow-Playground.git
cd OpenFlow-Playground

# Install dependencies with UV
uv sync --all-extras

# Run tests
make test-python
```

### **Development**
```bash
# Install development dependencies
uv sync --extra dev

# Run linting
make lint

# Run formatting
make format

# Run all tests
make test
```

## 📁 Project Structure

```
OpenFlow-Playground/
├── src/                          # Source code
│   ├── streamlit/                # Streamlit application
│   ├── security_first/           # Security components
│   ├── multi_agent_testing/      # Multi-agent testing
│   └── mdc_generator/           # MDC file generator
├── tests/                        # Test suite
├── scripts/                      # Utility scripts
├── config/                       # Configuration files
├── docs/                         # Documentation
├── healthcare-cdc/              # Healthcare CDC components
├── .cursor/                      # Cursor IDE configuration
│   ├── rules/                   # MDC rule files
│   └── plugins/                 # IDE plugins
├── project_model_registry.json   # Model registry
├── pyproject.toml               # UV project configuration
├── uv.lock                      # UV lock file
└── Makefile                     # Build system
```

## 🔧 Model-Driven Architecture

### **Domain Detection**
The project uses a model-driven approach with `project_model_registry.json` as the single source of truth:

- **Domain Detection**: Automatic detection of file types and domains
- **Tool Selection**: Domain-specific linting, formatting, and validation
- **Requirements Traceability**: Link requirements to implementations

### **Rule Compliance**
- **MDC Linter**: Validates `.mdc` files for proper structure
- **Pre-commit Hooks**: Automated rule enforcement
- **IDE Integration**: Cursor IDE plugin for immediate feedback

## 🧪 Testing

### **Test Categories**
- **Python Tests**: Core functionality and security validation
- **Core Concept Tests**: Architecture and design pattern validation
- **Healthcare CDC Tests**: HIPAA compliance and PHI detection
- **Rule Compliance Tests**: MDC validation and rule enforcement

### **Running Tests**
```bash
# Run all tests
make test

# Run specific test categories
make test-python
make test-core-concepts
make test-healthcare-cdc
make test-rule-compliance
```

## 🔒 Security Features

### **Credential Management**
- Environment variables for all sensitive data
- AWS Secrets Manager integration
- No hardcoded credentials in source code

### **Data Protection**
- Encryption at rest and in transit
- PHI detection and validation
- Immutable audit logging

### **Access Control**
- Role-based access control (RBAC)
- JWT-based session management
- Multi-factor authentication support

## 📊 Healthcare CDC Features

### **HIPAA Compliance**
- PHI detection and validation
- Healthcare data encryption
- Access control and authentication
- Immutable audit logging

### **CDC Integration**
- Clinical data transformation
- CDC format compliance
- Data retention policies

## 🚀 Deployment

### **Streamlit Application**
```bash
# Run the Streamlit app
streamlit run src/streamlit/openflow_quickstart_app.py
```

### **Security Validation**
```bash
# Run security scans
make security

# Check for vulnerabilities
uv run safety check
```

## 📚 Documentation

- **Architecture**: Model-driven development patterns
- **Security**: Security-first design principles
- **Testing**: Multi-agent testing framework
- **Healthcare**: CDC compliance and HIPAA requirements

## 🤝 Contributing

1. Follow the model-driven development approach
2. Ensure all tests pass
3. Follow security-first principles
4. Update documentation as needed

## 📄 License

[License information]

---

**Built with security-first principles and model-driven development.**
