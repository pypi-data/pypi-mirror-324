"""
OAuth2 Module

This module provides utilities and functionalities for handling OAuth2 authentication.

Features:
- OAuth2 authorization and token management
- Support for multiple providers (Google, GitHub, Facebook, etc.)
- Secure client credential handling

Version: 1.5.211
Author: [Jahongir Hakimjonov]
License: MIT (or specify the license)
"""

from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("drf-oauth2")
except PackageNotFoundError:
    __version__ = "0.1"
