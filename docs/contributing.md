# Contributing

## Development Workflow

1. Create a feature branch from `develop`
   ```bash
   git checkout develop
   git pull origin develop
   git checkout -b feature/your-feature-name
   ```

2. Make your changes

3. Run linting and tests locally before pushing
   ```bash
   ruff check tests/
   pytest tests/ -m smoke -v --headless
   ```

4. Push and open a pull request against `develop`

## Branch Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code |
| `develop` | Integration branch |
| `feature/*` | New features |
| `fix/*` | Bug fixes |
| `infra/*` | Infrastructure changes |

## Writing Tests

### Test Naming

Use descriptive names that explain what is being tested and the expected outcome:

```python
# Good
def test_login_with_invalid_credentials_shows_error_message():

# Bad
def test_login_2():
```

### Markers

Tag tests with appropriate markers:

```python
@pytest.mark.smoke      # Critical path, runs on every PR
@pytest.mark.regression # Full suite, runs nightly
@pytest.mark.ui         # Selenium tests
@pytest.mark.api        # API tests
@pytest.mark.slow       # Tests taking > 30 seconds
```

### Page Object Model

For UI tests, use the Page Object Model pattern to keep tests readable and maintainable:

```python
# tests/ui/pages/login_page.py
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.url = "/login"

    def navigate(self, base_url):
        self.driver.get(f"{base_url}{self.url}")
        return self

    def enter_credentials(self, email, password):
        self.driver.find_element(By.ID, "username").send_keys(email)
        self.driver.find_element(By.ID, "password").send_keys(password)
        return self

    def submit(self):
        self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        return self
```

## Terraform Guidelines

- Always run `terraform fmt` before committing
- Add descriptions to all variables and outputs
- Use `validation` blocks for variable constraints
- Tag all resources with `Environment`, `Project`, and `ManagedBy`
- Never commit `.tfstate` files or `.tfvars` files with secrets

## Code Review Checklist

- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] No hardcoded credentials or secrets
- [ ] Terraform resources are tagged
- [ ] Ansible tasks are idempotent
- [ ] Documentation updated if needed
