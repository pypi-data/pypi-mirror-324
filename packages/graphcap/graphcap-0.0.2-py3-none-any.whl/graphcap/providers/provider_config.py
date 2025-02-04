"""
# SPDX-License-Identifier: Apache-2.0
Provider Configuration Module

This module handles loading and validating provider configurations from TOML files.

Key features:
- TOML configuration loading
- Provider config validation
- Default model handling
- Environment variable management

Classes:
    ProviderConfig: Configuration dataclass for providers

Functions:
    load_provider_config: Load config from TOML file
    parse_provider_config: Parse config into ProviderConfig object
    get_providers_config: Load and parse all provider configs
    validate_config: Validate provider configurations
"""

import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from loguru import logger


@dataclass
class RateLimits:
    """Rate limits for a provider"""

    requests_per_minute: int | None = None
    tokens_per_minute: int | None = None


@dataclass
class ProviderConfig:
    """Configuration for a provider"""

    kind: str
    environment: str  # 'cloud' or 'local'
    env_var: str
    base_url: str
    models: list[str]
    default_model: str
    fetch_models: bool = False
    rate_limits: RateLimits | None = None


def load_provider_config(config_path: str | Path = "provider.config.toml") -> dict[str, Any]:
    """Load provider configuration from a TOML file."""
    config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with config_path.open("rb") as f:
        return tomllib.load(f)


def parse_provider_config(config_data: dict[str, Any]) -> ProviderConfig:
    """Parse a provider's configuration data into a ProviderConfig object"""
    # Get models list and default model
    models: list[str] = config_data.get("models", [])
    default_model: str = config_data.get("default_model")
    fetch_models: bool = config_data.get("fetch_models", False)

    kind: str = config_data["kind"]
    environment: str = config_data["environment"]
    env_var: str = config_data["env_var"]
    base_url: str = config_data["base_url"]

    # If no default model specified, require one to be set
    if not default_model:
        if models:
            default_model = models[0]
            logger.debug(f"Using first model as default: {default_model}")
        else:
            raise ValueError("Must specify default_model when no models list is provided")

    # Parse rate limits if present
    rate_limits = None
    if "rate_limits" in config_data:
        rate_limits_data: dict[str, int | None] = config_data["rate_limits"]
        rate_limits = RateLimits(
            requests_per_minute=rate_limits_data.get("requests_per_minute"),
            tokens_per_minute=rate_limits_data.get("tokens_per_minute"),
        )

    return ProviderConfig(
        kind=kind,
        environment=environment,
        env_var=env_var,
        base_url=base_url,
        models=models,
        default_model=default_model,
        fetch_models=fetch_models,
        rate_limits=rate_limits,
    )


def get_providers_config(config_path: str | Path = "provider.config.toml") -> dict[str, ProviderConfig]:
    """
    Load and parse the providers configuration.


    Args:
        config_path: Path to the TOML configuration file

    Returns:
        Dictionary mapping provider names to their configurations

    Example config:
        [openai]
        kind = "openai"
        environment = "cloud"
        env_var = "OPENAI_API_KEY"
        base_url = "https://api.openai.com/v1"
        models = ["gpt-4o", "gpt-4o-mini"]
        default_model = "gpt-4o-mini"  # Optional, defaults to first model in list

        [ollama]
        kind = "ollama"
        environment = "local"
        env_var = "CUSTOM_KEY"
        base_url = "http://localhost:11434"
        fetch_models = true
        default_model = "llama3.2"  # Optional, defaults to "default" if no models
    """
    config = load_provider_config(config_path)
    providers = {}

    # Parse all top-level provider configs
    for name, provider_config in config.items():
        if isinstance(provider_config, dict):  # Skip non-provider sections
            try:
                providers[name] = parse_provider_config(provider_config)
            except KeyError as e:
                logger.warning(f"Skipping provider '{name}': Missing required field {e}")

    logger.info(f"Loaded {len(providers)} providers")
    logger.debug(f"Providers: {providers}")
    return providers


def validate_config(providers: dict[str, ProviderConfig]) -> list[str]:
    """Validate the provider configuration."""
    errors: list[str] = []

    for name, provider in providers.items():
        # Required fields
        if not provider.env_var:
            errors.append(f"{name}: Missing env_var")
        if not provider.base_url:
            errors.append(f"{name}: Missing base URL")
        if not provider.kind:
            errors.append(f"{name}: Missing kind")
        if not provider.environment:
            errors.append(f"{name}: Missing environment")
        if not provider.default_model:
            errors.append(f"{name}: Missing default_model")

        # Environment validation
        if provider.environment not in ["cloud", "local"]:
            errors.append(f"{name}: Environment must be 'cloud' or 'local'")

        # URL format
        if provider.base_url and not (
            provider.base_url.startswith("http://") or provider.base_url.startswith("https://")
        ):
            errors.append(f"{name}: Base URL must start with http:// or https://")

        # Models list when fetch_models is False
        if not provider.fetch_models and not provider.models:
            errors.append(f"{name}: Must specify models list when fetch_models is False")

    return errors


if __name__ == "__main__":
    # Example usage
    try:
        providers = get_providers_config()
        errors = validate_config(providers)

        if errors:
            print("Configuration errors found:")
            for error in errors:
                print(f"- {error}")
        else:
            print("Configuration loaded successfully:")
            for name, provider in providers.items():
                print(f"\n{name}:")
                print(f"  Kind: {provider.kind}")
                print(f"  Environment: {provider.environment}")
                print(f"  Base URL: {provider.base_url}")
                print(f"  Models: {', '.join(provider.models) if provider.models else '[fetch at runtime]'}")

    except Exception as e:
        print(f"Error loading configuration: {e}")
