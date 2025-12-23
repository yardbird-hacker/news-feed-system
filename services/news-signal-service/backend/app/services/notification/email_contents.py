from datetime import datetime


def build_email_content(
    *,
    user_name: str,
    keyword: str,
    news_list,
):
    subject = f'[News Alert] Keyword "{keyword}" detected'

    lines = [
        f"Hello {user_name},",
        "",
        "Your notification rule was triggered.",
        "",
        f"Keyword:",
        f"- {keyword}",
        "",
        "Matched News:",
    ]

    if not news_list:
        lines.append("- No new articles found.")
    else:
        for idx, news in enumerate(news_list, start=1):
            lines.append(f"{idx}. News ID: {news.news_id}")
            lines.append(f"   keyword: {news.keyword}")
            lines.append(f"   URL: {news.url}") 
            lines.append("")

    lines.append(f"Sent at: {datetime.utcnow().isoformat()} UTC")

    return subject, "\n".join(lines)
