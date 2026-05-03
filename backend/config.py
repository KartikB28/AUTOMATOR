import os
from pathlib import Path
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    app_data_path: str = os.environ.get('APP_DATA_PATH', str(Path.home() / '.automator'))
    media_path: str = os.environ.get('MEDIA_PATH', str(Path.home() / '.automator' / 'media'))
    log_level: str = os.environ.get('LOG_LEVEL', 'INFO')
    port: int = int(os.environ.get('PORT', 8765))

    anthropic_api_key: str = os.environ.get('ANTHROPIC_API_KEY', '')
    openai_api_key: str = os.environ.get('OPENAI_API_KEY', '')
    stability_api_key: str = os.environ.get('STABILITY_API_KEY', '')
    pexels_api_key: str = os.environ.get('PEXELS_API_KEY', '')
    unsplash_access_key: str = os.environ.get('UNSPLASH_ACCESS_KEY', '')

    instagram_access_token: str = os.environ.get('INSTAGRAM_ACCESS_TOKEN', '')
    instagram_business_account_id: str = os.environ.get('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')

    tiktok_client_key: str = os.environ.get('TIKTOK_CLIENT_KEY', '')
    tiktok_client_secret: str = os.environ.get('TIKTOK_CLIENT_SECRET', '')
    tiktok_access_token: str = os.environ.get('TIKTOK_ACCESS_TOKEN', '')
    tiktok_open_id: str = os.environ.get('TIKTOK_OPEN_ID', '')

    youtube_client_id: str = os.environ.get('YOUTUBE_CLIENT_ID', '')
    youtube_client_secret: str = os.environ.get('YOUTUBE_CLIENT_SECRET', '')
    youtube_refresh_token: str = os.environ.get('YOUTUBE_REFRESH_TOKEN', '')

    twitter_api_key: str = os.environ.get('TWITTER_API_KEY', '')
    twitter_api_secret: str = os.environ.get('TWITTER_API_SECRET', '')
    twitter_access_token: str = os.environ.get('TWITTER_ACCESS_TOKEN', '')
    twitter_access_token_secret: str = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', '')
    twitter_bearer_token: str = os.environ.get('TWITTER_BEARER_TOKEN', '')

    linkedin_access_token: str = os.environ.get('LINKEDIN_ACCESS_TOKEN', '')
    linkedin_person_id: str = os.environ.get('LINKEDIN_PERSON_ID', '')

    facebook_page_access_token: str = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN', '')
    facebook_page_id: str = os.environ.get('FACEBOOK_PAGE_ID', '')

    supabase_url: str = os.environ.get('SUPABASE_URL', '')
    supabase_key: str = os.environ.get('SUPABASE_KEY', '')

    reddit_client_id: str = os.environ.get('REDDIT_CLIENT_ID', '')
    reddit_client_secret: str = os.environ.get('REDDIT_CLIENT_SECRET', '')

    class Config:
        env_file = str(env_path)
        extra = 'ignore'

    def get_db_path(self) -> str:
        Path(self.app_data_path).mkdir(parents=True, exist_ok=True)
        return str(Path(self.app_data_path) / 'automator.db')

    def get_media_path(self, niche_id: str = '', date_str: str = '') -> Path:
        base = Path(self.media_path)
        if niche_id and date_str:
            return base / niche_id / date_str
        return base


settings = Settings()
