import os
import sys
import json
import datetime

try:
    from google import genai
except ImportError:
    print("Error: google-genai package is not installed.")
    sys.exit(1)

DEFAULT_COCONALA_PROFILE = "https://coconala.com/users/668648"
DEFAULT_LANCERS_PROFILE = "https://www.lancers.jp/profile/hirotanabe"

def load_json(filepath):
    if not os.path.exists(filepath):
        return []
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def generate_image(client, prompt, output_path):
    print(f"Generating Wednesday topic image via Nano Banana API (gemini-3.1-flash-lite-image)...")
    print(f"Prompt: {prompt}")
    response = client.models.generate_content(
        model='gemini-3.1-flash-lite-image',
        contents=prompt,
    )
    if response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                with open(output_path, 'wb') as f:
                    f.write(part.inline_data.data)
                print(f"Success! Image saved to {output_path}")
                return True
    print("Failed to get image binary data.")
    return False

def create_detail_html(topic, news_num, date_str):
    filename = f"news-{news_num}.html"
    image_filename = f"images/news{news_num}_natural.jpg"

    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic['title']} | TTS</title>
    <meta name="description" content="タナベテックシステム（TTS）公式コラム。「{topic['title']}」。{topic['summary']}">
    <meta name="keywords" content="TTS, {topic['keywords']}, ココナラ 668648, ランサーズ hirotanabe">
    
    <!-- OGP -->
    <meta property="og:title" content="{topic['title']} | TTS">
    <meta property="og:description" content="{topic['summary']}">
    <meta property="og:type" content="article">
    <meta property="og:url" content="https://tts-pr-newsroom.pages.dev/{filename}">
    <meta property="og:image" content="https://tts-pr-newsroom.pages.dev/{image_filename}">

    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --color-primary: #e3000f;
            --color-primary-hover: #c4000d;
            --color-text: #333333;
            --color-text-light: #777777;
            --color-bg: #ffffff;
            --color-bg-gray: #f8f8f8;
            --color-border: #e0e0e0;
            --color-coconala: #41c9b4;
            --color-lancers: #2b6cb0;
        }}

        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Noto Sans JP', sans-serif; background-color: var(--color-bg); color: var(--color-text); line-height: 1.8; }}
        
        /* Header */
        header {{ border-bottom: 2px solid var(--color-primary); padding: 0; background: #fff; position: sticky; top: 0; z-index: 100; }}
        .header-inner {{ max-width: 1200px; margin: 0 auto; padding: 1.2rem 2rem; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 1.4rem; font-weight: 700; color: #000; text-decoration: none; letter-spacing: 0.05em; }}
        .logo span {{ color: var(--color-primary); }}
        .global-nav {{ display: flex; gap: 1.5rem; font-size: 0.9rem; font-weight: 500; align-items: center; }}
        .global-nav a {{ color: #000; text-decoration: none; transition: color 0.2s ease; }}
        .global-nav a:hover {{ color: var(--color-primary); }}
        .nav-order-btn {{ background-color: var(--color-primary); color: #fff !important; padding: 0.5rem 1.2rem; border-radius: 4px; font-weight: 700; }}

        /* Main Content */
        main {{ max-width: 800px; margin: 0 auto; padding: 4rem 2rem; }}
        .article-header {{ margin-bottom: 3rem; text-align: center; }}
        .article-meta {{ color: var(--color-text-light); font-size: 0.9rem; margin-bottom: 1rem; }}
        .article-title {{ font-size: 2rem; font-weight: 700; line-height: 1.4; margin-bottom: 2rem; }}
        .article-image {{ width: 100%; max-height: 400px; object-fit: cover; margin-bottom: 3rem; border-radius: 6px; }}
        .article-body {{ font-size: 1.05rem; }}
        .article-body h2 {{ font-size: 1.5rem; font-weight: 700; margin: 2rem 0 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid var(--color-border); }}
        .article-body p {{ margin-bottom: 1.5rem; }}

        /* Article CTA Card */
        .article-cta {{ background: var(--color-bg-gray); border: 2px solid var(--color-border); border-left: 6px solid var(--color-primary); padding: 2rem; margin-top: 4rem; border-radius: 6px; }}
        .article-cta h3 {{ font-size: 1.3rem; font-weight: 700; margin-bottom: 0.8rem; }}
        .article-cta p {{ font-size: 0.95rem; color: var(--color-text); margin-bottom: 1.5rem; line-height: 1.6; }}
        .cta-buttons {{ display: flex; gap: 1rem; flex-wrap: wrap; }}
        .cta-btn {{ display: inline-flex; align-items: center; justify-content: center; padding: 0.8rem 1.5rem; font-size: 0.95rem; font-weight: 700; text-decoration: none; border-radius: 4px; color: #fff; transition: opacity 0.2s ease; }}
        .cta-btn:hover {{ opacity: 0.9; }}
        .cta-btn-coconala {{ background-color: var(--color-coconala); }}
        .cta-btn-lancers {{ background-color: var(--color-lancers); }}

        /* Footer */
        footer {{ background: #f1f1f1; padding: 3rem 2rem; text-align: center; border-top: 1px solid var(--color-border); margin-top: 4rem; }}
        .footer-text {{ color: var(--color-text-light); font-size: 0.85rem; }}
    </style>
</head>
<body>
    <header>
        <div class="header-inner">
            <a href="index.html" class="logo">TTS <span>CORPORATION</span></a>
            <div class="global-nav">
                <a href="company.html">企業情報</a>
                <a href="index.html?cat=products">商品・サービス</a>
                <a href="index.html?cat=sustainability">サステナビリティ</a>
                <a href="index.html">ニュースルーム</a>
                <a href="index.html#order-section" class="nav-order-btn">ご依頼（ココナラ/ランサーズ）</a>
            </div>
        </div>
    </header>

    <main>
        <article>
            <div class="article-header">
                <div class="article-meta">{date_str} | {topic['category']}</div>
                <h1 class="article-title">{topic['title']}</h1>
            </div>
            
            <img src="./{image_filename}" alt="{topic['title']}" class="article-image">
            
            <div class="article-body">
                <h2>【水曜コラム】テクノロジーと現場をつなぐ実践思考</h2>
                <p>タナベテックシステム開発会社（TTS Corporation）では、日々の開発現場や経営支援の中で得られた技術的知見やトレンド考察を「水曜コラム」として発信しております。</p>
                <p>{topic['summary']}</p>
                
                <h2>背景と現場での応用アプローチ</h2>
                <p><strong>1. 理論と現場運用の融合</strong><br>
                最先端の技術トレンドを単なる知識にとどめず、実際の業務プロセスへ落とし込むことによって、初めて大きな価値が生まれます。</p>
                
                <p><strong>2. 継続的な改善と自動化の推進</strong><br>
                小さな業務改善の積み重ねが、組織全体の大きな生産性向上へとつながります。</p>
            </div>

            <!-- CTA Card -->
            <div class="article-cta">
                <h3>システム開発・IT業務自動化のご相談窓口</h3>
                <p>タナベテックシステム（TTS）では、EC自動化・AIシステム構築・Pythonプログラム開発のご相談をココナラおよびランサーズの田辺広徳（TTS）公式ページにて承っております。</p>
                <div class="cta-buttons">
                    <a href="{DEFAULT_COCONALA_PROFILE}" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn-coconala">ココナラで相談する</a>
                    <a href="{DEFAULT_LANCERS_PROFILE}" target="_blank" rel="noopener noreferrer" class="cta-btn cta-btn-lancers">ランサーズで相談する</a>
                </div>
            </div>
        </article>
    </main>

    <footer>
        <p class="footer-text">&copy; 2026 TTS Corporation. All Rights Reserved.</p>
    </footer>
</body>
</html>
"""
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Created {filename}")

def update_index_html(topic, news_num, date_str):
    filename = f"news-{news_num}.html"
    image_filename = f"images/news{news_num}_natural.jpg"
    
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    new_card = f"""        <div class="news-grid">
            <a href="{filename}" class="news-card" data-category="{topic['category_code']}">
                <div class="news-image">
                    <img src="./{image_filename}" alt="{topic['title']}">
                </div>
                <div class="news-content">
                    <div class="news-meta">
                        <span class="news-date">{date_str}</span>
                        <span class="news-category">{topic['category']}</span>
                    </div>
                    <h3 class="news-title">{topic['title']}</h3>
                </div>
            </a>"""

    updated_content = content.replace('<div class="news-grid">', new_card, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(updated_content)
    print("Updated index.html with new Wednesday topic card.")

def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable is not set.")
        sys.exit(1)
    client = genai.Client(api_key=api_key)

    master_path = os.path.join('data', 'random_topics_master.json')
    posted_path = os.path.join('data', 'posted_random_topics.json')

    topics = load_json(master_path)
    posted = load_json(posted_path)

    posted_ids = [p['id'] for p in posted]
    unposted = [t for t in topics if t['id'] not in posted_ids]

    if not unposted:
        print("All Wednesday topics have been posted. Refreshing queue for new cycle...")
        posted = []
        posted_ids = []
        unposted = topics

    selected_topic = unposted[0]
    print(f"Selected Wednesday Topic to Post: {selected_topic['title']} (ID: {selected_topic['id']})")

    # ニュース番号は9から自動割り振る（固定競合防止）
    existing_news_files = [f for f in os.listdir('.') if f.startswith('news-') and f.endswith('.html')]
    max_num = 8
    for nf in existing_news_files:
        try:
            num = int(nf.replace('news-', '').replace('.html', ''))
            if num > max_num:
                max_num = num
        except ValueError:
            pass
    news_num = max_num + 1

    date_str = datetime.date.today().strftime("%Y年%m月%d日")
    image_output_path = f"images/news{news_num}_natural.jpg"

    # 1. 画像生成
    generate_image(client, selected_topic['image_prompt'], image_output_path)

    # 2. 詳細ページ生成
    create_detail_html(selected_topic, news_num, date_str)

    # 3. トップページ更新
    update_index_html(selected_topic, news_num, date_str)

    # 4. 履歴保存
    posted.append({
        "id": selected_topic['id'],
        "posted_at": date_str,
        "news_file": f"news-{news_num}.html"
    })
    save_json(posted_path, posted)

    print("Wednesday Auto-Publisher completed successfully!")

if __name__ == "__main__":
    main()
