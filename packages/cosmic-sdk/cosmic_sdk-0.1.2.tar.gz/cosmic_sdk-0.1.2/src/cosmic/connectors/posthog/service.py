# posthog/service.py
# Purpose: Provides a service layer for the PostHog API. 
# This layer is responsible for interacting with the PostHog API and returning processed data.
from cosmic.connectors.posthog.client import PostHogClient

class PostHogService:
    def __init__(self, credentials: dict):
        self.client = PostHogClient(credentials)